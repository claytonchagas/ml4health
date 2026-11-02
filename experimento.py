"""Experimento: Aprendizado de Maquina versus Escore de Mayo (cirrose biliar primaria, UCI 878).

Rotulo: obito em ate 5 anos (1826 dias), apenas variaveis da linha de base.
Desenho 2 x 2: {regressao, aprendizado de maquina} x {5 variaveis de Mayo, 17 variaveis}.
Validacao: validacao cruzada estratificada repetida (5 x 5), ajuste de hiperparametros aninhado (3 folds).
"""
import hashlib
import os
import urllib.request
import warnings
# Silencia so avisos de API (FutureWarning/DeprecationWarning). Avisos de convergencia NAO sao silenciados:
# sao contados por modelo e por fold e reportados (auditoria, A-02).
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer, SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.model_selection import RandomizedSearchCV, RepeatedStratifiedKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from xgboost import XGBClassifier

SEMENTE = 2026
HORIZONTE = 1826  # 5 anos em dias
UCI_ID = 878
URL_ESPELHO = "https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/survival/pbc.csv"
# Copia versionada no repositorio (mesmo conteudo do espelho Rdatasets), usada na execucao oficial
CAMINHO_LOCAL = "data/pbc_rdatasets.csv"
URL_REPO = "https://raw.githubusercontent.com/ANONIMO/ml4health/main/data/pbc_rdatasets.csv"
SHA256_LOCAL = "797ea9b6abfec34297ef07f361a2e0bfdd90c3c2def180adf8547ea30e75b613"

# ----------------------------------------------------------------------------- dados

def carregar_dados(fonte="local", caminho=CAMINHO_LOCAL):
    """Carrega a coorte de 418 pacientes com os nomes de colunas do UCI 878.
    fonte="local" (padrao, reprodutivel): usa a copia versionada em data/ (baixa do repositorio se nao existir,
        por exemplo no Colab) e verifica o checksum SHA-256; aborta se o arquivo diferir.
    fonte="uci": baixa o dataset oficial pelo ucimlrepo (id 878); falha explicitamente se o servidor nao responder.
    Devolve (DataFrame, descricao da origem)."""
    if fonte == "uci":
        from ucimlrepo import fetch_ucirepo
        ds = fetch_ucirepo(id=UCI_ID)
        # N_Days tem papel "Other" no UCI e so aparece na tabela original, nao em features/targets
        df = ds.data.original.copy().replace({"NA": np.nan})
        for c in ["N_Days", "Age", "Bilirubin", "Cholesterol", "Albumin", "Copper", "Alk_Phos", "SGOT",
                  "Tryglicerides", "Platelets", "Prothrombin", "Stage"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df["Age"] = df["Age"] / 365.25  # dias -> anos
        return df, "UCI 878 (ucimlrepo)"
    if fonte != "local":
        raise ValueError("fonte deve ser 'local' ou 'uci'")
    if not os.path.exists(caminho):
        os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
        urllib.request.urlretrieve(URL_REPO, caminho)
    sha = hashlib.sha256(open(caminho, "rb").read()).hexdigest()
    if sha != SHA256_LOCAL:
        raise ValueError(f"Checksum de {caminho} difere do esperado ({sha} != {SHA256_LOCAL})")
    r = pd.read_csv(caminho)
    yn = lambda s: s.map({1.0: "Y", 0.0: "N"})
    df = pd.DataFrame({
        "ID": r["id"], "N_Days": r["time"],
        "Status": r["status"].map({0: "C", 1: "CL", 2: "D"}),
        "Drug": r["trt"].map({1.0: "D-penicillamine", 2.0: "Placebo"}),
        "Age": r["age"], "Sex": r["sex"].str.upper(),
        "Ascites": yn(r["ascites"]), "Hepatomegaly": yn(r["hepato"]), "Spiders": yn(r["spiders"]),
        "Edema": r["edema"].map({0.0: "N", 0.5: "S", 1.0: "Y"}),
        "Bilirubin": r["bili"], "Cholesterol": r["chol"], "Albumin": r["albumin"], "Copper": r["copper"],
        "Alk_Phos": r["alk.phos"], "SGOT": r["ast"], "Tryglicerides": r["trig"],
        "Platelets": r["platelet"], "Prothrombin": r["protime"], "Stage": r["stage"],
    })
    return df, f"copia local de survival::pbc (espelho do UCI 878), SHA-256 {sha[:12]}..."


def codificar(df):
    """Codificacao numerica das variaveis categoricas (sem imputar)."""
    X = pd.DataFrame(index=df.index)
    X["Age"] = df["Age"]
    X["Sex_M"] = (df["Sex"] == "M").astype(float)
    X["Edema"] = df["Edema"].map({"N": 0.0, "S": 0.5, "Y": 1.0})
    for c in ["Ascites", "Hepatomegaly", "Spiders"]:
        X[c] = df[c].map({"Y": 1.0, "N": 0.0})
    X["Drug_Dpen"] = df["Drug"].map({"D-penicillamine": 1.0, "Placebo": 0.0})
    for c in ["Bilirubin", "Cholesterol", "Albumin", "Copper", "Alk_Phos", "SGOT",
              "Tryglicerides", "Platelets", "Prothrombin", "Stage"]:
        X[c] = df[c].astype(float)
    return X


def rotulo_5anos(df):
    """1 = obito ate 5 anos; 0 = vivo aos 5 anos; NaN = saiu antes dos 5 anos sem obito (censura/transplante)."""
    y = pd.Series(np.nan, index=df.index)
    y[(df["Status"] == "D") & (df["N_Days"] <= HORIZONTE)] = 1.0
    y[df["N_Days"] > HORIZONTE] = 0.0
    return y


MAYO5 = ["Age", "Bilirubin", "Albumin", "Prothrombin", "Edema"]
TODAS17 = ["Age", "Sex_M", "Drug_Dpen", "Ascites", "Hepatomegaly", "Spiders", "Edema",
           "Bilirubin", "Cholesterol", "Albumin", "Copper", "Alk_Phos", "SGOT",
           "Tryglicerides", "Platelets", "Prothrombin", "Stage"]
LOG_LAB = ["Bilirubin", "Cholesterol", "Albumin", "Copper", "Alk_Phos", "SGOT", "Tryglicerides", "Prothrombin"]

# ----------------------------------------------------------------------------- Escore de Mayo

# Dickson et al. (1989). Modelo FINAL: formula de uso da p. 6, estimada com os 418 pacientes (inclui todos os
# pacientes usados como teste neste estudo; por isso e apresentado apenas como referencia historica).
COEF_MAYO = {"Age": 0.039, "log_Bilirubin": 0.871, "log_Albumin": -2.53, "log_Prothrombin": 2.38, "Edema": 0.859}
# Modelo INICIAL: Tabela 2, p. 4, estimado so com os 312 pacientes randomizados. Nao viu os 106 nao randomizados,
# e por isso e o comparador historico valido na validacao quase externa.
COEF_MAYO_INICIAL = {"Age": 0.0333, "log_Bilirubin": 0.8792, "log_Albumin": -3.053, "log_Prothrombin": 3.016,
                     "Edema": 0.7847}
COEFS = {"final": COEF_MAYO, "inicial": COEF_MAYO_INICIAL}


def escore_mayo(X, coef=COEF_MAYO):
    """Escore de risco de Mayo (Dickson et al., 1989): R = soma dos coeficientes x variaveis (logaritmo natural)."""
    return (coef["Age"] * X["Age"] + coef["log_Bilirubin"] * np.log(X["Bilirubin"])
            + coef["log_Albumin"] * np.log(X["Albumin"])
            + coef["log_Prothrombin"] * np.log(X["Prothrombin"]) + coef["Edema"] * X["Edema"])


class MayoOriginal(BaseEstimator, ClassifierMixin):
    """Usa os coeficientes de 1989 sem reestimar (versao 'final', n=418, ou 'inicial', n=312). A ordenacao
    (AUROC) e a do escore original; para obter probabilidades, recalibra apenas intercepto e inclinacao no treino."""
    def __init__(self, versao="final"):
        self.versao = versao

    def fit(self, X, y):
        X = pd.DataFrame(X, columns=MAYO5)
        med = X.median()
        self.med_ = med
        r = escore_mayo(X.fillna(med), COEFS[self.versao]).to_numpy().reshape(-1, 1)
        self.recal_ = LogisticRegression(C=1e6).fit(r, y)
        self.classes_ = np.array([0, 1])
        return self

    def predict_proba(self, X):
        X = pd.DataFrame(X, columns=MAYO5).fillna(self.med_)
        r = escore_mayo(X, COEFS[self.versao]).to_numpy().reshape(-1, 1)
        return self.recal_.predict_proba(r)

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)


# Probabilidade original do modelo de Cox final (Dickson et al., 1989, p. 6 e Tabela 4):
# S(t) = S0(t) ** exp(R - 5,07), com S0(5 anos) = 0,774 e 5,07 = media de R nos 418 pacientes.
S0_5ANOS = 0.774
R_MEDIO = 5.07


class MayoProbOriginal(BaseEstimator, ClassifierMixin):
    """Probabilidade de obito em 5 anos do modelo de Cox final publicado, sem nenhum ajuste:
    1 - S0(5) ** exp(R - 5,07). Do treino, aprende apenas a mediana para imputar ausentes.
    E crescente em R, entao sua AUROC e exatamente a do escore original."""
    def fit(self, X, y):
        self.med_ = pd.DataFrame(X, columns=MAYO5).median()
        self.classes_ = np.array([0, 1])
        return self

    def predict_proba(self, X):
        X = pd.DataFrame(X, columns=MAYO5).fillna(self.med_)
        r = escore_mayo(X, COEF_MAYO).to_numpy()
        p = 1 - S0_5ANOS ** np.exp(r - R_MEDIO)
        return np.column_stack([1 - p, p])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)

# ----------------------------------------------------------------------------- pipelines

def _log_cols(cols):
    idx = [i for i, c in enumerate(cols) if c in LOG_LAB]
    def f(A):
        A = np.array(A, dtype=float, copy=True)
        A[:, idx] = np.log(A[:, idx])
        return A
    return FunctionTransformer(f)


def pipe_regressao(cols, penalizada):
    imput = SimpleImputer(strategy="median") if cols == MAYO5 else IterativeImputer(random_state=SEMENTE, max_iter=10)
    passos = [("log", _log_cols(cols)), ("imput", imput), ("esc", StandardScaler())]
    if penalizada:
        clf = LogisticRegression(penalty="elasticnet", solver="saga", l1_ratio=0.5, C=1.0, max_iter=5000,
                                 random_state=SEMENTE)
    else:
        clf = LogisticRegression(C=1e6, max_iter=5000)
    return Pipeline(passos + [("clf", clf)])


def pipe_rf(cols):
    imput = SimpleImputer(strategy="median") if cols == MAYO5 else IterativeImputer(random_state=SEMENTE, max_iter=10)
    return Pipeline([("imput", imput), ("clf", RandomForestClassifier(n_estimators=300, random_state=SEMENTE, n_jobs=-1))])


def pipe_xgb(cols):
    # XGBoost aceita ausentes nativamente; nao imputamos (o modelo aprende a direcao dos ausentes)
    return Pipeline([("clf", XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=2, subsample=0.8,
                                           colsample_bytree=0.8, eval_metric="logloss", random_state=SEMENTE,
                                           n_jobs=-1, verbosity=0))])


def pipe_arvore_preproc_rl(algoritmo):
    """Analise de sensibilidade (auditoria, A-04): random forest ou XGBoost com 17 variaveis recebendo EXATAMENTE
    o mesmo pre-processamento da regressao logistica com 17 variaveis (logaritmo dos laboratorios, imputacao
    iterativa nessa escala e padronizacao). Arvores sao invariantes a transformacoes monotonicas, entao a unica
    diferenca restante em relacao a regressao e o algoritmo (e seus hiperparametros)."""
    base = pipe_regressao(TODAS17, True).steps[:-1]  # log, imputacao iterativa, padronizacao
    if algoritmo == "rf":
        clf = RandomForestClassifier(n_estimators=300, random_state=SEMENTE, n_jobs=-1)
    else:
        clf = XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=2, subsample=0.8, colsample_bytree=0.8,
                            eval_metric="logloss", random_state=SEMENTE, n_jobs=-1, verbosity=0)
    return Pipeline(base + [("clf", clf)])


# Grades definidas antes de qualquer resultado, com faixas usuais para dados tabulares pequenos; nao foram
# alteradas depois de ver o desempenho. Orcamento igual para todos: 12 configuracoes sorteadas.
N_CONFIG = 12

GRADES = {
    "rl_pen": {"clf__C": [0.01, 0.03, 0.1, 0.3, 1.0, 3.0], "clf__l1_ratio": [0.0, 0.5, 1.0]},
    "rf": {"clf__min_samples_leaf": [3, 5, 10, 20], "clf__max_features": ["sqrt", 0.5, 1.0], "clf__max_depth": [None, 4, 6]},
    "xgb": {"clf__n_estimators": [100, 200, 400], "clf__learning_rate": [0.02, 0.05, 0.1],
            "clf__max_depth": [1, 2, 3], "clf__min_child_weight": [1, 5], "clf__reg_lambda": [1.0, 5.0]},
}


def modelos():
    """Celulas do desenho 2 x 2 (mais o escore original). (nome, colunas, estimador, grade ou None)."""
    return [
        ("Mayo 1989 final, prob. original", MAYO5, MayoProbOriginal(), None),
        ("Mayo 1989 final, recalibrado", MAYO5, MayoOriginal("final"), None),
        ("RL, 5 var. (Mayo reestimado)", MAYO5, pipe_regressao(MAYO5, False), None),
        ("RL penalizada, 17 var.", TODAS17, pipe_regressao(TODAS17, True), "rl_pen"),
        ("Random forest, 5 var.", MAYO5, pipe_rf(MAYO5), "rf"),
        ("Random forest, 17 var.", TODAS17, pipe_rf(TODAS17), "rf"),
        ("XGBoost, 5 var.", MAYO5, pipe_xgb(MAYO5), "xgb"),
        ("XGBoost, 17 var.", TODAS17, pipe_xgb(TODAS17), "xgb"),
        # Sensibilidade (A-04): mesmo pre-processamento da RL com 17 variaveis
        ("Random forest, 17 var., pré-proc. da RL", TODAS17, pipe_arvore_preproc_rl("rf"), "rf"),
        ("XGBoost, 17 var., pré-proc. da RL", TODAS17, pipe_arvore_preproc_rl("xgb"), "xgb"),
    ]


def ajustar(est, grade, X, y, semente):
    """Ajusta o modelo (com busca aninhada, se houver grade) apenas nos dados recebidos.
    Devolve (modelo ajustado, hiperparametros escolhidos, avisos de convergencia), em que avisos e a
    lista de textos "Categoria: mensagem", um por aviso distinto (vazia quando nenhum ocorre)."""
    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always", ConvergenceWarning)
        if grade is None:
            m, hp = clone(est).fit(X, y), {}
        else:
            busca = RandomizedSearchCV(clone(est), GRADES[grade], n_iter=N_CONFIG, scoring="roc_auc",
                                       cv=StratifiedKFold(3, shuffle=True, random_state=semente),
                                       random_state=semente, n_jobs=1, refit=True)
            busca.fit(X, y)
            m, hp = busca.best_estimator_, busca.best_params_
    conv = [f"{a.category.__name__}: {a.message}" for a in avisos if issubclass(a.category, ConvergenceWarning)]
    return m, hp, conv

# ----------------------------------------------------------------------------- metricas

def calibracao(y, p):
    """Calibracao no geral (intercepto) e inclinacao de calibracao, por recalibracao logistica."""
    p = np.clip(p, 1e-6, 1 - 1e-6)
    y = np.asarray(y, dtype=float)
    lp = np.log(p / (1 - p))
    # Inclinacao: coeficiente b em logit P(y=1) = a + b * logit(p), sem penalizacao
    incl = LogisticRegression(penalty=None, max_iter=1000).fit(lp.reshape(-1, 1), y).coef_[0, 0]
    # CITL (calibracao no geral): intercepto a em logit P(y=1) = a + 1 * logit(p), isto e, com logit(p) como offset
    # (Van Calster et al., 2016; 2019). Estimado por Newton-Raphson em uma dimensao.
    a = 0.0
    for _ in range(50):
        mu = 1 / (1 + np.exp(-(a + lp)))
        passo = (y - mu).sum() / (mu * (1 - mu)).sum()
        a += passo
        if abs(passo) < 1e-10:
            break
    return a, incl


def metricas(y, p):
    """AUROC; AP = precisao media (average precision): soma da precisao ponderada pelos incrementos de revocacao,
    estimador usual da area sob a curva precisao-revocacao (nao e a integracao trapezoidal); Brier; CITL;
    inclinacao de calibracao."""
    citl, incl = calibracao(y, p)
    return {"AUROC": roc_auc_score(y, p), "AP": average_precision_score(y, p),
            "Brier": brier_score_loss(y, p), "CITL": citl, "Incl. calibr.": incl}


def validacao_cruzada(X, y, n_rep=5, n_folds=5, semente=SEMENTE, log=print):
    """Devolve (metricas por fold, predicoes fora-do-fold medias por paciente, hiperparametros por fold).
    As metricas por fold incluem o numero de avisos de convergencia do ajuste daquele fold e seus textos."""
    cv = RepeatedStratifiedKFold(n_splits=n_folds, n_repeats=n_rep, random_state=semente)
    linhas, oof, hiper = [], {}, []
    for nome, cols, est, grade in modelos():
        P = np.full((n_rep, len(y)), np.nan)
        for k, (tr, te) in enumerate(cv.split(X, y)):
            rep = k // n_folds
            m, hp, conv = ajustar(est, grade, X.iloc[tr][cols], y.iloc[tr], semente + k)
            p = m.predict_proba(X.iloc[te][cols])[:, 1]
            P[rep, te] = p
            linhas.append({"Modelo": nome, "Fold": k, **metricas(y.iloc[te].to_numpy(), p), "Avisos de convergência": len(conv),
                           "Mensagens dos avisos": " | ".join(sorted(set(conv)))})
            hiper.append({"Modelo": nome, "Fold": k, **{c.replace("clf__", ""): v for c, v in hp.items()}})
        oof[nome] = P.mean(axis=0)
        log(f"  {nome}: AUROC medio por fold = {np.mean([l['AUROC'] for l in linhas if l['Modelo'] == nome]):.3f}")
    return pd.DataFrame(linhas), pd.DataFrame(oof, index=y.index), pd.DataFrame(hiper)


def bootstrap_diferenca(y, p_ref, p_mod, n=2000, semente=SEMENTE, niveis=(0.95,)):
    """Diferenca de AUROC (modelo menos referencia) e ICs percentis por bootstrap PAREADO de pacientes.
    Os intervalos sao CONDICIONAIS as predicoes fora-do-fold ja obtidas: nao incorporam a variacao de refazer
    o treino, a busca de hiperparametros e as divisoes (exploratorios; ver A-03 da auditoria)."""
    rng = np.random.default_rng(semente)
    y = np.asarray(y); d = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].min() == y[i].max():
            continue
        d.append(roc_auc_score(y[i], p_mod[i]) - roc_auc_score(y[i], p_ref[i]))
    d = np.array(d)
    ics = [(np.percentile(d, 100 * (1 - nv) / 2), np.percentile(d, 100 * (1 + nv) / 2)) for nv in niveis]
    return roc_auc_score(y, p_mod) - roc_auc_score(y, p_ref), ics


def valor_incremental(y, oof, folds, ref, comparacoes):
    """Tabela de valor incremental contra uma referencia.
    - DeltaAUROC sobre as predicoes fora-do-fold medias, com IC 95% e IC simultaneo de Bonferroni
      (nivel 1 - 0,05/m, m = numero de comparacoes);
    - leitura: 'maior' ou 'menor' so quando o IC de Bonferroni exclui zero; caso contrario,
      'sem evidencia de diferenca' (nao e equivalencia: nenhuma margem foi pre-especificada);
    - dispersao fold a fold (25 folds): media e desvio da diferenca de AUROC dentro de cada fold, que reflete a
      variacao do treino, e fracao de folds em que o modelo superou a referencia."""
    m = len(comparacoes)
    nivel_b = 1 - 0.05 / m
    y = np.asarray(y); linhas = []
    for nome in comparacoes:
        d, ((l95, h95), (lb, hb)) = bootstrap_diferenca(y, oof[ref].to_numpy(), oof[nome].to_numpy(),
                                                       niveis=(0.95, nivel_b))
        a = folds.loc[folds.Modelo == nome].set_index("Fold")["AUROC"]
        b = folds.loc[folds.Modelo == ref].set_index("Fold")["AUROC"]
        df_ = (a - b).dropna()
        leitura = "maior" if lb > 0 else ("menor" if hb < 0 else "sem evidência de diferença")
        linhas.append({"Referência": ref, "Modelo": nome, "ΔAUROC": d, "IC95_inf": l95, "IC95_sup": h95,
                       "Comparações (m)": m, "Nível Bonferroni": nivel_b, "ICBonf_inf": lb, "ICBonf_sup": hb,
                       "Leitura (Bonferroni)": leitura, "Δ fold a fold (média)": df_.mean(),
                       "Δ fold a fold (desvio)": df_.std(), "Folds com ganho (%)": 100 * (df_ > 0).mean()})
    return pd.DataFrame(linhas)


COMPARACOES_SENSIBILIDADE = ["Random forest, 17 var., pré-proc. da RL", "XGBoost, 17 var., pré-proc. da RL"]

COMPARACOES_PRINCIPAIS = ["RL penalizada, 17 var.", "Random forest, 5 var.", "Random forest, 17 var.",
                          "XGBoost, 5 var.", "XGBoost, 17 var."]

# ----------------------------------------------------------------------------- vazamento (enquadramento PS3E26)

def experimento_vazamento(df, X, n_rep=5, n_folds=5, semente=SEMENTE):
    """Classificacao em 3 classes (C, CL, D), como na competicao Kaggle PS3E26, com e sem N_Days na entrada."""
    y3 = df["Status"].map({"C": 0, "CL": 1, "D": 2})
    Xs = X[TODAS17].copy()
    Xc = Xs.copy(); Xc["N_Days"] = df["N_Days"]
    cv = RepeatedStratifiedKFold(n_splits=n_folds, n_repeats=n_rep, random_state=semente)
    res = []
    for rotulo, XX in [("sem N_Days", Xs), ("com N_Days", Xc)]:
        for k, (tr, te) in enumerate(cv.split(XX, y3)):
            m = XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=3, subsample=0.8,
                              colsample_bytree=0.8, objective="multi:softprob", eval_metric="mlogloss",
                              random_state=semente, n_jobs=-1, verbosity=0)
            m.fit(XX.iloc[tr], y3.iloc[tr])
            p = m.predict_proba(XX.iloc[te])
            res.append({"Entrada": rotulo, "Fold": k, "Log loss": log_loss(y3.iloc[te], p, labels=[0, 1, 2]),
                        "AUROC macro (OvR)": roc_auc_score(y3.iloc[te], p, multi_class="ovr", average="macro"),
                        "Acuracia": (p.argmax(1) == y3.iloc[te].to_numpy()).mean()})
    return pd.DataFrame(res)

# ----------------------------------------------------------------------------- validacao quase externa

def validacao_quase_externa(df, X, y):
    """Desenvolve nos pacientes do ensaio randomizado; testa nos nao randomizados (Drug ausente).
    Devolve (metricas, n treino, n teste, obitos no teste, hiperparametros escolhidos por modelo)."""
    rot = y.notna()
    tr = rot & df["Drug"].notna(); te = rot & df["Drug"].isna()
    linhas, hiper = [], []
    # O Mayo inicial (n=312) entra aqui como comparador historico valido: foi estimado so nos randomizados.
    lista = [("Mayo 1989 inicial (n=312), recalibrado", MAYO5, MayoOriginal("inicial"), None)] + modelos()
    for nome, cols, est, grade in lista:
        m, hp, conv = ajustar(est, grade, X.loc[tr, cols], y[tr], SEMENTE)
        p = m.predict_proba(X.loc[te, cols])[:, 1]
        linhas.append({"Modelo": nome, **metricas(y[te].to_numpy(), p), "Avisos de convergência": len(conv),
                       "Mensagens dos avisos": " | ".join(sorted(set(conv)))})
        hiper.append({"Cenário": "quase externa", "Modelo": nome, **{c.replace("clf__", ""): v for c, v in hp.items()}})
    return pd.DataFrame(linhas), int(tr.sum()), int(te.sum()), int(y[te].sum()), pd.DataFrame(hiper)


if __name__ == "__main__":
    import time
    t0 = time.time()
    df, origem = carregar_dados("local")
    X = codificar(df); y = rotulo_5anos(df)
    rot = y.notna()
    print(origem, df.shape, "rotulados:", int(rot.sum()), "obitos 5a:", int(y.sum()), "excluidos:", int((~rot).sum()))
    print("completos 5 var:", int(X.loc[rot, MAYO5].notna().all(1).sum()), "completos 17 var:", int(X.loc[rot, TODAS17].notna().all(1).sum()))
    folds, oof, hiper = validacao_cruzada(X[rot], y[rot])
    folds.to_csv("resultados/folds.csv", index=False); oof.to_csv("resultados/oof.csv")
    hiper.to_csv("resultados/hiperparametros.csv", index=False)
    print(folds.drop(columns="Mensagens dos avisos").groupby("Modelo", sort=False).agg(["mean", "std"]).round(3).to_string())
    yy = y[rot].to_numpy()
    vi = valor_incremental(yy, oof, folds, "RL, 5 var. (Mayo reestimado)", COMPARACOES_PRINCIPAIS)
    vi.to_csv("resultados/valor_incremental.csv", index=False); print(vi.round(3).to_string())
    vz = experimento_vazamento(df, X); vz.to_csv("resultados/vazamento.csv", index=False)
    print(vz.groupby("Entrada").agg(["mean", "std"]).round(3).to_string())
    qe, ntr, nte, nev, hqe = validacao_quase_externa(df, X, y); qe.to_csv("resultados/quase_externa.csv", index=False)
    hqe.to_csv("resultados/hiperparametros_quase_externa.csv", index=False)
    print("quase externa: treino", ntr, "teste", nte, "obitos teste", nev); print(qe.round(3).to_string())
    print("tempo", round(time.time() - t0), "s")

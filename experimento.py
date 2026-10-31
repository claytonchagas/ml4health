"""Experimento: Aprendizado de Maquina versus Escore de Mayo (cirrose biliar primaria, UCI 878).

Rotulo: obito em ate 5 anos (1826 dias), apenas variaveis da linha de base.
Desenho 2 x 2: {regressao, aprendizado de maquina} x {5 variaveis de Mayo, 17 variaveis}.
Validacao: validacao cruzada estratificada repetida (5 x 5), ajuste de hiperparametros aninhado (3 folds).
"""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
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

# ----------------------------------------------------------------------------- dados

def carregar_dados(caminho_local=None):
    """Tenta o UCI 878; se falhar, usa o espelho Rdatasets (survival::pbc, mesma coorte de 418 pacientes).
    Devolve um DataFrame com os nomes de colunas do UCI 878 e a origem usada."""
    try:
        from ucimlrepo import fetch_ucirepo
        ds = fetch_ucirepo(id=UCI_ID)
        df = pd.concat([ds.data.ids, ds.data.features, ds.data.targets], axis=1)
        df["Age"] = df["Age"] / 365.25  # dias -> anos
        return df, "UCI 878 (ucimlrepo)"
    except Exception:
        pass
    r = pd.read_csv(caminho_local) if caminho_local else pd.read_csv(URL_ESPELHO)
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
    return df, "Rdatasets survival::pbc (espelho do UCI 878)"


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

COEF_MAYO = {"Age": 0.039, "log_Bilirubin": 0.871, "log_Albumin": -2.53, "log_Prothrombin": 2.38, "Edema": 0.859}


def escore_mayo(X):
    """Escore de risco de Mayo (Dickson et al., 1989), coeficientes publicados."""
    return (COEF_MAYO["Age"] * X["Age"] + COEF_MAYO["log_Bilirubin"] * np.log(X["Bilirubin"])
            + COEF_MAYO["log_Albumin"] * np.log(X["Albumin"])
            + COEF_MAYO["log_Prothrombin"] * np.log(X["Prothrombin"]) + COEF_MAYO["Edema"] * X["Edema"])


class MayoOriginal(BaseEstimator, ClassifierMixin):
    """Usa os coeficientes de 1989 sem reestimar. A ordenacao (AUROC) e a do escore original;
    para obter probabilidades, recalibra apenas intercepto e inclinacao no treino (2 parametros)."""
    def fit(self, X, y):
        X = pd.DataFrame(X, columns=MAYO5)
        med = X.median()
        self.med_ = med
        r = escore_mayo(X.fillna(med)).to_numpy().reshape(-1, 1)
        self.recal_ = LogisticRegression(C=1e6).fit(r, y)
        self.classes_ = np.array([0, 1])
        return self

    def predict_proba(self, X):
        X = pd.DataFrame(X, columns=MAYO5).fillna(self.med_)
        r = escore_mayo(X).to_numpy().reshape(-1, 1)
        return self.recal_.predict_proba(r)

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
        clf = LogisticRegression(penalty="elasticnet", solver="saga", l1_ratio=0.5, C=1.0, max_iter=5000)
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


GRADES = {
    "rl_pen": {"clf__C": [0.01, 0.03, 0.1, 0.3, 1.0, 3.0], "clf__l1_ratio": [0.0, 0.5, 1.0]},
    "rf": {"clf__min_samples_leaf": [3, 5, 10, 20], "clf__max_features": ["sqrt", 0.5, 1.0], "clf__max_depth": [None, 4, 6]},
    "xgb": {"clf__n_estimators": [100, 200, 400], "clf__learning_rate": [0.02, 0.05, 0.1],
            "clf__max_depth": [1, 2, 3], "clf__min_child_weight": [1, 5], "clf__reg_lambda": [1.0, 5.0]},
}


def modelos():
    """Celulas do desenho 2 x 2 (mais o escore original). (nome, colunas, estimador, grade ou None)."""
    return [
        ("Mayo 1989 (coef. publicados)", MAYO5, MayoOriginal(), None),
        ("RL, 5 var. (Mayo reestimado)", MAYO5, pipe_regressao(MAYO5, False), None),
        ("RL penalizada, 17 var.", TODAS17, pipe_regressao(TODAS17, True), "rl_pen"),
        ("Random forest, 5 var.", MAYO5, pipe_rf(MAYO5), "rf"),
        ("Random forest, 17 var.", TODAS17, pipe_rf(TODAS17), "rf"),
        ("XGBoost, 5 var.", MAYO5, pipe_xgb(MAYO5), "xgb"),
        ("XGBoost, 17 var.", TODAS17, pipe_xgb(TODAS17), "xgb"),
    ]


def ajustar(est, grade, X, y, semente):
    if grade is None:
        return clone(est).fit(X, y)
    busca = RandomizedSearchCV(clone(est), GRADES[grade], n_iter=8 if grade == "rf" else 12, scoring="roc_auc",
                               cv=StratifiedKFold(3, shuffle=True, random_state=semente),
                               random_state=semente, n_jobs=1, refit=True)
    return busca.fit(X, y).best_estimator_

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
    citl, incl = calibracao(y, p)
    return {"AUROC": roc_auc_score(y, p), "AUPRC": average_precision_score(y, p),
            "Brier": brier_score_loss(y, p), "CITL": citl, "Incl. calibr.": incl}


def validacao_cruzada(X, y, n_rep=5, n_folds=5, semente=SEMENTE, log=print):
    """Devolve (metricas por fold, predicoes fora-do-fold medias por paciente)."""
    cv = RepeatedStratifiedKFold(n_splits=n_folds, n_repeats=n_rep, random_state=semente)
    linhas, oof = [], {}
    for nome, cols, est, grade in modelos():
        P = np.full((n_rep, len(y)), np.nan)
        for k, (tr, te) in enumerate(cv.split(X, y)):
            rep = k // n_folds
            m = ajustar(est, grade, X.iloc[tr][cols], y.iloc[tr], semente + k)
            p = m.predict_proba(X.iloc[te][cols])[:, 1]
            P[rep, te] = p
            linhas.append({"Modelo": nome, "Fold": k, **metricas(y.iloc[te].to_numpy(), p)})
        oof[nome] = P.mean(axis=0)
        log(f"  {nome}: AUROC medio por fold = {np.mean([l['AUROC'] for l in linhas if l['Modelo'] == nome]):.3f}")
    return pd.DataFrame(linhas), pd.DataFrame(oof, index=y.index)


def bootstrap_diferenca(y, p_ref, p_mod, n=2000, semente=SEMENTE):
    """IC 95% por bootstrap de pacientes para a diferenca de AUROC (modelo menos referencia)."""
    rng = np.random.default_rng(semente)
    y = np.asarray(y); d = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].min() == y[i].max():
            continue
        d.append(roc_auc_score(y[i], p_mod[i]) - roc_auc_score(y[i], p_ref[i]))
    d = np.array(d)
    return roc_auc_score(y, p_mod) - roc_auc_score(y, p_ref), np.percentile(d, 2.5), np.percentile(d, 97.5)

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
    """Desenvolve nos pacientes do ensaio randomizado; testa nos nao randomizados (Drug ausente)."""
    rot = y.notna()
    tr = rot & df["Drug"].notna(); te = rot & df["Drug"].isna()
    linhas = []
    for nome, cols, est, grade in modelos():
        m = ajustar(est, grade, X.loc[tr, cols], y[tr], SEMENTE)
        p = m.predict_proba(X.loc[te, cols])[:, 1]
        linhas.append({"Modelo": nome, **metricas(y[te].to_numpy(), p)})
    return pd.DataFrame(linhas), int(tr.sum()), int(te.sum()), int(y[te].sum())


if __name__ == "__main__":
    import time
    t0 = time.time()
    df, origem = carregar_dados("data/pbc_rdatasets.csv")
    X = codificar(df); y = rotulo_5anos(df)
    rot = y.notna()
    print(origem, df.shape, "rotulados:", int(rot.sum()), "obitos 5a:", int(y.sum()), "excluidos:", int((~rot).sum()))
    print("completos 5 var:", int(X.loc[rot, MAYO5].notna().all(1).sum()), "completos 17 var:", int(X.loc[rot, TODAS17].notna().all(1).sum()))
    folds, oof = validacao_cruzada(X[rot], y[rot])
    folds.to_csv("resultados/folds.csv", index=False); oof.to_csv("resultados/oof.csv")
    print(folds.groupby("Modelo", sort=False).agg(["mean", "std"]).round(3).to_string())
    yy = y[rot].to_numpy()
    for ref in ["Mayo 1989 (coef. publicados)", "RL, 5 var. (Mayo reestimado)"]:
        for nome in oof.columns:
            if nome != ref:
                d, lo, hi = bootstrap_diferenca(yy, oof[ref].to_numpy(), oof[nome].to_numpy())
                print(f"  {nome} - {ref}: {d:+.3f} [{lo:+.3f}; {hi:+.3f}]")
    vz = experimento_vazamento(df, X); vz.to_csv("resultados/vazamento.csv", index=False)
    print(vz.groupby("Entrada").agg(["mean", "std"]).round(3).to_string())
    qe, ntr, nte, nev = validacao_quase_externa(df, X, y); qe.to_csv("resultados/quase_externa.csv", index=False)
    print("quase externa: treino", ntr, "teste", nte, "obitos teste", nev); print(qe.round(3).to_string())
    print("tempo", round(time.time() - t0), "s")

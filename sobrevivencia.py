"""Análise de sobrevivência da versão SBCAS 2027 (plano em sbcas/PLANO_ANALISE.md).

Pergunta: modelos de aprendizado de máquina para sobrevivência agregam valor ao modelo de Cox com as cinco
variáveis do Escore de Mayo? Desfecho principal: sobrevida livre de transplante (evento = óbito ou transplante),
nos 418 pacientes, sem exclusão pelo horizonte. Desenho 2 x 2: Cox e random survival forest, cada um com as
5 variáveis de Mayo e com as 17 variáveis.

Uso: python sobrevivencia.py [--desfecho obito] [--n-rep 5]
Saídas em resultados_sbcas/ (sufixo _obito para a análise de sensibilidade).
Reutiliza do módulo experimento.py a carga dos dados, a codificação e o pré-processamento."""
import argparse
import os
import time
import warnings

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import RandomizedSearchCV, ParameterGrid, RepeatedStratifiedKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import SimpleImputer, IterativeImputer
from sksurv.ensemble import RandomSurvivalForest
from sksurv.linear_model import CoxPHSurvivalAnalysis, CoxnetSurvivalAnalysis
from sksurv.metrics import (as_concordance_index_ipcw_scorer, brier_score, concordance_index_censored,
                            concordance_index_ipcw, cumulative_dynamic_auc, integrated_brier_score)
from sksurv.nonparametric import kaplan_meier_estimator
from sksurv.util import Surv

from experimento import MAYO5, SEMENTE, TODAS17, carregar_dados, codificar, pipe_regressao

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

HORIZONTE = 1826                       # 5 anos em dias
TEMPOS_IBS = np.array([365, 730, 1095, 1461, 1826])
N_CONFIG_RSF = 50
N_BOOT = 2000
MARGEM = 0.02                          # margem de relevância pré-especificada no C de Uno
REFERENCIA = "Cox, 5 var. (referência)"

# ----------------------------------------------------------------------------- modelos

def _preproc_cox(cols):
    """Mesmo pré-processamento da regressão do trabalho da disciplina: log, imputação e padronização."""
    return pipe_regressao(cols, False).steps[:-1]


def _preproc_arvore(cols):
    imput = SimpleImputer(strategy="median") if cols == MAYO5 else IterativeImputer(random_state=SEMENTE, max_iter=10)
    return [("imput", imput)]


def modelos():
    """(nome, colunas, pipeline, espaço de busca, n de configurações). Espaços fixados no plano de análise."""
    cox5 = Pipeline(_preproc_cox(MAYO5) + [("m", CoxPHSurvivalAnalysis(alpha=0.0, ties="breslow"))])
    coxnet = Pipeline(_preproc_cox(TODAS17) + [("m", CoxnetSurvivalAnalysis(l1_ratio=0.5, fit_baseline_model=True))])
    grade_coxnet = {"m__l1_ratio": [0.1, 0.5, 0.9, 1.0],
                    "m__alphas": [[a] for a in np.logspace(-3, 0, 10)]}
    def rsf(cols):
        return Pipeline(_preproc_arvore(cols) + [("m", RandomSurvivalForest(n_estimators=300, random_state=SEMENTE,
                                                                            n_jobs=-1))])
    grade_rsf = {"m__min_samples_leaf": [3, 5, 10, 15, 20, 30], "m__min_samples_split": [6, 10, 20, 40],
                 "m__max_features": ["sqrt", 0.33, 0.5, 1.0], "m__max_depth": [None, 3, 4, 6, 8]}
    return [
        (REFERENCIA, MAYO5, cox5, None, 0),
        ("Cox penalizado, 17 var.", TODAS17, coxnet, grade_coxnet, len(ParameterGrid(grade_coxnet))),
        ("RSF, 5 var.", MAYO5, rsf(MAYO5), grade_rsf, N_CONFIG_RSF),
        ("RSF, 17 var.", TODAS17, rsf(TODAS17), grade_rsf, N_CONFIG_RSF),
    ]


def ajustar(est, grade, n_config, X, y, semente):
    """Ajusta (com busca aninhada pelo C de Uno truncado em 5 anos, se houver grade). Devolve modelo,
    hiperparâmetros e a lista de avisos (categoria: mensagem) ocorridos."""
    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always")
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        if grade is None:
            m, hp = clone(est).fit(X, y), {}
        else:
            alvo = as_concordance_index_ipcw_scorer(clone(est), tau=HORIZONTE)
            grade_w = {f"estimator__{k}": v for k, v in grade.items()}
            cv = StratifiedKFold(3, shuffle=True, random_state=semente)
            busca = RandomizedSearchCV(alvo, grade_w, n_iter=n_config, cv=list(cv.split(X, y["event"])),
                                       random_state=semente, n_jobs=1, refit=True, error_score="raise")
            busca.fit(X, y)
            m = busca.best_estimator_.estimator_
            hp = {k.replace("estimator__m__", ""): (v[0] if isinstance(v, list) else v)
                  for k, v in busca.best_params_.items()}
    msgs = sorted({f"{a.category.__name__}: {str(a.message)[:160]}" for a in avisos})
    return m, hp, msgs


def predizer(m, X):
    """Escore de risco (maior = maior risco) e risco de evento em 5 anos (1 - S(5 anos))."""
    escore = m.predict(X)
    fs = m.predict_survival_function(X)
    s5 = np.array([f(HORIZONTE) for f in fs])
    return escore, 1.0 - s5, fs

# ----------------------------------------------------------------------------- métricas

def metricas(y_tr, y_te, risco5, fs):
    """Métricas no conjunto de teste, com a distribuição de censura estimada no treino."""
    tmax = y_te["time"].max()
    tempos = TEMPOS_IBS[TEMPOS_IBS < tmax]
    surv_grid = np.array([[f(t) for t in tempos] for f in fs])
    s5 = 1.0 - risco5
    return {
        "C de Uno (5 anos)": concordance_index_ipcw(y_tr, y_te, risco5, tau=HORIZONTE)[0],
        "C de Harrell": concordance_index_censored(y_te["event"], y_te["time"], risco5)[0],
        "AUC (5 anos)": cumulative_dynamic_auc(y_tr, y_te, risco5, [HORIZONTE])[0][0],
        "Brier (5 anos)": brier_score(y_tr, y_te, s5, [HORIZONTE])[1][0],
        "Brier integrado (1 a 5 anos)": integrated_brier_score(y_tr, y_te, surv_grid, tempos),
    }


def calibracao_5anos(y, risco5, n_grupos=5):
    """Razão observado/esperado em 5 anos (Kaplan-Meier) e tabela por quintis de risco previsto."""
    def km_risco(yy):
        t, s = kaplan_meier_estimator(yy["event"], yy["time"])
        return 1.0 - (s[t <= HORIZONTE][-1] if np.any(t <= HORIZONTE) else 1.0)
    obs = km_risco(y)
    grupos = pd.qcut(risco5, n_grupos, labels=False, duplicates="drop")
    tab = [{"Grupo": g + 1, "n": int((grupos == g).sum()), "Previsto": float(risco5[grupos == g].mean()),
            "Observado (KM)": km_risco(y[grupos == g])} for g in range(int(grupos.max()) + 1)]
    return obs / risco5.mean(), pd.DataFrame(tab)

# ----------------------------------------------------------------------------- validação cruzada

def validacao_cruzada(X, y, n_rep=5, n_folds=5, log=print):
    cv = RepeatedStratifiedKFold(n_splits=n_folds, n_repeats=n_rep, random_state=SEMENTE)
    divisoes = list(cv.split(X, y["event"]))
    linhas, hiper, oof = [], [], {}
    for nome, cols, est, grade, n_config in modelos():
        t0 = time.time()
        R = np.full((n_rep, len(y)), np.nan)
        for k, (tr, te) in enumerate(divisoes):
            m, hp, avisos = ajustar(est, grade, n_config, X.iloc[tr][cols], y[tr], SEMENTE + k)
            _, r5, fs = predizer(m, X.iloc[te][cols])
            R[k // n_folds, te] = r5
            linhas.append({"Modelo": nome, "Fold": k, **metricas(y[tr], y[te], r5, fs),
                           "Avisos": len(avisos), "Mensagens dos avisos": " | ".join(avisos)})
            hiper.append({"Modelo": nome, "Fold": k, **hp})
        oof[nome] = R.mean(axis=0)
        cuno = np.mean([l["C de Uno (5 anos)"] for l in linhas if l["Modelo"] == nome])
        log(f"  {nome}: C de Uno médio = {cuno:.3f} ({time.time() - t0:.0f} s)")
    return pd.DataFrame(linhas), pd.DataFrame(oof, index=X.index), pd.DataFrame(hiper)

# ----------------------------------------------------------------------------- valor incremental

def _cuno(y, r):
    return concordance_index_ipcw(y, y, r, tau=HORIZONTE)[0]


def _auc5(y, r):
    return cumulative_dynamic_auc(y, y, r, [HORIZONTE])[0][0]


def valor_incremental(y, oof, folds, comparacoes, n_boot=N_BOOT):
    """Diferenças contra a referência no C de Uno (principal) e na AUC em 5 anos, sobre as predições fora da
    partição, com bootstrap pareado de pacientes, IC 95% e IC de Bonferroni (1 - 0,05/m). Condicionais."""
    m = len(comparacoes); nivel = 1 - 0.05 / m
    rng = np.random.default_rng(SEMENTE)
    idx = rng.integers(0, len(y), (n_boot, len(y)))
    ref = oof[REFERENCIA].to_numpy()
    linhas = []
    for nome in comparacoes:
        r = oof[nome].to_numpy()
        for met, f in [("C de Uno (5 anos)", _cuno), ("AUC (5 anos)", _auc5)]:
            d = f(y, r) - f(y, ref)
            bs = []
            for i in idx:
                try:
                    bs.append(f(y[i], r[i]) - f(y[i], ref[i]))
                except ValueError:       # reamostragem sem eventos/censuras suficientes no horizonte
                    continue
            bs = np.array(bs)
            l95, h95 = np.quantile(bs, [0.025, 0.975]); lb, hb = np.quantile(bs, [(1 - nivel) / 2, 1 - (1 - nivel) / 2])
            a = folds.loc[folds.Modelo == nome].set_index("Fold")[met]
            b = folds.loc[folds.Modelo == REFERENCIA].set_index("Fold")[met]
            dfold = a - b
            leitura = "maior" if lb > 0 else ("menor" if hb < 0 else "sem evidência de diferença")
            if met == "C de Uno (5 anos)" and hb < MARGEM:
                leitura += f"; ganho ≥ {MARGEM} incompatível com os dados"
            linhas.append({"Modelo": nome, "Métrica": met, "Diferença": d, "IC95_inf": l95, "IC95_sup": h95,
                           "Comparações (m)": m, "Nível Bonferroni": nivel, "ICBonf_inf": lb, "ICBonf_sup": hb,
                           "Leitura": leitura, "Reamostragens válidas": len(bs),
                           "Δ por partição (média)": dfold.mean(), "Δ por partição (desvio)": dfold.std(),
                           "Partições com ganho (%)": 100 * (dfold > 0).mean()})
    return pd.DataFrame(linhas)

# ----------------------------------------------------------------------------- subgrupo independente

def validacao_subgrupo(df, X, y, n_boot=N_BOOT):
    """Treino nos pacientes dos ensaios randomizados; teste nos não randomizados (Drug ausente), todos."""
    tr = df["Drug"].notna().to_numpy(); te = ~tr
    rng = np.random.default_rng(SEMENTE)
    idx = rng.integers(0, te.sum(), (n_boot, te.sum()))
    linhas, hiper = [], []
    for nome, cols, est, grade, n_config in modelos():
        m, hp, avisos = ajustar(est, grade, n_config, X.loc[tr, cols], y[tr], SEMENTE)
        _, r5, fs = predizer(m, X.loc[te, cols])
        met = metricas(y[tr], y[te], r5, fs)
        oe, _ = calibracao_5anos(y[te], r5)
        yt = y[te]
        bs = []
        for i in idx:
            try:
                bs.append((concordance_index_ipcw(y[tr], yt[i], r5[i], tau=HORIZONTE)[0],
                           cumulative_dynamic_auc(y[tr], yt[i], r5[i], [HORIZONTE])[0][0]))
            except ValueError:
                continue
        bs = np.array(bs)
        linhas.append({"Modelo": nome, **met, "O/E (5 anos)": oe,
                       "C de Uno IC95_inf": np.quantile(bs[:, 0], 0.025), "C de Uno IC95_sup": np.quantile(bs[:, 0], 0.975),
                       "AUC IC95_inf": np.quantile(bs[:, 1], 0.025), "AUC IC95_sup": np.quantile(bs[:, 1], 0.975),
                       "Avisos": len(avisos), "Mensagens dos avisos": " | ".join(avisos)})
        hiper.append({"Cenário": "subgrupo independente", "Modelo": nome, **hp})
    return pd.DataFrame(linhas), int(tr.sum()), int(te.sum()), int(y[te]["event"].sum()), pd.DataFrame(hiper)

# ----------------------------------------------------------------------------- principal

def preparar(desfecho="transplante_livre"):
    df, origem = carregar_dados("local")
    X = codificar(df)
    eventos = ["D", "CL"] if desfecho == "transplante_livre" else ["D"]
    y = Surv.from_arrays(df["Status"].isin(eventos).to_numpy(), df["N_Days"].to_numpy().astype(float))
    return df, X, y, origem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desfecho", choices=["transplante_livre", "obito"], default="transplante_livre")
    ap.add_argument("--n-rep", type=int, default=5)
    a = ap.parse_args()
    suf = "" if a.desfecho == "transplante_livre" else "_obito"
    os.makedirs("resultados_sbcas", exist_ok=True)
    t0 = time.time()
    df, X, y, origem = preparar(a.desfecho)
    print(origem, "| pacientes:", len(y), "| eventos:", int(y["event"].sum()), "| desfecho:", a.desfecho)
    folds, oof, hiper = validacao_cruzada(X, y, n_rep=a.n_rep)
    folds.to_csv(f"resultados_sbcas/folds{suf}.csv", index=False)
    oof.to_csv(f"resultados_sbcas/oof_risco5{suf}.csv")
    hiper.to_csv(f"resultados_sbcas/hiperparametros{suf}.csv", index=False)
    resumo = folds.drop(columns=["Fold", "Avisos", "Mensagens dos avisos"]).groupby("Modelo", sort=False).agg(["mean", "std"])
    resumo.to_csv(f"resultados_sbcas/resumo_cv{suf}.csv")
    print(resumo.round(3).to_string())
    comp = [n for n, *_ in modelos() if n != REFERENCIA]
    vi = valor_incremental(y, oof, folds, comp)
    vi.to_csv(f"resultados_sbcas/valor_incremental{suf}.csv", index=False)
    print(vi[["Modelo", "Métrica", "Diferença", "ICBonf_inf", "ICBonf_sup", "Leitura"]].round(3).to_string())
    cal = []
    for nome in oof.columns:
        oe, tab = calibracao_5anos(y, oof[nome].to_numpy())
        tab.insert(0, "Modelo", nome); tab["O/E (5 anos)"] = oe; cal.append(tab)
    pd.concat(cal).to_csv(f"resultados_sbcas/calibracao_5anos{suf}.csv", index=False)
    if a.desfecho == "transplante_livre":
        sg, ntr, nte, nev, hsg = validacao_subgrupo(df, X, y)
        sg.to_csv("resultados_sbcas/subgrupo_independente.csv", index=False)
        hsg.to_csv("resultados_sbcas/hiperparametros_subgrupo.csv", index=False)
        print(f"subgrupo: treino {ntr}, teste {nte} ({nev} eventos)")
        print(sg.drop(columns=["Mensagens dos avisos"]).round(3).to_string())
    print("avisos na validação cruzada:", int(folds["Avisos"].sum()))
    print("tempo", round(time.time() - t0), "s")


if __name__ == "__main__":
    main()

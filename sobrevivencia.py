"""Análise de sobrevivência da versão SBCAS 2027 (plano em sbcas/PLANO_ANALISE.md).

Pergunta: modelos de aprendizado de máquina para sobrevivência agregam valor ao modelo de Cox com as cinco
variáveis do Escore de Mayo? Desfecho principal: sobrevida livre de transplante (evento = óbito ou transplante),
nos 418 pacientes, sem exclusão pelo horizonte. Desenho 2 x 2: Cox e random survival forest, cada um com as
5 variáveis de Mayo e com as 17 variáveis.

Uso: python sobrevivencia.py [--desfecho obito] [--n-rep 5]
Saídas em resultados_sbcas/ (sufixo _obito para a análise de sensibilidade).
Reutiliza do módulo experimento.py a carga dos dados, a codificação e o pré-processamento."""
import argparse
import json
import os
import platform
import subprocess
import sys
import time
import warnings
from collections import Counter

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
TEMPOS_IBS = np.array([365, 730, 1095, 1461, 1826])   # grade anual do Brier integrado (aproximação trapezoidal)
N_CONFIG_RSF = 50
N_BOOT = 2000
MARGEM = 0.02                          # margem de relevância pré-especificada no C de Uno
REFERENCIA = "Cox, 5 var. (referência)"

# ----------------------------------------------------------------------------- modelos

class UnoRisco5(as_concordance_index_ipcw_scorer):
    """C de Uno truncado em 5 anos calculado sobre o risco em 5 anos, 1 - S(5 anos), a mesma quantidade usada
    na avaliação, na calibração e na curva de decisão (passada A3, achado A3-01). A distribuição de censura
    vem do treino interno, como no scorer original do scikit-survival."""
    def _do_predict(self, X):
        return 1.0 - np.array([f(HORIZONTE) for f in self.estimator_.predict_survival_function(X)])


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
            alvo = UnoRisco5(clone(est), tau=HORIZONTE)
            grade_w = {f"estimator__{k}": v for k, v in grade.items()}
            cv = StratifiedKFold(3, shuffle=True, random_state=semente)
            busca = RandomizedSearchCV(alvo, grade_w, n_iter=n_config, cv=list(cv.split(X, y["event"])),
                                       random_state=semente, n_jobs=1, refit=True, error_score="raise")
            busca.fit(X, y)
            m = busca.best_estimator_.estimator_
            hp = {k.replace("estimator__m__", ""): (v[0] if isinstance(v, list) else v)
                  for k, v in busca.best_params_.items()}
    cont = Counter(f"{a.category.__name__}: {str(a.message)}" for a in avisos)
    if hasattr(m, "named_steps") and isinstance(m.named_steps["m"], CoxnetSurvivalAnalysis):
        hp["coeficientes não nulos"] = int(np.count_nonzero(m.named_steps["m"].coef_[:, -1]))
    return m, hp, cont


def _fmt_avisos(cont):
    """Ocorrências e mensagens distintas completas, com a contagem de cada uma."""
    return sum(cont.values()), len(cont), " | ".join(f"[{n}x] {msg}" for msg, n in sorted(cont.items()))


def predizer(m, X):
    """Escore de risco (maior = maior risco) e risco de evento em 5 anos (1 - S(5 anos))."""
    escore = m.predict(X)
    fs = m.predict_survival_function(X)
    s5 = np.array([f(HORIZONTE) for f in fs])
    return escore, 1.0 - s5, fs

# ----------------------------------------------------------------------------- métricas

def metricas(y_tr, y_te, risco5, fs):
    """Métricas no conjunto de teste, com a distribuição de censura estimada no treino."""
    tmin, tmax = y_te["time"].min(), y_te["time"].max()
    # Suporte completo exigido (A3-04): todos os pontos de 1 a 5 anos dentro do seguimento do teste.
    suporte = bool(tmin < TEMPOS_IBS[0] and TEMPOS_IBS[-1] < tmax)
    s5 = 1.0 - risco5
    res = {
        "C de Uno (5 anos)": concordance_index_ipcw(y_tr, y_te, risco5, tau=HORIZONTE)[0],
        "C de Harrell (risco em 5 anos)": concordance_index_censored(y_te["event"], y_te["time"], risco5)[0],
        "AUC (5 anos)": np.nan, "Brier (5 anos)": np.nan, "Brier integrado (1 a 5 anos)": np.nan,
        "Suporte 1 a 5 anos": suporte,
    }
    if suporte:
        surv_grid = np.array([[f(t) for t in TEMPOS_IBS] for f in fs])
        res["AUC (5 anos)"] = cumulative_dynamic_auc(y_tr, y_te, risco5, [HORIZONTE])[0][0]
        res["Brier (5 anos)"] = brier_score(y_tr, y_te, s5, [HORIZONTE])[1][0]
        res["Brier integrado (1 a 5 anos)"] = integrated_brier_score(y_tr, y_te, surv_grid, TEMPOS_IBS)
    return res


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
    P = np.full((n_rep, len(y)), -1)
    for k, (tr, te) in enumerate(divisoes):
        P[k // n_folds, te] = k % n_folds
    part = pd.DataFrame(P.T, index=X.index, columns=[f"Repetição {r}" for r in range(n_rep)])
    linhas, hiper, oof, oof_nat = [], [], {}, {}
    for nome, cols, est, grade, n_config in modelos():
        t0 = time.time()
        R = np.full((n_rep, len(y)), np.nan); E = np.full((n_rep, len(y)), np.nan)
        for k, (tr, te) in enumerate(divisoes):
            m, hp, avisos = ajustar(est, grade, n_config, X.iloc[tr][cols], y[tr], SEMENTE + k)
            esc, r5, fs = predizer(m, X.iloc[te][cols])
            R[k // n_folds, te] = r5; E[k // n_folds, te] = esc
            n_oc, n_dist, msgs = _fmt_avisos(avisos)
            linhas.append({"Modelo": nome, "Fold": k, **metricas(y[tr], y[te], r5, fs),
                           "C de Uno, escore nativo (5 anos)": concordance_index_ipcw(y[tr], y[te], esc, tau=HORIZONTE)[0],
                           "Avisos (ocorrências)": n_oc, "Avisos (mensagens distintas)": n_dist,
                           "Mensagens dos avisos": msgs})
            hiper.append({"Modelo": nome, "Fold": k, **hp})
        oof[nome] = R.mean(axis=0); oof_nat[nome] = E.mean(axis=0)
        cuno = np.mean([l["C de Uno (5 anos)"] for l in linhas if l["Modelo"] == nome])
        log(f"  {nome}: C de Uno médio = {cuno:.3f} ({time.time() - t0:.0f} s)")
    return (pd.DataFrame(linhas), pd.DataFrame(oof, index=X.index), pd.DataFrame(hiper),
            pd.DataFrame(oof_nat, index=X.index), part)

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
            bs, motivos = [], Counter()
            for i in idx:
                try:
                    bs.append(f(y[i], r[i]) - f(y[i], ref[i]))
                except ValueError as e:  # registrado por motivo (A3-05); outros erros não são silenciados
                    motivos[str(e)[:200]] += 1
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
                           "Reamostragens descartadas": sum(motivos.values()),
                           "Motivos dos descartes": " | ".join(f"[{n}x] {k}" for k, n in motivos.items()),
                           "Δ por partição (média)": dfold.mean(), "Δ por partição (desvio)": dfold.std(),
                           "Partições com ganho (%)": 100 * (dfold > 0).mean()})
    return pd.DataFrame(linhas)

# ----------------------------------------------------------------------------- subgrupo independente

def validacao_subgrupo(df, X, y, n_boot=N_BOOT):
    """Treino nos pacientes dos ensaios randomizados; teste nos não randomizados (Drug ausente), todos."""
    tr = df["Drug"].notna().to_numpy(); te = ~tr
    rng = np.random.default_rng(SEMENTE)
    idx = rng.integers(0, te.sum(), (n_boot, te.sum()))
    linhas, hiper, pred = [], [], pd.DataFrame(index=X.index[te])
    for nome, cols, est, grade, n_config in modelos():
        m, hp, avisos = ajustar(est, grade, n_config, X.loc[tr, cols], y[tr], SEMENTE)
        esc, r5, fs = predizer(m, X.loc[te, cols])
        pred[f"{nome} | risco 5 anos"] = r5; pred[f"{nome} | escore nativo"] = esc
        met = metricas(y[tr], y[te], r5, fs)
        oe, _ = calibracao_5anos(y[te], r5)
        yt = y[te]
        bs, motivos = [], Counter()
        for i in idx:
            try:
                bs.append((concordance_index_ipcw(y[tr], yt[i], r5[i], tau=HORIZONTE)[0],
                           cumulative_dynamic_auc(y[tr], yt[i], r5[i], [HORIZONTE])[0][0]))
            except ValueError as e:      # registrado por motivo (A3-05)
                motivos[str(e)[:200]] += 1
        bs = np.array(bs)
        n_oc, n_dist, msgs = _fmt_avisos(avisos)
        linhas.append({"Modelo": nome, **met, "O/E (5 anos)": oe,
                       "C de Uno IC95_inf": np.quantile(bs[:, 0], 0.025), "C de Uno IC95_sup": np.quantile(bs[:, 0], 0.975),
                       "AUC IC95_inf": np.quantile(bs[:, 1], 0.025), "AUC IC95_sup": np.quantile(bs[:, 1], 0.975),
                       "Reamostragens válidas": len(bs), "Reamostragens descartadas": sum(motivos.values()),
                       "Motivos dos descartes": " | ".join(f"[{n}x] {k}" for k, n in motivos.items()),
                       "Avisos (ocorrências)": n_oc, "Avisos (mensagens distintas)": n_dist,
                       "Mensagens dos avisos": msgs})
        hiper.append({"Cenário": "subgrupo independente", "Modelo": nome, **hp})
    return (pd.DataFrame(linhas), int(tr.sum()), int(te.sum()), int(y[te]["event"].sum()), pd.DataFrame(hiper), pred)

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
    folds, oof, hiper, oof_nat, part = validacao_cruzada(X, y, n_rep=a.n_rep)
    folds.to_csv(f"resultados_sbcas/folds{suf}.csv", index=False)
    oof.to_csv(f"resultados_sbcas/oof_risco5{suf}.csv")
    oof_nat.to_csv(f"resultados_sbcas/oof_escore_nativo{suf}.csv")
    part.to_csv(f"resultados_sbcas/particoes{suf}.csv")
    hiper.to_csv(f"resultados_sbcas/hiperparametros{suf}.csv", index=False)
    resumo = (folds.drop(columns=["Fold", "Suporte 1 a 5 anos", "Avisos (ocorrências)", "Avisos (mensagens distintas)",
                                  "Mensagens dos avisos"]).groupby("Modelo", sort=False).agg(["mean", "std"]))
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
        sg, ntr, nte, nev, hsg, psg = validacao_subgrupo(df, X, y)
        sg.to_csv("resultados_sbcas/subgrupo_independente.csv", index=False)
        hsg.to_csv("resultados_sbcas/hiperparametros_subgrupo.csv", index=False)
        psg.to_csv("resultados_sbcas/predicoes_subgrupo.csv")
        print(f"subgrupo: treino {ntr}, teste {nte} ({nev} eventos)")
        print(sg.drop(columns=["Mensagens dos avisos", "Motivos dos descartes"]).round(3).to_string())
    print("avisos na validação cruzada (ocorrências):", int(folds["Avisos (ocorrências)"].sum()),
          "| partições sem suporte completo de 1 a 5 anos:", int((~folds["Suporte 1 a 5 anos"]).sum()))
    print("tempo", round(time.time() - t0), "s")
    manifesto(a, suf, origem, time.time() - t0)


def manifesto(a, suf, origem, segundos):
    """Proveniência da execução (A3-09): versões efetivas, commit, comando e parâmetros."""
    import sklearn, sksurv
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        sujo = bool(subprocess.run(["git", "status", "--porcelain", "--", "sobrevivencia.py", "experimento.py"],
                                   capture_output=True, text=True).stdout.strip())
    except OSError:
        commit, sujo = "indisponível", None
    info = {"comando": " ".join(sys.argv), "desfecho": a.desfecho, "n_rep": a.n_rep, "commit": commit,
            "código alterado em relação ao commit": sujo, "dados": origem, "segundos": round(segundos),
            "python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
            "scikit-learn": sklearn.__version__, "scikit-survival": sksurv.__version__,
            "semente": SEMENTE, "horizonte (dias)": HORIZONTE, "configurações RSF": N_CONFIG_RSF,
            "reamostragens bootstrap": N_BOOT, "margem": MARGEM}
    with open(f"resultados_sbcas/manifesto{suf}.json", "w", encoding="utf-8") as fh:
        json.dump(info, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()

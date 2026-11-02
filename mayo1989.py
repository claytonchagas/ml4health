"""Plano complementar, D14 e D15: fórmula de Mayo publicada em 1989 (Dickson et al.) como segunda referência.

Só discriminação (C de Uno em 5 anos sobre o escore). Nada é reajustado: os modelos de AM e o Cox reestimado
entram pelas predições já salvas (oof_risco5*.csv, predicoes_subgrupo.csv, folds*.csv, particoes*.csv).
Fórmula final (n = 418, a de uso clínico) e inicial (n = 312, só randomizados): ver sbcas/PLANO_COMPLEMENTAR.md.

Uso (na raiz do repositório): python mayo1989.py
Saídas em resultados_sbcas/: mayo1989_coorte.csv, mayo1989_coorte_obito.csv, mayo1989_derivacao.csv,
mayo1989_subgrupo.csv"""
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from scipy import stats
from sksurv.metrics import concordance_index_ipcw

from experimento import COEF_MAYO, COEF_MAYO_INICIAL, escore_mayo
from sobrevivencia import HORIZONTE, N_BOOT, REFERENCIA, SEMENTE, preparar

R = "resultados_sbcas/"
AM = ["Cox penalizado, 17 var.", "RSF, 5 var.", "RSF, 17 var."]
NIVEL = 1 - 0.05 / 3


def cuno(y_tr, y_te, r):
    return concordance_index_ipcw(y_tr, y_te, r, tau=HORIZONTE)[0]


def escore(X, mediana, coef):
    Z = X.copy()
    Z["Prothrombin"] = Z["Prothrombin"].fillna(mediana)
    return escore_mayo(Z, coef).to_numpy()


def boot_dif(y_cens, y, a, b, nivel, semente=SEMENTE):
    """Diferença pareada C(a) - C(b) com bootstrap de pacientes; censura estimada em y_cens (None = na reamostra)."""
    idx = np.random.default_rng(semente).integers(0, len(y), (N_BOOT, len(y)))
    bs = []
    for i in idx:
        yc = y[i] if y_cens is None else y_cens
        bs.append(cuno(yc, y[i], a[i]) - cuno(yc, y[i], b[i]))
    bs = np.array(bs)
    q = (1 - nivel) / 2
    return np.quantile(bs, q), np.quantile(bs, 1 - q)


def coorte(suf, desfecho):
    """D14 na coorte inteira: fórmula final, C agregado, diferenças pareadas e teste t corrigido."""
    _, X, y, _ = preparar(desfecho)
    oof = pd.read_csv(R + f"oof_risco5{suf}.csv", index_col=0)
    part = pd.read_csv(R + f"particoes{suf}.csv", index_col=0)
    folds = pd.read_csv(R + f"folds{suf}.csv")
    n_rep, n_folds = part.shape[1], int(part.values.max()) + 1
    S = np.full((n_rep, len(y)), np.nan); c_fold = []
    for k in range(n_rep * n_folds):
        rep, f = divmod(k, n_folds)
        te = part.iloc[:, rep].to_numpy() == f; tr = ~te
        s = escore(X[te], X.loc[tr, "Prothrombin"].median(), COEF_MAYO)
        S[rep, te] = s
        c_fold.append(cuno(y[tr], y[te], s))
    s_oof = S.mean(axis=0)
    c_form = cuno(y, y, s_oof)
    linhas = [{"Comparação": "Fórmula de 1989 (final, n = 418)", "C de Uno agregado": c_form,
               "C de Uno médio por partição": np.mean(c_fold)}]
    tcrit = stats.t.ppf(1 - (1 - NIVEL) / 2, len(c_fold) - 1)
    for nome in [REFERENCIA] + AM:
        nivel = 0.95 if nome == REFERENCIA else NIVEL
        r = oof[nome].to_numpy()
        lo, hi = boot_dif(None, y, r, s_oof, nivel)
        d = folds[folds.Modelo == nome].sort_values("Fold")["C de Uno (5 anos)"].to_numpy() - np.array(c_fold)
        ep = np.sqrt(1 / len(d) + 1 / 4) * d.std(ddof=1)
        tc = stats.t.ppf(1 - (1 - nivel) / 2, len(d) - 1) if nome == REFERENCIA else tcrit
        linhas.append({"Comparação": f"{nome} menos fórmula", "C de Uno agregado": cuno(y, y, r),
                       "Diferença": cuno(y, y, r) - c_form, "Nível": nivel,
                       "IC bootstrap inf": lo, "IC bootstrap sup": hi,
                       "Diferença média por partição": d.mean(),
                       "IC teste corrigido inf": d.mean() - tc * ep, "IC teste corrigido sup": d.mean() + tc * ep})
    t = pd.DataFrame(linhas)
    t.to_csv(R + f"mayo1989_coorte{suf}.csv", index=False)
    return t


def derivacao():
    """Vantagem de derivação nos 312 randomizados: fórmulas avaliadas na amostra em que foram estimadas
    contra o Cox reestimado fora da partição (predições agregadas), nos mesmos 312."""
    linhas = []
    for suf, desfecho in [("", "transplante_livre"), ("_obito", "obito")]:
        df, X, y, _ = preparar(desfecho)
        rand = df["Drug"].notna().to_numpy()
        oof = pd.read_csv(R + f"oof_risco5{suf}.csv", index_col=0)
        y3 = y[rand]; med = X.loc[rand, "Prothrombin"].median()
        ref = oof[REFERENCIA].to_numpy()[rand]
        for nome, coef in [("inicial, n = 312", COEF_MAYO_INICIAL), ("final, n = 418", COEF_MAYO)]:
            s = escore(X[rand], med, coef)
            lo, hi = boot_dif(None, y3, ref, s, 0.95)
            linhas.append({"Desfecho": desfecho, "Fórmula": nome, "C fórmula (312)": cuno(y3, y3, s),
                           "C Cox reestimado fora da partição (312)": cuno(y3, y3, ref),
                           "Diferença (Cox reestimado menos fórmula)": cuno(y3, y3, ref) - cuno(y3, y3, s),
                           "IC95 inf": lo, "IC95 sup": hi})
    t = pd.DataFrame(linhas)
    t.to_csv(R + "mayo1989_derivacao.csv", index=False)
    return t


def subgrupo():
    """D15: treino nos 312, teste nos 106 (predições salvas); diferenças pareadas contra a fórmula inicial,
    a final e o Cox reestimado; censura estimada nos 312, como em validacao_subgrupo."""
    df, X, y, _ = preparar()
    tr = df["Drug"].notna().to_numpy(); te = ~tr
    pred = pd.read_csv(R + "predicoes_subgrupo.csv", index_col=0)
    yt, ytr = y[te], y[tr]
    med = X.loc[tr, "Prothrombin"].median()
    refs = {"fórmula inicial (312)": escore(X[te], med, COEF_MAYO_INICIAL),
            "fórmula final (418)": escore(X[te], med, COEF_MAYO),
            REFERENCIA: pred[f"{REFERENCIA} | risco 5 anos"].to_numpy()}
    linhas = [{"Modelo": k, "C de Uno (106)": cuno(ytr, yt, v)} for k, v in refs.items()][:2]
    for nome in [REFERENCIA] + AM:
        r = pred[f"{nome} | risco 5 anos"].to_numpy()
        lin = {"Modelo": nome, "C de Uno (106)": cuno(ytr, yt, r)}
        for k, v in refs.items():
            if k == nome:
                continue
            lo, hi = boot_dif(ytr, yt, r, v, 0.95)
            lin[f"Dif. contra {k}"] = cuno(ytr, yt, r) - cuno(ytr, yt, v)
            lin[f"IC95 inf contra {k}"], lin[f"IC95 sup contra {k}"] = lo, hi
        linhas.append(lin)
    t = pd.DataFrame(linhas)
    t["Eventos (106)"] = int(yt["event"].sum())
    t.to_csv(R + "mayo1989_subgrupo.csv", index=False)
    return t


def main():
    with ProcessPoolExecutor(2) as ex:
        fut = [ex.submit(coorte, "", "transplante_livre"), ex.submit(coorte, "_obito", "obito")]
        d, s = derivacao(), subgrupo()
        c, co = [f.result() for f in fut]
    for nome, t in [("Coorte, principal", c), ("Coorte, só óbito", co), ("Derivação (312)", d), ("Subgrupo (106)", s)]:
        print(f"== {nome}\n{t.round(4).to_string(index=False)}\n")


if __name__ == "__main__":
    main()

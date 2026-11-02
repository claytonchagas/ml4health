"""Plano complementar, D16 (exploratório): comparador alternativo e avaliação dentro da amostra nos 312 randomizados.

Não é reprodução de Graf et al. (2026): o artigo não diz que o C de 0,776 vem do modelo com as sete variáveis do seu
conjunto final (idade, bilirrubina, albumina, fosfatase alcalina, plaquetas, protrombina, estágio). Aqui:
- Cox com essas sete variáveis, Cox com as cinco de Mayo e RSF de 17 variáveis, nas mesmas partições do estudo
  (particoes.csv) restritas aos 312; Cox com o mesmo pré-processamento do Cox de referência (log dos exames
  assimétricos, imputação no treino, padronização); RSF com os hiperparâmetros já escolhidos no treino dos 312
  (hiperparametros_subgrupo.csv), sem nova busca;
- C de Harrell (a métrica de Graf) e C de Uno em 5 anos, por partição e nas predições agregadas, com diferenças
  pareadas por bootstrap (2.000, semente 2026, IC 95%);
- avaliação dentro da amostra: cada modelo ajustado nos 312 e avaliado nos mesmos 312.

Uso (na raiz do repositório): python comparador_graf.py
Saídas: resultados_sbcas/graf312_particoes.csv, graf312_comparacoes.csv, graf312_dentro_amostra.csv"""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sksurv.ensemble import RandomSurvivalForest
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw

from experimento import MAYO5, TODAS17
from sobrevivencia import (HORIZONTE, N_BOOT, REFERENCIA, SEMENTE, _preproc_arvore, _preproc_cox, predizer,
                           preparar)

R = "resultados_sbcas/"
GRAF7 = ["Age", "Bilirubin", "Albumin", "Alk_Phos", "Platelets", "Prothrombin", "Stage"]
NOME_GRAF = "Cox, 7 var. (conjunto final de Graf et al.)"
NOME_RSF = "RSF, 17 var."


def modelos_312():
    hp = pd.read_csv(R + "hiperparametros_subgrupo.csv").set_index("Modelo").loc[NOME_RSF]
    prof = None if pd.isna(hp["max_depth"]) else int(hp["max_depth"])
    mf = hp["max_features"]
    try:
        mf = float(mf)
    except ValueError:
        pass
    rsf = RandomSurvivalForest(n_estimators=300, random_state=SEMENTE, n_jobs=-1,
                               min_samples_leaf=int(hp["min_samples_leaf"]), min_samples_split=int(hp["min_samples_split"]),
                               max_features=mf, max_depth=prof)
    return [(REFERENCIA, MAYO5, Pipeline(_preproc_cox(MAYO5) + [("m", CoxPHSurvivalAnalysis(alpha=0.0, ties="breslow"))])),
            (NOME_GRAF, GRAF7, Pipeline(_preproc_cox(GRAF7) + [("m", CoxPHSurvivalAnalysis(alpha=0.0, ties="breslow"))])),
            (NOME_RSF, TODAS17, Pipeline(_preproc_arvore(TODAS17) + [("m", rsf)]))]


def harrell(y, r):
    return concordance_index_censored(y["event"], y["time"], r)[0]


def uno(y_tr, y_te, r):
    return concordance_index_ipcw(y_tr, y_te, r, tau=HORIZONTE)[0]


def main():
    df, X, y, _ = preparar()
    rand = df["Drug"].notna().to_numpy()
    X3, y3 = X[rand], y[rand]
    part = pd.read_csv(R + "particoes.csv", index_col=0).loc[X3.index]
    n_rep, n_folds = part.shape[1], int(part.values.max()) + 1
    mods = modelos_312()
    oof = {n: np.full((n_rep, len(y3)), np.nan) for n, _, _ in mods}
    linhas = []
    for k in range(n_rep * n_folds):
        rep, f = divmod(k, n_folds)
        te = part.iloc[:, rep].to_numpy() == f; tr = ~te
        for nome, cols, est in mods:
            m = clone(est).fit(X3.iloc[tr][cols], y3[tr])
            _, r5, _ = predizer(m, X3.iloc[te][cols])
            oof[nome][rep, te] = r5
            linhas.append({"Modelo": nome, "Fold": k, "C de Harrell": harrell(y3[te], r5),
                           "C de Uno (5 anos)": uno(y3[tr], y3[te], r5)})
    pd.DataFrame(linhas).to_csv(R + "graf312_particoes.csv", index=False)
    agg = {n: v.mean(axis=0) for n, v in oof.items()}

    idx = np.random.default_rng(SEMENTE).integers(0, len(y3), (N_BOOT, len(y3)))
    comp = []
    for a, b in [(NOME_GRAF, REFERENCIA), (NOME_RSF, REFERENCIA), (NOME_RSF, NOME_GRAF)]:
        for met, fn in [("C de Harrell", lambda yy, r: harrell(yy, r)), ("C de Uno (5 anos)", lambda yy, r: uno(yy, yy, r))]:
            d = fn(y3, agg[a]) - fn(y3, agg[b])
            bs = np.array([fn(y3[i], agg[a][i]) - fn(y3[i], agg[b][i]) for i in idx])
            comp.append({"Comparação": f"{a} menos {b}", "Métrica": met, "C de a": fn(y3, agg[a]), "C de b": fn(y3, agg[b]),
                         "Diferença": d, "IC95 inf": np.quantile(bs, 0.025), "IC95 sup": np.quantile(bs, 0.975)})
    pd.DataFrame(comp).to_csv(R + "graf312_comparacoes.csv", index=False)

    dentro = []
    for nome, cols, est in mods:
        m = clone(est).fit(X3[cols], y3)
        _, r5, _ = predizer(m, X3[cols])
        fora = pd.DataFrame(linhas).query("Modelo == @nome")["C de Harrell"].mean()
        dentro.append({"Modelo": nome, "C de Harrell dentro da amostra": harrell(y3, r5),
                       "C de Harrell fora da partição (média)": fora,
                       "Otimismo": harrell(y3, r5) - fora})
    pd.DataFrame(dentro).to_csv(R + "graf312_dentro_amostra.csv", index=False)

    print(pd.DataFrame(linhas).groupby("Modelo")[["C de Harrell", "C de Uno (5 anos)"]].mean().round(4).to_string())
    print(pd.DataFrame(comp).round(4).to_string(index=False))
    print(pd.DataFrame(dentro).round(4).to_string(index=False))


if __name__ == "__main__":
    main()

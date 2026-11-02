"""Importância por permutação da random survival forest de 17 variáveis (plano SBCAS, seção 7; DESVIOS.md, D8).

Medida fora da amostra: na primeira repetição da validação cruzada (5 partições, as mesmas de sobrevivencia.py),
a floresta é reajustada no treino de cada partição com os hiperparâmetros escolhidos naquela partição
(hiperparametros.csv), e a importância é a queda média no C de Uno truncado em 5 anos (risco em 5 anos) no teste
quando a variável é permutada, com 30 permutações por variável (semente 2026). A distribuição de censura vem do
treino. Resultado: média e desvio entre as 5 partições. Vai para o material suplementar.

Uso: python importancia_permutacao.py"""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import RepeatedStratifiedKFold
from sksurv.metrics import concordance_index_ipcw

from experimento import TODAS17
from sobrevivencia import HORIZONTE, SEMENTE, modelos, predizer, preparar

N_PERM = 30
NOME = "RSF, 17 var."


def main():
    _, X, y, _ = preparar("transplante_livre")
    hp = pd.read_csv("resultados_sbcas/hiperparametros.csv")
    hp = hp[hp.Modelo == NOME].set_index("Fold")
    est = [e for n, _, e, _, _ in modelos() if n == NOME][0]
    divisoes = list(RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=SEMENTE).split(X, y["event"]))[:5]
    rng = np.random.default_rng(SEMENTE)
    quedas = []
    for k, (tr, te) in enumerate(divisoes):
        h = hp.loc[k]
        params = {"m__min_samples_leaf": int(h["min_samples_leaf"]), "m__min_samples_split": int(h["min_samples_split"]),
                  "m__max_features": h["max_features"] if h["max_features"] == "sqrt" else float(h["max_features"]),
                  "m__max_depth": None if pd.isna(h["max_depth"]) else int(h["max_depth"])}
        m = clone(est).set_params(**params).fit(X.iloc[tr][TODAS17], y[tr])
        Xte = X.iloc[te][TODAS17].reset_index(drop=True)
        base = concordance_index_ipcw(y[tr], y[te], predizer(m, Xte)[1], tau=HORIZONTE)[0]
        for c in TODAS17:
            vals = []
            for _ in range(N_PERM):
                Xp = Xte.copy(); Xp[c] = rng.permutation(Xp[c].to_numpy())
                vals.append(base - concordance_index_ipcw(y[tr], y[te], predizer(m, Xp)[1], tau=HORIZONTE)[0])
            quedas.append({"Partição": k, "Variável": c, "Queda no C de Uno": float(np.mean(vals))})
        print(f"partição {k}: C de Uno {base:.3f}")
    q = pd.DataFrame(quedas)
    res = (q.groupby("Variável")["Queda no C de Uno"].agg(["mean", "std"]).sort_values("mean", ascending=False)
           .rename(columns={"mean": "Queda média", "std": "Desvio entre partições"}))
    res.to_csv("resultados_sbcas/importancia_permutacao_rsf17.csv")
    print(res.round(4).to_string())


if __name__ == "__main__":
    main()

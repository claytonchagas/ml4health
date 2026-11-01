"""Intervalos de confiança 95% da AUROC, da calibração no geral (CITL) e da inclinação de calibração
de cada modelo, sobre as predições fora da partição já salvas em resultados/oof.csv.

Uso: python ic_desempenho.py   (segundos; não treina nada)
Saída: resultados/ic_desempenho_oof.csv

Procedimento: bootstrap pareado de pacientes, 2.000 reamostragens, semente 2026, as mesmas reamostragens
para todos os modelos. As estimativas pontuais são calculadas sobre as predições médias das 5 repetições
e diferem ligeiramente das médias por partição da Tabela 4 do artigo. Como as predições já estão fixadas,
os intervalos não incorporam a variação de refazer o treino (são condicionais, como os de valor incremental)."""
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

from experimento import SEMENTE, calibracao, carregar_dados, rotulo_5anos

N_BOOT = 2000


def main():
    warnings.filterwarnings("ignore")
    df, _ = carregar_dados("local")
    y = rotulo_5anos(df)
    y = y[y.notna()].astype(int)
    oof = pd.read_csv("resultados/oof.csv", index_col=0)
    assert oof.index.equals(y.index), "predições e rótulos desalinhados"
    yv = y.to_numpy()
    idx = np.random.default_rng(SEMENTE).integers(0, len(yv), (N_BOOT, len(yv)))
    linhas = []
    for nome in oof.columns:
        p = oof[nome].to_numpy()
        auc = roc_auc_score(yv, p)
        citl, incl = calibracao(yv, p)
        bs = np.array([[roc_auc_score(yv[i], p[i]), *calibracao(yv[i], p[i])] for i in idx])
        q = np.quantile(bs, [0.025, 0.975], axis=0)
        linhas.append({"Modelo": nome,
                       "AUROC": auc, "AUROC_IC95_inf": q[0, 0], "AUROC_IC95_sup": q[1, 0],
                       "CITL": citl, "CITL_IC95_inf": q[0, 1], "CITL_IC95_sup": q[1, 1],
                       "Incl. calibr.": incl, "Incl_IC95_inf": q[0, 2], "Incl_IC95_sup": q[1, 2]})
    res = pd.DataFrame(linhas)
    res.to_csv("resultados/ic_desempenho_oof.csv", index=False)
    print(res.round(3).to_string(index=False))


if __name__ == "__main__":
    main()

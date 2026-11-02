"""Pressupostos e razões de risco do Cox de referência (plano SBCAS, seção 7; passada A3, achado A3-11).

Ajusta o Cox com as 5 variáveis de Mayo nos 418 pacientes, com a mesma forma do modelo de referência
(log natural de bilirrubina, albumina e protrombina; imputação pela mediana dos 2 valores ausentes de protrombina),
sem padronização, para que as razões de risco tenham unidade clínica:
- idade: por 10 anos;
- bilirrubina, albumina e protrombina: por duplicação do valor (coeficiente do log natural vezes ln 2);
- edema: de ausente (0) a presente apesar de diurético (1), na codificação 0 / 0,5 / 1 de Mayo.

Teste de riscos proporcionais de Grambsch e Therneau (resíduos de Schoenfeld escalonados), por variável,
com o tempo transformado pelo Kaplan-Meier (padrão de cox.zph no R) e também pelo posto, como sensibilidade.
A biblioteca não oferece o teste global exato; a leitura é por variável, com correção de Bonferroni para 5 testes.
Sensibilidade: o mesmo teste com o seguimento censurado em 5 anos, a janela usada na predição.
O modelo é descritivo (ajustado em todos os pacientes) e não entra na avaliação preditiva.

Uso: python pressupostos_cox.py [--desfecho obito]"""
import argparse

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from lifelines.statistics import proportional_hazard_test

from experimento import MAYO5
from sobrevivencia import HORIZONTE, preparar

ESCALA = {"Age": ("Idade (por 10 anos)", 10.0), "Bilirubin": ("Bilirrubina (por duplicação)", np.log(2)),
          "Albumin": ("Albumina (por duplicação)", np.log(2)), "Prothrombin": ("Tempo de protrombina (por duplicação)", np.log(2)),
          "Edema": ("Edema (0 a 1)", 1.0)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desfecho", choices=["transplante_livre", "obito"], default="transplante_livre")
    a = ap.parse_args()
    suf = "" if a.desfecho == "transplante_livre" else "_obito"
    _, X, y, _ = preparar(a.desfecho)
    d = X[MAYO5].copy()
    d["Prothrombin"] = d["Prothrombin"].fillna(d["Prothrombin"].median())
    for c in ["Bilirubin", "Albumin", "Prothrombin"]:
        d[c] = np.log(d[c])
    d["T"] = y["time"]; d["E"] = y["event"].astype(int)
    cph = CoxPHFitter(baseline_estimation_method="breslow").fit(d, "T", "E")

    s = cph.summary
    hr = pd.DataFrame({
        "Variável": [ESCALA[c][0] for c in MAYO5],
        "Razão de risco": [np.exp(s.loc[c, "coef"] * ESCALA[c][1]) for c in MAYO5],
        "IC95_inf": [np.exp(s.loc[c, "coef lower 95%"] * ESCALA[c][1]) for c in MAYO5],
        "IC95_sup": [np.exp(s.loc[c, "coef upper 95%"] * ESCALA[c][1]) for c in MAYO5],
        "p (Wald)": [s.loc[c, "p"] for c in MAYO5],
    })

    # Sensibilidade: seguimento censurado administrativamente em 5 anos, a janela que a predição usa.
    d5 = d.copy()
    d5["E"] = ((d["E"] == 1) & (d["T"] <= HORIZONTE)).astype(int); d5["T"] = np.minimum(d["T"], HORIZONTE)
    cph5 = CoxPHFitter(baseline_estimation_method="breslow").fit(d5, "T", "E")

    linhas = []
    for janela, modelo, dados in [("todo o seguimento", cph, d), ("até 5 anos", cph5, d5)]:
        for transf in ["km", "rank"]:
            t = proportional_hazard_test(modelo, dados, time_transform=transf)
            for c in MAYO5:
                linhas.append({"Janela": janela, "Transformação do tempo": transf, "Variável": ESCALA[c][0],
                               "Estatística": t.summary.loc[c, "test_statistic"], "p": t.summary.loc[c, "p"]})
    ph = pd.DataFrame(linhas)
    # Sem teste global exato nesta biblioteca: leitura por variável com correção de Bonferroni para 5 testes.
    ph["p (Bonferroni, 5 testes)"] = np.minimum(ph["p"] * len(MAYO5), 1.0)

    hr.to_csv(f"resultados_sbcas/cox5_razoes_risco{suf}.csv", index=False)
    ph.to_csv(f"resultados_sbcas/cox5_riscos_proporcionais{suf}.csv", index=False)
    print(f"desfecho: {a.desfecho} | pacientes: {len(d)} | eventos: {int(d['E'].sum())} | "
          f"C de Harrell aparente: {cph.concordance_index_:.3f}")
    print(hr.round(3).to_string(index=False))
    print(ph.round(4).to_string(index=False))


if __name__ == "__main__":
    main()

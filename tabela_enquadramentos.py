"""Tabela de enquadramentos (plano SBCAS, seção 7; DESVIOS.md, D8).

Uma linha por enquadramento, só com resultados já salvos (nada é retreinado):
(a) classificação de óbito em 5 anos com exclusão de quem saiu antes sem óbito (disciplina; resultados/);
(b) sobrevivência, desfecho composto óbito ou transplante (principal; resultados_sbcas/);
(c) sobrevivência, só óbito, transplante censurado (sensibilidade; resultados_sbcas/*_obito);
(d) classificação em 3 classes (C, CL, D) com e sem N_Days na entrada (disciplina; resultados/vazamento.csv).

Em (a) a (c), "melhor AM" é o modelo de aprendizado de máquina com a maior diferença pontual contra a referência
naquele enquadramento (a escolha mais favorável ao AM), com o IC de Bonferroni já calculado no script de origem.
(a) e (c) têm o mesmo evento (óbito) e diferem na tarefa; (b) e (c) têm a mesma tarefa e diferem no desfecho.
Em (d) a comparação é outra (com contra sem N_Days, mesmo modelo): diferença média pareada por partição
(mesmas 25 partições), com desvio e porcentagem de partições com ganho; não há bootstrap nesse experimento.

Uso: python tabela_enquadramentos.py"""
import numpy as np
import pandas as pd

from experimento import carregar_dados, rotulo_5anos
from sobrevivencia import preparar


def melhor(vi, col_delta):
    return vi.loc[vi[col_delta].idxmax()], len(vi)


def main():
    linhas = []

    # (a) classificação em 5 anos com exclusão
    df, _ = carregar_dados("local")
    y = rotulo_5anos(df)
    vi = pd.read_csv("resultados/valor_incremental.csv")
    lin, m = melhor(vi, "ΔAUROC")
    linhas.append({"Enquadramento": "(a) Classificação, óbito até 5 anos, com exclusão", "Papel": "disciplina",
                   "n": int(y.notna().sum()), "Eventos": int(y.sum()), "Métrica": "AUROC",
                   "Referência": lin["Referência"], "Comparação": lin["Modelo"], "Δ": lin["ΔAUROC"],
                   "IC_inf": lin["ICBonf_inf"], "IC_sup": lin["ICBonf_sup"],
                   "Tipo de IC": f"bootstrap pareado, Bonferroni m={int(lin['Comparações (m)'])}",
                   "Modelos de AM comparados": m})

    # (b) e (c) sobrevivência
    for rot, papel, suf, desf in [("(b) Sobrevivência, óbito ou transplante", "principal", "", "transplante_livre"),
                                  ("(c) Sobrevivência, só óbito (transplante censurado)", "sensibilidade", "_obito", "obito")]:
        _, _, ys, _ = preparar(desf)
        vi = pd.read_csv(f"resultados_sbcas/valor_incremental{suf}.csv")
        vi = vi[vi["Métrica"] == "C de Uno (5 anos)"]
        lin, m = melhor(vi, "Diferença")
        linhas.append({"Enquadramento": rot, "Papel": papel, "n": len(ys), "Eventos": int(ys["event"].sum()),
                       "Métrica": "C de Uno (5 anos)", "Referência": "Cox, 5 var.", "Comparação": lin["Modelo"],
                       "Δ": lin["Diferença"], "IC_inf": lin["ICBonf_inf"], "IC_sup": lin["ICBonf_sup"],
                       "Tipo de IC": f"bootstrap pareado, Bonferroni m={int(lin['Comparações (m)'])}",
                       "Modelos de AM comparados": m})

    # (d) N_Days como entrada
    vz = pd.read_csv("resultados/vazamento.csv")
    p = vz.pivot(index="Fold", columns="Entrada", values="AUROC macro (OvR)")
    dlt = p["com N_Days"] - p["sem N_Days"]
    st = df["Status"]
    linhas.append({"Enquadramento": "(d) Classificação C/CL/D, com contra sem N_Days na entrada", "Papel": "disciplina",
                   "n": int(st.notna().sum()), "Eventos": int((st == "D").sum()), "Métrica": "AUROC macro (OvR)",
                   "Referência": "XGBoost, 17 var., sem N_Days", "Comparação": "XGBoost, 17 var., com N_Days",
                   "Δ": dlt.mean(), "IC_inf": np.nan, "IC_sup": np.nan,
                   "Tipo de IC": f"sem IC; desvio entre partições {dlt.std():.3f}; "
                                 f"{100 * (dlt > 0).mean():.0f}% das {len(dlt)} partições com ganho",
                   "Modelos de AM comparados": 1})

    tab = pd.DataFrame(linhas)
    tab.to_csv("resultados_sbcas/tabela_enquadramentos.csv", index=False)
    print(tab.round(3).to_string(index=False))


if __name__ == "__main__":
    main()

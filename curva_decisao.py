"""Curva de decisão (benefício líquido) em 5 anos com censura (plano SBCAS, seção 7; DESVIOS.md, D8).

Benefício líquido no limiar p (Vickers et al., 2008, extensão para desfechos de sobrevivência):
    BL(p) = P(evento até 5 anos e risco >= p) - P(sem evento até 5 anos e risco >= p) * p / (1 - p),
com P(evento até 5 anos | risco >= p) estimada por Kaplan-Meier no grupo acima do limiar, o que trata a censura.
"Tratar todos" usa o Kaplan-Meier da coorte; "tratar nenhum" vale zero.
Sobre as predições fora da partição salvas por sobrevivencia.py, sem retreinar.
Modelos: referência e a random survival forest de maior C de Uno médio (mesma regra de calibracao_figura.py).
Escolher o melhor modelo nesta coorte introduz seleção; o texto do artigo declara isso.

Uso: python curva_decisao.py [--desfecho obito]"""
import argparse

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42  # fontes TrueType embutidas (sem Type 3)
matplotlib.rcParams["font.family"] = "DejaVu Sans"  # fonte TrueType pura, aceita por verificadores de PDF
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
from sksurv.nonparametric import kaplan_meier_estimator

from sobrevivencia import HORIZONTE, REFERENCIA, preparar

LIMIARES = np.round(np.arange(0.05, 0.501, 0.01), 2)


VIRGULA = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))  # vírgula decimal (artigo em português)


def risco_km(evento, tempo):
    if len(tempo) == 0:
        return 0.0
    t, s = kaplan_meier_estimator(evento, tempo)
    j = np.searchsorted(t, HORIZONTE, side="right") - 1
    return 1 - s[j] if j >= 0 else 0.0


def beneficio_liquido(y, risco, p):
    acima = risco >= p
    frac = acima.mean()
    if frac == 0:
        return 0.0
    r = risco_km(y["event"][acima], y["time"][acima])
    return r * frac - (1 - r) * frac * p / (1 - p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desfecho", choices=["transplante_livre", "obito"], default="transplante_livre")
    a = ap.parse_args()
    suf = "" if a.desfecho == "transplante_livre" else "_obito"
    _, X, y, _ = preparar(a.desfecho)
    oof = pd.read_csv(f"resultados_sbcas/oof_risco5{suf}.csv", index_col=0)
    resumo = pd.read_csv(f"resultados_sbcas/resumo_cv{suf}.csv", header=[0, 1], index_col=0)
    c_uno = resumo[("C de Uno (5 anos)", "mean")]
    melhor_am = c_uno[[n for n in c_uno.index if n.startswith("RSF")]].idxmax()

    r_todos = risco_km(y["event"], y["time"])
    linhas = []
    for p in LIMIARES:
        lin = {"Limiar": p, "Tratar todos": r_todos - (1 - r_todos) * p / (1 - p), "Tratar nenhum": 0.0}
        for nome in oof.columns:
            lin[nome] = beneficio_liquido(y, oof[nome].to_numpy(), p)
        linhas.append(lin)
    tab = pd.DataFrame(linhas)
    tab.to_csv(f"resultados_sbcas/curva_decisao{suf}.csv", index=False)

    fig, ax = plt.subplots(figsize=(4.6, 3.1))
    ax.plot(tab["Limiar"], tab["Tratar todos"], color="0.6", lw=1, ls=":", label="Tratar todos")
    ax.axhline(0, color="0.3", lw=1, label="Tratar nenhum")
    ax.plot(tab["Limiar"], tab[REFERENCIA], color="#1f4e79", lw=1.8, label=REFERENCIA)
    ax.plot(tab["Limiar"], tab[melhor_am], color="#c55a11", lw=1.8, ls="--", label=melhor_am)
    topo = max(tab[[REFERENCIA, melhor_am]].max().max(), r_todos) * 1.1
    ax.set_ylim(-0.05, topo); ax.set_xlim(LIMIARES[0], LIMIARES[-1])
    ax.set_xlabel("Limiar de risco em 5 anos", fontsize=10); ax.set_ylabel("Benefício líquido", fontsize=10)
    ax.tick_params(labelsize=9)
    ax.xaxis.set_major_formatter(VIRGULA); ax.yaxis.set_major_formatter(VIRGULA); ax.grid(alpha=0.25); ax.legend(fontsize=8.5, frameon=False)
    fig.tight_layout()
    fig.savefig(f"resultados_sbcas/figura_curva_decisao{suf}.pdf")
    fig.savefig(f"resultados_sbcas/figura_curva_decisao{suf}.png", dpi=200)
    print("melhor modelo de AM pela regra:", melhor_am)
    print(tab.iloc[::5].round(3).to_string(index=False))


if __name__ == "__main__":
    main()

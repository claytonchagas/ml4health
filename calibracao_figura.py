"""Calibração em 5 anos com incerteza (plano SBCAS, seção 5; passada A3, achado A3-06).

Lê as predições fora da partição salvas por sobrevivencia.py (sem retreinar) e produz:
- tabela por quintis de risco previsto: n, número em risco aos 5 anos, eventos até 5 anos, risco médio previsto,
  risco observado por Kaplan-Meier com IC 95% (Greenwood, transformação log-log);
- razão observado/esperado em 5 anos com IC 95% por bootstrap de pacientes (2.000 reamostragens, semente 2026);
- figura previsto contra observado: referência e o melhor modelo de aprendizado de máquina (figura principal),
  e os quatro modelos (suplementar).

Regra de escolha do "melhor modelo de aprendizado de máquina", fixada antes de ver a figura: a random survival
forest com maior C de Uno médio na validação cruzada (resumo_cv). Os intervalos são condicionais às predições.
Hipótese: censura independente dentro de cada quintil (Kaplan-Meier por grupo).

Uso: python calibracao_figura.py [--desfecho obito]"""
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
from sksurv.nonparametric import kaplan_meier_estimator

from sobrevivencia import HORIZONTE, REFERENCIA, SEMENTE, preparar

N_BOOT = 2000


VIRGULA = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))  # vírgula decimal (artigo em português)


def km_horizonte(evento, tempo):
    """Risco observado em 5 anos (1 - S) e IC 95% (Greenwood, log-log)."""
    t, s, ic = kaplan_meier_estimator(evento, tempo, conf_type="log-log")
    j = np.searchsorted(t, HORIZONTE, side="right") - 1
    if j < 0:
        return 0.0, 0.0, 0.0
    return 1 - s[j], 1 - ic[1][j], 1 - ic[0][j]


def km_simples(evento, tempo):
    t, s = kaplan_meier_estimator(evento, tempo)
    j = np.searchsorted(t, HORIZONTE, side="right") - 1
    return 1 - s[j] if j >= 0 else 0.0


def tabela_quintis(y, risco, nome):
    grupos = pd.qcut(risco, 5, labels=False, duplicates="drop")
    linhas = []
    for g in range(int(grupos.max()) + 1):
        sel = grupos == g
        ev, tp = y["event"][sel], y["time"][sel]
        obs, li, ls = km_horizonte(ev, tp)
        n5 = int((tp >= HORIZONTE).sum())
        nota = ""
        if not np.any(ev & (tp <= HORIZONTE)):
            # Sem eventos até 5 anos: Greenwood não define o intervalo. Limite superior binomial exato
            # (Clopper-Pearson, 97,5%) com o número em risco aos 5 anos; aproximação conservadora sob censura.
            li, ls = 0.0, 1 - 0.025 ** (1 / max(n5, 1))
            nota = "sem eventos; limite superior binomial exato"
        linhas.append({"Modelo": nome, "Quintil": g + 1, "n": int(sel.sum()),
                       "Em risco aos 5 anos": n5,
                       "Eventos até 5 anos": int((ev & (tp <= HORIZONTE)).sum()),
                       "Previsto (média)": float(risco[sel].mean()),
                       "Observado (KM)": obs, "Observado IC95_inf": li, "Observado IC95_sup": ls, "Nota": nota})
    return pd.DataFrame(linhas)


def oe_bootstrap(y, risco, idx):
    oe = km_simples(y["event"], y["time"]) / risco.mean()
    bs = np.array([km_simples(y["event"][i], y["time"][i]) / risco[i].mean() for i in idx])
    return oe, *np.quantile(bs, [0.025, 0.975])


def painel(ax, tab, titulo, oe):
    lim = 1.0
    ax.plot([0, lim], [0, lim], ls="--", lw=1, color="0.6", zorder=1)
    err = np.vstack([tab["Observado (KM)"] - tab["Observado IC95_inf"],
                     tab["Observado IC95_sup"] - tab["Observado (KM)"]])
    ax.errorbar(tab["Previsto (média)"], tab["Observado (KM)"], yerr=err, fmt="o", ms=5, capsize=3,
                color="#1f4e79", ecolor="#1f4e79", lw=1.2, zorder=2)
    ax.set_xlim(0, lim); ax.set_ylim(0, lim); ax.set_aspect("equal")
    ax.set_title(titulo, fontsize=11)
    ax.set_xlabel("Risco previsto em 5 anos", fontsize=10)
    ax.set_ylabel("Risco observado em 5 anos (KM)", fontsize=10)
    ax.text(0.04, 0.93, f"O/E = {oe[0]:.2f} ({oe[1]:.2f} a {oe[2]:.2f})".replace(".", ","),
            transform=ax.transAxes, fontsize=9)
    ax.tick_params(labelsize=9)
    ax.xaxis.set_major_formatter(VIRGULA); ax.yaxis.set_major_formatter(VIRGULA)
    ax.grid(alpha=0.25)


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
    idx = np.random.default_rng(SEMENTE).integers(0, len(y), (N_BOOT, len(y)))

    tabs, oes = [], {}
    for nome in oof.columns:
        r = oof[nome].to_numpy()
        tabs.append(tabela_quintis(y, r, nome))
        oes[nome] = oe_bootstrap(y, r, idx)
    tab = pd.concat(tabs, ignore_index=True)
    tab["O/E (5 anos)"] = tab["Modelo"].map(lambda n: oes[n][0])
    tab["O/E IC95_inf"] = tab["Modelo"].map(lambda n: oes[n][1])
    tab["O/E IC95_sup"] = tab["Modelo"].map(lambda n: oes[n][2])
    tab.to_csv(f"resultados_sbcas/calibracao_quintis_ic{suf}.csv", index=False)

    for arq, nomes in [(f"figura_calibracao{suf}", [REFERENCIA, melhor_am]),
                       (f"figura_calibracao_suplementar{suf}", list(oof.columns))]:
        ncol = 2
        nlin = int(np.ceil(len(nomes) / ncol))
        fig, axs = plt.subplots(nlin, ncol, figsize=(5.2, 2.75 * nlin))
        for ax, nome in zip(np.atleast_1d(axs).ravel(), nomes):
            painel(ax, tab[tab.Modelo == nome], nome, oes[nome])
        fig.tight_layout()
        fig.savefig(f"resultados_sbcas/{arq}.pdf"); fig.savefig(f"resultados_sbcas/{arq}.png", dpi=200)
        plt.close(fig)
    print("melhor modelo de AM pela regra:", melhor_am)
    print(tab.round(3).to_string())


if __name__ == "__main__":
    main()

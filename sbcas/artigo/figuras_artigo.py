"""Figuras do artigo SBCAS, geradas no tamanho em que são impressas (largura do texto, 16 cm), com fontes reais
de 7 a 8 pt, para que nada seja reduzido na inclusão.

Figura única do artigo (figura_painel.pdf), em duas linhas. Em cima, (a) a (c): calibração em 5 anos por quintis na
referência, no Cox penalizado de 17 variáveis (o desvio mais nítido, acrescentado à figura depois dos resultados) e na
RSF de maior C de Uno médio (regra fixada após a primeira execução); os quatro modelos estão em
resultados_sbcas/figura_calibracao_suplementar.pdf. Embaixo, (d) curva de decisão em 5 anos e (e) importância por
permutação da RSF de 17 variáveis (5 partições da primeira repetição; as oito maiores quedas).

Só lê CSVs já salvos (calibracao_quintis_ic.csv, curva_decisao.csv, importancia_permutacao_rsf17.csv, resumo_cv.csv);
nada é reajustado nem recalculado. Uso (na raiz do repositório): python sbcas/artigo/figuras_artigo.py"""
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42  # fontes TrueType embutidas (sem Type 3)
matplotlib.rcParams["font.family"] = "DejaVu Sans"  # fonte TrueType pura, aceita por verificadores de PDF
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

VIRGULA = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
REF, COXPEN, RSF17 = "Cox, 5 var. (referência)", "Cox penalizado, 17 var.", "RSF, 17 var."
NOMES = {"Bilirubin": "Bilirrubina", "Copper": "Cobre urinário", "Albumin": "Albumina", "Stage": "Estágio histológico",
         "Edema": "Edema", "Ascites": "Ascite", "Prothrombin": "Tempo de protrombina", "Age": "Idade",
         "SGOT": "AST", "Cholesterol": "Colesterol", "Tryglicerides": "Triglicerídeos", "Sex_M": "Sexo",
         "Spiders": "Aranhas vasculares", "Hepatomegaly": "Hepatomegalia", "Drug_Dpen": "Tratamento",
         "Alk_Phos": "Fosfatase alcalina", "Platelets": "Plaquetas"}
MAYO = {"Bilirubin", "Albumin", "Prothrombin", "Edema", "Age"}
N_MOSTRAR = 8
LARGURA = 6.3  # polegadas: largura do texto no modelo da SBC (16 cm)
AZUL, LARANJA = "#1f4e79", "#c55a11"
R = "resultados_sbcas"
SAIDA = "sbcas/artigo/figuras"


def melhor_rsf():
    """A RSF de maior C de Uno médio na validação cruzada (mesma regra de calibracao_figura.py, desvio D6)."""
    resumo = pd.read_csv(f"{R}/resumo_cv.csv", header=[0, 1], index_col=0)
    c = resumo[("C de Uno (5 anos)", "mean")]
    return c[[n for n in c.index if n.startswith("RSF")]].idxmax()


def painel_calibracao(ax, tab, titulo, mostrar_y):
    ax.plot([0, 1], [0, 1], ls="--", lw=0.8, color="0.6", zorder=1)
    err = np.vstack([tab["Observado (KM)"] - tab["Observado IC95_inf"], tab["Observado IC95_sup"] - tab["Observado (KM)"]])
    ax.errorbar(tab["Previsto (média)"], tab["Observado (KM)"], yerr=err, fmt="o", ms=3.5, capsize=2.5,
                color=AZUL, ecolor=AZUL, lw=1, zorder=2)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.set_title(titulo, fontsize=8)
    ax.set_xlabel("Risco previsto em 5 anos", fontsize=7.5)
    if mostrar_y:
        ax.set_ylabel("Risco observado (KM)", fontsize=7.5)
    else:
        ax.tick_params(labelleft=False)
    # a razão O/E com IC 95% está na Tabela 2; repeti-la no painel sobrepunha os pontos
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1]); ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.tick_params(labelsize=7)
    ax.xaxis.set_major_formatter(VIRGULA); ax.yaxis.set_major_formatter(VIRGULA)
    ax.grid(alpha=0.25)


def figura_painel(altura=3.1):
    """Uma figura, duas linhas: calibração (3 painéis) em cima; curva de decisão e importância embaixo."""
    cal = pd.read_csv(f"{R}/calibracao_quintis_ic.csv")
    dc = pd.read_csv(f"{R}/curva_decisao.csv")
    imp = pd.read_csv(f"{R}/importancia_permutacao_rsf17.csv").sort_values("Queda média", ascending=False)
    am = melhor_rsf()
    fig = plt.figure(figsize=(LARGURA, altura), layout="constrained")
    fig.get_layout_engine().set(w_pad=0.04, h_pad=0.04, hspace=0.02, wspace=0.03)
    cima, baixo = fig.subfigures(2, 1, height_ratios=[1, 1])
    topo = cima.subplots(1, 3)
    for i, (ax, m, letra) in enumerate(zip(topo, [REF, COXPEN, am], "abc")):
        painel_calibracao(ax, cal[cal.Modelo == m], f"({letra}) {m}", mostrar_y=(i == 0))
    a, b = baixo.subplots(1, 2, gridspec_kw={"width_ratios": [1.25, 1]})
    painel_decisao(a, dc, am, "(d) Curva de decisão")
    painel_importancia(b, imp, "(e) Importância (RSF, 17 var.)")
    fig.savefig(f"{SAIDA}/figura_painel.pdf")
    fig.savefig(f"{SAIDA}/figura_painel.png", dpi=150)
    plt.close(fig)


def painel_decisao(a, dc, am, titulo):
    a.plot(dc["Limiar"], dc["Tratar todos"], color="0.45", lw=1.1, ls=":", label="Tratar todos")
    a.axhline(0, color="0.3", lw=0.9, label="Tratar nenhum")
    a.plot(dc["Limiar"], dc[REF], color=AZUL, lw=1.6, label=REF)
    a.plot(dc["Limiar"], dc[am], color=LARANJA, lw=1.6, ls="--", label=am)
    a.set_ylim(-0.03, max(dc[[REF, am]].max().max(), dc["Tratar todos"].max()) * 1.12)
    a.set_xlim(dc["Limiar"].min(), dc["Limiar"].max())
    a.set_xlabel("Limiar de risco em 5 anos", fontsize=7.5); a.set_ylabel("Benefício líquido", fontsize=7.5)
    a.set_title(titulo, fontsize=8, loc="left")
    a.legend(fontsize=6.8, frameon=True, framealpha=1, edgecolor="white", loc="lower right", ncol=2, columnspacing=0.8, handlelength=1.8, handletextpad=0.5, borderpad=0.2)
    a.tick_params(labelsize=7)
    a.xaxis.set_major_formatter(VIRGULA); a.yaxis.set_major_formatter(VIRGULA)
    a.grid(alpha=0.25)


def painel_importancia(b, imp, titulo):
    top = imp.head(N_MOSTRAR).iloc[::-1]
    cores = [AZUL if v in MAYO else "#9aa5ae" for v in top["Variável"]]
    b.barh([NOMES[v] for v in top["Variável"]], top["Queda média"], xerr=top["Desvio entre partições"],
           color=cores, ecolor="0.35", capsize=1.8, height=0.65)
    b.axvline(0, color="0.3", lw=0.7)
    b.set_xlabel("Queda no C de Uno ao permutar", fontsize=7.5)
    b.set_title(titulo, fontsize=8, loc="left")
    b.text(0.97, 0.05, "azul: variáveis de Mayo", transform=b.transAxes, ha="right", fontsize=6.8, color=AZUL)
    b.tick_params(labelsize=7)
    b.xaxis.set_major_formatter(VIRGULA)
    b.grid(alpha=0.25, axis="x")


if __name__ == "__main__":
    figura_painel()
    print("figura gravada em", SAIDA)

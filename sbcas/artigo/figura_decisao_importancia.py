"""Figura 2 do artigo: (a) curva de decisão em 5 anos e (b) importância por permutação da RSF de 17 variáveis.

Só lê CSVs já salvos (resultados_sbcas/curva_decisao.csv e importancia_permutacao_rsf17.csv); nada é reajustado.
Uso (na raiz do repositório): python sbcas/artigo/figura_decisao_importancia.py
Saída: sbcas/artigo/figuras/figura_decisao_importancia.pdf"""
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42  # fontes TrueType embutidas (sem Type 3)
matplotlib.rcParams["font.family"] = "DejaVu Sans"  # fonte TrueType pura, aceita por verificadores de PDF
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

VIRGULA = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
REF, AM = "Cox, 5 var. (referência)", "RSF, 17 var."
NOMES = {"Bilirubin": "Bilirrubina", "Copper": "Cobre urinário", "Albumin": "Albumina", "Stage": "Estágio histológico",
         "Edema": "Edema", "Ascites": "Ascite", "Prothrombin": "Tempo de protrombina", "Age": "Idade",
         "SGOT": "AST", "Cholesterol": "Colesterol", "Tryglicerides": "Triglicerídeos", "Sex_M": "Sexo",
         "Spiders": "Aranhas vasculares", "Hepatomegaly": "Hepatomegalia", "Drug_Dpen": "Tratamento",
         "Alk_Phos": "Fosfatase alcalina", "Platelets": "Plaquetas"}
MAYO = {"Bilirubin", "Albumin", "Prothrombin", "Edema", "Age"}
N_MOSTRAR = 8


def main():
    dc = pd.read_csv("resultados_sbcas/curva_decisao.csv")
    imp = pd.read_csv("resultados_sbcas/importancia_permutacao_rsf17.csv").sort_values("Queda média", ascending=False)

    fig, (a, b) = plt.subplots(1, 2, figsize=(6.6, 2.9), gridspec_kw={"width_ratios": [1.15, 1]})
    a.plot(dc["Limiar"], dc["Tratar todos"], color="0.6", lw=1, ls=":", label="Tratar todos")
    a.axhline(0, color="0.3", lw=1, label="Tratar nenhum")
    a.plot(dc["Limiar"], dc[REF], color="#1f4e79", lw=1.8, label=REF)
    a.plot(dc["Limiar"], dc[AM], color="#c55a11", lw=1.8, ls="--", label=AM)
    a.set_ylim(-0.05, max(dc[[REF, AM]].max().max(), dc["Tratar todos"].max()) * 1.1)
    a.set_xlim(dc["Limiar"].min(), dc["Limiar"].max())
    a.set_xlabel("Limiar de risco em 5 anos", fontsize=9.5); a.set_ylabel("Benefício líquido", fontsize=9.5)
    a.set_title("(a) Curva de decisão", fontsize=9.5, loc="left")
    a.legend(fontsize=7.5, frameon=False, loc="lower left")

    top = imp.head(N_MOSTRAR).iloc[::-1]
    cores = ["#1f4e79" if v in MAYO else "#9aa5ae" for v in top["Variável"]]
    b.barh([NOMES[v] for v in top["Variável"]], top["Queda média"], xerr=top["Desvio entre partições"],
           color=cores, ecolor="0.35", capsize=2, height=0.65)
    b.axvline(0, color="0.3", lw=0.8)
    b.set_xlabel("Queda no C de Uno ao permutar", fontsize=9.5)
    b.set_title("(b) Importância (RSF, 17 var.)", fontsize=9.5, loc="left")
    b.text(0.97, 0.05, "azul: variáveis de Mayo", transform=b.transAxes, ha="right", fontsize=7.5, color="#1f4e79")

    for ax in (a, b):
        ax.tick_params(labelsize=8)
        ax.xaxis.set_major_formatter(VIRGULA)
        ax.grid(alpha=0.25, axis="x" if ax is b else "both")
    a.yaxis.set_major_formatter(VIRGULA)
    fig.tight_layout()
    fig.savefig("sbcas/artigo/figuras/figura_decisao_importancia.pdf")
    fig.savefig("sbcas/artigo/figuras/figura_decisao_importancia.png", dpi=150)


if __name__ == "__main__":
    main()

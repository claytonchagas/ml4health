"""Material suplementar do artigo SBCAS (achado C3-08): variáveis, codificação, ausências por subgrupo e seguimento.

Uso (na raiz do repositório): python sbcas/artigo/gerar_suplementar.py
Saídas: resultados_sbcas/suplementar_variaveis.csv, resultados_sbcas/suplementar_seguimento.csv e
sbcas/artigo/tabelas/suplementar.tex (macros com os números citados no texto).
Unidades conforme a documentação de survival::pbc (R)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # raiz do repositório

import numpy as np
import pandas as pd
from sksurv.nonparametric import kaplan_meier_estimator

from experimento import MAYO5, TODAS17
from sobrevivencia import preparar

UNIDADE = {
    "Age": "anos", "Sex_M": "0/1 (1 = masculino)", "Drug_Dpen": "0/1 (1 = D-penicilamina, 0 = placebo)",
    "Ascites": "0/1", "Hepatomegaly": "0/1", "Spiders": "0/1 (aranhas vasculares)",
    "Edema": "0 / 0,5 / 1 (codificação de Mayo)", "Bilirubin": "mg/dL", "Cholesterol": "mg/dL", "Albumin": "g/dL",
    "Copper": "µg/dia (cobre urinário)", "Alk_Phos": "U/L (fosfatase alcalina)", "SGOT": "U/mL (AST)",
    "Tryglicerides": "mg/dL", "Platelets": "contagem de plaquetas", "Prothrombin": "segundos (tempo de protrombina)",
    "Stage": "1 a 4 (estágio histológico, exige biópsia)",
}


def seguimento_mediano(y):
    """Mediana do seguimento por Kaplan-Meier reverso (censura como 'evento'), em anos."""
    t, s = kaplan_meier_estimator(~y["event"], y["time"])
    return t[np.searchsorted(-s, -0.5)] / 365.25


def main():
    df, X, y, _ = preparar("transplante_livre")
    rand = df["Drug"].notna().to_numpy()
    linhas = []
    for c in TODAS17:
        linhas.append({"Variável": c, "Unidade ou codificação": UNIDADE[c],
                       "Função": "Mayo (5 e 17 variáveis)" if c in MAYO5 else "Adicional (17 variáveis)",
                       "Ausentes (418)": int(X[c].isna().sum()),
                       "Ausentes nos 312 randomizados": int(X.loc[rand, c].isna().sum()),
                       "Ausentes nos 106 não randomizados": int(X.loc[~rand, c].isna().sum())})
    Path("resultados_sbcas").mkdir(exist_ok=True)
    pd.DataFrame(linhas).to_csv("resultados_sbcas/suplementar_variaveis.csv", index=False)

    seg = []
    for d in ["transplante_livre", "obito"]:
        _, _, yy, _ = preparar(d)
        seg.append({"Desfecho": d, "Pacientes": len(yy), "Eventos": int(yy["event"].sum()),
                    "Eventos até 5 anos": int((yy["event"] & (yy["time"] <= 1826)).sum()),
                    "Seguimento mediano, KM reverso (anos)": round(seguimento_mediano(yy), 2)})
    seg = pd.DataFrame(seg)
    seg.to_csv("resultados_sbcas/suplementar_seguimento.csv", index=False)

    med = seg.loc[seg.Desfecho == "transplante_livre", "Seguimento mediano, KM reverso (anos)"].iloc[0]
    with open("sbcas/artigo/tabelas/suplementar.tex", "w") as fh:
        fh.write("% Gerado por gerar_suplementar.py. Não editar.\n")
        valor = f"{med:.1f}".replace(".", "{,}")
        fh.write(f"\\newcommand{{\\seguimentoMediano}}{{${valor}$}}\n")
    print(pd.DataFrame(linhas).to_string(index=False))
    print(seg.to_string(index=False))


if __name__ == "__main__":
    main()

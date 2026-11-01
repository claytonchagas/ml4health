"""Compara, valor a valor, a cópia local usada no experimento (data/pbc_rdatasets.csv, distribuição
survival::pbc do R via Rdatasets) com o dataset oficial UCI 878, baixado pelo ucimlrepo.

Uso (na raiz do repositório, com o ambiente ativado e acesso à internet):
    python auditoria/comparar_uci_rdatasets.py

Grava a saída em auditoria/comparacao_uci_rdatasets.txt. Não treina nada.
As duas versões são alinhadas pelo identificador do paciente e comparadas depois da mesma
codificação usada no experimento (função codificar), mais Status e N_Days.
A idade é comparada com tolerância de 0,01 ano (cerca de 4 dias), porque a UCI a fornece em dias
e o R em anos com casas decimais; as demais variáveis numéricas, com tolerância de 1e-9."""
import io, os, sys
from contextlib import redirect_stdout

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from experimento import carregar_dados, codificar  # noqa: E402

SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comparacao_uci_rdatasets.txt")
NUMERICAS = ["Bilirubin", "Cholesterol", "Albumin", "Copper", "Alk_Phos", "SGOT",
             "Tryglicerides", "Platelets", "Prothrombin", "Stage", "Age", "N_Days"]


def limpar_uci(df):
    df = df.replace({"NA": np.nan, "": np.nan})
    for c in NUMERICAS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def preparar(df):
    X = codificar(df)
    X["N_Days"] = pd.to_numeric(df["N_Days"], errors="coerce").astype(float)
    X["Status"] = df["Status"].astype(str)
    X.index = pd.to_numeric(df["ID"], errors="coerce").astype(int)
    return X.sort_index()


def main():
    loc, origem_loc = carregar_dados("local")
    uci, origem_uci = carregar_dados("uci")
    uci = limpar_uci(uci)
    a, b = preparar(loc), preparar(uci)

    print("Comparação valor a valor: cópia local (Rdatasets) x UCI 878")
    print(f"Local: {origem_loc}")
    print(f"UCI:   {origem_uci}")
    print(f"Pacientes: local {len(a)}, UCI {len(b)}; identificadores iguais: {a.index.equals(b.index)}")
    if not a.index.equals(b.index):
        print("Identificadores só no local:", sorted(set(a.index) - set(b.index))[:20])
        print("Identificadores só na UCI:  ", sorted(set(b.index) - set(a.index))[:20])
        ids = a.index.intersection(b.index); a, b = a.loc[ids], b.loc[ids]
    print()
    print(f"{'variável':16s} {'iguais':>7s} {'diferentes':>10s} {'ausência diverge':>17s} {'dif. máx.':>10s}")
    total_dif = 0
    for c in a.columns:
        x, z = a[c], b[c]
        if c == "Status":
            dif = int((x != z).sum()); aus = 0; dmax = float("nan")
        else:
            x, z = x.astype(float), z.astype(float)
            aus = int((x.isna() != z.isna()).sum())
            amb = x.notna() & z.notna()
            d = (x[amb] - z[amb]).abs()
            tol = 0.01 if c == "Age" else 1e-9
            dif = int((d > tol).sum()); dmax = float(d.max()) if len(d) else 0.0
        iguais = len(x) - dif - aus
        total_dif += dif + aus
        print(f"{c:16s} {iguais:7d} {dif:10d} {aus:17d} {dmax:10.2e}")
    print()
    if total_dif == 0:
        print("RESULTADO: as duas versões são idênticas em todos os pacientes e variáveis usados no experimento "
              "(idade dentro de 0,01 ano).")
    else:
        print(f"RESULTADO: {total_dif} valores divergem entre as versões (ver tabela acima).")


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    texto = buf.getvalue()
    print(texto)
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"Saída gravada em {SAIDA}")

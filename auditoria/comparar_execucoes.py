"""Compara os resultados de duas execuções completas do notebook, guardadas em commits do git.

Uso: python auditoria/comparar_execucoes.py [commit_a] [commit_b]
Padrão: 00d1773 (execução após a passada A) e 0fb5b54 (execução após a passada A2).
Entre esses commits só mudou o que é registrado (colunas novas), não os cálculos; por isso
apenas as colunas comuns são comparadas. Não treina nada: lê os CSVs do histórico do git."""
import hashlib, io, subprocess, sys
import numpy as np, pandas as pd

A = sys.argv[1] if len(sys.argv) > 1 else "00d1773"
B = sys.argv[2] if len(sys.argv) > 2 else "0fb5b54"
ARQS = ["folds", "oof", "resumo_cv", "quase_externa", "valor_incremental",
        "valor_incremental_vs_mayo_publicado", "sensibilidade_preprocessamento", "vazamento", "hiperparametros"]
RENOMEAR = lambda c: ("ICBonf_inf" if c.startswith("ICBonf") and c.endswith("_inf") else
                      "ICBonf_sup" if c.startswith("ICBonf") and c.endswith("_sup") else c)

def ler(commit, nome):
    txt = subprocess.run(["git", "show", f"{commit}:resultados/{nome}.csv"], capture_output=True, check=True).stdout
    return txt, pd.read_csv(io.BytesIO(txt), header=[0, 1] if nome == "resumo_cv" else 0)

print(f"Execução A: commit {A}\nExecução B: commit {B}\n")
print(f"{'arquivo':40s} {'linhas':>7s} {'dif. máx.':>10s}  texto igual  sha256 A / B")
pior = 0.0
for n in ARQS:
    ta, a = ler(A, n); tb, b = ler(B, n)
    if n != "resumo_cv":
        a = a.rename(columns=RENOMEAR); b = b.rename(columns=RENOMEAR)
    comuns = [c for c in a.columns if c in b.columns]
    num = [c for c in comuns if pd.api.types.is_numeric_dtype(a[c])]
    d = float(np.nanmax(np.abs(a[num].to_numpy(float) - b[num].to_numpy(float)))) if num else 0.0
    txt = all(a[c].fillna("").astype(str).equals(b[c].fillna("").astype(str)) for c in comuns if c not in num)
    pior = max(pior, d)
    print(f"{n:40s} {len(a):7d} {d:10.1e}  {str(txt):11s}  {hashlib.sha256(ta).hexdigest()[:12]} / {hashlib.sha256(tb).hexdigest()[:12]}")
print(f"\nMaior diferença absoluta entre as duas execuções: {pior:.1e}")

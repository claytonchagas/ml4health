"""Sensibilidade do limite superior de Bonferroni à semente do bootstrap pareado (achado da terceira revisão tripla).

Repete o bootstrap do plano (sobrevivencia.valor_incremental: 2.000 reamostragens pareadas de pacientes sobre as
predições fora da partição, nível de Bonferroni para 3 comparações) com 25 sementes alternativas (1 a 25), além da
semente do plano (2026), para a diferença de C de Uno da RSF de 17 variáveis contra a referência. Nada é reajustado.

Uso (na raiz do repositório): python sensibilidade_semente.py
Saída: resultados_sbcas/sensibilidade_semente_bootstrap.csv"""
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

from sobrevivencia import HORIZONTE, MARGEM, N_BOOT, REFERENCIA, SEMENTE, _cuno, preparar

MODELO = "RSF, 17 var."
SEMENTES = [SEMENTE] + list(range(1, 26))
NIVEL = 1 - 0.05 / 3


def limite(semente):
    _, _, y, _ = preparar()
    oof = pd.read_csv("resultados_sbcas/oof_risco5.csv", index_col=0)
    ref, r = oof[REFERENCIA].to_numpy(), oof[MODELO].to_numpy()
    idx = np.random.default_rng(semente).integers(0, len(y), (N_BOOT, len(y)))
    bs = np.array([_cuno(y[i], r[i]) - _cuno(y[i], ref[i]) for i in idx])
    return {"Semente": semente, "Modelo": MODELO, "ICBonf_sup": np.quantile(bs, 1 - (1 - NIVEL) / 2),
            "Réplicas acima da margem (%)": 100 * (bs >= MARGEM).mean(), "Exclui a margem": bool(np.quantile(bs, 1 - (1 - NIVEL) / 2) < MARGEM)}


def main():
    with ProcessPoolExecutor(2) as ex:
        linhas = list(ex.map(limite, SEMENTES))
    t = pd.DataFrame(linhas)
    t.to_csv("resultados_sbcas/sensibilidade_semente_bootstrap.csv", index=False)
    alt = t[t.Semente != SEMENTE]
    print(t.round(4).to_string(index=False))
    print(f"Sementes alternativas: média {alt.ICBonf_sup.mean():.4f}, desvio {alt.ICBonf_sup.std():.4f}, "
          f"excluem a margem em {int(alt['Exclui a margem'].sum())} de {len(alt)}")


if __name__ == "__main__":
    main()

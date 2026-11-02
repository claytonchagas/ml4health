# O aprendizado de máquina acrescenta valor ao modelo de Mayo? (material da submissão ao SBCAS 2027)

Repositório anonimizado para a revisão. Contém código, dados, plano de análise, desvios, resultados e relatórios de auditoria do artigo.

## Onde está cada coisa

| Caminho | Conteúdo |
|---|---|
| `sbcas/PLANO_ANALISE.md` | Plano de análise, registrado antes de qualquer resultado e nunca alterado |
| `sbcas/DESVIOS.md` | Todos os desvios e complementações do plano (D1 a D9), com data, origem e motivo |
| `sobrevivencia.py` | Análise principal: Cox, Cox penalizado e *random survival forests*, validação cruzada aninhada 5×5, valor incremental, subgrupo independente |
| `calibracao_figura.py`, `curva_decisao.py`, `pressupostos_cox.py`, `importancia_permutacao.py`, `tabela_enquadramentos.py` | Análises de apoio (fase 2), sobre as predições salvas, sem retreinar |
| `experimento.py`, `resultados/` | Análise anterior de classificação (linhas (a) e (d) da Tabela 3 do artigo) |
| `resultados_sbcas/` | Resultados, predições fora da partição, partições, hiperparâmetros, logs e manifestos das execuções |
| `auditoria/` | Relatórios das auditorias independentes do código e das conclusões |
| `sbcas/artigo/` | Fonte LaTeX do artigo; `gerar_tabelas.py` gera as tabelas e os números do texto a partir de `resultados_sbcas/` |
| `data/pbc_rdatasets.csv` | Cópia dos 418 pacientes da Mayo Clinic (idêntica ao UCI 878, licença CC BY 4.0), verificada por SHA-256 |

## Como reproduzir

Python 3.13; versões fixadas em `requirements.txt`.

```bash
pip install -r requirements.txt
python sobrevivencia.py                      # desfecho principal (cerca de 75 min)
python sobrevivencia.py --desfecho obito     # sensibilidade
for d in transplante_livre obito; do
  python calibracao_figura.py --desfecho $d
  python curva_decisao.py --desfecho $d
  python pressupostos_cox.py --desfecho $d
done
python importancia_permutacao.py
python tabela_enquadramentos.py
python sbcas/artigo/gerar_tabelas.py
```

Semente 2026 em todos os componentes aleatórios. Cada execução de `sobrevivencia.py` grava um manifesto (`resultados_sbcas/manifesto*.json`) com versões efetivas, commit e comando.

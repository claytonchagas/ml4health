# Material suplementar do artigo

Detalhes técnicos que o artigo resume em linguagem direta. Cada item aponta o script que o implementa e o arquivo de resultados correspondente. O plano de análise está em `sbcas/PLANO_ANALISE.md` e os desvios, em `sbcas/DESVIOS.md`.

## S1. Dados, variáveis e seguimento

- Coorte: 418 pacientes da Mayo Clinic (cópia de `survival::pbc`, idêntica ao UCI 878, verificada por SHA-256 em `experimento.py`).
- Variáveis, unidades, codificação e ausências por subgrupo (312 randomizados e 106 não randomizados): `resultados_sbcas/suplementar_variaveis.csv`.
- Eventos, eventos até 5 anos e seguimento mediano por Kaplan-Meier reverso, por desfecho: `resultados_sbcas/suplementar_seguimento.csv`.
- Gerados por `sbcas/artigo/gerar_suplementar.py`.

## S2. Modelos e pré-processamento (`sobrevivencia.py`)

- Referência: Cox sem penalização, empates pelo método de Breslow; logaritmo natural de bilirrubina, albumina e protrombina; imputação pela mediana do treino (só 2 pacientes com protrombina ausente); padronização.
- Cox penalizado (17 variáveis): `CoxnetSurvivalAnalysis`; proporção L1 em {0,1; 0,5; 0,9; 1} e 10 intensidades log-espaçadas de 10⁻³ a 1 (grade completa de 40 combinações); logaritmo de bilirrubina, colesterol, albumina, cobre, fosfatase alcalina, AST, triglicerídeos e protrombina; imputação iterativa; padronização. Coeficientes não nulos dos modelos escolhidos: `resultados_sbcas/hiperparametros.csv`.
- RSF: 300 árvores; busca aleatória de 50 configurações sobre tamanho mínimo da folha {3, 5, 10, 15, 20, 30}, tamanho mínimo para divisão {6, 10, 20, 40}, variáveis por divisão {raiz de p; 0,33p; 0,5p; p} e profundidade {livre, 3, 4, 6, 8}; imputação na escala original (mediana com 5 variáveis, iterativa com 17), sem padronização.
- Todas as transformações dependentes dos dados são aprendidas só no treino de cada partição, dentro de um `Pipeline`.

## S3. Validação e métricas

- Validação cruzada 5 × 5 estratificada pelo evento (semente 2026), as mesmas partições para os 4 modelos (`resultados_sbcas/particoes.csv`); busca aninhada com 3 partições internas (sementes 2026 + índice da partição externa, de 2026 a 2050).
- Critério da busca e métrica principal: C de Uno truncado em 1.826 dias, calculado sobre o risco em 5 anos, 1 − S(1.826 | x) (desvio D1).
- Distribuição de censura (G): nas métricas por partição, estimada por Kaplan-Meier no treino; no valor incremental, estimada na coorte inteira das predições fora da partição e reestimada em cada reamostragem *bootstrap* (desvio D10). G entra só no cálculo das métricas, não no ajuste dos modelos.
- AUC dependente do tempo (cumulativa/dinâmica) em 5 anos; Brier em 5 anos; Brier integrado numa grade anual de 365 a 1.826 dias. AUC, Brier e Brier integrado só são calculados quando o seguimento do teste cobre de 1 a 5 anos (todas as partições cobrem; desvio D4).
- Resultados por partição: `resultados_sbcas/folds.csv`; resumo: `resultados_sbcas/resumo_cv.csv`.
- O Cox penalizado manteve entre 9 e 16 das 17 variáveis nos 25 modelos escolhidos (`hiperparametros.csv`). O C de Uno médio calculado sobre o escore nativo de cada modelo diferiu do calculado sobre o risco em 5 anos em até 0,0012 (coluna "C de Uno, escore nativo" de `resumo_cv.csv`; desvio D2).

## S4. Valor incremental (`sobrevivencia.py`)

- 2.000 reamostragens *bootstrap* pareadas de pacientes (semente 2026) sobre as predições fora da partição; IC 95% e IC de Bonferroni para 3 comparações (98,33%); reamostragens descartadas e motivos registrados (zero em todas as análises).
- Resultados: `resultados_sbcas/valor_incremental.csv` e `valor_incremental_obito.csv`.

## S5. Calibração (`calibracao_figura.py`)

- Quintis de risco previsto; risco observado por Kaplan-Meier com IC 95% de Greenwood, transformação log-log; num quintil sem eventos até 5 anos, limite superior binomial exato (Clopper-Pearson, 97,5%) com o número em risco aos 5 anos.
- Razão O/E em 5 anos com IC 95% por *bootstrap* de pacientes (2.000, semente 2026).
- Os 4 modelos: `resultados_sbcas/figura_calibracao_suplementar.pdf` e `calibracao_quintis_ic.csv`.

## S6. Curva de decisão (`curva_decisao.py`)

- Benefício líquido em 5 anos com a proporção de eventos acima do limiar estimada por Kaplan-Meier (extensão de Vickers et al., 2008, para sobrevivência), limiares de 5% a 50% de 1 em 1 ponto; "tratar todos" e "tratar nenhum".
- Resultados dos 4 modelos: `resultados_sbcas/curva_decisao.csv`.

## S7. Pressupostos da referência (`pressupostos_cox.py`)

- Cox descritivo nos 418 pacientes, no `lifelines` 0.30.3 (empates pelo método de Efron; imputação dos 2 valores ausentes de protrombina antes do logaritmo, diferente do pipeline preditivo).
- Razões de risco: idade por 10 anos; bilirrubina, albumina e protrombina por duplicação; edema de 0 a 1 (`resultados_sbcas/cox5_razoes_risco.csv`).
- Teste de Grambsch-Therneau por variável, tempo transformado por Kaplan-Meier e por posto, correção de Bonferroni para 5 testes, no seguimento completo e censurado em 5 anos (`resultados_sbcas/cox5_riscos_proporcionais.csv`). A biblioteca não oferece o teste global exato.

## S8. Importância por permutação (`importancia_permutacao.py`)

- RSF de 17 variáveis, reajustada no treino de cada uma das 5 partições da primeira repetição com os hiperparâmetros escolhidos naquela partição; queda média do C de Uno no teste em 30 permutações por variável (semente 2026): `resultados_sbcas/importancia_permutacao_rsf17.csv`.

## S9. Sensibilidade com óbito como evento

- Mesmos procedimentos, transplante tratado como censura (análise de causa específica): arquivos com sufixo `_obito` em `resultados_sbcas/`.

## S10. Reprodutibilidade

- Python 3.13; versões fixadas em `requirements.txt`; manifesto de cada execução em `resultados_sbcas/manifesto*.json`.
- Tabelas e números do artigo gerados de `resultados_sbcas/` por `sbcas/artigo/gerar_tabelas.py` e `gerar_suplementar.py`; compilação verificável por `sbcas/artigo/compilar.sh` (`log_compilacao.txt`).

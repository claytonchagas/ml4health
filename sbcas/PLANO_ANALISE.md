# Plano de análise da versão SBCAS 2027 (registrado antes dos resultados)

Este documento fixa, antes de qualquer resultado da análise de sobrevivência, as escolhas de desfecho, modelos, métricas, orçamento de ajuste, comparações e critérios de interpretação. Ele é registrado no git (ramo `sbcas-2027`) e não será alterado depois que os resultados existirem; qualquer desvio será relatado no artigo como desvio do plano. O trabalho da disciplina (ramo `main`) permanece como foi entregue e passa a ser a análise de classificação citada adiante.

## 1. Pergunta

Modelos de aprendizado de máquina para sobrevivência agregam valor, em discriminação e calibração, ao modelo de Cox com as cinco variáveis do Escore de Mayo, na predição de óbito ou transplante em até cinco anos na cirrose biliar primária? O ganho, se houver, vem do algoritmo ou das variáveis extras?

Achado secundário, pré-especificado: a conclusão sobre o valor incremental muda com o enquadramento da tarefa (classificação em horizonte fixo com exclusão de censurados, sobrevivência com todos os pacientes, e uso do tempo de seguimento como entrada)?

## 2. Dados e desfecho

- Coorte: os 418 pacientes da Mayo Clinic (cópia local verificada por SHA-256; idêntica ao UCI 878).
- **Desfecho principal: sobrevida livre de transplante.** Evento: óbito ou transplante (`Status` D ou CL). Censura: vivo sem transplante no fim do seguimento (`Status` C). Tempo: `N_Days`. É o desfecho usado pelos escores contemporâneos de CBP (GLOBE e UK-PBC). Todos os 418 pacientes entram; ninguém é excluído pelo horizonte.
- **Sensibilidade (material suplementar):** óbito como evento, com transplante tratado como censura (análise de causa específica).
- Horizonte de interesse para as métricas dependentes do tempo: 5 anos (1.826 dias).
- Preditores: as 5 variáveis de Mayo (idade, bilirrubina, albumina, tempo de protrombina, edema) e as 17 variáveis de linha de base, com a mesma codificação do trabalho da disciplina. `N_Days` nunca é preditor.

## 3. Modelos (desenho 2 x 2)

| | 5 variáveis | 17 variáveis |
|---|---|---|
| **Cox** | Cox de riscos proporcionais, sem penalização (**referência**) | Cox com penalização *elastic net* |
| **Aprendizado de máquina** | *Random survival forest* | *Random survival forest* |

- Pré-processamento dentro do *pipeline*, aprendido só no treino de cada partição: nos modelos de Cox, logaritmo natural de bilirrubina, albumina e protrombina (e, nas 17 variáveis, também de colesterol, cobre, fosfatase alcalina, AST e triglicerídeos), imputação (mediana para 5 variáveis; iterativa para 17) e padronização; nas florestas, imputação na escala original, sem padronização.
- Cox penalizado: grade de `l1_ratio` em {0,1; 0,5; 0,9; 1,0} e de intensidade de penalização em 10 valores log-espaçados; seleção na validação interna.
- *Random survival forest*: 300 árvores; busca aleatória de **50 configurações** sobre tamanho mínimo da folha {3, 5, 10, 15, 20, 30}, tamanho mínimo para divisão {6, 10, 20, 40}, variáveis por divisão {raiz de p, 0,33p, 0,5p, p} e profundidade {livre, 3, 4, 6, 8}.
- Mesmo orçamento (50 configurações) para os dois modelos com busca contínua; o Cox penalizado usa a grade completa (40 combinações).

## 4. Validação

- Validação cruzada repetida 5 x 5, estratificada pelo indicador de evento, com as mesmas partições para os 4 modelos.
- Ajuste de hiperparâmetros aninhado (3 partições internas), critério: índice C de Uno truncado em 5 anos.
- Predição fora da partição de cada paciente: média das 5 repetições do risco em 5 anos e do escore de risco.
- **Validação em subgrupo independente do desenvolvimento:** treino nos 312 pacientes dos ensaios randomizados, teste nos 106 não randomizados (todos, com censura), com intervalos de confiança por *bootstrap*.

## 5. Métricas

- **Principal: índice C de Uno truncado em 5 anos.**
- Secundárias: AUC dependente do tempo em 5 anos (cumulativa/dinâmica); escore de Brier em 5 anos e Brier integrado entre 1 e 5 anos, ambos com ponderação pelo inverso da probabilidade de censura; índice C de Harrell (descritivo).
- Calibração em 5 anos: razão observado/esperado (risco observado por Kaplan-Meier dividido pelo risco médio previsto) e gráfico por quintis de risco previsto (Kaplan-Meier observado contra previsto).

## 6. Valor incremental e interpretação

- Para cada um dos 3 modelos contra a referência: diferença no C de Uno (principal) e na AUC em 5 anos, sobre as predições fora da partição, com *bootstrap* pareado de pacientes (2.000 reamostragens, semente 2026), IC 95% e IC de Bonferroni para as 3 comparações (nível 1 menos 0,05/3). Dispersão da diferença entre as 25 partições e fração de partições com ganho.
- Leitura: "maior" ou "menor" só quando o IC de Bonferroni exclui zero.
- **Margem de relevância pré-especificada: ganho de 0,02 no C de Uno.** Se o limite superior do IC de Bonferroni de um modelo ficar abaixo de +0,02, o artigo dirá que ganhos dessa magnitude ou maiores são incompatíveis com os dados para aquele modelo. Se o limite inferior ficar acima de zero, o artigo relatará ganho, qualquer que seja a direção da conclusão anterior do trabalho da disciplina.
- Os intervalos são condicionais às predições obtidas (não refazem o treino), como no trabalho da disciplina, e serão descritos assim.

## 7. Análises de apoio (fase 2, também pré-especificadas)

- Tabela "o enquadramento muda a conclusão": (a) classificação em 5 anos com exclusão de censurados (resultado do trabalho da disciplina); (b) sobrevivência com todos os pacientes (esta análise); (c) uso de `N_Days` como entrada no enquadramento de 3 classes (resultado do trabalho da disciplina, delimitado como configuração inspirada na competição, nos dados originais).
- Curva de decisão (benefício líquido) em 5 anos para a referência e o melhor modelo de aprendizado de máquina.
- Razões de risco do Cox de 5 variáveis e importância por permutação das florestas.

## 8. Reprodutibilidade

Python 3.13, scikit-learn 1.9.1, scikit-survival 0.28.0, semente 2026 em todos os componentes aleatórios, versões fixadas, hiperparâmetros escolhidos salvos, avisos registrados. A execução e o código passam por auditoria independente (passada A3), como no trabalho da disciplina.

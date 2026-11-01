# Auditoria independente: Passada B, afirmações e números

Data: 01/11/2026. Células numeradas a partir de 1, contando Markdown e código; o notebook atual tem 43 células. Evidências de CSV contam o cabeçalho como linha 1. Nenhum treinamento foi reexecutado. Apenas este relatório foi escrito.

## Escopo, procedimento e limites

Foram examinados `AUDITORIA.md`, `auditoria/relatorio_A2.md`, `artigo/main.tex`, todas as seções incluídas, `artigo/referencias.bib`, o texto extraído das 15 páginas de `artigo/main.pdf`, README, os 10 CSVs de resultados, os dados locais, as fontes e saídas textuais do notebook, o código experimental e seu gerador. A figura de discriminação/calibração também foi inspecionada visualmente. Dickson foi conferido no texto privado, confrontado com a extração do PDF disponível; não se reproduzem passagens extensas aqui.

As verificações usaram scripts curtos executados em memória: pandas para contagens, quantis e matrizes de confusão; AUROC por postos médios para conferir independentemente os 2.000 bootstraps pareados, com semente 2026; agregação por modelo das 250 linhas de folds. Não foram executadas funções de treino ou de instalação.

Foi respeitado o escopo exclusivo do repositório: não houve consulta externa nem busca de arquivos fora dele. Consequentemente, os outros 22 trabalhos/fontes bibliográficos **não tiveram seus metadados nem sua sustentação factual verificados em fonte primária**; a matriz abaixo identifica cada caso. A existência de DOI no .bib não prova sua correção. Esta limitação impede afirmar que todas as citações foram validadas.

Não foi executada nova compilação: pdfLaTeX/BibTeX gerariam arquivos auxiliares, contrariando a instrução de escrever somente o relatório. Há executáveis disponíveis, mas sua presença e a existência de um PDF não demonstram compilação limpa do fonte atual. A verificação de forma distingue inspeção estática e PDF entregue de uma compilação efetivamente testada.

## Conferência dos números e das fontes

| Bloco do artigo | Fonte e evidência | Resultado |
|---|---|---|
| Resumo; amostras e fluxo: 418, 312, 115, 197, 106; 374 mulheres e 89,5%; classes 232/161/25 | `data/pbc_rdatasets.csv:1–419`; regra em `experimento.py:93–98`; notebook células 20–21; `metodos.tex:10,44–49,59`; `resultados.tex:5` | Conferem. 115/312 = 36,85897%; 374/418 = 89,47368%. |
| Exclusões 89 censuras e 17 transplantes | Mesmo CSV; filtrar `time <= 1826` e `status != 2`; `metodos.tex:59` | Conferem; não são o grupo de 106 não randomizados. |
| Quase externa: 244/68 pacientes, 85/30 óbitos, 34,8%/44,1% | Mesmo CSV, separar `trt` presente/ausente entre rotulados; notebook célula 38; `metodos.tex:72` | Conferem: 159/85 sobreviventes/óbitos no treino e 38/30 no teste. |
| Completos 310/210, duas ausências Mayo; ausências gerais e cerca de 30 exames faltantes no ensaio | Mesmo CSV, colunas definidas em `experimento.py:101–105`; notebook célula 21; `README.md:42–60`; `metodos.tex:34,59` | Conferem. No ensaio: colesterol 28, triglicerídeos 30, cobre 2. |
| Tabela 3 inteira: caracterização | `resultados.tex:16–30`; quantis dos dados rotulados, sem imputar | Conferida abaixo. Sem divergência material. |
| Tabela 4 inteira: dez modelos, cinco métricas, média e desvio | `resultados.tex:48–57`; `resultados/resumo_cv.csv:4–13`; `resultados/folds.csv:2–251`; notebook célula 30 | Todos os valores conferem nas casas apresentadas. Reagregação versus resumo: diferença máxima 2,22 × 10⁻¹⁶. |
| Tabela 5 inteira e resumo: diferenças e ICs principais, 60/24/40/20/24% dos folds | `resultados.tex:64,78–86`; `resultados/valor_incremental.csv:2–6`; notebook célula 32 | Conferem; cinco ICs Bonferroni incluem zero. Recálculo independente dos ICs: erro máximo 1,88 × 10⁻¹⁶. |
| Sensibilidade: −0,006/−0,013 e IC 97,5%; aumentos nominais | `resultados.tex:89`; `resultados/sensibilidade_preprocessamento.csv:2–3`; `resumo_cv.csv:9,11–13`; notebook célula 34 | Conferem, ressalvada a aproximação horizontal descrita em B-04. Erro máximo nos ICs 1,95 × 10⁻¹⁶. |
| Figura 3: AUROCs OOF e cerca de 31 pessoas/decil | `resultados.tex:91–98`; `resultados/oof.csv:2–313`; notebook célula 36; `artigo/figuras/discriminacao_roc_calibracao.png` | AUROCs OOF: 0,911; 0,908; 0,904; 0,913; 0,891; 0,903; 0,890; 0,898. Conferem na legenda; 312/10 = 31,2. Divergência no README em B-05. |
| Tabela 6 inteira e narrativa de erros: 89 TP, 23 FP, 26 FN da referência; 32–34 FN das árvores principais | `resultados.tex:102,115–126`; `oof.csv:2–313`, alinhado pelo índice ao snapshot | Todas as 40 entradas da tabela conferem; matrizes abaixo. |
| Referência histórica: −0,007, IC [−0,018; 0,003], árvores 5 variáveis −0,021 | `resultados.tex:129`; `resultados/valor_incremental_vs_mayo_publicado.csv:2–7`; notebook célula 32 | Conferem. ICs recalculados: erro máximo 2,16 × 10⁻¹⁶; RF5 e XGB5 têm limite superior Bonferroni negativo. |
| Tabela 7 inteira: nove modelos e cinco métricas | `resultados.tex:144–156`; `resultados/quase_externa.csv:2,5–12`; notebook célula 38 | Conferem, inclusive 0,845/−0,81 e sensibilidade 0,888. Penalização forte sustentada por C=0,01, `hiperparametros_quase_externa.csv:6` e célula 39. |
| Vazamento: 0,753/0,645; 0,788/0,822; 0,721/0,763, respectivos desvios; redução 14% e diferença 0,034 | `resultados.tex:159`; `discussao.tex:10`; `resultados/vazamento.csv:2–51`; notebook célula 41 | Conferem por agregação. Redução relativa exata 14,30813%; diferença AUROC 0,034291. |
| Parâmetros: 1.826 dias; 5 × 5; 3 folds internos; 12 configurações; 300 árvores; grades; 2.000 bootstraps; semente 2026 | `metodos.tex:5,70,89–108`; `experimento.py:33–35,185–233,254–265,298–331`; notebook células 5,12,14,23 | Correspondem ao código e às saídas, sem comprovar cronologia da escolha das grades. As referências sem busca não recebem 12 ajustes. |
| Versões Python 3.13, sklearn 1.9.1, XGBoost 3.4.1 | `metodos.tex:108`; notebook célula 3; `requirements.txt:3–11` | Coerentes com as versões declaradas nas saídas salvas. Não foi reinstalado o ambiente. |
| Escore de Dickson: cinco coeficientes finais, 0,774, 5,07, exemplos 3,12/8,39; n inicial 312 e final 418 | `metodos.tex:77–85`; `privado/Dickson1989.txt:458–504,660–716,756–761`; notebook células 10,22 | Conferem na precisão operacional publicada. O modelo final incorpora os não randomizados. |
| Números de estudos externos | `introducao.tex:5,9`; `relacionados.tex:8–12,24–30,36` | Sem fonte primária local, exceto Dickson. Enumerados na matriz bibliográfica; não verificados. |
| Segunda execução e diferenças abaixo de 10⁻¹² | `metodos.tex:108` | Sem registro comparativo disponível: B-03. |

### Recálculos da caracterização e do limiar

A seleção independente foi `(status == 2 & time <= 1826) | (time > 1826)`, com óbito definido pela primeira condição. As linhas OOF coincidem, em ordem e índice, com as 312 linhas selecionadas. Quantis por interpolação linear, sobre valores observados:

| Variável | Vivos: Q1; mediana; Q3 | Óbitos: Q1; mediana; Q3 | Ausentes |
|---|---|---|---|
| Idade | 42,6393; 49,7632; 56 | 46,7091; 53,9302; 61,7659 | 0 |
| Bilirrubina | 0,60; 0,90; 1,60 | 2,30; 4,40; 10,15 | 0 |
| Albumina | 3,48; 3,67; 3,94 | 3,01; 3,26; 3,525 | 0 |
| Protrombina | 10; 10,45; 11 | 10,525; 11,10; 11,975 | 2 |
| Plaquetas | 202,5; 266,5; 336,25 | 156; 214; 292 | 11 |
| Estágio | 2; 3; 3 | 3; 4; 4 | 6 |

Sexo masculino: 16/197 e 18/115 (8,1%/15,7%). Edema > 0: 15/197 e 40/115 (7,6%/34,8%). Ascite entre observados: 3/159 e 20/85 (1,9%/23,5%); 68 ausências. Pontos exatamente no meio do arredondamento, como 3,525 e 336,25, dependem da convenção e representação numérica; não foram classificados como erro material.

| Modelo, na ordem da Tabela 6 | TP | FP | FN | TN | Precisão; sensibilidade; especificidade; F1 |
|---|---:|---:|---:|---:|---|
| Mayo original | 69 | 10 | 46 | 187 | 0,873; 0,600; 0,949; 0,711 |
| Mayo recalibrado | 87 | 19 | 28 | 178 | 0,821; 0,757; 0,904; 0,787 |
| RL5 | 89 | 23 | 26 | 174 | 0,795; 0,774; 0,883; 0,784 |
| RL17 | 86 | 19 | 29 | 178 | 0,819; 0,748; 0,904; 0,782 |
| RF5 | 81 | 21 | 34 | 176 | 0,794; 0,704; 0,893; 0,747 |
| RF17 | 82 | 23 | 33 | 174 | 0,781; 0,713; 0,883; 0,745 |
| XGB5 | 81 | 22 | 34 | 175 | 0,786; 0,704; 0,888; 0,743 |
| XGB17 | 83 | 22 | 32 | 175 | 0,790; 0,722; 0,888; 0,755 |

Receita dos scripts, suficiente para repetir os cálculos sem treinar: ler o snapshot com `pd.read_csv`, aplicar a seleção acima; usar `groupby(y)[coluna].quantile([.25,.5,.75])` e denominadores não ausentes para a caracterização; ler OOF com `index_col=0`, alinhar o rótulo por índice e classificar com `p >= .5`; contar TP/FP/FN/TN. Para os ICs, gerar matriz de índices de tamanho `(2000,312)` com `np.random.default_rng(2026).integers(0,312,...)`, calcular AUROC por postos médios em cada reamostragem e quantis das diferenças pareadas nos níveis registrados em cada CSV. O checksum do snapshot conferiu com `experimento.py:38`.

## Citações: inventário e sustentação

Todas as **23 chaves** citadas existem. Não há referência do .bib sem citação no texto. Nenhuma referência externa foi considerada correta só por parecer plausível. “Não verificado” abaixo vale tanto para autores/ano/veículo/volume/páginas/DOI (quando aplicáveis) quanto para sustentação da frase.

| Chave e início no .bib | Uso no artigo | Situação nesta auditoria |
|---|---|---|
| dickson1989prognosis, linha 6 | `introducao.tex:7`; `relacionados.tex:8,24`; `metodos.tex:10,77–85` | Texto primário local conferido: autores, título, Hepatology 10(1):1–7, 1989 (`privado/Dickson1989.txt:1–10`); DOI não impresso no texto extraído, não verificado externamente. Derivação, cinco variáveis, validação 106, reestimação 418, fórmula e datas sustentados. Eram dois ensaios combinados (`65–83`), não literalmente um único ensaio; 112 recusaram, 106 foram usados (`257–265`). |
| uci878, linha 18 | `metodos.tex:10,30,66`; `introducao.tex:7` | Não verificado: identificação 878, autores, ano bibliográfico 1989 versus disponibilização 2023, DOI e licença. O snapshot executado é Rdatasets, documentado no README:65; coincidência de contagens não prova identidade de todos os valores UCI. README:259 cita dataset como 2023, enquanto .bib cita 1989; critério de data precisa ser explicitado. |
| fleming1991counting, linha 28 | `introducao.tex:7`; `metodos.tex:10` | Não verificado: livro e sustentação histórica. |
| beuers2015nomenclature, linha 36 | `introducao.tex:5` | Não verificado: mudança de nome em 2015 e descrição clínica. |
| lammers2015globe, linha 48 | `relacionados.tex:8,25` | Não verificado: 4.119, oito países, C=0,82, medidas após um ano e população tratada. |
| carbone2016ukpbc, linha 60 | `relacionados.tex:8,26` | Não verificado: 1.916/1.249, AUC >0,90 em 5/10/15 anos e preditores. |
| gerussi2022ml, linha 72 | `relacionados.tex:10,27` | Não verificado: 11.819/1.069, quatro perfis e ausência de comparação preditiva. |
| ishwaran2008rsf, linha 84 | `relacionados.tex:10,28` | Não verificado: método e uso dos 312 randomizados. |
| reade2023ps3e26, linha 96 | `introducao.tex:7`; `relacionados.tex:12` | Não verificado: autoria, competição, origem sintética e disponibilidade de N_Days. O experimento local testa o controle, não documenta a popularidade desse enquadramento. |
| shakir2025cirrhosis, linha 104 | `relacionados.tex:12,29`; `discussao.tex:6` | Não verificado: cinco classificadores, 89,55%, remoção do tempo, ordem do balanceamento/divisão e ausência de calibração. Não se confirma a crítica metodológica sem abrir o trabalho. |
| tu2025cirrhosis, linha 116 | `relacionados.tex:12,30`; `discussao.tex:6` | Não verificado: cinco modelos, 418 no teste, desfecho, 89%, AUC=0,95, origem do treino e ausência de calibração. |
| christodoulou2019systematic, linha 124 | `introducao.tex:9`; `relacionados.tex:36,39`; `metodos.tex:34`; `discussao.tex:6` | Não verificado: 71 estudos, 282 pares, 79%, diferença 0,00 [−0,18;0,18] e alegação sobre balanceamento. |
| kapoor2023leakage, linha 135 | `introducao.tex:9`; `relacionados.tex:36`; `discussao.tex:10` | Não verificado: sustentação bibliográfica do vazamento e metadados. |
| vancalster2019calibration, linha 147 | `relacionados.tex:36`; `metodos.tex:103`; `discussao.tex:8` | Não verificado na publicação. Definições apresentadas são coerentes com o código local, o que não valida a atribuição. |
| steyerberg2014seven, linha 158 | `relacionados.tex:39` | Não verificado: recomendações e metadados. |
| collins2024tripodai, linha 170 | `introducao.tex:13`; `metodos.tex:5` | Não verificado: metadados e alegação de relato segundo TRIPOD+AI; não há checklist preenchido apresentado como evidência. |
| varma2006bias, linha 181 | `metodos.tex:70` | Não verificado na publicação; aninhamento está implementado no código. |
| zou2005elasticnet, linha 192 | `metodos.tex:89` | Não verificado na publicação; grade e penalização declaradas constam do código. |
| breiman2001random, linha 204 | `metodos.tex:91` | Não verificado na publicação; 300 árvores constam do código. |
| chen2016xgboost, linha 216 | `metodos.tex:93` | Não verificado na publicação; grade consta do código. |
| vanbuuren2011mice, linha 226 | `metodos.tex:34` | Não verificado. O software executado é IterativeImputer do sklearn; a referência descreve mice em R pelo próprio título, sem comprovar identidade de implementação. |
| pedregosa2011scikit, linha 238 | `metodos.tex:34` | Não verificado: metadados e publicação. Uso local de pipelines conferido. |
| fawcett2006roc, linha 248 | `metodos.tex:98` | Não verificado: metadados e atribuição da definição. |

Não foram identificados adjetivos “IA”/“hype” usados para desqualificar modelos ou autores. “Agente de IA” em `metodos.tex:108` é descrição do auditor. A crítica aos estudos relacionados é metodológica, sem ataque pessoal, mas sua exatidão permanece não verificada. `discussao.tex:12` exclui utilidade clínica demonstrada e pacientes atuais; `conclusao.tex:6` propõe estudos futuros em tratados com ácido ursodesoxicólico, não aplicação imediata. Não se encontrou recomendação direta de usar os modelos atuais nesses pacientes.

## Achados

### B-01  Custo de variáveis ainda generalizado na introdução
- Gravidade: importante
- Evidência: `artigo/secoes/introducao.tex:7` e `README.md:17`, “exigem mais variáveis, mais pacientes com dados completos”; `experimento.py:243–246` inclui RF/XGB de cinco variáveis; `README.md:141,215,218` e `artigo/secoes/discussao.tex:4` distinguem corretamente o custo.
- Problema: a abertura ainda atribui à família AM um custo de entradas que os modelos RF5 e XGB5 não têm. Os 312 pacientes foram avaliados em todos os pipelines; 310/210 são elegibilidades hipotéticas sem imputação. A correção A2-02 não chegou a todo o texto.
- Sugestão: restringir custo adicional de coleta à coluna de 17 variáveis, inclusive à regressão; separar esse custo do custo computacional e de interpretabilidade.

### B-02  Linguagem de igualdade e incerteza de calibração excedem as análises
- Gravidade: importante
- Evidência: `artigo/secoes/discussao.tex:4`, “capturada tão bem”; `:8`, “discrimina tão bem quanto qualquer modelo”; `artigo/secoes/conclusao.tex:4`, “discriminação comparável”; `artigo/secoes/resultados.tex:91`, “flutuações compatíveis”; `README.md:216`, “ficou bem calibrada”. Contrastar com `metodos.tex:105` e `resultados/valor_incremental.csv:2–6`.
- Problema: os ICs condicionais incluem ganhos e perdas, e não houve margem/teste de equivalência. “Sugere” atenua a primeira frase, mas não demonstra igualdade. A leitura de calibração é pontual/descritiva: não há IC para CITL/inclinação nem bandas que estabeleçam a compatibilidade estatística das flutuações com o tamanho dos decis. A afirmação “qualquer modelo” tampouco resulta de todos os contrastes pareados. A descrição dos pontos estimados é válida; essas garantias mais amplas não foram testadas.
- Sugestão: usar “não demonstrou ganho nas comparações avaliadas”, “estimativas próximas dos valores ideais” e qualificar o gráfico como descritivo, sem inferir equivalência ou adequação probabilística comprovada. Preservar as hipóteses causais explicitamente não testadas em `discussao.tex:6,8`.

### B-03  Precisão da reprodução não tem evidência arquivada
- Gravidade: importante
- Evidência: `artigo/secoes/metodos.tex:108`, “Uma segunda execução completa reproduziu todos os resultados, com diferenças abaixo de 10⁻¹²”; `introducao.tex:13`, “reprodução verificada”. O notebook salva uma execução; `auditoria/relatorio_A2.md`, seção “Verificações e limites”, explicita que não houve reprodução integral.
- Problema: não foi localizado no material examinado um segundo conjunto de resultados, log de comparação, hashes de duas execuções ou saída com esse limite. Recalcular métricas a partir de predições já salvas verifica consistência, não repetição de treinamento. Não se conclui que a execução não ocorreu: a afirmação e o número não são auditáveis.
- Sugestão: arquivar evidência comparativa com comandos, versões e resultados ou retirar a alegação quantitativa. Não reexecutar o treinamento para corrigir este relatório.

### B-04  Duas aproximações numéricas induzem leitura incorreta
- Gravidade: menor
- Evidência: `artigo/secoes/discussao.tex:4`, diferenças “de no máximo um centésimo”; `resultados.tex:89` e `README.md:215`, extras acrescentam “cerca de 0,01 ... em cada família”; `resultados/resumo_cv.csv:6–11`; `resultados/valor_incremental.csv:3,5`.
- Problema: em relação à referência, os deltas OOF das árvores de cinco entradas são −0,0132 e −0,0134, maiores em módulo que 0,01. Entre quaisquer modelos principais, a distância de AUROC média chega a 0,0244 (RL17 versus XGB5). O ganho horizontal médio do XGB é 0,00475, enquanto RL e RF ganham 0,00886 e 0,01042. Os números explícitos estão corretos, mas os resumos verbais não preservam essas escalas.
- Sugestão: informar o contraste e a faixa exata; descrever ganhos horizontais como aproximadamente 0,009/0,010/0,005, respectivamente.

### B-05  README diverge da AUROC da curva histórica
- Gravidade: menor
- Evidência: `README.md:123`, “0,910 e 0,908 ... Mayo publicado”; figura `artigo/figuras/discriminacao_roc_calibracao.png`, legenda central; `resultados/oof.csv:2–313`; notebook célula 36.
- Problema: a AUROC sobre OOF médias do Mayo original é 0,911 (arredondada), não 0,910. O segundo valor, Mayo recalibrado 0,908, confere. 0,910 é a média por fold e está correto nas tabelas; foi reutilizado incorretamente no exemplo das curvas.
- Sugestão: corrigir apenas o exemplo OOF para 0,911/0,908, mantendo explícita a distinção entre estimadores.

### B-06  Travessão persiste no PDF pela bibliografia
- Gravidade: menor
- Evidência: `artigo/main.pdf`, página 15, entrada Tu: “Dissertação (Mestrado) — University of California”; origem em `artigo/referencias.bib:116–122` e estilo `abntex2cite` em `artigo/main.tex:34`.
- Problema: não há U+2014 nas fontes .tex, mas o PDF final contém esse caractere gerado pelo estilo bibliográfico. Assim, a exigência literal de ausência de travessão no texto final não foi atendida.
- Sugestão: adequar a formatação dessa entrada/estilo e conferir novamente o texto extraído do PDF.

## Reavaliação das correções A2

| Item solicitado | Situação | Evidência no estado atual |
|---|---|---|
| A-02 residual: hiperparâmetros quase externos | **Resolvido** | `experimento.py:387–401,421–422` devolve e salva `hqe`; `construir_notebook.py:235–244`; notebook células 16,38–39, com saída salva; `resultados/hiperparametros_quase_externa.csv:1–12` identifica cenário e escolhas. `README.md:229` registra persistência; `metodos.tex:108` descreve os registros, embora não detalhe o arquivo quase externo. Avisos agora preservam categoria/mensagem em `experimento.py:254–265,398–399`; CSVs e saída reportam zero. |
| A-04 residual: fechamento dizia “isola o algoritmo” | **Resolvido** | `construir_notebook.py:257–264` e notebook célula 43 dizem “compara pipelines”; célula 33 limita a sensibilidade e não atribui efeito causal ao pré-processamento; `README.md:215` e `artigo/secoes/metodos.tex:7` concordam. Nenhuma mudança metodológica adicional é necessária para esse residual específico. |
| A2-01: extrapolações de diferenças e causas | **Parcialmente resolvido** | `README.md:201,215–216` retira segurança excessiva, reconhece contrastes horizontais e de pré-processamento não testados e chama explicação das ausências de hipótese; notebook células 33,43; `resultados.tex:89,131`; `discussao.tex:6,8,12`. Não houve novos testes alegados. Permanecem formulações de igualdade e compatibilidade em B-02. |
| A2-02: custo das 17 entradas atribuído a AM | **Parcialmente resolvido** | `README.md:141,215,218`; notebook célula 43; `discussao.tex:4`; `conclusao.tex:4` limitam corretamente o custo à coluna. A abertura ainda generaliza em `README.md:17` e `introducao.tex:7` (B-01). Código usa cinco entradas para RF5/XGB5 e todas as avaliações mantêm 312 pacientes. |
| A2-03: nível Bonferroni arredondado nos cabeçalhos | **Resolvido** | `experimento.py:342–355`, notebook células 14,32,34 e cabeçalhos dos três CSVs: limites estáveis `ICBonf_inf/sup`, colunas `Comparações (m)` e `Nível Bonferroni`. Valores: 5/0,99; 2/0,975; 6/0,9916666666666667. `README.md:115,178` e `resultados.tex:76,89` usam níveis corretos. |

## Forma e coerência global

As sete tabelas e quatro figuras possuem chamadas no texto; todos os rótulos referenciados existem. As 23 chaves bibliográficas existem e são usadas. O PDF entregue tem 15 páginas e nenhum marcador `??` na extração; citações aparecem resolvidas. Isso **não certifica compilação sem erros**: não foi produzida compilação nova nem fornecido log de compilação para análise. A exigência de ausência de travessão falha somente no ponto identificado em B-06 para o texto extraído examinado.

Resumo, tabelas, resultados, discussão, conclusão e README mantêm os resultados centrais 0,906/1,04, cinco intervalos contendo zero, ausência de ganho demonstrado, amostras 312/115 e controle 0,753/0,645. A diferença histórica no README:183 [−0,016;+0,000] é o **IC95**, enquanto `resultados.tex:129` mostra o **Bonferroni** [−0,018;0,003]; ambos conferem, mas o README deve nomear o nível para facilitar a comparação. Não é divergência de cálculo. As exceções numéricas e verbais encontradas estão em B-03–B-05.

## Tabela-resumo

| Achado | Gravidade | Síntese |
|---|---|---|
| B-01 | importante | Custo adicional de entradas ainda generalizado na abertura |
| B-02 | importante | Linguagem de igualdade/calibração ultrapassa a inferência disponível |
| B-03 | importante | Segunda execução e limite 10⁻¹² sem evidência arquivada |
| B-04 | menor | “No máximo 0,01” e ganho horizontal generalizado são imprecisos |
| B-05 | menor | AUROC OOF do Mayo original no README: 0,910 em vez de 0,911 |
| B-06 | menor | Travessão gerado na referência de Tu no PDF |

## Veredito

**Aprovado com ressalvas.** As tabelas empíricas, contagens, erros no limiar e intervalos são internamente consistentes; não foi encontrado erro numérico que invalide a comparação principal. Dos cinco itens A2 solicitados, três estão resolvidos e dois parcialmente resolvidos. Persistem correções importantes de redação e de rastreabilidade da reprodução. A aprovação cobre a consistência local examinada: a validação externa dos metadados e do conteúdo de 22 referências, do DOI de Dickson e a compilação limpa permanecem **não verificadas**, não aprovadas por presunção. Não há evidência de utilidade clínica para pacientes atuais nem demonstração de equivalência entre modelos.

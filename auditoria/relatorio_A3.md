# Relatório A3 — método e código da análise de sobrevivência

Auditoria independente do ramo `sbcas-2027`, HEAD `859b37d`, em 01/11/2026. Escopo: plano, implementação, funções reutilizadas e todos os CSVs em `resultados_sbcas/`. Sem web, sem análise completa e sem alteração dos insumos. Somente este relatório foi escrito. Testes em memória: conferência de dados, partições, suporte temporal, métricas das predições salvas, calibração, resumos e ensaio reduzido de RSF (20 árvores, 200 pacientes de treino). Os testes reduzidos não estimam novamente o desempenho publicado.

## Registro anterior e aderência

O histórico disponível confirma a sequência: `677a281` (plano, 01/11/2026 18:44:05 −03), `13276aa` (implementação, 18:47:14), `70cc304` (resultados principais, 20:47:41), `859b37d` (sensibilidade, 22:00:13). `git merge-base --is-ancestor 677a281 70cc304` retornou sucesso; `git diff 677a281 HEAD -- sbcas/PLANO_ANALISE.md` foi vazio. Portanto o plano é ancestral dos resultados e não foi alterado no histórico examinado. Isso comprova a ordem dos registros disponíveis, não a inexistência de experimentos privados anteriores.

| Item do plano | Implementação/evidência | Avaliação |
|---|---|---|
| 418 pacientes, sem exclusão pelo horizonte | `sobrevivencia.py:226–231`; `experimento.py:63–79`; `resultados_sbcas/log_transplante_livre.txt:1` | Conforme: SHA-256 integral confere, 418 registros, 186 eventos compostos, 232 censuras. |
| D ou CL como evento; óbito isolado como sensibilidade | `sobrevivencia.py:229–230,236,260`; `resultados_sbcas/log_obito.txt:1` | Conforme: sensibilidade com 161 óbitos e 25 transplantes censurados; não há filtro por 1.826 dias. |
| Desenho 2 × 2 e variáveis basais | `sobrevivencia.py:54–70`; `experimento.py:105–109` | Conforme; Cox de cinco variáveis reestimado, não coeficientes históricos de Mayo. |
| Log, imputação e padronização no Cox; imputação original nas RSF | `sobrevivencia.py:44–51`; `experimento.py:180–197` | Conforme. Mediana em cinco variáveis e imputação iterativa em 17. |
| Grade Cox 4 × 10; RSF 300 árvores e 50 configurações | `sobrevivencia.py:58–69,83–88` | Conforme. RandomizedSearchCV percorre as 40 combinações Cox porque o espaço é finito e `n_iter=40`. Intervalo numérico de alpha especificado somente na implementação: A3-03. |
| CV externa 5 × 5, interna 3, evento estratificado, mesmas partições | `sobrevivencia.py:85–88,133–146`; 100 linhas em cada `folds*.csv` | Conforme: 25 avaliações por modelo e desfecho. Sementes internas derivadas, A3-03. |
| Média das cinco predições fora da partição: risco e escore | `sbcas/PLANO_ANALISE.md:35`; `sobrevivencia.py:139–147` | Apenas risco salvo; escore descartado: A3-01. |
| C de Uno truncado; AUC, Brier, IBS e Harrell | `sobrevivencia.py:105–117` | Fórmulas chamadas adequadamente, mas escore da busca difere da avaliação (A3-01); robustez temporal incompleta (A3-04). |
| Bootstrap pareado 2.000, três comparações, margem 0,02 | `sobrevivencia.py:162–193`; `valor_incremental*.csv:2–7` | Conforme ao plano, condicionado às predições. Limites em A3-02 e A3-05. |
| Calibração KM e O/E, gráfico por quintis | `sobrevivencia.py:120–129,255–259` | Cálculo e tabela presentes; gráfico e incerteza ausentes: A3-06. |
| Treino 312 / teste 106 com IC | `sobrevivencia.py:197–222`; `subgrupo_independente.csv:2–5` | Implementado; escopo dos IC e interpretação em A3-07. |
| Sensibilidade por óbito | Todos os seis CSVs com sufixo `_obito` | Executada: folds, resumo, hiperparâmetros, OOF, incremental e calibração; sem subgrupo por óbito, não exigido explicitamente no plano. |
| Análises de apoio da fase 2 | `sbcas/PLANO_ANALISE.md:51–55`; `sobrevivencia.py:234–267` | Não entregues nesta versão: A3-08. |
| Versões, sementes, avisos e hiperparâmetros | `requirements.txt:1–12`; `sobrevivencia.py:76–93,141,245–247,263` | Versões fixadas, inclusive scikit-survival 0.28.0; limitações em A3-03 e A3-09. |

## Verificações positivas e resultados conferidos

**Independência do ajuste.** A codificação anterior à divisão (`experimento.py:82–94`) é determinística e não estima estatísticas. Imputação, log e escala pertencem ao pipeline clonado e ajustado dentro das divisões internas; o refit recebe somente o treino externo (`sobrevivencia.py:80–89,141`). A lista de divisões externas é criada uma vez, antes do laço dos quatro modelos (`:134–140`). Não encontrei uso do teste no ajuste, nem `N_Days`, `Status` ou ID entre os preditores. `N_Days` aparece corretamente como tempo do alvo (`:230`). Não se empregam os coeficientes históricos ajustados nos 418 pacientes.

**Métricas.** `tau=1826` está presente no Uno da busca e da avaliação (`sobrevivencia.py:83,112`). Na avaliação externa e no subgrupo, a distribuição de censura vem do treino (`:112,114–116,206,212–213`); o scorer envolve o pipeline ajustado somente no treino interno. AUC é cumulativa/dinâmica em 1.826 dias; Brier recebe sobrevivência, não risco; o risco é `1-S(1826)` e maior valor significa maior risco (`:96–101`). Harrell usa o mesmo risco em cinco anos e todo o seguimento, portanto deve ser descrito como concordância desse preditor, não como concordância do escore nativo.

Recriando somente as divisões, o mínimo de seguimento de cada teste externo variou de 41 a 193 dias no principal e de 41 a 140 na sensibilidade; o máximo variou de 4.427 a 4.795 e de 4.184 a 4.795 dias, respectivamente. Assim, os cinco pontos IBS (365, 730, 1.095, 1.461, 1.826) estão dentro do intervalo observado de **todos** os testes atuais. Nas divisões internas, o maior mínimo foi 264 dias no principal e 131 no óbito; o menor máximo foi 4.079 dias em ambos. G do treino em 1.826 dias variou de 0,6843 a 0,7373 no principal e de 0,6366 a 0,6968 na sensibilidade: não houve falta de suporte no horizonte. O teste independente cobre 41 a 4.795 dias. Isso afasta um erro temporal nos resultados atuais, sem tornar a função robusta a outros recortes.

**Resultados salvos.** Os OOF têm 418 linhas em cada desfecho; folds e hiperparâmetros têm 100 linhas por desfecho; calibração tem 20 linhas por desfecho. As médias dos resumos conferem com os folds (erro máximo < 3 × 10⁻¹⁶). Todas as 12 diferenças pontuais incrementais conferem com as métricas recalculadas nos OOF (erro < 10⁻¹⁶). As 40 estimativas KM por quintis e os oito O/E conferem (erro < 10⁻¹⁵). O máximo de seguimento de todos os quintis ultrapassa cinco anos: menor máximo de 3.428 dias no principal e 3.282 no óbito.

**Bootstrap e leitura.** A mesma matriz de índices de pacientes é usada para referência e candidatos, nas duas métricas (`sobrevivencia.py:165–177`). Os CSVs registram 2.000 reamostragens válidas em todas as 12 linhas: **zero descartes no incremental**, portanto não há evidência de viés por descarte nessa execução. Bonferroni é 98,3333%, com quantis 0,0083333 e 0,9916667; protege as três comparações separadamente em cada métrica/desfecho, como registrado. Não protege conjuntamente todas as métricas e sensibilidades.

No principal (`valor_incremental.csv:2–7`), nenhum IC ajustado do C exclui zero. Para RSF de cinco variáveis, limite superior 0,003912 < 0,02; para RSF de 17, **0,020874 > 0,02**; para Cox penalizado, 0,032423 > 0,02. Só a primeira permite a frase de incompatibilidade com ganho ≥ 0,02. AUC da RSF de cinco variáveis é menor (IC ajustado −0,048337 a −0,001192). Na sensibilidade (`valor_incremental_obito.csv:2–7`), nenhum IC ajustado exclui zero; os limites superiores do C das duas RSF são 0,006121 e 0,014714, ambos abaixo da margem. Todas as leituras salvas estão coerentes, inclusive a AUC da RSF de cinco variáveis no óbito, cujo IC95% exclui zero mas o ajustado não. Ausência de evidência de diferença não equivale a equivalência.

## Achados

### A3-01  Busca e avaliação usam ordenações diferentes; escore OOF previsto no plano não foi salvo
- Gravidade: importante
- Evidência: `sbcas/PLANO_ANALISE.md:34–35`, “média ... do risco ... e do escore”; `sobrevivencia.py:83–88` usa o scorer sobre o estimador; `:98–101` retorna escore e risco; `:142–147,154–159` descarta o escore e avalia o risco em cinco anos.
- Problema: a busca usa `predict`, enquanto Uno e Harrell externos e incrementais usam `1-S(1826)`. No Cox, a ordenação tende a coincidir; na RSF, o escore nativo agrega risco ao longo do tempo e não precisa ordenar como o risco no horizonte. Um ensaio reduzido em memória produziu 1.236 pares com ordem invertida entre as duas saídas. Isso demonstra a possibilidade concreta, sem quantificar o impacto nos modelos publicados. O C calculado sobre risco5 é uma concordância válida; o problema é otimizar outra ordenação e omitir a segunda saída prevista no plano.
- Sugestão: definir explicitamente qual preditor constitui o C principal e alinhar o scorer e a avaliação; preservar ambas as saídas OOF previstas. Relatar o desvio e avaliar seu impacto antes de fechar conclusões sobre as RSF.

### A3-02  Censura marginal no OOF e inferência condicionada exigem delimitação
- Gravidade: importante
- Evidência: `sobrevivencia.py:154–159`, `concordance_index_ipcw(y, y, ...)` e `cumulative_dynamic_auc(y, y, ...)`; `:175–181` recalcula essas métricas em cada bootstrap; `sbcas/PLANO_ANALISE.md:49` fixa intervalos condicionais.
- Problema: ao contrário das métricas por fold, a análise incremental estima G na coorte OOF inteira e novamente na reamostra. Isso usa desfechos de avaliação para estimar um componente da **métrica**, não para treinar os modelos; não é vazamento do ajuste. É uma escolha estatística distinta, não explicitada no plano. Os IC incluem a variabilidade do G marginal reestimado, mas não a do treinamento, seleção ou dependência causada pelos treinos sobrepostos. A margem de 0,02 fica excluída apenas nessa inferência condicional, não para qualquer futura amostra ou procedimento de desenvolvimento.
- Sugestão: declarar a origem de G em cada etapa e o caráter condicional dos IC junto das conclusões de margem; não apresentar esses intervalos como incerteza total da generalização. Usar análise adicional previamente delimitada se se desejar inferência sobre todo o treinamento.

### A3-03  Pequenas decisões não registradas e semente literal divergente
- Gravidade: menor
- Evidência: `sbcas/PLANO_ANALISE.md:27,59` fixa dez intensidades log-espaçadas e “semente 2026 em todos”; `sobrevivencia.py:56,59,85–87,141` fixa Breslow, alpha de 10⁻³ a 1 e `SEMENTE + k`.
- Problema: os extremos da grade, o tratamento de empates e a grade anual do IBS não constam do plano; são complementações anteriores aos resultados no commit de implementação, não alterações oportunistas demonstradas. As sementes internas variam de 2026 a 2050, divergindo literalmente do texto do plano, embora sejam determinísticas e comuns aos modelos em cada fold. A semente das florestas e imputadores permanece 2026.
- Sugestão: registrar esses detalhes como complementações e a derivação de sementes como pequeno desvio; preservar o plano original. Não alegar que os extremos da grade foram pré-especificados nele.

### A3-04  Função de métricas não garante o intervalo anunciado em novos recortes
- Gravidade: menor
- Evidência: `sobrevivencia.py:36,107–116`, `tempos = TEMPOS_IBS[TEMPOS_IBS < tmax]`.
- Problema: filtra somente o limite superior, não o mínimo do teste; não garante dois pontos para integrar nem que o último seja cinco anos. Ainda chama AUC/Brier em 1.826 dias incondicionalmente e rotula o IBS como “1 a 5 anos” mesmo se remover o horizonte. Pode falhar ou mudar o estimando silenciosamente em outro recorte. Os testes de suporte acima mostram que esse defeito **não afetou as partições atuais**. Cinco pontos anuais produzem aproximação trapezoidal relativamente grosseira, não uma integração densa de toda a curva.
- Sugestão: exigir suporte completo de 365 a 1.826 dias para essa métrica, validar mínimo/máximo e G positivo, e registrar indisponibilidade quando necessário; documentar os cinco pontos e, como sensibilidade, avaliar a precisão com grade mais densa.

### A3-05  Descartes genéricos e não contabilizados no bootstrap do subgrupo
- Gravidade: menor
- Evidência: `sobrevivencia.py:178–190` guarda válidas no incremental, mas captura todo `ValueError`; `:210–220` faz o mesmo no subgrupo sem salvar quantidade nem motivo; `resultados_sbcas/subgrupo_independente.csv:1` não contém contagem.
- Problema: se ocorrerem, descartes condicionam a distribuição bootstrap à validade, podendo enviesar percentis; não existe reposição nem limiar mínimo. O comentário “sem eventos/censuras suficientes” não identifica todos os possíveis motivos do erro. No incremental atual, zero descartes registrados. Para o subgrupo, reproduzi os mesmos 2.000 índices e as chamadas Uno/AUC com escore finito auxiliar baseado no tempo, sem ajustar modelos: **zero erros por suporte/eventos**. Isso sugere zero descartes desse tipo na execução, mas não substitui o registro das chamadas com as predições originais, que não estão salvas.
- Sugestão: salvar tentativas, válidas, descartes e motivos por cenário/métrica; não silenciar erros inesperados. Caso haja descarte, relatar a proporção e investigar sua associação ao estimando antes de interpretar os IC.

### A3-06  Calibração correta sob suas hipóteses, mas gráfico e incerteza estão ausentes
- Gravidade: importante
- Evidência: `sbcas/PLANO_ANALISE.md:42` exige gráfico; `sobrevivencia.py:120–129,255–259` só produz tabela; `resultados_sbcas/calibracao_5anos.csv:2–11` mostra O/E 0,9915 na referência e 0,9297 no Cox penalizado, mas riscos nos extremos discrepantes.
- Problema: KM por quintis trata corretamente censura à direita se esta for independente dentro dos grupos; O/E global usa KM global, que requer independência marginal adequada. Não é taxa bruta de eventos, e isso está correto. Contudo, não há gráfico, IC de KM/O/E nem números em risco aos cinco anos. O/E próximo de 1 mascara má calibração local: referência no primeiro quintil prevê 0,0799 contra KM 0,0365; Cox penalizado prevê 0,1271 contra KM 0 no primeiro quintil e 0,7378 contra 0,8429 no último. Zero observado não é certeza de risco zero. O código também estende o último KM sem verificar suporte no grupo; nos quintis atuais há seguimento além do horizonte.
- Sugestão: entregar o gráfico pré-especificado, incluir incerteza e números em risco, e descrever a hipótese de censura. Evitar concluir boa calibração apenas pelo O/E; considerar avaliação contínua de calibração e sensibilidade à censura dependente dos preditores.

### A3-07  Teste independente de 17 variáveis é um teste de transporte com ausência estrutural
- Gravidade: importante
- Evidência: `sobrevivencia.py:199–207,217–222`; `experimento.py:71–77,88–93,190–191`; `data/pbc_rdatasets.csv:314–419` contém os 106 não randomizados; `resultados_sbcas/subgrupo_independente.csv:2–5`.
- Problema: treino/teste são de fato disjuntos (312/106; 42 eventos compostos no teste). Porém, Drug, Ascites, Hepatomegaly, Spiders, Cholesterol, Copper, Alk_Phos, SGOT e Tryglicerides faltam em **todos** os 106 pacientes; faltam ainda Platelets em 7, Prothrombin em 2 e Stage em 6. Nove dos 17 preditores são reconstruídos pelo imputador treinado em outro padrão de disponibilidade. Isso não é vazamento, mas mistura transporte populacional, seleção para ensaio e desempenho sob imputação estrutural. Não comprova valor das 17 variáveis efetivamente medidas no teste nem validação externa de outro centro. IC95% só são entregues para C e AUC, condicionais ao treino; Brier, IBS e O/E não têm IC, apesar da formulação ampla do plano “com intervalos de confiança”. Não há IC pareado da diferença no subgrupo.
- Sugestão: explicitar a ausência estrutural, o caráter de validação independente dentro da mesma coorte/centro e o alcance dos IC; justificar a extrapolação do imputador. Complementar intervalos das métricas restantes ou declarar a entrega parcial. Comparações de superioridade no subgrupo exigem diferenças pareadas, não apenas IC individuais sobrepostos.

### A3-08  Análises de apoio pré-especificadas ainda não foram entregues
- Gravidade: importante
- Evidência: `sbcas/PLANO_ANALISE.md:51–55` exige tabela de enquadramentos, curva de decisão, razões de risco e importância por permutação; `sobrevivencia.py:234–267` termina após CSVs de métricas/calibração/subgrupo; não há esses artefatos em `sbcas/` ou `resultados_sbcas/`.
- Problema: a fase 2 está identificada como posterior no plano, portanto sua ausência não invalida automaticamente a fase 1. Entretanto, não se pode chamar o plano inteiro de executado. Também falta o gráfico de calibração (A3-06). Para a tabela de enquadramentos, classificação por óbito e sobrevivência pelo composto diferem tanto na tarefa como no desfecho; a sensibilidade por óbito é necessária para evitar atribuir toda mudança apenas ao enquadramento.
- Sugestão: registrar explicitamente as pendências e concluir a fase 2 antes de afirmar cumprimento integral. Na curva de decisão, tratar a censura e explicitar que escolher o melhor ML nesta coorte introduz seleção na avaliação de utilidade.

### A3-09  Avisos e proveniência da execução são registrados de forma incompleta
- Gravidade: menor
- Evidência: `requirements.txt:1–12`; `sobrevivencia.py:76–92,145–146,237,243–247`; `resultados_sbcas/folds.csv:27–51` e `folds_obito.csv:27–51`; `resultados_sbcas/log_transplante_livre.txt:26` informa 25 avisos.
- Problema: cada contagem representa mensagens **distintas**, deduplicadas e truncadas em 160 caracteres, não o número de ocorrências; não informa candidato/fold interno onde surgiu “all coefficients are zero”. Há essa mensagem nos 25 ajustes Cox penalizados de cada desfecho e no subgrupo, mas isso não prova que o modelo final escolhido teve coeficientes nulos. FutureWarning/DeprecationWarning são suprimidos. As versões requeridas estão fixadas, inclusive scikit-survival 0.28.0; o ambiente disponível confirmou NumPy 2.5.3, pandas 3.0.5, sklearn 1.9.1 e sksurv 0.28.0. Os logs oficiais, porém, não gravam versões efetivas, commit, comando ou n_rep. Não se salvam escores OOF nativos, predições do teste independente nem índices de partição explícitos; hiperparâmetros escolhidos estão salvos para os 100 ajustes de cada desfecho e quatro do subgrupo.
- Sugestão: distinguir mensagens distintas de ocorrências, associar avisos a candidatos e preservar mensagens completas. Gravar manifesto da execução e predições/partições necessárias à auditoria dos IC, sem inferir falha do vencedor a partir de aviso de candidato.

### A3-10  Hipótese de censura e estimando da sensibilidade precisam ser explicitados
- Gravidade: importante
- Evidência: `sobrevivencia.py:112–116,123–129,154–159,229–230`; `sbcas/PLANO_ANALISE.md:15` chama a sensibilidade de causa específica.
- Problema: IPCW usa KM marginal da censura, sem avaliação de dependência de censura em características prognósticas ou no subgrupo. Estratificar as partições pelo evento não garante essa hipótese. Na sensibilidade, tratar transplante como censura permite modelar o hazard de causa específica; porém `1-S(5)` obtido somente do hazard de óbito é risco líquido/hipotético, não incidência cumulativa observável de óbito em presença do transplante como evento competitivo. KM e calibração dessa sensibilidade têm o mesmo limite. Não existe demonstração de viés concreto nos arquivos, mas a interpretação clínica pode ser errada se esses riscos forem apresentados como incidência real.
- Sugestão: enunciar os estimandos e hipóteses; delimitar a análise de causa específica e evitar chamá-la de incidência cumulativa. Se esse risco observado for o objetivo, propor análise de riscos competitivos e calibração correspondente, como adição identificada ao plano.

### A3-11  Pressupostos do Cox e atribuição de ganho ao algoritmo não foram avaliados
- Gravidade: importante
- Evidência: `sbcas/PLANO_ANALISE.md:7,23–26`; `sobrevivencia.py:44–64`; `experimento.py:180–191` usa efeitos lineares após log e imputação distinta entre famílias; não há diagnóstico desses pressupostos no fluxo `sobrevivencia.py:234–267`.
- Problema: não há exame de proporcionalidade dos riscos, formas funcionais, influência ou adequação da referência ao composto óbito/transplante. Isso não é desvio de uma obrigação expressa do plano, mas é objeção bioestatística relevante. O 2 × 2 permite comparações úteis, porém Cox e RSF de 17 variáveis têm imputação em escalas diferentes, e Cox de 5 versus 17 também muda penalização. Portanto não isola estritamente efeito do algoritmo ou das variáveis. Os resumos mostram Cox penalizado com melhor discriminação média e Brier pior que a referência (`resumo_cv.csv:4–5`): melhora em uma métrica não implica valor clínico global.
- Sugestão: acrescentar diagnósticos e discutir sua implicação preditiva; relatar as diferenças de pipeline na atribuição dos ganhos. Considerar sensibilidade com pré-processamento comum e análise de calibração/utilidade, identificadas como adicionais ao plano.

## Tabela-resumo

| Achado | Gravidade | Situação |
|---|---|---|
| A3-01 — Escore da busca versus avaliação e escore OOF omitido | importante | Desvio e impacto nas RSF a avaliar |
| A3-02 — G marginal OOF e alcance da inferência | importante | Explicitação e delimitação necessárias |
| A3-03 — Complementações e sementes derivadas | menor | Pequenos desvios a registrar |
| A3-04 — Proteções temporais incompletas | menor | Sem efeito observado na execução atual |
| A3-05 — Descartes bootstrap | menor | Zero no incremental; registro do subgrupo incompleto |
| A3-06 — Calibração sem gráfico e incerteza | importante | Entrega parcial; não concluir pelo O/E isolado |
| A3-07 — Subgrupo e ausência estrutural | importante | Limite de transporte e IC parciais |
| A3-08 — Fase 2 ausente | importante | Pendência explícita do plano |
| A3-09 — Avisos e proveniência | menor | Hiperparâmetros/versões fixados; registro incompleto |
| A3-10 — Censura e risco competitivo | importante | Hipóteses e estimando a explicitar |
| A3-11 — Pressupostos e atribuição de efeito | importante | Limites metodológicos ainda não tratados |

## Veredito

**Aprovado com ressalvas.** A fase 1 apresenta estrutura de ajuste sem vazamento identificado, métricas válidas nas partições atuais e resultados salvos internamente coerentes. Não há evidência de descarte seletivo no bootstrap incremental nem de erro na regra de Bonferroni/margem. A aprovação não significa execução integral do plano, equivalência dos modelos ou exclusão de ganho clinicamente relevante para todos: no desfecho principal, o limite superior da RSF de 17 variáveis ainda excede 0,02. Antes do fechamento científico, devem ser resolvidos ou explicitamente justificados o desalinhamento entre busca e avaliação, as entregas faltantes, a ausência estrutural do subgrupo e os limites da inferência e dos estimandos. Nenhuma correção foi aplicada nesta auditoria.

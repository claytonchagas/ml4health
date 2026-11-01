# Reauditoria independente — Passada A2: método e código

Data: 01/11/2026. Células numeradas a partir de 1, incluindo Markdown e código.

Foram lidos `AUDITORIA.md`, o relatório A, README, módulo experimental, gerador, requirements, as 42 células do notebook (código, texto e saídas salvas, incluindo as quatro figuras) e os nove CSVs de `resultados/`. Os coeficientes e a probabilidade histórica foram conferidos diretamente em `privado/Dickson1989.txt`. Nenhum arquivo do repositório foi alterado além deste relatório. Não foi reexecutado o treinamento completo.

## Verificações e limites

- O gerador foi executado somente em memória, substituindo sua chamada de escrita por uma função sem efeito. As fontes das **42 células** coincidem integralmente com o notebook entregue. As funções/classes também foram comparadas por árvore sintática com `experimento.py`.
- `resumo_cv.csv` foi recalculado a partir das 250 linhas de `folds.csv`; maior diferença absoluta: 2,22 × 10⁻¹⁶. Há 25 folds por modelo, 312 linhas OOF, 250 registros de hiperparâmetros e 50 avaliações do controle de vazamento.
- As tabelas das células 30, 32, 34, 38 e 40 conferem com os CSVs e com as tabelas do README, nas precisões apresentadas. Contagens e ausências das células 20–21 conferem com o snapshot local: 418 pacientes, 312 rotulados, 115 óbitos, 310 completos com cinco variáveis e 210 com 17.
- Os ICs foram conferidos pelo procedimento de bootstrap sobre as predições salvas, sem refazer ajustes. Isso verifica consistência interna; não demonstra a cobertura frequentista dos intervalos nem a proveniência das saídas de treinamento.
- As versões fixadas em `requirements.txt:3–11` coincidem, para os cinco pacotes exibidos, com a saída da célula 3. Não foi reinstalado esse ambiente nem verificada sua disponibilidade em índices de pacotes. A inspeção e os testes locais não equivalem a reprodução integral da execução oficial.

## Reavaliação individual

### A-01 — Resolvido

A comparação principal usa explicitamente `"RL, 5 var. (Mayo reestimado)"` (`experimento.py:239,412`; notebook, célula 32; README:86,115). Essa regressão tem logaritmos, imputação e padronização no pipeline (`experimento.py:185–193`), e seu ajuste recebe somente o treino externo (`304–307`). `C=1e6` aproxima uma regressão sem penalização; não é literalmente `penalty=None`, mas não identifica aqui o problema histórico do achado A-01.

As duas versões finais de Mayo estão separadas e qualificadas como referências históricas, com aviso de sobreposição da derivação e do teste (`README.md:79–84,147–148,183,201`; notebook, células 23 e 31). A quase externa acrescenta o modelo **inicial**, sem remover as linhas finais históricas (`experimento.py:390–395`; célula 38).

Os coeficientes iniciais em `experimento.py:114–115` conferem com a Tabela 2, página 4, no texto privado: bilirrubina 0,8792 (`Dickson1989.txt:489`), albumina −3,053 (`493`), idade 0,0333 (`497`), protrombina 3,016 (`500`), edema 0,7847 (`504`). A identificação n=312 está em `460–463`. São aplicados em log natural aos três exames e recalibrados somente nos randomizados rotulados. O bloqueio histórico da comparação principal foi removido.

### A-02 — Parcialmente resolvido

`random_state=SEMENTE` está no SAGA (`experimento.py:189–190`). As supressões globais agora atingem somente FutureWarning e DeprecationWarning (`11–14`); `ajustar` captura e conta ConvergenceWarning, incluindo a busca (`254–265`), e a contagem é salva por fold (`309`). A célula 28 reporta zero; `folds.csv` e `quase_externa.csv` também têm contagem zero. Os avisos são capturados e resumidos, portanto deixam de aparecer individualmente no console, mas já não são descartados sem registro de ocorrência.

A fonte é selecionável e tem padrão local (`42–61`; célula 20); o SHA-256 completo está em `38` e é verificado antes da leitura. O snapshot local passou nessa verificação. A opção UCI é explicitamente alternativa e não recebe o checksum do snapshot. Todas as dependências listadas estão fixadas (`requirements.txt:3–11`). Os hiperparâmetros da validação cruzada estão salvos por modelo/fold (`experimento.py:310,409`; notebook, células 28–29).

**Resta:** na quase externa, `hp` é recebido e descartado (`experimento.py:393–396`); não há arquivo com suas escolhas. O CSV de hiperparâmetros tem somente os 25 folds de cada modelo, sem identificação de ajuste quase externo. Isso impede auditar diretamente as escolhas que produziram aquela tabela. Sugestão: persistir também esses hiperparâmetros, com identificação do cenário; preservar categoria/mensagem dos avisos, se ocorrerem. A ausência de convergência problemática nas saídas atuais não é contrariada pelos dados examinados.

### A-03 — Resolvido

O bootstrap está expressamente descrito como condicional e exploratório (`experimento.py:316–319`; `README.md:115,220`; notebook, célula 31). As cinco comparações principais estão enumeradas em `experimento.py:359–360`; `valor_incremental` calcula nível 1 − 0,05/5 = 0,99 e usa os limites simultâneos para a leitura (`340–352`). A célula 32, o CSV principal e `README.md:168–174` concordam: **nenhum dos cinco ICs de Bonferroni exclui zero**.

Não se afirma equivalência ou empate; a ausência de margem é explícita. As únicas linhas classificadas como “menor” na referência histórica são RF5 e XGB5, e seus limites superiores simultâneos são negativos (aproximadamente −0,000216 e −0,004864). O arredondamento do primeiro a −0,000 na célula 32 pode dificultar a leitura, mas a decisão usa a precisão completa. A correção de multiplicidade não resolve as limitações de cobertura do bootstrap condicional, que agora são declaradas. As extrapolações adicionais da conclusão são registradas em A2-01.

### A-04 — Parcialmente resolvido

O orçamento é **12** para todos os modelos com busca (`experimento.py:224,259–261`), inclusive as duas sensibilidades. A regressão de cinco variáveis e Mayo não têm busca. RF usa 300 árvores (`198,215`); a grade XGBoost ajusta 100/200/400 árvores (`229–230`).

Na sensibilidade, `pipe_arvore_preproc_rl` reutiliza literalmente `pipe_regressao(TODAS17, True).steps[:-1]` (`208–219`): logaritmos, imputação iterativa na escala transformada e padronização. Os mesmos mecanismos de busca/folds são aplicados a esses pipelines, e os resultados estão nas células 30 e 34 e no CSV de sensibilidade.

**Resta:** o fechamento do notebook ainda diz “a leitura vertical (mesma coluna) isola o algoritmo” (célula 42; `construir_notebook.py:254`), sem restringir isso à sensibilidade. A descrição inicial foi corrigida, mas essa conclusão antiga contradiz o desenho principal. A afirmação no README:215 de que a sensibilidade identifica a causa da ausência de ganho também excede o teste realizado (A2-01). Sugestão: corrigir o fechamento no gerador e no notebook e restringir a conclusão aos pipelines efetivamente avaliados.

### A-05 — Resolvido

A célula 23 agora descreve 300 árvores e 12 configurações, em acordo com `experimento.py:198,224,259` e `construir_notebook.py:94–100`. A calibração usa `n_bins=10, strategy="quantile"` (`construir_notebook.py:229`; célula 36). A conferência sobre as OOF confirma dez grupos para cada uma das oito linhas principais. A imagem salva identifica corretamente decis de risco.

As curvas da célula 26 são qualificadas como **demonstrativas** na célula 25 (`construir_notebook.py:119–123`), incluindo RF até 500 árvores e a ressalva de imputação antes do bootstrap OOB. Não entram na busca principal. Há divergência menor na estimativa de duração: célula 1 informa 10–20 minutos, enquanto só a célula 28 registra 2.172 segundos e o README informa cerca de 35 minutos; não afeta o achado original sobre parâmetros/grupos.

### A-06 — Resolvido

A métrica é nomeada AP e continua sendo calculada por `average_precision_score` (`experimento.py:288–294`). A convenção de soma ponderada pelos incrementos de revocação, distinta de integração trapezoidal, é explícita em `README.md:116` e na célula 23. Tabelas e CSVs atuais usam AP.

### A-07 — Resolvido

`MayoProbOriginal.predict_proba` implementa **1 − 0,774^exp(R − 5,07)** (`experimento.py:150–169`), com os coeficientes finais operacionais da página 6. A fórmula de sobrevivência e a centralização estão em `privado/Dickson1989.txt:681–686`, e S0(5)=0,774 na Tabela 4 (`756–761`). A função foi testada diretamente contra a expressão numérica em pacientes do snapshot.

A outra classe estima a conversão logística local no treino (`experimento.py:132–144`). Os dois modelos recebem nomes distintos (`237–238`), mantidos nas células 30 e 38, nos CSVs e nas tabelas do README. A probabilidade original tem Brier médio 0,121 e CITL +0,334; a recalibrada, 0,112 e −0,002. A conclusão distingue essas probabilidades (`README.md:216`). A imputação por mediana continua dependente do treino para os poucos ausentes e está declarada na classe; “sem ajuste” se refere à fórmula probabilística.

## Tabela de situação dos achados anteriores

| Achado | Situação | Evidência |
|---|---|---|
| A-01 | resolvido | `experimento.py:114–115,239,304–307,390–395`; `README.md:79–86,115,201`; células 23, 31–32 e 38; Dickson, Tabela 2 |
| A-02 | parcialmente resolvido | `experimento.py:38–61,189–190,254–265,309–310`; `requirements.txt:3–11`; células 3, 28–29; `393–396` descarta os hiperparâmetros quase externos |
| A-03 | resolvido | `experimento.py:316–352,359–360`; `README.md:115,168–174,220`; células 31–32 |
| A-04 | parcialmente resolvido | `experimento.py:208–224,259–261`; células 33–34; contradição na célula 42 e em `construir_notebook.py:254` |
| A-05 | resolvido | `experimento.py:198,224`; `construir_notebook.py:229`; células 23, 25–26 e 36 |
| A-06 | resolvido | `experimento.py:288–294`; `README.md:116`; células 23 e 30 |
| A-07 | resolvido | `experimento.py:132–169,237–238`; células 30 e 38; `README.md:81–82,216`; Dickson, p. 6 e Tabela 4 |

## Novos achados

### A2-01  Conclusão atribui causas e diferenças não testadas
- Gravidade: importante
- Evidência: `README.md:215`, “sem evidência de diferença” na comparação horizontal e “a ausência de ganho não se deve ao tratamento dos dados”; `README.md:201`, “dentro do ruído” e “mostra com segurança”; `README.md:216`, atribuição da queda quase externa do XGBoost às ausências. `experimento.py:359–360` e notebook, células 32 e 34, mostram quais contrastes receberam intervalos.
- Problema: os ICs principais comparam cada modelo com RL5; não comparam RF17 com RF5 nem XGB17 com XGB5. Portanto, não fundamentam a declaração inferencial horizontal. A sensibilidade compara árvores com pré-processamento comum contra RL17; não estima diretamente o efeito de trocar o pré-processamento de cada árvore e não prova sua irrelevância. Os resultados nominais mudam: RF17 sobe de 0,903 para 0,907 e XGB17 de 0,895 para 0,899 na CV; o XGB17 quase externo sobe de 0,845 para 0,888. Finalmente, não há IC quase externo nem análise que separe os efeitos das ausências, da composição da população e da variabilidade amostral. Essas causas são plausíveis, mas não identificadas pelo desenho.
- Sugestão: limitar as afirmações à ausência de ganho demonstrado nos contrastes avaliados; chamar explicações causais de hipóteses e apresentar a variação nominal da sensibilidade. Se houver interesse inferencial horizontal ou no efeito do pré-processamento, definir esses contrastes e sua família de multiplicidade, respeitando o caráter exploratório e as limitações do bootstrap.

### A2-02  Custo de 17 variáveis é atribuído também aos modelos com cinco
- Gravidade: importante
- Evidência: `README.md:218`, “seus custos são certos (mais variáveis, um terço a menos de pacientes com dados completos...)”; `experimento.py:241,243`, modelos RF5 e XGB5 usam `MAYO5`; `README.md:141` e notebook, célula 21, distinguem 310 e 210 pacientes completos.
- Problema: RF5 e XGB5 exigem as mesmas cinco entradas da referência e têm os mesmos 310 pacientes completos. O custo de mais variáveis e redução para 210 pertence aos pipelines com 17 variáveis, inclusive à regressão penalizada, e não ao AM como família. Além disso, todos os pipelines da avaliação principal usam os 312 rotulados por meio de imputação/tratamento nativo de ausentes: não ocorreu perda efetiva de um terço da amostra avaliada. A preferência prática pode considerar interpretabilidade, mas o argumento de custo de dados está generalizado indevidamente.
- Sugestão: separar custo de variáveis do custo do algoritmo e explicitar que 310/210 é elegibilidade hipotética sem imputação. Restringir o custo adicional de coleta aos modelos com 17 entradas.

### A2-03  Cabeçalhos dos CSVs arredondam o nível de confiança
- Gravidade: menor
- Evidência: `experimento.py:341,351`, nível calculado com `1 - 0.05 / m`, mas rotulado com `:.0f`; `resultados/sensibilidade_preprocessamento.csv:1` usa `ICBonf98_inf/sup`, enquanto `README.md:178` informa 97,5%; `resultados/valor_incremental_vs_mayo_publicado.csv:1` usa `ICBonf99_inf/sup` para seis comparações.
- Problema: os cálculos usam os níveis corretos, mas o CSV de sensibilidade anuncia 98% para um intervalo de 97,5%. O histórico anuncia 99% para 99,1666…%. Não muda os limites ou decisões atuais, mas a exportação não descreve exatamente o procedimento que gerou os valores.
- Sugestão: salvar o nível numérico em coluna própria e usar nomes estáveis para os limites; alternativamente, preservar casas decimais suficientes nos cabeçalhos.

## Veredito

**Aprovado com ressalvas.** O bloqueio histórico foi removido, a probabilidade original está correta e as comparações principais agora recebem interpretação exploratória e correção de multiplicidade. Cinco achados anteriores estão resolvidos e dois parcialmente resolvidos. As ressalvas exigem corrigir as extrapolações da conclusão, a contradição remanescente do notebook e o registro incompleto dos ajustes quase externos. Não há evidência nesta reauditoria de erro numérico que invalide as tabelas principais; sua concordância não substitui reprodução integral nem validação externa independente.

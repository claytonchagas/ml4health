# Auditoria independente — Passada A: método e código

Data: 31/10/2026. Escopo: `AUDITORIA.md`, `README.md`, `experimento.py`, `construir_notebook.py` e todas as 38 células de `ml4health_cbp_mayo.ipynb`, incluindo saídas textuais, tabelas e quatro figuras incorporadas. Referência primária de Mayo: `privado/Dickson1989.pdf`, conferida também em `privado/Dickson1989.txt`. Células numeradas a partir de 1, contando Markdown e código. Nenhuma correção foi aplicada ao código ou aos resultados.

**Veredito: reprovado para sustentar a conclusão comparativa principal na forma atual.** O motivo bloqueante é a sobreposição entre os pacientes que originaram os coeficientes publicados de Mayo e os pacientes tratados como teste. O código de validação aninhada dos modelos reestimados está, em geral, corretamente isolado. A fórmula de Mayo está correta e reproduz os dois exemplos publicados.

## Procedimentos e limites da verificação

Foram realizadas leitura integral do código e das saídas, comparação literal dos seis blocos de funções do notebook com o módulo, comparação estrutural das 17 funções/classes e das nove constantes/grades e reconstrução do notebook **somente em memória**, sem executar a escrita do gerador. Todas as fontes das 38 células coincidiram com o gerador atual.

Foram executadas verificações em memória dos exemplos de Mayo, dos limites do rótulo, das contagens da cópia local dos dados, da repetição dos índices dos folds, da equação de CITL e dos seis bootstraps contra Mayo usando `resultados/oof.csv`. Os CSVs auxiliares de resultados foram lidos. Não foi reexecutado o treinamento completo dos 175 ajustes externos nem a busca aninhada; portanto, a concordância das saídas salvas não prova, por si só, que foram produzidas pelo ambiente e código apresentados. Ambiente desta auditoria: NumPy 2.2.6, pandas 2.3.3, scikit-learn 1.7.2 e XGBoost 3.2.0; o notebook registra outras versões na célula 3.

## Verificações sem erro operacional identificado

| Item | Resultado e evidência |
|---|---|
| Rótulo de 5 anos | Correto segundo a regra solicitada: `experimento.py:73–78` inicia com NaN, marca D até 1826 como 1 e qualquer tempo maior como 0. Testes com D em 1825/1826/1827 deram 1/1/0; C e CL em 1826 permaneceram NaN, e em 1827 deram 0. |
| Preditores e vazamento direto | `codificar`, em `experimento.py:58–70`, e as listas em `81–84` não incluem ID, Status ou N_Days. A inclusão de N_Days como preditor ocorre exclusivamente em `243`, no controle de três classes. Seu uso no rótulo e no gráfico da célula 22 é apropriado. |
| Pré-processamento | Logaritmos e codificação são transformações fixas (`58–70`, `121–127`). Imputadores e padronização estão nos pipelines (`130–149`), reajustados nos treinos internos pela busca (`173–179`). Medianas e recalibração de Mayo são aprendidas no `fit` (`102–108`) e reutilizadas no teste (`111–114`). Ressalva histórica: A-01. |
| Folds compartilhados | `RepeatedStratifiedKFold` recebe uma semente inteira (`210`); cada chamada a `cv.split` em `214` reproduz as mesmas 25 divisões. Isso foi verificado diretamente. A busca interna usa os mesmos índices relativos para modelos ajustáveis em cada fold (`177–178`, `216`). O controle com/sem N_Days também compartilha divisões (`244–247`). |
| Busca aninhada | `ajustar` recebe somente `X.iloc[tr]` e `y.iloc[tr]` (`216`), e o teste só entra em `predict_proba` (`217`). O refit da configuração vencedora usa o treino externo. Não há early stopping sobre teste no procedimento principal. |
| Validação quase externa | A separação por Drug presente/ausente precede o ajuste (`260–269`), incluindo a busca interna e a recalibração no treino. São 244/68 pacientes rotulados, com 30 óbitos no teste. A independência histórica de Mayo é inválida, conforme A-01. |
| AUROC e Brier | Chamadas apropriadas a `roc_auc_score` e `brier_score_loss` (`202–205`), com probabilidade da classe 1 (`217`). |
| CITL | Correto: resolve a equação de escore `sum(y − sigmoid(a + logit(p))) = 0`, mantendo a inclinação em 1 (`183–199`). Uma otimização independente da log-verossimilhança com offset reproduziu os interceptos nas sete colunas OOF, com diferença inferior a 10⁻⁶. |
| Inclinação | `LogisticRegression(penalty=None)` em `189` estima intercepto livre e inclinação do logit, como requerido. Não confunde esse intercepto livre com CITL. Clipping em `185` é explícito. |
| Pareamento do bootstrap | Correto: um único vetor de índices de pacientes é aplicado a y, p_mod e p_ref (`230–233`); não reamostra predições dos modelos separadamente nem considera as cinco predições de cada paciente como cinco pacientes. Limite inferencial: A-03. |

As curvas demonstrativas da célula 26 (`construir_notebook.py:116–149`) mostram desempenho de teste ao longo de hiperparâmetros. Os estimadores dessas figuras não alimentam a avaliação principal, e não há seleção automática baseada nessas curvas. Porém, esse corte não deve ser usado para rever grades e depois alegar avaliação intocada na mesma coorte. No RF demonstrativo, a imputação é ajustada antes do bootstrap OOB, de modo que a curva OOB também não é uma validação integral do pipeline; ela não compõe as tabelas principais.

## Conferência do Escore de Mayo com o artigo original

A equação implementada em `experimento.py:89–96` coincide com a equação operacional publicada na **página 6**, seção “Use of the Mayo Model” (`Dickson1989.txt:675–680`): idade em anos, bilirrubina em mg/dL, albumina em g/dL e protrombina em segundos, com **logaritmos naturais** dos três exames. Coeficientes: idade 0,039; ln(bilirrubina) 0,871; ln(albumina) −2,53; ln(protrombina) 2,38; edema 0,859. Não confundir esses arredondamentos da fórmula de uso com os coeficientes mais precisos da Tabela 2, página 4 (0,0394; 0,8707; −2,533; 2,380; 0,8592): a implementação segue legitimamente a fórmula apresentada aos usuários no próprio artigo.

O modelo final tem exatamente essas cinco variáveis. A seleção é descrita na página 3 (`txt:410–423`), e a Tabela 2 distingue modelo inicial com 312 pacientes e final com 418. A codificação na **página 4** (`txt:426–431`, `456–457`) é: 0 para ausência de edema e de tratamento diurético; 0,5 para edema sem diurético ou resolvido com diurético; 1 para edema persistente apesar de diurético. O mapeamento N/S/Y → 0/0,5/1 em `experimento.py:63`, e sua ida e volta pelo espelho em `50`, preservam essa escala.

| Exemplo, página 6 | Entrada (idade; bilirrubina; albumina; protrombina; edema) | `escore_mayo` executada | Artigo |
|---|---|---|---|
| 1 (`txt:688–704`) | 52; 0,5; 4,5; 10,1; 0 | 3,1227873006446827 | 3,12 |
| 2 (`txt:710–716`) | 52; 13,9; 2,8; 13,8; 0,5 | 8,391649303639007 | 8,39 |

Ambos reproduzem o resultado na precisão publicada. No exemplo 2, ausência de edema **com diurético** exige 0,5, e não 0. A mediana e os dois parâmetros de recalibração da implementação atual usam somente o treino recebido por `MayoOriginal.fit`; isso não desfaz a reutilização dos pacientes na estimação histórica dos cinco coeficientes.

## Consistência das saídas salvas

- Células 20–21 versus `README.md:38–63`, `123–130`: 418 pacientes; Status C/D/CL = 232/161/25; 312 rotulados; 115 óbitos; 106 excluídos; 310 completos com cinco variáveis e 210 com 17. Conferem com a cópia local. Os 106 excluídos do horizonte e os 106 não randomizados são conjuntos distintos; a coincidência das contagens não deve sugerir identidade.
- Células 28–31 versus `README.md:132–161`: todas as médias, desvios e diferenças contra Mayo conferem nas precisões exibidas. O bootstrap foi repetido com 2.000 amostras e reproduziu os seis intervalos publicados. Por exemplo, RF5 −0,017524 [−0,033941; −0,001629] e XGB5 −0,017833 [−0,031402; −0,005579].
- Célula 34 versus `README.md:163–173`: os sete modelos, tamanhos de treino/teste e 30 óbitos conferem; AUPRC também está salva no notebook, embora não transcrita nessa tabela do README.
- Célula 36 versus `README.md:177–182`: log loss, AUROC macro e acurácia, incluindo desvios, conferem.
- Figuras das células 22, 26, 32 e 37 foram inspecionadas. As AUROCs na legenda ROC da célula 32 usam predições OOF médias, enquanto a tabela principal usa média de AUROCs por fold. Por exemplo, Mayo aparece como 0,908 no gráfico e 0,910 na tabela: são estimandos diferentes, coerentes com `experimento.py:219–220` e `construir_notebook.py:189–195`, não um erro de transcrição. Há um erro de legenda de agrupamento, descrito em A-05.

## Achados

### A-01  Coeficientes finais de Mayo incorporam os pacientes de teste
- Gravidade: bloqueante
- Evidência: `experimento.py:89–107`, coeficientes publicados mantidos em todos os folds; `163`, inclusão do escore como comparador; `260–267`, uso do mesmo escore no teste não randomizado. Dickson, página 4, Tabela 2: “Final Mayo model (n = 418)” (`privado/Dickson1989.txt:458–525`); página 5, seção “Final Mayo Model” (`660–665`), combinação dos dois conjuntos. `README.md:188–194` reconhece a sobreposição, mas mantém a conclusão de vantagem do escore.
- Problema: o teste externo ao ajuste atual não é externo à estimação histórica do escore. Os 68 não randomizados rotulados também pertencem aos 106 pacientes incorporados no modelo final, portanto a análise quase externa tampouco valida independentemente esse comparador. É reutilização histórica de informação de desfecho, mesmo sem qualquer acesso ao teste no `fit` atual. Favorece Mayo perante modelos treinados apenas nas partições de desenvolvimento. A diferença de −0,005 da RL5 não quantifica nem corrige esse otimismo: além da amostra de ajuste, mudam a função de perda e o enquadramento Cox versus logístico.
- Sugestão: usar como comparação principal justa RL5/RL17 e AM reestimados nos mesmos folds, apresentando Mayo publicado apenas como referência contaminada pela derivação. Para avaliar o escore final de forma independente, usar outra coorte. No teste não randomizado, uma análise histórica adicional poderia usar os coeficientes **iniciais** de n=312, identificados corretamente, sem substituir silenciosamente a fórmula final. Reescrever as conclusões e a qualificação de validação para Mayo.

### A-02  A semente declarada não controla toda a aleatoriedade
- Gravidade: importante
- Evidência: `experimento.py:24`, `SEMENTE = 2026`; `134`, `LogisticRegression(... solver="saga" ...)` sem `random_state`; `8`, supressão global de avisos. `requirements.txt:1–7` contém versões abertas, e a célula 3 instala apenas pacotes ausentes. `experimento.py:34–42` tenta a fonte remota antes da cópia local.
- Problema: SAGA usa aleatoriedade e fica com `random_state=None`, confirmado por inspeção do estimador. Sem semente global NumPy definida, buscas com divisões e candidatos fixos podem produzir coeficientes, escores e escolhas diferentes entre execuções. As versões abertas e a escolha automática de fonte também impedem prometer reprodução numérica exata somente com “semente 2026”. Não foi demonstrado que essa variação altere a conclusão; o ponto é que a garantia não está implementada. A supressão de avisos oculta eventual falta de convergência.
- Sugestão: definir `random_state` também na RL SAGA; registrar configurações vencedoras, convergência e versões exatas; oferecer execução sobre um snapshot local explicitamente selecionável, com checksum. Preservar avisos de convergência e investigar os que ocorrerem. Repetir a execução após esses controles antes de atualizar números.

### A-03  Intervalos condicionais recebem interpretação mais ampla que o procedimento permite
- Gravidade: importante
- Evidência: `experimento.py:220`, média OOF por paciente; `225–235`, reamostragem de pares de predições fixas, sem treinamento; `README.md:106`, IC 95%; `188`, afirmações de inferioridade e de empate. Célula 30 mostra os intervalos condicionais.
- Problema: o pareamento está correto, mas as predições OOF provêm de modelos com treinos sobrepostos. Reamostrar as linhas dessa tabela não incorpora a instabilidade de seleção de hiperparâmetros, dos ajustes e das divisões, nem a dependência induzida pelo treinamento compartilhado. Os intervalos são uma aproximação condicional às predições salvas, não uma quantificação completa da diferença entre procedimentos de aprendizagem. A direção ou magnitude de eventual erro de cobertura não foi estimada nesta auditoria. Além disso, incluir zero não demonstra equivalência: chamar isso de “empate” requer uma margem e análise próprias. Há ainda seis comparações contra a mesma referência, sem tratamento da multiplicidade para as alegações de inferioridade.
- Sugestão: explicitar o caráter condicional/exploratório dos intervalos e a diferença entre AUROC de OOF média e AUROC média por fold. Para inferência confirmatória, priorizar teste independente com bootstrap pareado ou um procedimento de reamostragem que refaça o desenvolvimento completo e respeite a unidade paciente. Predefinir comparações e eventual margem de equivalência; substituir “empataram” por ausência de evidência de diferença quando apropriado.

### A-04  A comparação vertical estima o efeito do pipeline completo
- Gravidade: importante
- Evidência: `experimento.py:130–149`, RL17 recebe logaritmos e imputação iterativa na escala log, RF17 recebe imputação iterativa na escala original e XGB usa ausentes nativamente; `153–156`, grades e espaços de busca distintos; `176`, oito configurações RF versus 12 RL17/XGB. `README.md:25` e `189` afirmam que a leitura vertical “isola” o algoritmo.
- Problema: as mesmas variáveis e pacientes são usados, mas também variam a representação, o modelo de imputação e a estratégia de tratamento dos ausentes. Na validação quase externa, há ausência estrutural de múltiplas variáveis (`README.md:45–52`), aumentando a relevância dessas escolhas. Logo, as diferenças não podem ser atribuídas exclusivamente ao classificador. Logaritmos para RL e ausência nativa para XGB são escolhas defensáveis, não prova automática de favorecimento; o sentido e tamanho do efeito exigem sensibilidade. O orçamento reduzido de busca também não permite concluir ausência de ganho de AM em geral.
- Sugestão: nomear a análise como comparação de pipelines predefinidos; apresentar análise de sensibilidade com pré-processamento compartilhado, especialmente imputação para os modelos de 17 variáveis, além das versões apropriadas a cada método. Justificar espaços e orçamento de busca sem usar resultados externos para escolhê-los. Restringir conclusões às implementações avaliadas.

### A-05  Texto do notebook diverge dos hiperparâmetros e do gráfico
- Gravidade: menor
- Evidência: `construir_notebook.py:95`, “12 configurações”; `99`, “Random forest: 500 árvores”; notebook, célula 23, repete ambas as descrições. O código usa 300 árvores (`experimento.py:142`) e oito configurações para RF (`176`); o README descreve corretamente 300 e oito (`README.md:83`, `97`). `construir_notebook.py:195–196` usa `n_bins=8`, mas intitula “Calibração (decis de risco)”; a imagem salva da célula 32 mantém esse título.
- Problema: as tabelas numéricas conferem, mas o leitor do notebook recebe uma configuração que não é a implementada. O gráfico usa oito grupos quantílicos, não dez.
- Sugestão: corrigir as descrições no gerador e regenerar o notebook em uma etapa posterior, identificando corretamente as curvas demonstrativas, que chegam a 500 árvores, e o RF principal de 300 árvores. Trocar “decis” por oito grupos quantílicos.

### A-06  AUPRC é implementada como average precision sem explicitar a convenção
- Gravidade: menor
- Evidência: `experimento.py:18`, importação de `average_precision_score`; `204`, `"AUPRC": average_precision_score(y, p)`. `README.md:107` define genericamente área sob a curva precisão-revocação; notebook, célula 29, exibe AUPRC.
- Problema: o cálculo é average precision (AP), soma ponderada dos incrementos de recall, e não integração trapezoidal da curva PR. É uma medida válida e comum, mas as duas convenções não são numericamente idênticas; o nome sem esclarecimento dificulta reprodução. Não foi identificado erro de orientação da classe positiva ou de transcrição dos valores.
- Sugestão: chamar de “AP (average precision)” ou declarar expressamente que AUPRC é estimada por AP, mantendo a mesma convenção em código, tabelas e texto.

### A-07  A calibração avaliada não é a probabilidade original de Mayo
- Gravidade: importante
- Evidência: `experimento.py:100–107`, ajuste logístico de intercepto e inclinação sobre R, e `114`, probabilidades dessa regressão. `README.md:136`, linha “Mayo 1989 (coef. publicados)”; `192`, conclusão de que o escore é bem calibrado. Dickson, página 6, equação de sobrevivência e Tabela 4 (`privado/Dickson1989.txt:681–686`, `756–761`), usa `S(t) = S0(t) ** exp(R − 5,07)`, com S0(5)=0,774.
- Problema: R está correto e a recalibração é feita no treino, conforme o desenho solicitado. Entretanto, Brier, CITL e inclinação apresentados avaliam **Mayo com conversão logística local aprendida**, não as probabilidades publicadas de sobrevivência do modelo Cox. A expressão “coeficientes publicados” é verdadeira para R, mas não basta para atribuir ao modelo original a calibração observada. O sentido da ordenação também depende da inclinação logística aprendida; igualdade de AUROC com R pressupõe inclinação positiva, não imposta pelo código.
- Sugestão: identificar a linha como “Mayo 1989, recalibração logística no treino” e restringir a conclusão de calibração a essa versão. Se a probabilidade original for objeto de avaliação, acrescentar separadamente a fórmula publicada, sem confundir seus resultados com os recalibrados. Explicitar as diferenças de atualização de probabilidades entre os pipelines.

## Cinco sinais de viés de Christodoulou et al. (2019)

Enquadramento pelos cinco domínios usados no artigo original, página 17/Figura 2: procedimento de validação, seleção de variáveis, tratamento de preditores contínuos, conjunto de preditores e desequilíbrio do desfecho. Fonte: [Christodoulou et al., 2019, texto do artigo](https://www.rama.mahidol.ac.th/ceb/sites/default/files/public/pdf/Repository/1-s2.0-S0895435618310813-main.pdf). A avaliação abaixo é por comparação, distinguindo o comparador histórico dos modelos reajustados.

| Sinal | Avaliação neste estudo | Evidência e interpretação |
|---|---|---|
| Validação inadequada ou pouco clara | **Sim para Mayo publicado; não identificado no isolamento operacional da CV dos demais** | A-01. A busca aninhada e o teste compartilhado estão corretos (`experimento.py:173–179`, `208–222`), mas não removem a informação incorporada no escore final. A-03 limita a inferência. |
| Seleção de variáveis orientada por dados diferente entre famílias | **Não identificada como etapa pré-CV no código atual** | As listas são fixas (`81–85`) e compartilhadas dentro de cada coluna. Elastic net seleciona/encolhe dentro do pipeline e da busca. A escolha histórica das cinco variáveis veio da própria coorte (Dickson, página 3), mas é compartilhada por RL5, RF5 e XGB5; não constitui uma etapa de seleção exclusiva de um desses braços. O escore histórico tem a vantagem adicional de coeficientes já estimados, A-01. |
| Tratamento diferente dos contínuos | **Sim, diferença presente; favorecimento quantitativo não determinado** | Logaritmos na RL, valores originais nas árvores e imputações em escalas distintas (`121–149`). Não há dicotomização arbitrária que enfraqueça somente RL; há adaptação clínica plausível da especificação. Mesmo assim, a alegação de isolamento do algoritmo exige a ressalva A-04. |
| Preditores diferentes entre LR e AM | **Não dentro de cada coluna; sim se comparar Mayo5 diretamente com AM17** | `modelos`, `160–170`, usa as mesmas cinco ou 17 variáveis por coluna. A comparação de 5 contra 17 avalia informação adicional e método juntos, não apenas algoritmo. Todos os modelos principais usam os mesmos 312 pacientes com imputação; 310/210 são contagens de completude, não tamanhos efetivos dos braços. |
| Correção assimétrica do desequilíbrio | **Não identificada** | Não há SMOTE, reamostragem de classes, `class_weight` ou `scale_pos_weight` assimétricos nas definições (`130–179`). Estratificação é compartilhada. |

Não é apropriado declarar toda a comparação como de baixo risco: o primeiro sinal já é positivo para o comparador principal. Os sinais são alertas metodológicos, não uma demonstração de que cada diferença de implementação favoreça uma família específica.

## Tabela-resumo e veredito

| Achado | Gravidade | Consequência principal |
|---|---|---|
| A-01 | bloqueante | Desempenho de Mayo publicado não é validado independentemente nesta coorte. |
| A-02 | importante | Semente e ambiente não garantem reprodução numérica completa. |
| A-03 | importante | IC condicional e ausência de significância não sustentam todas as conclusões inferenciais. |
| A-04 | importante | Comparação de pipelines não isola exclusivamente o algoritmo. |
| A-05 | menor | Texto do notebook descreve RF e agrupamento de calibração incorretamente. |
| A-06 | menor | Convenção de AP/AUPRC precisa ser explicitada. |
| A-07 | importante | Calibração local não deve ser atribuída às probabilidades originais de Mayo. |

**Veredito: reprovado.** Há um achado bloqueante, quatro importantes e dois menores. A reprovação incide sobre a sustentação da comparação principal e de suas conclusões, não sobre a correção da fórmula de Mayo nem sobre o isolamento operacional dos pipelines reestimados. O resultado pode ser reapresentado como comparação exploratória dos pipelines treinados nos mesmos folds, com Mayo publicado como referência histórica sujeita à sobreposição de derivação; validação independente do escore final requer outra coorte.

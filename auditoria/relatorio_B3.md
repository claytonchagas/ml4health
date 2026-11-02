# Relatório B3 — afirmações e números do artigo SBCAS

Auditoria independente em 02/11/2026, ramo `sbcas-2027`, HEAD `d9894c6`. Veredito: **aprovado com ressalvas**. Os resultados centrais e as tabelas têm fontes rastreáveis e conferem; há exageros de interpretação e duas imprecisões numéricas no texto. A exclusão da margem para a RSF de 17 variáveis é formalmente correta na segunda execução, mas não é um resultado robusto às duas execuções disponíveis.

## Escopo e verificações

Foram lidos `AUDITORIA.md`, o plano, D1–D9, A3, `main.tex`, os cinco arquivos de tabelas, a bibliografia, o gerador, os seis scripts solicitados, as notas de literatura e todos os 40 CSVs em `resultados_sbcas/` e `resultados/`. Também foram consultados os dados locais, funções pertinentes de `experimento.py`, o histórico git, os registros locais de referências e o artigo de Dickson em `privado/`. O PDF do artigo foi lido por extração integral; as páginas 7 e 8, com as figuras, também foram inspecionadas visualmente. As linhas abaixo são as do estado auditado; intervalos indicam blocos de evidência.

Não houve web, consulta a fontes documentais fora do repositório, retreino ou execução completa. Scripts curtos em memória recalcularam contagens, métricas incrementais pontuais, quintis/IC observados, curvas de decisão e resumos dos folds. Os intervalos bootstrap salvos foram conferidos como fontes, mas os 2.000 retreinos não existem nesse procedimento e os 2.000 bootstraps não foram reproduzidos nesta passada. O gerador foi avaliado sem executar suas rotinas de gravação: as quatro tabelas regeneradas em memória coincidem literalmente com os arquivos `.tex`.

Registro de execução: importar as funções de calibração/decisão carregou Matplotlib, que informou a criação automática de cache temporário em `/tmp/matplotlib-g_eiksbu`. Esse efeito incidental contrariou a restrição literal de não gravar outros arquivos; não foi usado como fonte nem houve modificação intencional dos insumos. A única alteração feita no repositório por esta auditoria é este relatório.

## Conferência dos números

### Dados, desenho e números digitados no texto

| Local no artigo | Número/afirmação numérica | Fonte e resultado da conferência |
|---|---|---|
| `main.tex:31,35,65,67,100` | 418; 312/106; 186 = 161 + 25; 232 | `data/pbc_rdatasets.csv:2–419`, colunas `status`, `trt`; mapeamento em `experimento.py:68–77`. Recontagem: 418; status 0/1/2 = 232/25/161; tratamento observado/ausente = 312/106. Conferem. A descrição dos censurados exige B3-06. |
| `main.tex:65,181` | 1974–1984; dois ensaios; 1989 e cinco variáveis em `:31,35,41` | `privado/Dickson1989.txt:5,21–28,67–77`; PDF privado pp.1–3. Conferem. A história inclui 106 de 112 recusantes, não todos os recusantes (`:257–265`). |
| `main.tex:67` | cinco anos = 1.826 dias; 132 eventos até o horizonte | `sobrevivencia.py:40,269–270`; dados `:2–419`. Recontagem: 115 óbitos + 17 transplantes = 132; 89 censuras até o horizonte. Conferem. |
| `main.tex:85` | 42 eventos nos 106 | Dados `:314–419`: 36 óbitos + 6 transplantes, 64 censurados. Conferem. |
| `main.tex:85` | nove de 17 variáveis inteiramente ausentes no teste | Dados `:314–419`; `experimento.py:105–108`. Tratamento, ascite, hepatomegalia, aranhas vasculares, colesterol, cobre, fosfatase alcalina, AST e triglicerídeos: 106 ausências cada. Plaquetas têm mais 7, protrombina 2 e estágio 6 ausências parciais. Confere a contagem de nove. |
| `main.tex:71,75,77,81,85` | 2×2; 5/17 variáveis; 300 árvores; 50 buscas; L1 0,1/0,5/0,9/1; dez intensidades 10⁻³–1; CV 5×5; três internas; cinco predições; 2.000 bootstraps; três comparações; 98,3%; 30 permutações; cinco testes | `sobrevivencia.py:40–44,67–82,98–100,158–179,198–214`; `importancia_permutacao.py:19,28,41–44`; `pressupostos_cox.py:60–68`. Conferem, com a ressalva sobre orçamento em B3-07. Bonferroni é exatamente 98,333…%, adequadamente arredondado. |
| `main.tex:77,117` | limiares de 5% a 50% | `curva_decisao.py:24`: 46 pontos, passo de um ponto percentual. Confere para a grade calculada, não para todos os reais do intervalo. |
| `main.tex:89` | nove desvios; Python 3.13, sklearn 1.9.1, sksurv 0.28.0, semente 2026 | `DESVIOS.md:7–15`; `resultados_sbcas/manifesto.json:9–18` e manifesto de óbito. Conferem; sementes internas são derivadas, como registra D3. |
| `main.tex:31,35,96` | referência 0,833; diferenças +0,015, −0,014, −0,001; IC; ganho em 68% de 25 folds | `resumo_cv.csv:4`; `valor_incremental.csv:2,4,6`. Todos os arredondamentos desses números conferem. Ganho em 68% = 17/25. |
| `main.tex:96` | desvios de 0,017 a 0,019; diferença nativa de no máximo 0,001 | **Divergem** da execução atual: B3-01. |
| `main.tex:96` | limite 0,0197; primeira execução 0,0209 | `valor_incremental.csv:6`: 0,0196996472; `git show 859b37d:resultados_sbcas/valor_incremental.csv`, linha 6: 0,0208741633. Conferem. |
| `main.tex:96` | AUC da RSF5: −0,024 [−0,047; −0,001]; 9–16 coeficientes não nulos | `valor_incremental.csv:5`; `hiperparametros.csv:27–51`; `numeros.tex:23–24`. Conferem. O IC de AUC ajustado exclui zero. |
| `main.tex:113` | óbito: referência 0,854; +0,010 [−0,006; 0,026], −0,013 [−0,031; 0,003], −0,007 [−0,029; 0,014] | `resumo_cv_obito.csv:4`; `valor_incremental_obito.csv:2,4,6`. Conferem, inclusive −0,0065327 → −0,007. |
| `main.tex:117` | O/E 0,93–0,99; referência 0,080/0,036; RSF17 0,712/0,808; Cox17 0,127/zero, limite 0,054 | `calibracao_quintis_ic.csv:2,7,12,17,21`. Conferem numericamente; limitações de interpretação e do IC em B3-03. |
| `main.tex:117,135,137` | macros de decisão, subgrupo e importância | `numeros.tex:2–22`; `subgrupo_independente.csv:2–5`; `importancia_permutacao_rsf17.csv:2–4`; `curva_decisao.csv:2–47`. Conferem; detalhes abaixo. |
| `main.tex:155` | +0,034 e 96% | `vazamento.csv:2–51`, pareamento por Fold; `tabela_enquadramentos.csv:5`: média 0,0342913682; 24/25 folds positivos; desvio 0,019. Conferem. |
| `main.tex:177` | Harrell 0,814 e 0,815 | `resumo_cv.csv:4,7`: 0,81444976 e 0,81462962. Conferem como médias das partições, sobre risco em cinco anos. |
| `main.tex:43,45,54,56,177` | 71 estudos, C de 0,855/0,776, sete variáveis, .632+, acurácia próxima de 90% | São números de literatura, não resultados próprios. 71 e aproximadamente 90% têm registro secundário local; 0,855/0,776 conferem com as notas. Sete e .632+ não têm suporte nas notas fornecidas: B3-09 e seção de citações. |
| `main.tex:65` | identificador 878, CC BY 4.0; identidade com UCI | `auditoria/verificacao_referencias.md:10`, `auditoria/comparacao_uci_rdatasets.txt` e checksum da carga local. Registro local favorável; não se refez download nem verificação online. |

### Tabelas, macros e figuras

**Tabela 1**, `main.tex:100–108`, `tabelas/desempenho.tex:1–8`: todos os valores de Uno, AUC, Brier pontual/integrado e desvios coincidem com `resumo_cv.csv:4–7`; O/E e IC com `calibracao_quintis_ic.csv:2,7,12,17`; diferenças e IC com `valor_incremental.csv:2,4,6`. O gerador usa essas fontes em `gerar_tabelas.py:31–50`. A tabela de óbito, `tabelas/desempenho_obito.tex:1–8`, também confere com os arquivos de mesmo sufixo; ela não é inserida no PDF principal.

**Tabela 2**, `tabelas/cox.tex:1–5`: HR/IC 1,27 [1,10; 1,46], 1,79 [1,62; 1,99], 0,16 [0,07; 0,37], 3,02 [1,11; 8,23], 2,32 [1,39; 3,86] conferem com `cox5_razoes_risco.csv:2–6`. Todos os valores p, inclusive 0,007/0,024 da protrombina e 0,689/0,202 da bilirrubina, conferem com `cox5_riscos_proporcionais.csv:2–6,12–16`. Os valores ajustados iguais a 1 aparecem corretamente como >0,99. O problema é de interpretação e identificação do ajuste descritivo, não de transcrição: B3-05.

**Tabela 3**, `tabelas/enquadramentos.tex:1–4`: (a) 312/115, Δ 0,009 [−0,017; 0,035]; (b) 418/186, 0,015 [−0,004; 0,032]; (c) 418/161, 0,010 [−0,006; 0,026]; (d) 418/161, 0,034, sem IC e 96%. Conferem com `tabela_enquadramentos.csv:2–5` e as fontes originais. A recontagem da regra em `experimento.py:97–102` reproduz os 312 elegíveis e 115 óbitos em (a). Bonferroni é de **99% em (a), cinco comparações**, e **98,333…% em (b)/(c), três comparações**; a legenda não informa essa diferença. A escolha do maior Δ é reproduzível e não foi tratada como pré-especificada. Limites da comparação: B3-08.

**Todas as 23 macros**, `numeros.tex:2–24`, têm correspondência nas fontes indicadas pelo gerador (`:87–105`). No subgrupo: Uno/IC95% de referência 0,790 [0,718; 0,857], Cox17 0,806 [0,736; 0,869], RSF5 0,797 [0,726; 0,861], RSF17 0,807 [0,738; 0,871]; O/E 1,05/1,06/1,12/1,16. Importâncias: 0,128/0,019/0,007. Diferenças máximas absolutas de benefício líquido: 0,0154521 e 0,0183868 no composto/óbito, arredondadas para 0,015/0,018. Extremos de coeficientes: 9/16. Algumas macros não são usadas no corpo, o que não constitui divergência.

**Figuras 1 e 2**, `main.tex:119–130`: os PDFs inseridos são byte a byte iguais aos respectivos PDFs de `resultados_sbcas/`. Na Figura 1, os dois O/E/IC impressos (0,99 [0,87; 1,10] e 0,99 [0,88; 1,11]), pontos e barras correspondem aos quintis da referência e RSF17. Os eixos 0–1 e a diagonal são escalas, não estimativas adicionais. A Figura 2 usa as 46 linhas da curva, com estratégias extremas corretas. As curvas dos dois modelos ficam acima de tratar todos e tratar nenhum nos 46 pontos: a menor vantagem sobre tratar todos é 0,0010584 na referência e 0,0017254 na RSF17; o benefício mínimo é 0,1440237 e 0,1428535. Isso sustenta uma descrição **pontual**, não equivalência clínica ou uma garantia fora da grade.

As diferenças incrementais pontuais recalculadas nos OOF concordaram com os CSVs a menos de 10⁻¹⁶. As médias/desvios recompostos a partir dos folds concordaram a menos de 3×10⁻¹⁶. Para ambos os desfechos, todos os 40 quintis e as curvas dos quatro modelos foram reproduzidos em memória, com diferenças inferiores a 2×10⁻¹⁶. Isso confere a implementação das quantidades salvas, não valida por si só as hipóteses estatísticas dos estimadores.

### Leitura da margem por modelo

| Desfecho/modelo | Δ Uno OOF | IC Bonferroni | Leitura permitida |
|---|---:|---|---|
| Composto, Cox17 | +0,014831 | [−0,004187; 0,032423] | Sem superioridade demonstrada; ganho ≥0,02 não excluído. |
| Composto, RSF5 | −0,013639 | [−0,032313; 0,004175] | Sem diferença demonstrada em Uno; exclui ganho ≥0,02 na inferência condicional. |
| Composto, RSF17 | −0,000997 | [−0,021980; 0,019700] | Exclui formalmente ganho ≥0,02, por somente 0,00030035 abaixo da margem; primeira execução não exclui. |
| Óbito, Cox17 | +0,010458 | [−0,006395; 0,026111] | Sem superioridade demonstrada; ganho ≥0,02 não excluído. |
| Óbito, RSF5 | −0,013194 | [−0,031255; 0,003004] | Exclui ganho ≥0,02 condicionalmente. |
| Óbito, RSF17 | −0,006533 | [−0,029243; 0,014433] | Exclui ganho ≥0,02 condicionalmente. |

Fontes: `valor_incremental.csv:2,4,6` e `valor_incremental_obito.csv:2,4,6`. Nenhum desses IC exclui zero. AUC da RSF5 é inferior nos dois desfechos (`:5` em ambos); no óbito, o limite ajustado superior é −0,00008107, próximo de zero. Ausência de superioridade, exclusão de ganho de determinada magnitude e equivalência são afirmações diferentes. A margem de Uno não pode ser aplicada à AUROC da classificação.

## Achados

### B3-01  Duas imprecisões numéricas no texto da discriminação
- Gravidade: menor
- Evidência: `sbcas/artigo/main.tex:96`, “desvios de 0,017 a 0,019” e “em no máximo 0,001”; `resultados_sbcas/valor_incremental.csv:2,4,6`; `resultados_sbcas/resumo_cv.csv:6–7`.
- Problema: os desvios atuais são 0,01796037, 0,01694601 e 0,01846584: o intervalo arredondado a três casas é **0,017 a 0,018**. O limite 0,019 é compatível com a execução anterior, mas não com o arredondamento da atual. A diferença absoluta entre as médias de Uno nativo e Uno por risco5 chega a **0,00117703** na RSF5 (0,81940381 contra 0,82058084), maior que o teto literal de 0,001. Na RSF17 é 0,00073972. Dizer “no máximo” transforma um arredondamento em limite falso.
- Sugestão: gerar também esses números das fontes atuais; usar 0,017–0,018 e “aproximadamente 0,0012 nas médias”, deixando explícito que se comparam médias, não todas as partições.

### B3-02  Resumos e conclusão perdem as ressalvas que tornam válida a leitura da margem
- Gravidade: importante
- Evidência: `sbcas/artigo/main.tex:31,35,175,186`, “incompatíveis com os dados” e resultado “negativo e estável”; `:81,96,181` fazem as ressalvas; `resultados_sbcas/valor_incremental.csv:6`; primeira execução em `859b37d`, mesmo CSV, linha 6.
- Problema: a regra foi aplicada corretamente à segunda execução, inclusive à RSF17. Porém os resumos e a conclusão apresentam o resultado sem sua condição inferencial e sem a fragilidade: 0,01969965 está só 0,00030035 abaixo de 0,02; a primeira execução deu 0,02087416. A ausência de superioridade é estável, mas a exclusão da margem na RSF17 não é. O IC não contempla refazer o treino/seleção. O subgrupo não tem IC pareado da diferença, e a classificação não foi submetida à mesma margem de Uno. “A conclusão se manteve” não pode abranger indistintamente todas essas proposições.
- Sugestão: incluir “nos intervalos condicionais às predições” nos resumos/conclusão; registrar que a exclusão para RSF17 é limítrofe e sensível ao protocolo da busca. Reservar a estabilidade entre análises à ausência de ganho demonstrado, sem afirmar equivalência ou exclusão universal de ganho relevante.

### B3-03  Calibração semelhante e desvios por quintil são descritos com certeza excessiva
- Gravidade: importante
- Evidência: `sbcas/artigo/main.tex:31,35,117,186`; `resultados_sbcas/calibracao_quintis_ic.csv:2,7–8,11,21`; `calibracao_figura.py:55–61`; `main.tex:77` descreve os IC como Greenwood/log-log.
- Problema: O/E próximo de um não demonstra calibração semelhante. No Cox17, os dois primeiros quintis preveem 0,1271 e 0,2020 contra KM 0 e 0,0798; ambos os valores previstos ultrapassam os limites observados superiores (0,0544 e 0,1705). No quintil alto, 0,7378 fica abaixo do limite inferior 0,7479. Já 0,07986 da referência está dentro do IC observado [0,01191; 0,10894] do primeiro quintil, e 0,71249 da RSF17 está dentro de [0,71168; 0,88781] do último. São direções das estimativas, não comprovação de erro sistemático nesses dois quintis. As barras condicionais não são testes completos de calibração. O limite de 0,054 é numericamente correto, mas é uma aproximação binomial baseada em 66 pacientes em risco, e não um IC Greenwood de KM como a descrição geral faz supor.
- Sugestão: distinguir O/E global, padrões pontuais locais e sua incerteza; evitar “calibração semelhante” sem delimitação. Informar a exceção do limite binomial no quintil sem eventos, e apontar explicitamente para o arquivo/figura suplementar dos quatro modelos, que não é citado no artigo.

### B3-04  A curva não demonstra equivalência de utilidade nem o sentido do viés de seleção
- Gravidade: importante
- Evidência: `sbcas/artigo/main.tex:117,129,175,186`; `curva_decisao.py:24,55–56,60–64`; `resultados_sbcas/curva_decisao.csv:2–47`; `gerar_tabelas.py:99–102`.
- Problema: as curvas são próximas visualmente e a diferença máxima 0,015 está corretamente arredondada. Não há IC da diferença, margem de equivalência, ação clínica definida ou justificativa dos limiares. Um benefício líquido de 0,015 corresponde a 1,5 verdadeiros positivos líquidos por 100 pacientes, cuja importância depende da decisão. Além disso, a seleção é pelo C de Uno médio, não pelo benefício líquido; portanto a legenda pode alertar para seleção, mas não afirmar como fato que ela “favorece a RSF” nessa métrica. A figura compara uma RSF à referência, não demonstra semelhança de utilidade de todos os modelos.
- Sugestão: descrever proximidade das estimativas nos 46 limiares, sem equivalência demonstrada; definir um uso clínico hipotético e explicar a escala. Trocar a direção garantida de favorecimento por possível otimismo decorrente da seleção na mesma coorte. Se equivalência for objetivo futuro, planejar sua inferência específica.

### B3-05  Não rejeitar proporcionalidade não comprova ausência de violação; diagnóstico é outro ajuste
- Gravidade: importante
- Evidência: `sbcas/artigo/main.tex:85,137,141`; `resultados_sbcas/cox5_riscos_proporcionais.csv:2–21`; `pressupostos_cox.py:3–14,39–43,57,60–68`; `sobrevivencia.py:69`; `experimento.py:180–197`.
- Problema: “foi violado ... e não pelas demais variáveis” converte não rejeição em confirmação. Os resultados apoiam evidência de não proporcionalidade para protrombina nos testes usados; não certificam os demais efeitos. A tabela é de ajuste descritivo integral em lifelines, não dos 25 modelos preditivos. Há diferença adicional: o pipeline preditivo aplica log antes da imputação; o descritivo imputa a protrombina antes do log. `baseline_estimation_method='breslow'` identifica a estimação basal, não demonstra igualdade do tratamento de empates dos coeficientes com `ties='breslow'` do sksurv. Não foram examinadas formas funcionais, influência ou adequação completa. Chamar esse ajuste simplesmente de “Cox de referência” oculta essas distinções.
- Sugestão: dizer “houve evidência contra proporcionalidade para protrombina; não se detectou para as demais”; identificar a tabela como ajuste descritivo de mesma especificação de covariáveis e informar diferenças de implementação. Não apresentar o teste como certificação de todos os pressupostos nem inferir que a violação favoreceria necessariamente as florestas.

### B3-06  Referência reestimada e censura não estão suficientemente distinguidas do Mayo histórico
- Gravidade: importante
- Evidência: título e `sbcas/artigo/main.tex:31,35,41,65,67,71,175,186`; `sobrevivencia.py:69,94,170,269–270`; `privado/Dickson1989.txt:247–274`; PDF privado pp.2 e 5–6; `experimento.py:113–120`.
- Problema: a comparação é com um **novo Cox ajustado nos treinos**, com as covariáveis/transformações de Mayo, para o composto; não com a fórmula ou as probabilidades publicadas em 1989. O texto permite inferir isso pelos métodos, mas não o afirma diretamente e volta a chamá-lo de “Cox de Mayo”. Dickson tratou transplante como censura e reestimou o modelo final nos 418 após desenvolvimento nos 312. A frase “232 vivos sem transplante no fim do seguimento” também sugere seguimento completo: há perdas de acompanhamento descritas no original (oito no grupo de ensaio). Status C informa ausência de evento até o último contato, não que todos estavam vivos numa data final comum. Os 106 correspondem a 106 dos 112 recusantes, após seis exclusões históricas, não à totalidade inicial.
- Sugestão: declarar já no resumo/métodos “Cox reestimado com as cinco covariáveis de Mayo, não o escore publicado”; explicar o desfecho original e o composto atual. Descrever status C como censura no último acompanhamento sem evento registrado e resumir a origem dos 106 de 112.

### B3-07  Mesmo orçamento de ajuste é uma descrição inexata do desenho
- Gravidade: menor
- Evidência: `sbcas/artigo/main.tex:47`, “mesmo orçamento de ajuste”; `:71`; `sbcas/PLANO_ANALISE.md:27–29`; `sobrevivencia.py:69–82`.
- Problema: as duas RSF recebem 50 configurações cada; Cox17 recebe 40 combinações, e a referência não passa por busca. Não houve descumprimento da regra do plano, que distingue esses casos, mas a contribuição enunciada generaliza a igualdade para todos. Também há diferenças de penalização e imputação, já parcialmente reconhecidas em `main.tex:181`.
- Sugestão: especificar orçamento igual entre as duas florestas, grade completa de 40 para Cox17 e referência sem ajuste de hiperparâmetros. Manter a ressalva de que o 2×2 não isola exclusivamente algoritmo e informação adicional.

### B3-08  Tabela 3 é rastreável, mas não mede o efeito isolado do enquadramento
- Gravidade: importante
- Evidência: `sbcas/artigo/main.tex:85,155,159,165,186`; `tabelas/enquadramentos.tex:1–4`; `tabela_enquadramentos.py:9–13,30–65`; `sbcas/DESVIOS.md:15`; `experimento.py:97–102`.
- Problema: a regra pós-resultados do maior Δ está honestamente declarada. Contudo (a) e (c) mudam também amostra, métrica e comparador (RL versus Cox), além da tarefa; (d) muda alvo e contraste, usando AUROC macro de três classes e o mesmo XGBoost com/sem seguimento. Não se podem ordenar magnitudes de Δ entre essas escalas para dizer que +0,034 é “maior que qualquer diferença entre algoritmos” como evidência de efeito maior. O padrão 24/25 é descritivo em folds dependentes, não evidência de significância pelo critério dos IC. Em (d), “161 eventos” são apenas os óbitos de uma classificação com 232 C, 25 CL e 161 D; a coluna comum n/eventos é ambígua. “As duas de classificação, com regressão logística como referência” (`:85`) contradiz a referência de (d).
- Sugestão: apresentar a tabela como comparação descritiva de conclusões, indicando que não identifica causalmente o efeito do enquadramento. Corrigir a referência de (d), explicitar as três classes e informar os níveis Bonferroni distintos em (a) e (b)/(c). Restringir “consistente” à frequência descritiva das partições; não transportar a margem de Uno para AUROC.

### B3-09  Detalhes do protocolo de Graf não são verificáveis nas notas locais
- Gravidade: importante
- Evidência: `sbcas/artigo/main.tex:45,54,177`; `sbcas/notas_literatura.md:4–9`; `sbcas/artigo/referencias.bib:93–98`.
- Problema: 312 pacientes, C 0,776/0,855, sobreposição dos IC e melhor calibração do Cox nas simulações conferem com as notas. Estas também especificam RSF com divisão log-rank, IC [0,735; 0,817]/[0,778; 0,932] e IBS 0,131/0,116. Entretanto **sete variáveis, seleção retroativa por AIC, bootstrap .632+ e ausência de comparação pareada** não são documentados ali. A nota `:9` manda verificar o protocolo, em vez de registrar a verificação. Não foi encontrada nas fontes documentais consultadas uma cópia integral desse trabalho. Isso é suporte local insuficiente, não demonstração de que as frases são falsas.
- Sugestão: registrar localização precisa na fonte primária para esses quatro detalhes em uma próxima conferência autorizada, ou retirar os detalhes ainda não verificados. Distinguir números apoiados nas notas de protocolo não confirmado. Sobreposição de IC individuais, isoladamente, também não é teste de diferença pareada.

### B3-10  Lista de desvios ainda omite escolhas e entregas parciais já identificadas em A3
- Gravidade: menor
- Evidência: `sbcas/artigo/main.tex:61,81,85,89`; `sbcas/DESVIOS.md:7–15`; `sbcas/PLANO_ANALISE.md:36,55`; `auditoria/relatorio_A3.md`, A3-02/A3-07/A3-11; `resultados_sbcas/subgrupo_independente.csv:1`; `importancia_permutacao.py:19–20,28`.
- Problema: o texto declara que “toda mudança” foi registrada, mas D1–D9 não nomeiam a escolha de G marginal da coorte inteira no incremental como complementação ao plano. A escolha é explicada corretamente no artigo, sem evidência de vazamento de treino. Permanecem IC apenas de Uno/AUC no subgrupo, sem IC de Brier/IBS/O/E ou diferença pareada; isso não é explicitado como entrega limitada frente à redação ampla do plano. A importância foi restringida à RSF17 e à primeira repetição; D8 registra a escolha, mas não reconhece explicitamente a redução frente a “das florestas” no plano. D3 está disponível, mas a frase isolada “semente 2026” pode ocultar as sementes internas 2026–2050.
- Sugestão: completar o registro, preservando o plano original: origem de G, alcance dos IC do subgrupo e escopo reduzido da importância. Tornar explícito no artigo que as sementes internas são derivadas. Não é necessário repetir a análise para relatar essas escolhas com honestidade.

### B3-11  Regressão na paginação bibliográfica do GLOBE
- Gravidade: menor
- Evidência: `sbcas/artigo/referencias.bib:46`, `1804--1812`; `auditoria/verificacao_referencias.md:13`; `auditoria/relatorio_C2.md:18`.
- Problema: a versão SBCAS voltou à paginação abreviada que a auditoria anterior havia corrigido para **1804–1812.e4**. O registro local já documenta a paginação completa; não houve reconferência externa nesta passada.
- Sugestão: restaurar a paginação completa documentada. A omissão não muda os resultados nem invalida a identificação do trabalho.

### B3-12  Faltam definições e contexto para os dois públicos; importância não é efeito clínico
- Gravidade: menor
- Evidência: `sbcas/artigo/main.tex:65–85,117,137,175,179`; `experimento.py:105–109`; `resultados_sbcas/importancia_permutacao_rsf17.csv:2–18`; `main.tex:61` declara seguir TRIPOD+AI.
- Problema: o artigo não enumera as 17 entradas, suas unidades/codificações e disponibilidade; estágio histológico exige biópsia e tratamento é uma atribuição basal, o que importa para custo e aplicabilidade. Para computação, faltam explicação curta de censura, pares comparáveis, distinção entre média dos folds e métrica dos OOF médios e definição da AUC cumulativa/dinâmica. Os Δ da Tabela 1 não são simplesmente a subtração das médias de Uno impressas, embora isso esteja inferível dos métodos. Para clínica, faltam perfil basal, frequências de ausência e ação associada à curva de decisão. “O tratamento não contribuiu” é mais amplo que a queda média de −0,00136 por permutação de Drug_Dpen: mede contribuição preditiva naquele pipeline, não eficácia terapêutica. A explicação sobre poucos eventos, linearização e bilirrubina em `:175` é corretamente rotulada como plausível/não testada; a frase anterior sobre transformações que tornam a relação aproximadamente linear ainda soa como adequação já demonstrada. Não há checklist local que permita certificar a adesão integral ao TRIPOD+AI.
- Sugestão: incluir um quadro compacto ou suplemento com variáveis, unidades, ausências e perfil da coorte; explicar as escalas de métricas e a origem do Δ; definir o uso clínico hipotético. Escrever “não apresentou contribuição preditiva positiva nesta análise de permutação” para tratamento. Manter as explicações mecanísticas como hipóteses e apresentar checklist se a adesão integral ao TRIPOD+AI for reivindicada.

## Tratamento dos achados textuais de A3

| Achado anterior | Classificação nesta passada | Evidência e limite |
|---|---|---|
| A3-02 — IC condicionais e G na coorte inteira | **Parcialmente resolvido** | `main.tex:77,81,181` distingue G de treino/G marginal e informa reestimação bootstrap, sem chamar isso de vazamento. A limitação dos IC está correta no corpo. Falta propagá-la aos resumos/conclusão e registrar G como complementação; B3-02/B3-10. A dispersão de folds (`:81`) é descrição de estabilidade, não substituto de IC incondicional de todo o desenvolvimento. |
| A3-03 — decisões complementares e sementes | **Resolvido quanto à transparência documental** | D3 (`DESVIOS.md:9`) registra extremos, Breslow, grade anual e sementes 2026–2050, incluindo origem anterior aos resultados. `main.tex:71,89,181` apresenta extremos, complementações e grade. Melhorar a frase sobre semente é recomendável, mas o registro acessível impede confusão de cronologia. |
| A3-07 — ausência estrutural e subgrupo | **Parcialmente resolvido** | `main.tex:85,135,181` explica as nove ausências estruturais, transporte interno e ausência de comparação pareada, sem chamar de validação externa. A descrição de O/E é pontual e não prova pior calibração das florestas. Alcance dos IC, ausências parciais e sustentação da “conclusão se repete” ainda pedem delimitação; B3-02/B3-10/B3-12. |
| A3-10 — hipótese de censura e estimando de causa específica | **Resolvido quanto ao texto solicitado** | `main.tex:181` explicita independência, KM marginal, ausência de verificação e risco hipotético, distinguindo-o da incidência observável com competição. Isso não verifica a hipótese empiricamente nem produz análise de riscos competitivos, mas atende ao pedido de delimitação. B3-06 trata da descrição adicional das censuras históricas. |
| A3-11 — pressupostos e diferenças de pipeline | **Parcialmente resolvido** | `main.tex:85,137,141,179,181` e Tabela 2 apresentam diagnóstico de proporcionalidade e reconhecem que imputação/algoritmo não estão isolados. Permanecem a afirmação de ausência de violação nos demais efeitos, a identificação imprecisa do ajuste descritivo e ausência de exame de formas funcionais/influência. A troca de penalização entre Cox5/Cox17 também merece lembrança na atribuição a variáveis; B3-05/B3-07. |

## Plano, cronologia e honestidade dos desvios

`git diff 677a281 HEAD -- sbcas/PLANO_ANALISE.md` é vazio. O histórico confirma plano em 01/11 às 18:44, implementação às 18:47, primeiros resultados às 20:47/22:00; D8 foi registrado em `9d79736` às 22:31 e revisado em `012bfaa` às 22:37, antes dos resultados finais de `ebcc88c`/`bbcf04d` às 23:46/00:57. Isso comprova a ordem no histórico disponível, não ausência de experiências privadas.

| Item | Avaliação |
|---|---|
| D1/D2 | Artigo relata busca desalinhada, segunda execução corrigida e sensibilidade nativa (`main.tex:89,96`). A diferença numérica da sensibilidade nativa precisa B3-01. |
| D3 | Complementações não são falsamente chamadas de itens do plano original; registro distingue implementação pré-resultados de redação original. |
| D4/D5 | Proteções de suporte e proveniência existem; os resumos recompostos conferem. A explicação abreviada no artigo é aceitável com registro acessível. |
| D6 | A figura escolhe a RSF de maior **C médio nos folds**, não maior Δ OOF ou menor Brier. Código `calibracao_figura.py:101–103` e legenda `main.tex:122` são fiéis. A regra é complementação, não item do plano original. Fixada antes de gerar a figura final não significa fixada antes de todos os resultados; o texto não deve ampliar essa alegação. |
| D7 | Diagnóstico de proporcionalidade é adição após A3; `main.tex:89` inclui detalhamento das análises de apoio. Não foi falsamente reivindicado como teste originalmente pré-especificado. |
| D8 | Curva de decisão, HR e enquadramentos já eram previstos; detalhes de execução vieram depois. Linha de óbito adicional evita confundir inteiramente tarefa e desfecho. Restrição da importância à RSF17 pede a explicação de B3-10. |
| D9 | Escolha do maior Δ após conhecer resultados está declarada em `main.tex:89,155`; código usa `idxmax` (`tabela_enquadramentos.py:23–24`). Essa regra difere da escolha por C médio da figura, e o artigo descreve ambas corretamente. Não há evidência de escolha do modelo para obter IC mais favorável à tese. |

Não identifiquei teste pós-resultados claramente apresentado como pré-especificado em sua integralidade. Há exagero na universalidade do registro de “toda mudança” e na igualdade de orçamento, descritos nos achados. O motivo de D9 afirma que a escolha não favorece a tese; isso é uma justificativa dos autores, não garantia estatística de neutralidade de toda seleção.

## Citações e sustentação documental sem web

As **28 chaves citadas existem**, e as **28 entradas do `.bib` são citadas**: nenhuma referência órfã ou chave indefinida. Ano, volume e páginas bibliográficas não são resultados próprios; a validade externa integral dos metadados não foi recertificada. Os registros anteriores são evidência secundária local, não substituem leitura das fontes nesta passada.

| Chave(s) | Frase no artigo | Resultado e alcance da conferência |
|---|---|---|
| `dickson1989prognosis` | `main.tex:31,35,41,52,65,71` | Fonte primária privada lida: ano, duas pesquisas, datas, cinco variáveis, logs e derivação/validação conferem. Esclarecimentos de B3-06. Não se transportou a fórmula histórica para os resultados atuais. |
| `graf2025coxrsf` | `:45,54,177` | Números e calibração nas simulações conferem com `notas_literatura.md:5–8`; protocolo e comparação pareada não foram verificados: B3-09. |
| `uci878` | `:43,65` | Sustentação local em `auditoria/verificacao_referencias.md:10` e comparação de dados arquivada; site/licença não reabertos. |
| `fleming1991counting` | `:43,65` | Registro `verificacao_referencias.md:11` confirma metadados e aponta conteúdo do apêndice ainda não verificado. História básica é corroborada por Dickson; livro não foi lido integralmente. |
| `beuers2015nomenclature` | `:41` | Mudança em 2015 apoiada no registro anterior (`verificacao_referencias.md:12`); original não relido nesta passada. |
| `lammers2015globe`, `carbone2016ukpbc` | `:52,67` | Contexto após tratamento apoiado nos registros `verificacao_referencias.md:13–14` e `artigo/secoes/relacionados.tex:8`. UK-PBC combina também exames basais e tem avaliação em não tratados; não convém sugerir exclusividade absoluta. A identidade exata do composto atual com os desfechos desses escores não foi confirmada nos originais nesta passada. Paginação GLOBE: B3-11. |
| `ishwaran2008rsf` | `:52,71` | Uso dos 312/17 variáveis documentado em `verificacao_referencias.md:16`; fonte integral não relida. Citação tem pertinência metodológica. |
| `reade2023ps3e26` | `:43,56` | Três classes e origem sintética documentadas em `verificacao_referencias.md:17`; página da competição não consultada. |
| `shakir2025cirrhosis`, `tu2025cirrhosis` | `:56,177` | Registro anterior `verificacao_referencias.md:18–19` e `relatorio_C.md` sustenta a descrição geral dos experimentos; não se releram os trabalhos originais nesta passada. Aproximadamente 90% e acusações específicas de vazamento devem manter atribuição clara a cada trabalho; Kapoor fornece conceito geral, não prova independente do protocolo desses autores. |
| `christodoulou2019systematic` | `:43,175` | 71 estudos e resultado em baixo risco de viés apoiados em `verificacao_referencias.md:20`. É revisão sobre classificação com regressão logística; analogia com sobrevivência é contextual, não valida diretamente a tese deste experimento. |
| `kapoor2023leakage`, `vancalster2019calibration`, `varma2006bias` | `:45,56,75,177` | Pertinência conceitual e registros anteriores em `verificacao_referencias.md:22–23,26`; fontes primárias não relidas. |
| `collins2024tripodai` | `:61` | Metadados registrados anteriormente (`verificacao_referencias.md:25`); seguir integralmente a diretriz não foi demonstrado por checklist nesta passada. |
| `cox1972regression`, `simon2011coxnet` | `:41,71` | Pertinentes aos métodos descritos; fontes integrais não disponíveis entre os textos primários consultados. Não certificadas frase a frase. |
| `uno2011cstat`, `uno2007auc`, `graf1999brier`, `harrell1982yield` | `:77` | Citações metodologicamente pertinentes; código usa métricas compatíveis. Fontes originais não relidas. “Mesma ponderação” deve ser entendido como família IPCW, não igualdade literal dos pesos/fórmulas de Uno, AUC e Brier. |
| `grambsch1994ph` | `:85` | Pertinente ao diagnóstico implementado; original não relido. Não sustenta provar proporcionalidade por não rejeição. |
| `vickers2006dca`, `vickers2008extensions` | `:77` | Pertinentes à curva e extensão para sobrevivência; cálculo salvo reproduzido. Fontes integrais não relidas; B3-04 limita a interpretação. |
| `putter2007competing` | `:181` | Pertinente à distinção entre risco líquido e incidência cumulativa; texto primário não relido. |
| `polsterl2020sksurv`, `davidsonpilon2019lifelines` | `:71,85` | Uso das bibliotecas confirmado no código/manifestos; metadados bibliográficos não recertificados externamente. |

Não se identificou contradição numérica entre as notas de Graf e os números transcritos. Não há base, sem seu original, para certificar os detalhes adicionais ou declarar que estão errados. Tampouco esta passada certifica a alegação de ausência de estudos equivalentes no levantamento (`main.tex:56`), que dependeria da estratégia e data de busca.

## Coerência interna, anonimato e forma

- Abstract e resumo são numericamente concordantes; resultados repetidos em discussão e conclusão conservam os valores. As falhas de coerência relevantes são de **alcance inferencial** (B3-02/B3-03/B3-08), não troca de números entre idiomas.
- O PDF existente tem **11 páginas**, abaixo do limite de 12. Figuras 1/2 e Tabelas 1/2/3 têm chamadas no texto; seus rótulos têm correspondência. A tabela de óbito não incluída não precisa de chamada como tabela do PDF principal, mas a disponibilização suplementar deveria ser explícita.
- Não encontrei nomes, afiliações, login ou endereço identificador da autoria no conteúdo de `sbcas/artigo/main.tex`, no texto extraído do PDF ou nos campos de metadados exibidos por `pdfinfo`. Há marcadores de autoria/afiliação omitidas (`main.tex:23–24`). Nomes de pesquisadores citados e instituições das coortes não são identificação da autoria submetente. O endereço anonimizado (`:89`) é textual; seu destino e seu conteúdo não foram acessados nem certificados nesta passada sem web.
- A declaração de IA está presente (`main.tex:188–190`, PDF p.9), com ferramentas e responsabilidade da autoria. “Auditor independente” deve ser entendido como agente separado; a própria declaração identifica uso de IA.
- Não há caractere de travessão **U+2014 (—)** no `.tex` principal nem no texto extraído do PDF. Traços de intervalo e sinais de menos não foram confundidos com esse caractere.
- Não há `??` no texto extraído, as citações aparecem resolvidas, todas as chaves existem e todos os `ref` têm `label`. **Compilação sem erros não foi certificada**: não há `.log` de compilação entre os artefatos disponíveis e não se fez compilação nova, pois ela produziria arquivos além do relatório, contrariando a restrição desta passada. A existência de um PDF legível não prova compilação limpa da versão atual. A conferência de tabelas, textos e figuras reduz a dúvida sobre correspondência, mas não substitui o log.
- Visualmente, as figuras estão legíveis nas páginas examinadas; há dispersão de floats (Figura 2 só na p.8), mas não foi identificado erro material de legenda ou figura trocada. Para o SBCAS, as maiores barreiras de leitura são os parágrafos densos de métodos e as definições/contexto ausentes em B3-12, mais que o formato visual.

## Tabela-resumo

| Achado | Gravidade | Providência principal |
|---|---|---|
| B3-01 — Dois limites/arredondamentos inexatos | menor | Atualizar desvio entre folds e diferença nativa máxima. |
| B3-02 — Margem e estabilidade sem ressalvas nos resumos/conclusão | importante | Explicitar inferência condicional e fragilidade da RSF17. |
| B3-03 — Calibração global/local e IC sem distinção suficiente | importante | Separar estimativas pontuais, incerteza e limite binomial. |
| B3-04 — Curva de decisão interpretada como equivalência | importante | Delimitar análise descritiva e seleção; definir contexto clínico. |
| B3-05 — Proporcionalidade e identidade do Cox descritivo | importante | Relatar não detecção e diferenças do ajuste diagnóstico. |
| B3-06 — Referência reestimada e censura histórica | importante | Distinguir novo Cox/escore original e último contato/fim comum. |
| B3-07 — Orçamento declarado igual para todos | menor | Dizer 50 por RSF, 40 Cox17, sem busca Cox5. |
| B3-08 — Tabela 3 não isola efeito do enquadramento | importante | Delimitar contrastes/métricas e corrigir referência da linha (d). |
| B3-09 — Protocolo de Graf sem suporte local suficiente | importante | Verificar fonte primária ou retirar detalhes não confirmados. |
| B3-10 — Registro de desvios e entregas parciais incompleto | menor | Acrescentar G marginal e alcance de subgrupo/importância. |
| B3-11 — Paginação GLOBE regressiva | menor | Restaurar 1804–1812.e4 documentado. |
| B3-12 — Clareza e contexto para computação/clínica | menor | Explicar variáveis, métricas, ação clínica e importância preditiva. |

## Veredito

**Aprovado com ressalvas.** Não foi encontrado erro que derrube os números centrais, a implementação da regra da margem na segunda execução ou a conclusão restrita de ausência de superioridade demonstrada. Há **7 achados importantes e 5 menores; nenhum bloqueante**. As correções principais são de redação científica e transparência: a exclusão da margem na RSF17 é condicional e limítrofe; calibração e utilidade não têm equivalência demonstrada; os contrastes da Tabela 3 não identificam o efeito isolado da tarefa. Recomenda-se tratar esses pontos antes da submissão. A compilação limpa e os detalhes adicionais do protocolo de Graf permanecem não certificados nesta passada, pelas limitações documentais e operacionais declaradas. Nenhum insumo do artigo ou da análise foi corrigido.

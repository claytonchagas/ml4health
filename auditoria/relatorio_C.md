# Auditoria independente: Passada C, conformidade e referências

Data: 01/11/2026. Veredito: **aprovado com ressalvas**.

## Escopo e procedimento

Foram lidos `AUDITORIA.md`, `auditoria/relatorio_B.md`, `artigo/LEIA-ME.md`, README, notebook, `artigo/main.tex`, as sete seções, a bibliografia e o texto extraído das 15 páginas do PDF entregue. O texto privado de Dickson foi consultado dentro de `privado/`. As células são numeradas desde 1, incluindo Markdown (43 no total). As referências de linha correspondem ao estado examinado, não ao relatório B.

Somente este relatório foi escrito. Não houve busca ou leitura de arquivos fora do repositório, instalação, compilação LaTeX ou treinamento. A web foi usada exclusivamente para verificar as referências do item 3; a avaliação de conformidade abaixo foi feita sobre os arquivos locais. Executou-se apenas o comparador de CSVs já existente, que lê dois commits, e a análise sintática das células em memória. Todas as células de código passaram no parser Python; não há saída de erro salva. Isso não certifica execução integral nem compatibilidade com o ambiente atual do Colab.

Na consulta bibliográfica, resultados indexados do próprio periódico/PubMed/repositório institucional também foram utilizados quando a abertura direta falhou. A matriz distingue metadados confirmados, sustentação confirmada e aspectos inacessíveis. DOI resolvível ou título plausível, isoladamente, não foram tratados como comprovação. Não se certifica que todas as 23 referências foram integralmente verificadas.

## 1. Enunciado: README e notebook

| Exigência | Evidência | Resultado |
|---|---|---|
| README: motivação/objetivo | `README.md:13–25` | Presente: problema clínico, comparador e perguntas. |
| Descrição do dataset | `README.md:31–52` | Presente: fonte, população, unidade, variáveis, desfecho e ausências. |
| Preparação/pré-processamento | `README.md:54–61` | Presente: horizonte, exclusões, codificação, transformações e imputação no treino. |
| Link para o dataset | `README.md:35,63–65` | Presente: DOI/UCI e cópia efetivamente executada, com origem Rdatasets. |
| Modelo: formalização matemática | `README.md:71–101` | Presente: alvo, Mayo, regressão, floresta e boosting. |
| Modelo: validação | `README.md:103–110` | Presente: CV repetida, busca interna e teste quase externo. |
| Modelo: medidas de desempenho | `README.md:112–123` | Presente: AUROC, AP, Brier, calibração, diferenças e métricas do controle. |
| Avaliação: treino, validação e teste | `README.md:129–139` | Presente: tamanhos aproximados dos folds externos/internos e 244/68 na quase externa. Não é obrigatório criar um holdout adicional: o teste é o fold externo. |
| Avaliação: desempenho observado | `README.md:143–208` | Presente: tabelas de métricas, dispersão, ICs e análises complementares. |
| Conclusão | `README.md:212–220` | Presente, com limitações. |
| Notebook: dependências | Células 2–3; `requirements.txt:1–11` | Presente: instalação condicional e versões impressas; ambiente oficial fixado separadamente. |
| Bibliotecas | Célula 5 | Presente. |
| Funções de apoio | Células 8,10,12,14,16,18 | Presente: carga, rótulo, modelos, métricas e validação. |
| Carregamento/pré-processamento | Células 8,12,19–22 | Presente; fonte local com download de contingência e checksum. |
| Hiperparâmetros | Células 12,23–24,29,39 | Presente: grades e escolhas salvas. |
| Gráficos de iteração | Células 25–26 | Presente: log loss por rodada do XGBoost, erro OOB por número de árvores e AUROC por C. A curva da RL é de regularização, não iteração de otimização; o XGBoost atende literalmente à exigência de perda por iteração. São demonstrações separadas da seleção. |
| Gráficos das medidas | Células 36,42, com imagens salvas | Presente: boxplots, ROC, calibração e controle de vazamento. |

Não falta uma seção obrigatória do enunciado. A executabilidade foi examinada estaticamente e por saídas arquivadas; não foi retestada. As ressalvas de proveniência, referências e relato estão nos achados, sem implicar ausência dos blocos exigidos.

## 2. Orientações do professor e artigo

| Orientação em `artigo/LEIA-ME.md` | Evidência no artigo | Avaliação |
|---|---|---|
| Título/autoria/resumo com resultados reais (:16) | `main.tex:69–74`; `secoes/resumo.tex:8` | Atendida: identificação real, objetivo, amostra 312/115, desenho, AUROC 0,906 e resultados incrementais. |
| Introdução sem subdivisões (:17) | `secoes/introducao.tex:3–15` | Atendida: somente uma seção, sem subseções. Contexto em :5; problema em :7–9; lacuna e pergunta em :9–11; objetivo em :11; contribuições em :13. |
| Levantamento e comparação crítica (:18) | `secoes/relacionados.tex:4–12,22–39` | Atendida estruturalmente: revisão narrativa declarada, bases, termos, grupos selecionados e comparação de populações/métodos/validação/limitações. Faltam data final da busca e estratégias completas para reproduzi-la, aperfeiçoamentos desejáveis para uma revisão narrativa, sem exigir retrospectivamente revisão sistemática. Há correções factuais em C-01/C-02 e verificações pendentes em C-07. |
| Métodos completos (:19) | `secoes/metodos.tex:5–10,22–34,59,70–108` | Unidade, seleção, alvo, EDA, pipeline, particionamento, ajuste e métricas presentes. Reprodutibilidade documentada; fonte efetivamente executada não está identificada corretamente no artigo (C-03). Relato amostral e de incerteza parcial (C-05). Ética presente, com base da dispensa não explicitada (C-06). |
| Resultados reais, conjunto, n, variabilidade (:20) | `secoes/resultados.tex:5,16–30,34–86,91–98,126–159` | Atendida em grande parte: resultados correspondem aos artefatos locais já auditados em B, amostra identificada e média/desvio/ICs. Resultados no limiar e quase externos são expressamente descritivos, sem IC; isso é transparente, mas impede conformidade integral de desempenho com incerteza (C-05). |
| Discussão e conclusão proporcionais (:21) | `secoes/discussao.tex:4–12`; `secoes/conclusao.tex:4–6` | Atendida: comparação com literatura, hipóteses identificadas como não testadas e limitações extensas. Igualdade/equivalência não é mais alegada nos pontos de B-02. “Vale mais a pena” é uma interpretação prática sem ganho demonstrado, não avaliação econômica formal. |
| Bibliografia e comandos (:22) | `main.tex:34,80–90`; `.bib:6–259`; chamadas nas seções | 23 entradas e 23 chaves citadas, sem órfãs nem chave ausente. Há uma chave `}` excedente em `.bib:123` (C-04); metadados e suporte exigem as ressalvas da matriz. |
| Figuras reais na pasta indicada (:23) | `metodos.tex:63`; `resultados.tex:95,163`; figura TikZ em `metodos.tex:38–55` | Atendida: figuras do experimento, fontes e legendas; não persistem dados fictícios do modelo. |

O PDF entregue tem 15 páginas, citações resolvidas e nenhum `??` na extração. Ele contém o texto atualizado das correções B. Não foi recompilado; sua existência não prova compilação limpa do fonte atual. Esta inspeção não é uma certificação de adequação estrita à ABNT, que o próprio LEIA-ME (:25) distingue do uso do pacote.

## 3. Referências: metadados e sustentação

Consulta em 01/11/2026. Nas linhas abaixo, “confere” para metadados abrange autores explicitamente cadastrados, ano, título, veículo, volume, número, páginas/identificador e DOI, quando esses campos foram disponibilizados pela fonte; exceções são nomeadas. `and others` é abreviação de lista, não autoria falsa. Livros, datasets, competições e dissertações não exigem volume/número de periódico. Números de artigo em periódicos de publicação contínua não são intervalos de páginas; não se inventa fascículo ausente. A sustentação foi avaliada separadamente dos metadados.

| Entrada e linhas em `artigo/referencias.bib` | Fonte/URL consultada | Resultado dos metadados e da frase citada |
|---|---|---|
| `dickson1989prognosis` :6–16 | [PubMed 2737595](https://pubmed.ncbi.nlm.nih.gov/2737595/); texto local `privado/Dickson1989.txt:5–10,67–90,257–265,660–716` | **Confere**: cinco autores, 1989, título, Hepatology 10(1):1–7 e DOI 10.1002/hep.1840100102. Sustenta derivação nos 312, validação nos 106, combinação final nos 418, cinco preditores, dois ensaios e fórmula/exemplos em `introducao.tex:7`, `relacionados.tex:8,24`, `metodos.tex:10,77–85`. |
| `uci878` :18–26 | [UCI 878](https://archive-beta.ics.uci.edu/dataset/878/cirrhosis%2Bpatient%2Bsurvival%2Bprediction%2Bdataset-1) | **Confere** quanto aos cinco autores, título, repositório, ano de criação 1989, DOI 10.24432/C5R02G e CC BY 4.0. Não foi possível confirmar, na página retornada, a data de disponibilização 2023 da nota. Fonte confirma 418, 17 entradas, 312/112/106 e definição temporal. Não demonstra identidade valor a valor com o snapshot Rdatasets nem autoriza atribuir a execução ao download UCI (`metodos.tex:10,44,66`; C-03). |
| `fleming1991counting` :28–34 | [Wiley, livro](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118150672) | **Confere**: Fleming/Harrington, título, Wiley, copyright original 1991; a página eletrônica é de 2005 e não invalida a edição original. Local New York não confirmado nessa página. O DOI eletrônico 10.1002/9781118150672 não consta no .bib, omissão não tratada como erro da edição impressa. Sustenta assunto de sobrevivência (`introducao.tex:7`); não foi possível verificar diretamente o apêndice de dados nem a história detalhada atribuída em `metodos.tex:10`, sustentada independentemente por Dickson. |
| `beuers2015nomenclature` :36–46 | [PubMed 26372460](https://pubmed.ncbi.nlm.nih.gov/26372460/); [DOI](https://doi.org/10.1002/hep.28140) | **Confere**: 12 autores, título, 2015, Hepatology 62(5):1620–1622 e DOI. Título/ano sustentam a mudança de nomenclatura (`introducao.tex:5`). **Não foi possível verificar integralmente** a descrição clínica e a afirmação “maioria ... não tem cirrose no diagnóstico”: PubMed sem resumo, acesso integral ao DOI indisponível. |
| `lammers2015globe` :48–58 | [PubMed 26261009](https://pubmed.ncbi.nlm.nih.gov/26261009/); [Erasmus University](https://pure.eur.nl/en/publications/development-and-validation-of-a-scoring-system-to-predict-outcome/) | **Diverge** na paginação completa: 1804–1812.e4, em vez de apenas 1804–1812. Demais campos conferem: autores iniciais, título, 2015, Gastroenterology 149(7), DOI. **Diverge** a derivação em 4.119 (`relacionados.tex:8`): total 4.119, derivação 2.488, validação 1.631. Oito países e C de validação 0,82 conferem; preditores após um ano sustentam a distinção temporal. C-01/C-04. |
| `carbone2016ukpbc` :60–70 | [PubMed 26223498](https://pubmed.ncbi.nlm.nih.gov/26223498/); [texto integral PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6984963/) | **Confere**: autores iniciais, título, Hepatology 63(3):930–950, 2016, DOI 10.1002/hep.28017 (online em 2015). Sustenta 1.916/1.249 e AUCs >0,90 (`relacionados.tex:8,26`); análise de validação completa usa 1.109 com dados disponíveis, com AUC 0,96/0,95/0,94. Albumina/plaquetas são basais; demais exames aos 12 meses. **Diverge por excesso** a incompatibilidade absoluta com linha de base: o trabalho também testa não tratados e discute aplicação pré-tratamento, com cautela. C-02. |
| `gerussi2022ml` :72–82 | [PubMed 34951722](https://pubmed.ncbi.nlm.nih.gov/34951722/); [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/liv.15141) | **Confere**: autores iniciais, título, Liver International 42(3):615–627, 2022 e DOI 10.1111/liv.15141; online em dezembro de 2021. Resumo confirma 11.819 de treino, 1.069 de validação, quatro grupos e método não supervisionado (`relacionados.tex:10,27`). **Não foi possível verificar integralmente** a afirmação negativa “sem comparação preditiva com escore”: acesso retornou principalmente resumo e referências, com timeout na tentativa de consultar o corpo. |
| `ishwaran2008rsf` :84–94 | [Reimpressão dos autores no arXiv](https://arxiv.org/pdf/0811.1645), pp. 1 e 14 da reimpressão | **Confere**: quatro autores, título, 2008, Annals of Applied Statistics 2(3):841–860, DOI 10.1214/08-AOAS169. Seção 8.5 confirma 312 randomizados e 17 variáveis; sustenta método e caráter ilustrativo de PBC (`relacionados.tex:10,28`), não comparação incremental específica com Mayo. |
| `reade2023ps3e26` :96–102 | [Kaggle, competição](https://www.kaggle.com/competitions/playground-series-s3e26); [dados](https://www.kaggle.com/competitions/playground-series-s3e26/data); [citação](https://www.kaggle.com/competitions/playground-series-s3e26/overview/citation) | **Confere**: Reade/Chow, título, temporada/episódio e 2023 na página indexada oficial. Sustenta três classes, log loss e caráter sintético (`relacionados.tex:12`). **Não foi possível verificar integralmente** a lista de colunas/N_Days e geração a partir da base original: página de dados sem texto legível. A tese de Tu descreve essa origem, mas isso não substitui verificar a página do dataset. Não há evidência quantitativa para “enquadramento mais difundido” (`introducao.tex:9`, `relacionados.tex:39`). |
| `shakir2025cirrhosis` :104–114 | [PDF do periódico](https://journal.irpi.or.id/index.php/predatecs/article/download/2015/1052/11445); [página](https://journal.irpi.or.id/index.php/predatecs/article/view/2015) | **Confere** nos metadados e resumo indexados do próprio PDF: Yasir Hussein Shakir, Eshaq Aziz Awadh AL Mandhari, Ali Alkhazraji; título, 2025, veículo, 3(1):22–30 e DOI 10.57152/predatecs.v3i1.2015. Confirma cinco modelos, SVMSMOTE e 89,55% para XGBoost. **Não foi possível verificar** remoção de N_Days, três classes, fonte sintética, ordem no fluxograma e ausência de calibração (`relacionados.tex:12,29`; `discussao.tex:6`): downloads repetidos deram timeout; só o início indexado ficou disponível. C-07. |
| `tu2025cirrhosis` :116–123 | [Registro UCLA](https://escholarship.org/uc/item/0d66m3m6); [PDF institucional](https://escholarship.org/content/qt0d66m3m6/qt0d66m3m6.pdf), pp. internas 3,5,23–24 | **Confere**: Timothy Enoch Tu, título, 2025, mestrado UCLA (Master of Applied Statistics and Data Science); DOI/volume/fascículo não se aplicam ao registro. Sustenta treino sintético, teste nos 418 originais, cinco modelos, C/CL agrupados, sem horizonte, RF 89% e XGBoost AUC 0,95 (`relacionados.tex:12,30`). Não apresenta avaliação de calibração no relato consultado. A abertura do registro sofreu barreira JavaScript, superada pelo PDF institucional. |
| `christodoulou2019systematic` :125–134 | [PubMed 30763612](https://pubmed.ncbi.nlm.nih.gov/30763612/) | **Confere**: seis autores, título, J Clin Epidemiol 110:12–22, 2019, DOI 10.1016/j.jclinepi.2019.02.004. Sustenta 71 estudos, 282 pares, 79% sem calibração e diferença de logito 0,00 [−0,18;0,18] em baixo risco (`introducao.tex:9`, `relacionados.tex:36,39`, `discussao.tex:6`). **Não foi possível verificar** suporte específico a “balanceamento ... distorceria probabilidades” em `metodos.tex:34`: essa proposição não consta no resumo acessível. C-07. |
| `kapoor2023leakage` :136–146 | [PubMed 37720327](https://pubmed.ncbi.nlm.nih.gov/37720327/); [artigo em repositório NSF](https://par.nsf.gov/servlets/purl/10513990) | **Confere**: Kapoor/Narayanan, título, Patterns 4(9):100804, 2023, DOI 10.1016/j.patter.2023.100804. Sustenta problema de vazamento, resultados otimistas e irreprodutibilidade (`introducao.tex:9`, `relacionados.tex:36`, `discussao.tex:10`). Não documenta especificamente frequência do enquadramento PBC/Kaggle; essa generalização é do artigo auditado. |
| `vancalster2019calibration` :148–157 | [BMC Medicine](https://link.springer.com/article/10.1186/s12916-019-1466-7) | **Confere**: cinco autores nomeados, título, 2019, volume 17, artigo 230 e DOI. Há também atribuição ao grupo STRATOS na publicação. Sustenta necessidade de calibração, metas 0/1 e sentidos de intercepto/inclinação (`relacionados.tex:36`, `metodos.tex:103`, `discussao.tex:8`). Não sustenta que proximidade pontual garanta adequação: a fonte explicitamente diferencia isso de curva bem calibrada. |
| `steyerberg2014seven` :159–169 | [PubMed 24898551](https://pubmed.ncbi.nlm.nih.gov/24898551/) | **Confere**: dois autores, título, Eur Heart J 35(29):1925–1931, 2014, DOI 10.1093/eurheartj/ehu207. Sustenta desenvolvimento/validação e avaliação de calibração/discriminação (`relacionados.tex:39`). |
| `collins2024tripodai` :171–180 | [PubMed original 38626948](https://pubmed.ncbi.nlm.nih.gov/38626948/); [texto integral PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11019967/) | **Confere**: autores iniciais, título, BMJ 385:e078378, 2024, DOI 10.1136/bmj-2023-078378. Sustenta o padrão de relato (`introducao.tex:13`, `metodos.tex:5`), mas a citação não comprova que o estudo o cumpre integralmente. O resultado PubMed 38636956 é uma errata q902, não deve substituir a referência original. |
| `varma2006bias` :182–191 | [BMC Bioinformatics](https://link.springer.com/article/10.1186/1471-2105-7-91) | **Confere**: Varma/Simon, título, 2006, volume 7, artigo 91, DOI. Sustenta CV aninhada para reduzir viés de seleção (`metodos.tex:70`). |
| `zou2005elasticnet` :193–203 | [Oxford, página indexada do periódico](https://academic.oup.com/jrsssb/article/67/2/301/7109482?searchresult=1); [DOI](https://doi.org/10.1111/j.1467-9868.2005.00503.x) | **Confere**: Zou/Hastie, título, JRSS B 67(2):301–320, 2005 e DOI. Sustenta penalização elastic net (`metodos.tex:89`). Abertura direta redirecionou com erro; a página indexada permitiu conferir identificação/conceito, não todos os detalhes da parametrização logística específica do software. |
| `breiman2001random` :205–215 | [Springer](https://doi.org/10.1023/A%3A1010933404324) | **Confere**: Breiman, título, Machine Learning 45:5–32, 2001 e DOI. O número 1 não foi exibido no trecho acessível, ficando sem confirmação independente nesta consulta. Sustenta combinação de árvores e seleção aleatória de entradas (`metodos.tex:91`); 300 árvores é configuração deste experimento, não resultado atribuído ao autor. |
| `chen2016xgboost` :217–225 | [ACM, registro indexado](https://doi.org/10.1145/2939672.2939785); [arXiv dos autores](https://arxiv.org/abs/1603.02754); [texto](https://arxiv.org/pdf/1603.02754) | **Confere**: Chen/Guestrin, título, KDD 2016, 785–794 e DOI ACM. Texto sustenta árvores aditivas, regularização e aproximação de segunda ordem (`metodos.tex:93`). Volume/fascículo não se aplicam. |
| `vanbuuren2011mice` :227–237 | [JSS](https://www.jstatsoft.org/article/view/v045i03) | **Confere**: van Buuren/Groothuis-Oudshoorn, título, 2011, DOI 10.18637/jss.v045.i03; volume 45/número 3 identificados pelo registro. Páginas 1–67 não ficaram visíveis no HTML e o PDF não abriu, portanto **não foi possível verificar** essa extensão nesta consulta. Sustenta conceito de equações encadeadas (`metodos.tex:34`), não identidade entre mice em R e IterativeImputer nem execução de imputação múltipla com pooling. O texto atual não afirma ter usado o pacote R. |
| `pedregosa2011scikit` :239–247 | [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html) | **Confere**: lista de 16 autores (diferenças de acentuação/transliteração não materiais), título, 2011, volume 12:2825–2830. Página identifica artigo 85; não há DOI informado no registro. Sustenta uso do software (`metodos.tex:34`); não é prova de ausência de vazamento no pipeline concreto. |
| `fawcett2006roc` :249–259 | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S016786550500303X); [texto em instituição acadêmica](https://people.inf.elte.hu/kiss/13dwhdm/roc.pdf) | **Confere**: Fawcett, título, Pattern Recognition Letters 27(8):861–874, 2006 e DOI. Sustenta interpretação probabilística da AUROC (`metodos.tex:98`), com convenção de meio crédito para empates que a formulação abreviada não explicita. |

As verificações incompletas acima são limitações de acesso, não demonstrações de que os trabalhos sejam falsos. Também não se deve transformar ausência de verificação em aprovação da crítica feita a terceiros. Nenhum número inacessível foi validado apenas por constar no relatório B.

## 4. Itens essenciais de relato TRIPOD+AI

Esta matriz examina os itens solicitados no prompt. Não representa certificação de todos os subitens do checklist completo.

| Item | Evidência local | Situação |
|---|---|---|
| Fonte de dados, local e período | `metodos.tex:10,108`; README :35–40,65 | **Parcial**: Mayo, período e acesso informados; falta no artigo distinguir snapshot Rdatasets de UCI (C-03). |
| Participantes/unidade/seleção | `metodos.tex:5,10,59,72`; `resultados.tex:5,16–30` | **Parcial**: paciente, coorte, seleção por horizonte e fluxo numérico presentes. Critérios clínicos de elegibilidade dos ensaios são apenas remetidos a Dickson; não se detalha seleção consecutiva nem aferição clínica original. Não confundir essa omissão de relato com exclusão adicional no código. |
| Desfecho | `metodos.tex:5,26–27,59`; notebook célula 8 | **Atendido no essencial**: óbito em cinco anos, tempo, censura e transplante explicitados. Não se detalha como o estudo original confirmou óbitos; pode-se esclarecer óbito por qualquer causa, como Dickson (:267). |
| Preditores | `metodos.tex:22–25,34,75–95`; células 8,12 | **Parcial**: nomes, momento basal, transformações e codificação presentes; faltam unidades de vários laboratórios e descrição de aferição original. O código permite recuperar especificações operacionais. |
| Tamanho amostral | `metodos.tex:59,72`; `resultados.tex:5`; `discussao.tex:6,12` | **Parcial**: n/eventos e limitação de base pequena presentes; não explica explicitamente que o tamanho foi determinado pela totalidade de dados elegíveis, sem cálculo prospectivo de suficiência/precisão (C-05). |
| Dados ausentes | `metodos.tex:34,59,72`; README :42–60 | **Atendido no essencial**: padrão por desenho, elegibilidade completa e tratamento por pipeline; poderia trazer tabela integral de ausências ao artigo. |
| Análise/validação/ajuste | `metodos.tex:70–105`; células 12–18,23–24 | **Atendido no essencial**: seleção, ajuste aninhado, partições, orçamento, métricas, ICs condicionais e comparações múltiplas claros. |
| Desempenho: discriminação/calibração | `resultados.tex:38–86,91–98,126,131–156` | **Parcial**: ambas avaliadas, dispersão por fold e IC de diferenças presentes. Não há IC para desempenho absoluto ou calibração; quase externa sem qualquer IC. Desvio entre folds não é IC de desempenho (C-05). |
| Limitações | `discussao.tex:12`; README :220 | **Atendido**: centro/período, seleção por censura, ausência de validação externa verdadeira, incerteza condicional, ausência de equivalência e busca modesta. |
| Disponibilidade de código/dados | `metodos.tex:108`; README :5,35,65,238–250 | **Atendido**, com ressalva de proveniência no artigo: código/notebook/snapshot/resultados e URL pública declarada. A publicidade efetiva do servidor não foi consultada, pois web ficou restrita às referências. |

## 5. Colab

O badge em `README.md:7` aponta para `https://colab.research.google.com/github/ANONIMO/ml4health/blob/main/ml4health_cbp_mayo.ipynb`. Proprietário/repositório coincidem com o remote local e o notebook existe na raiz com esse nome. **Caminho correto na inspeção local**; não foi feito teste HTTP do badge nem execução Colab.

A primeira célula de código é a **célula 3**. Ela verifica os módulos `ucimlrepo`, `xgboost`, `sklearn`, `pandas`, `numpy`, `matplotlib`, instala os ausentes por `sys.executable -m pip` e mapeia `sklearn` para o nome de pacote `scikit-learn`. Cria `resultados/` e `figs/` com `exist_ok=True`. **Atende ao solicitado**. `data/` é criada sob demanda pela função da célula 8, antes do download do snapshot. Portanto, não depende de clone prévio para obter o CSV.

A instalação verifica presença, não versão mínima/compatibilidade. Essa diferença do ambiente oficial está declarada em `README.md:250`; não constitui falha comprovada no Colab. O teste manual autorizado ao autor continua necessário. A análise sintática e as saídas arquivadas não o substituem.

## 6. Correções da passada B

| Item | Classificação | Evidência no estado atual |
|---|---|---|
| B-01: custo de variáveis generalizado | **Resolvido** | `introducao.tex:7` e `README.md:17` condicionam exames extras ao uso além das cinco variáveis. `discussao.tex:4` e `conclusao.tex:4` distinguem custo das 17 entradas e transparência. |
| B-02: igualdade e calibração além da análise | **Resolvido** | `discussao.tex:4` nega teste de aproveitamento igual; :8 fala em estimativas próximas das ideais; `conclusao.tex:4` usa proximidade nominal/sem diferença demonstrada. `resultados.tex:91` chama a figura descritiva e sem bandas; `README.md:216` evita “bem calibrada”. A falta de IC absoluto persiste como limitação de relato (C-05), mas as formulações apontadas em B foram corrigidas. |
| B-03: reprodução sem registro | **Resolvido**, no alcance dos artefatos comparados | `metodos.tex:108`; `README.md:250`; `auditoria/comparar_execucoes.py:10–33`; `auditoria/comparacao_execucoes.txt:1–15`. O comparador foi reexecutado sem treino e reproduziu máximo arredondado 1,6e-13 nos nove CSVs comuns dos commits 00d1773/0fb5b54. Compara colunas comuns, não comprova identidade de todas as figuras/saídas nem audita a realização histórica dos treinos. |
| B-04: aproximações incorretas | **Resolvido** | `discussao.tex:4` informa −0,013 a +0,009; `resultados.tex:89` e `README.md:215` informam faixa 0,005–0,010; README discrimina +0,009/+0,010/+0,005. |
| B-05: AUROC histórica da curva | **Resolvido** | `README.md:123` agora distingue OOF 0,911/0,908 de média por fold 0,910; célula 36 calcula a legenda sobre OOF médias. |
| B-06: travessão na entrada Tu do PDF | **Resolvido** | `referencias.bib:119` usa vírgula em “Dissertação (Mestrado), University...”; PDF p.15 também. Extração integral do PDF: zero U+2014. Há outros tipos de traço tipográfico, que não são o caractere específico apontado em B. |
| Origem: dois ensaios; 106 dos 112 que recusaram | **Resolvido** no artigo e README | `introducao.tex:7`, `metodos.tex:10`, `README.md:36–37`; PDF pp.1–2,5. Conferido contra `privado/Dickson1989.txt:67–85,257–265`: dois ensaios separados por estágio, 112 recusas, seis perdas precoces, 106 analisados. O notebook não repete toda essa história, mas sua descrição operacional não a contradiz. O singular residual “desse ensaio” em `introducao.tex:7` pode ser ajustado editorialmente. Isso é distinto da proveniência do arquivo executado (C-03). |

## Achados

### C-01  GLOBE: total confundido com amostra de derivação
- Gravidade: importante
- Evidência: `artigo/secoes/relacionados.tex:8`, “GLOBE foi derivado em 4.119 pacientes”; PDF p.3. [Fonte institucional de Lammers](https://pure.eur.nl/en/publications/development-and-validation-of-a-scoring-system-to-predict-outcome/), resumo.
- Problema: 4.119 é o total, dividido em 2.488 de derivação e 1.631 de validação. Oito países e C=0,82 conferem; o erro altera a descrição do desenho do comparador clínico.
- Sugestão: informar os três tamanhos e associar C=0,82 à validação. A tabela em `relacionados.tex:25` pode explicitar a divisão.

### C-02  Incompatibilidade do UK-PBC com linha de base está categórica demais
- Gravidade: importante
- Evidência: `artigo/secoes/relacionados.tex:8`, “o que os torna incompatíveis com uma predição feita na linha de base”; :26 resume somente após um ano. [Carbone, texto integral](https://pmc.ncbi.nlm.nih.gov/articles/PMC6984963/), resumo e discussão.
- Problema: o modelo principal usa exames aos 12 meses, mas também albumina/plaquetas basais; a publicação avalia pacientes não tratados e discute previsão anterior ao tratamento, com cautela pela amostra pequena. A distinção entre tarefas é pertinente, porém a exclusão absoluta de uso basal omite essa análise.
- Sugestão: dizer que a derivação principal e o contexto de uso diferem do presente estudo, descrevendo a análise em não tratados e sua limitação. Não sugerir que o UK-PBC já esteja validado para esta tarefa binária específica.

### C-03  Artigo não identifica o snapshot efetivamente executado
- Gravidade: importante
- Evidência: `artigo/secoes/metodos.tex:10,44,66` identifica dados/fluxo/figura como UCI 878; :108 menciona checksum sem nomear a cópia. `README.md:65` declara Rdatasets; notebook células 5,8,19–20 usa `data/pbc_rdatasets.csv` por padrão.
- Problema: o artigo permite entender que o experimento baixou diretamente o UCI. Coorte e contagens coincidentes não demonstram igualdade de todos os valores, convenções e ausências entre distribuições. O README já fornece a distinção necessária, mas ela falta ao artigo.
- Sugestão: declarar snapshot de `survival::pbc` via Rdatasets, caminho/checksum e recodificações; citar UCI como distribuição relacionada. Se quiser afirmar identidade integral, apresentar comparação verificável entre as versões. Não é necessário retreinar para corrigir a identificação.

### C-04  Limpeza da bibliografia incompleta
- Gravidade: menor
- Evidência: `artigo/referencias.bib:122–123` contém dois fechamentos consecutivos após Tu; :55 traz “1804--1812”. [PubMed de Lammers](https://pubmed.ncbi.nlm.nih.gov/26261009/) registra 1804–1812.e4.
- Problema: há chave solta fora da entrada, embora o PDF entregue resolva as citações; não se verificou se o processador a ignora ou gera aviso. A paginação de Lammers omite o sufixo eletrônico. Não há entradas sem citação.
- Sugestão: remover somente a chave excedente, completar paginação e depois conferir o processamento BibTeX e o PDF. Preservar a distinção entre número de artigo e páginas nos demais registros.

### C-05  Relato amostral e de incerteza ainda parcial
- Gravidade: importante
- Evidência: `artigo/secoes/metodos.tex:5,59,72,105`; `resultados.tex:38–61,126,131` (“nenhum intervalo de confiança foi calculado” na quase externa); `discussao.tex:12`.
- Problema: n e eventos são claros, mas não há justificativa explícita da determinação do tamanho amostral. Só diferenças de AUROC recebem ICs; desempenho absoluto, calibração e teste quase externo não têm intervalos. Desvios entre folds e aviso de análise descritiva são úteis, mas não equivalem a estimativas de precisão. A alegação de relato “segundo TRIPOD+AI” não deve ser lida como conformidade integral.
- Sugestão: explicar que o tamanho deriva da base disponível e da seleção predefinida, sem cálculo de suficiência; relatar a precisão das estimativas quando disponível, deixando claro o procedimento e suas limitações. Se novas análises não forem feitas, declarar os itens não atendidos e restringir a alegação de conformidade. Nenhum treinamento foi solicitado por este achado.

### C-06  Base da declaração de dispensa ética não está identificada
- Gravidade: menor
- Evidência: `artigo/secoes/metodos.tex:108`, “públicos, anonimizados e licenciados ... o que dispensa aprovação ética”.
- Problema: há seção ética, mas o texto não identifica se a conclusão é enquadramento do autor, orientação institucional ou manifestação de comitê. Licença de reúso, anonimização e aprovação ética são informações distintas; a frase não documenta a origem da dispensa. Não foi feita consulta normativa externa, em respeito ao escopo.
- Sugestão: indicar a base institucional/documental aplicável, se existente, e declarar com precisão se houve ou não submissão/apreciação. Não inventar número de parecer nem apresentar uma dispensa formal que não ocorreu.

### C-07  Verificação integral das fontes e de algumas atribuições permanece pendente
- Gravidade: importante
- Evidência: `artigo/referencias.bib:2–3`, “Todas ... conferidas na fonte original”; `relacionados.tex:10,12,29,39`; `metodos.tex:34`; `introducao.tex:9`.
- Problema: a matriz desta passada encontrou confirmações, divergências e limites de acesso. Não se conseguiu conferir o fluxograma e a crítica metodológica integral a Shakir, a ausência de comparação em Gerussi, nem suporte específico de Christodoulou ao balanceamento. O qualificativo “mais difundido” não vem acompanhado de levantamento de frequência. Esses pontos não foram demonstrados falsos; também não recebem confirmação por repetição no artigo ou no relatório B. A afirmação do comentário bibliográfico pode refletir trabalho prévio do autor, mas não há registro local detalhado que permita auditá-lo nesses pontos.
- Sugestão: registrar página/figura e fonte consultada para cada atribuição; obter confirmação direta dos pontos pendentes ou reduzir a redação ao que foi efetivamente verificado. Para balanceamento, usar fonte específica ou justificativa explicitada como do próprio estudo. Substituir “mais difundido” por descrição identificável do enquadramento Kaggle, caso não haja evidência de frequência. Atualizar o comentário do .bib para refletir o alcance real da conferência.

## Tabela-resumo e veredito

| Achado | Gravidade | Síntese |
|---|---|---|
| C-01 | importante | GLOBE: corrigir derivação 2.488 e validação 1.631. |
| C-02 | importante | Qualificar incompatibilidade temporal do UK-PBC. |
| C-03 | importante | Identificar Rdatasets como cópia executada no artigo. |
| C-04 | menor | Chave excedente e paginação bibliográfica. |
| C-05 | importante | Determinação do n e incerteza de desempenho incompletas. |
| C-06 | menor | Documentar a base da declaração ética. |
| C-07 | importante | Completar ou limitar atribuições ainda não verificadas. |

**Veredito: aprovado com ressalvas.** Os componentes exigidos pela disciplina estão presentes, o badge e a preparação inicial do notebook atendem à inspeção estática, e B-01 a B-06 e a precisão histórica solicitada foram resolvidos no alcance descrito. Permanecem cinco achados importantes e dois menores de referências, proveniência e completude de relato; nenhum bloqueante de ausência de entrega foi identificado. A aprovação não certifica execução no Colab, compilação limpa nem conformidade integral com TRIPOD+AI. As ressalvas devem ser tratadas antes de apresentar as referências como inteiramente conferidas ou o relato como integralmente conforme.

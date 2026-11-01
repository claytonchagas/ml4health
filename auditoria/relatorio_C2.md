# Auditoria independente: Passada C2, fechamento

Data: 01/11/2026. Veredito: **aprovado com ressalvas**.

## Escopo e procedimento

Reauditoria limitada às correções C-01 a C-07, aos novos números e referências, às verificações bibliográficas pendentes e à forma final. Foram lidos `AUDITORIA.md`, `auditoria/relatorio_C.md`, `README.md`, `artigo/main.tex`, todas as seções e a bibliografia, além do texto integral extraído do PDF de 16 páginas. Consultaram-se os dois artefatos e scripts indicados no pedido. As linhas abaixo correspondem ao estado atual dos arquivos.

Somente este relatório foi escrito. Não houve leitura ou busca de arquivos fora do repositório, treinamento, instalação, compilação ou download de dados pelo comparador UCI. A web foi usada exclusivamente para referências (itens 2 e 3). Não se reexecutou `ic_desempenho.py`: a conferência numérica foi feita contra o CSV existente e a inspeção de seu procedimento, sem certificar sua regeneração nesta passada. Não se repetiram as auditorias metodológicas anteriores.

## 1. Fechamento dos achados C

| Item | Classificação | Evidência e resultado |
|---|---|---|
| C-01 | **Resolvido** | `artigo/secoes/relacionados.tex:8,25`: total 4.119, derivação 2.488, validação 1.631 e C=0,82 na validação. Corrige precisamente a confusão identificada em C. |
| C-02 | **Resolvido** | `artigo/secoes/relacionados.tex:8,26`: distingue exames aos 12 meses de albumina/plaquetas basais, abandona a incompatibilidade absoluta e menciona avaliação em não tratados com amostra pequena. |
| C-03 | **Resolvido**, no alcance do registro local | `artigo/secoes/metodos.tex:10,108` identifica R/Rdatasets, cópia versionada e checksum; `README.md:65` faz a mesma distinção. `auditoria/comparacao_uci_rdatasets.txt:4,7–27` registra 418 IDs iguais, nenhuma divergência de valores/ausências e diferença máxima de idade de 7,11e-15 ano. A designação UCI no fluxograma (`metodos.tex:44`) fica contextualizada pelo texto. A igualdade é operacional após recodificação, não identidade dos arquivos brutos; ver abaixo. |
| C-04 | **Resolvido** | `artigo/referencias.bib:55` traz `1804--1812.e4`; a entrada Tu termina uma única vez em `:122`, seguida da próxima entrada em `:124`. Não há chave solta nesse ponto; o saldo de chaves do arquivo é zero. Citações e bibliografia do PDF estão resolvidas na inspeção descrita na seção 4. |
| C-05 | **Parcialmente resolvido** | `artigo/secoes/metodos.tex:59` declara tamanho determinado pelos dados disponíveis, sem cálculo prévio; `:105` acrescenta ICs absolutos condicionais e `resultados.tex:64` os relata corretamente. Entretanto, continuam sem IC os resultados no limiar (`resultados.tex:128`) e quase externos (`:133`; `README.md:203`). A ressalva sobre conformidade foi atendida em `metodos.tex:5`, que declara ausência de verificação formal de todos os itens TRIPOD+AI. Não se exige retreino para fechar essa limitação de relato. |
| C-06 | **Parcialmente resolvido** | `artigo/secoes/metodos.tex:108` agora declara que não houve submissão e atribui o enquadramento ao autor, com artigo/inciso da norma. Resolve a ambiguidade sobre dispensa formal, mas a aplicabilidade da base escolhida ainda não está demonstrada (C2-01). |
| C-07 | **Parcialmente resolvido** | `introducao.tex:9` e `relacionados.tex:39` retiram a generalização “mais difundido”; `relacionados.tex:10,27` restringe Gerussi ao foco/objetivo; `metodos.tex:34` troca a referência ao balanceamento por fonte específica. A nova fonte exige delimitação (C2-02), e algumas verificações continuam incompletas (C2-03). O comentário em `referencias.bib:2–3` remete ao relatório C, que explicitamente contém pendências, sem registrar seu fechamento. |

### Conferência dos novos intervalos

Os valores efetivamente impressos em `artigo/secoes/resultados.tex:64` e `README.md:158` conferem com o arredondamento do CSV. O parágrafo aparece no PDF nas páginas 9–10. Não se deve comparar diretamente esses pontos OOF com a média das 25 partições: o artigo explica a distinção na mesma linha 64.

| Estimativa OOF | Ponto e IC 95% no CSV, arredondados como no artigo | Evidência |
|---|---|---|
| AUROC, RL 5 variáveis | 0,904 [0,864; 0,937] | `resultados/ic_desempenho_oof.csv:4` |
| CITL, Mayo original | 0,34 [0,06; 0,59] | CSV `:2` |
| Inclinação, RL penalizada 17 | 1,46 [1,19; 1,86] | CSV `:5` |
| Inclinação, RF 17 | 1,41 [1,14; 1,82] | CSV `:7` |
| Inclinação, RF 17 com pré-processamento da RL | 1,35 [1,09; 1,74] | CSV `:10` |
| Inclinação, Mayo original | 1,41 [1,10; 1,88] | CSV `:2` |
| Inclinação, RL 5 | 0,91 [0,72; 1,19] | CSV `:4` |

Também confere a largura aproximada de 0,06–0,08 dos ICs de AUROC dos demais modelos (`CSV:2–3,5–11`; larguras aproximadamente 0,064–0,078). O CITL de Mayo exclui 0, e as quatro inclinações destacadas excluem 1. O README menciona um subconjunto verdadeiro desses resultados. “Dois achados” no artigo significa dois tipos de desvio (CITL e inclinação), não apenas dois modelos.

`ic_desempenho.py:19,24–41` usa 2.000 reamostragens de pacientes, os mesmos índices para todos os modelos, pontos nas predições OOF médias e quantis 0,025/0,975. Verifica alinhamento dos índices em `:28`. O CSV é gravado em `:43`, razão para não executar o script diretamente nesta auditoria. A descrição condicional em `metodos.tex:105` e `README.md:158` é coerente com o procedimento inspecionado. Não inclui a incerteza de repetir ajuste/seleção.

### Conferência da comparação UCI

As afirmações em `metodos.tex:10` e `README.md:65` correspondem à saída arquivada (`auditoria/comparacao_uci_rdatasets.txt:4,7–27`). O script alinha por ID e ordena (`auditoria/comparar_uci_rdatasets.py:33–38`), compara as entradas recodificadas mais `Status` e `N_Days` (`:34–36`), verifica ausências e usa tolerâncias de 0,01 ano para idade e 1e-9 para os demais números (`:58–70`). Na saída efetiva, a diferença máxima de idade é desprezível e as demais diferenças numéricas são zero. Isso sustenta coincidência das variáveis usadas, não comprova identidade binária dos downloads nem constitui nova consulta independente ao UCI nesta passada.

## 2. Referências novas: metadados e sustentação

Consulta em 01/11/2026. “Confere” abaixo se refere ao aspecto explicitamente indicado, sem converter acesso parcial em verificação integral.

| Referência e evidência local | URL consultada | Resultado |
|---|---|---|
| van den Goorbergh et al.; `artigo/referencias.bib:135–145`; citação em `metodos.tex:34` e menção em `README.md:61` | [PubMed 35686364](https://pubmed.ncbi.nlm.nih.gov/35686364/); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9382395/) | **Metadados conferem**: Ruben van den Goorbergh, Maarten van Smeden, Dirk Timmerman e Ben Van Calster; título cadastrado; JAMIA, 2022, 29(9):1525–1534; DOI 10.1093/jamia/ocac093. O resumo primário confirma pior calibração e ausência de ganho de AUROC com subamostragem, sobreamostragem e SMOTE em regressão logística convencional/ridge. **Sustentação parcial** da frase irrestrita sobre correções de desbalanceamento: o experimento da fonte não estabelece essa regra para qualquer algoritmo (C2-02). PMC retornou barreira de navegador; a confirmação usa o resumo disponível no PubMed. |
| Resolução CNS nº 510/2016; `artigo/referencias.bib:272–277`; citação em `metodos.tex:108` | [Ministério da Saúde, texto da resolução](https://bvsms.saude.gov.br/bvs/saudelegis/cns/2016/res0510_07_04_2016.html); [antigo endereço CNS](https://conselho.saude.gov.br/resolucoes/2016/Reso510.pdf) | **Metadados conferem**: CNS, nº 510, 7/4/2016, normas para pesquisas em Ciências Humanas e Sociais. O art. 1º, parágrafo único, III, efetivamente exclui de registro/avaliação pesquisas com informações de domínio público. **Sustentação parcial**: a norma confirma o teor do inciso, mas não demonstra, por si, que este estudo clínico retrospectivo e a base CC BY se enquadram nele. O endereço antigo redirecionou à página geral; o texto foi obtido na BVS (C2-01). |

## 3. Nova tentativa das pendências bibliográficas C

### Pontos prioritários

| Ponto e evidência local | URL consultada e localização na fonte | Resultado |
|---|---|---|
| Shakir: remoção de `N_Days`; `relacionados.tex:12` | [Reprodução do artigo no ResearchGate](https://www.researchgate.net/publication/394892047_Leveraging_Machine_Learning_for_Early_Risk_Prediction_in_Cirrhosis_Outcome_Patients), seção 2.2.1, p.24 | **Confere**: exclusão expressa dessa coluna. |
| Shakir: três classes; `relacionados.tex:12,29` | Mesma URL, Tabela 1, p.24; seção 3.3, p.27 | **Confere**: C, CL e D. |
| Shakir: Kaggle/sintéticos; `relacionados.tex:12,29`; `discussao.tex:6` | Mesma URL, seção 2.1, p.23, referência 13, p.30; [Kaggle, dados](https://www.kaggle.com/competitions/playground-series-s3e26/data) | **Confere**: fonte é PS3E26; natureza sintética é confirmada pela documentação Kaggle, não apenas inferida do artigo. |
| Shakir: posição do balanceamento; `relacionados.tex:12,29` | Mesma reprodução, descrição da Figura 1, p.23, seções 2.2.3 e 2.4, pp.24–25 | **Confere na sequência textual**: balanceamento precede divisão. A imagem do fluxograma não foi recuperada para inspeção visual; essa parte estritamente gráfica continua sem verificação. |
| Shakir: ausência de calibração; `relacionados.tex:12,29` | Mesma reprodução, avaliação/resultados, pp.26–29 | **Confere no relato consultado**: métricas e resultados não apresentam avaliação de calibração; não certifica código não publicado. |
| Beuers: justificativa da mudança de nome; `introducao.tex:5` | [PDF institucional Amsterdam UMC](https://pure.amsterdamumc.nl/ws/portalfiles/portal/160708336/Changing-nomenclature-for-pbc-from-cirrhosis-to-cholangitis.pdf), pp.1671–1672 (páginas 2–3 do arquivo); [versão conjunta em PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4679751/) | **Confere no sentido clínico**: texto liga a mudança ao diagnóstico precoce, à inadequação de “cirrose” e ao fato de apenas uma minoria vir a desenvolver cirrose; também aborda estigma e manutenção da sigla. É sustentação qualitativa, não estimativa formal da proporção no diagnóstico. O PDF acessível é a publicação conjunta em Gut, DOI 10.1136/gutjnl-2015-310593, não a paginação Hepatology cadastrada; não há motivo para substituir o DOI do .bib. A nota editorial da versão conjunta confirma publicação em múltiplos periódicos. |
| Kaggle: presença de `N_Days`; `introducao.tex:9`; `metodos.tex:72` | [Página oficial de dados](https://www.kaggle.com/competitions/playground-series-s3e26/data) | **Confere sua presença na descrição da tarefa**: os três estados são definidos em relação a `N_Days`. **Continua sem verificação direta do cabeçalho dos CSVs**: o explorador exige autenticação/aceite de regras. A descrição não foi tratada como inspeção do arquivo de treino. |
| Kaggle: origem sintética; `relacionados.tex:12` | Mesma página oficial, “Dataset Description” | **Confere**: treino e teste gerados por modelo de aprendizado profundo treinado no conjunto Cirrhosis Patient Survival Prediction; distribuições próximas, sem identidade com o original. |
| Gerussi: objetivo declarado; `relacionados.tex:10,27` | [Pôster dos autores, EASL 2021](https://www.postersessiononline.eu/173580348_eu/congresos/ILC2021/aula/-PO_376_ILC2021.pdf), bloco 2, “Aim”; [registro institucional do artigo](https://boa.unimib.it/handle/10281/363246); [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/liv.15141); [PubMed](https://pubmed.ncbi.nlm.nih.gov/34951722/) | **Confere o objetivo de subfenotipagem/estratificação**, declarado pelos autores no pôster do mesmo estudo, com os mesmos tamanhos de coorte. A redação atual evita a antiga afirmação absoluta de ausência de comparação em todo o artigo. **Continua sem verificação integral do corpo da versão final**: Wiley deu timeout, PubMed retornou conteúdo incompleto e o registro institucional indica texto reservado (abertura direta: 403). Isso limita a confirmação ao foco declarado, não a uma prova de ausência de análises adicionais. |

Os downloads oficiais de Shakir em [página do periódico](https://journal.irpi.or.id/index.php/predatecs/article/view/2015), [PDF original](https://journal.irpi.or.id/index.php/predatecs/article/download/2015/1052/11445) e [PDF alternativo com www](https://www.journal.irpi.or.id/index.php/predatecs/article/download/2015/1052) voltaram a dar timeout. O texto reproduzido permitiu avançar além do resumo; sua identificação coincide com os metadados oficiais indexados. Não foi possível verificar visualmente a Figura 1 nem comparar os bytes dessa reprodução com o PDF oficial.

### Outras verificações incompletas assinaladas em C

| Pendência | URL consultada | Resultado nesta tentativa |
|---|---|---|
| Data de disponibilização UCI | [UCI 878](https://archive.ics.uci.edu/dataset/878/cirrhosis+patient+survival+prediction+dataset-1) | **Confere 2023**, conforme cabeçalho “Donated on 9/11/2023”; sustenta a nota de `referencias.bib:23`. Não se reinterpretou o formato de dia/mês para inferir uma data mais específica. |
| van Buuren: páginas 1–67 | [Exportação de citação do próprio JSS](https://www.jstatsoft.org/citationstylelanguage/get/associacao-brasileira-de-normas-tecnicas?publicationId=1945&submissionId=1946) | **Confere**, volume 45, número 3, páginas 1–67; fecha a pendência de `referencias.bib:245`. |
| Fleming/Harrington: apêndice e local editorial | [Wiley, livro](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118150672) | **Confere a existência do Apêndice D, Data, pp.359–383**. **Continuam sem verificação** seu conteúdo específico sobre PBC e o local New York (`referencias.bib:32`): não ficaram disponíveis no texto consultado. Isso não contradiz os dados históricos já verificados em C por outra fonte. |
| Breiman: fascículo 1 | [Springer, artigo](https://link.springer.com/article/10.1023/A:1010933404324) | **Continua sem verificação** do fascículo de `referencias.bib:222`: página informa volume 45, páginas e outubro/2001, mas não exibe o número no conteúdo acessível. Demais metadados permanecem coerentes. |
| Christodoulou e balanceamento | [Fonte substituta, PubMed 35686364](https://pubmed.ncbi.nlm.nih.gov/35686364/) | A atribuição pendente foi **retirada** de `metodos.tex:34`; não é necessário provar que Christodoulou sustentava a frase antiga. A substituição oferece evidência específica, com a limitação registrada em C2-02. |

Nenhuma atribuição foi classificada como falsa apenas por falha de acesso. Não foi encontrada divergência numérica nova nos itens prioritários; os limites remanescentes estão discriminados, sem aprovação integral presumida.

## 4. Forma do PDF e da bibliografia

- **Travessão U+2014:** zero ocorrências na extração integral `pdftotext -layout artigo/main.pdf -`. Há outros traços tipográficos, distintos do caractere solicitado. Resultado conforme no texto extraível do PDF.
- **Citações:** 25 chaves distintas citadas nos fontes incluídos por `artigo/main.tex:80–86`, todas existentes nas 25 entradas de `artigo/referencias.bib:6–277`. Inspeção do texto do PDF, incluindo referências nas pp.14–16, não encontrou citações pendentes nem `??`.
- **Entradas sem citação:** zero; a diferença de conjuntos entre chaves do .bib e citações é vazia em ambos os sentidos. A chave nova de balanceamento é usada em `metodos.tex:34`; a norma, em `:108`.
- Não foram encontrados logs/auxiliares LaTeX arquivados na pasta do artigo pela busca restrita a essas extensões. Não houve compilação; portanto, não se certifica processamento sem avisos do fonte atual. O PDF entregue contém as alterações examinadas, inclusive os novos ICs e as novas referências.

## Achados C2

### C2-01  Base normativa citada não demonstra o enquadramento do estudo
- Gravidade: importante
- Evidência: `artigo/secoes/metodos.tex:108`, “na avaliação do autor ... inciso III”; `artigo/referencias.bib:272–277`. [Resolução, art. 1º e parágrafo único](https://bvsms.saude.gov.br/bvs/saudelegis/cns/2016/res0510_07_04_2016.html).
- Problema: o inciso foi transcrito corretamente e a ausência de submissão está transparente, mas o caput delimita pesquisas em Ciências Humanas e Sociais. O artigo não explica sua aplicabilidade à presente análise de predição clínica nem demonstra a passagem de dados públicos licenciados CC BY para a categoria normativa de domínio público. Isso não demonstra obrigatoriedade de submissão; demonstra insuficiência da justificativa.
- Sugestão: explicitar a base aplicável a esta modalidade de análise e a razão do enquadramento, com documento pertinente quando disponível. Preservar a distinção entre avaliação do autor e manifestação formal de comitê; não inventar parecer ou dispensa.

### C2-02  Fonte de balanceamento é generalizada além dos modelos estudados
- Gravidade: menor
- Evidência: `artigo/secoes/metodos.tex:34` e `README.md:61`, “correções de desbalanceamento pioram ... sem melhorar”; referência em `artigo/referencias.bib:135–145`. [Resumo primário de van den Goorbergh](https://pubmed.ncbi.nlm.nih.gov/35686364/).
- Problema: a nova referência é correta e pertinente à decisão de preservar as probabilidades, mas investiga regressão logística convencional/ridge com três estratégias de reamostragem. A redação apresenta uma regra geral, em contexto que inclui árvores e boosting, sem delimitar o alcance empírico da fonte.
- Sugestão: dizer que essas correções podem prejudicar a calibração e que, nos cenários de regressão logística investigados pela fonte, não houve ganho de discriminação. Apresentar a decisão de não balancear como escolha deste estudo, sem universalizar o resultado.

### C2-03  Registro de conferência bibliográfica ainda não fecha todas as pendências
- Gravidade: menor
- Evidência: `artigo/referencias.bib:2–3`, “Metadados conferidos na fonte; resultado ... relatorio_C.md”; `artigo/secoes/relacionados.tex:12,29`, atribuição à posição no fluxograma. URLs, localizações e limites registrados na seção 3 deste relatório.
- Problema: houve avanço substancial, mas a figura original de Shakir e os cabeçalhos Kaggle não foram inspecionados diretamente; persistem pequenas lacunas de metadados e acesso integral. A sequência textual de Shakir sustenta a preocupação metodológica, mas não equivale à inspeção visual pedida. O comentário bibliográfico remete ao relatório anterior sem discriminar o fechamento parcial.
- Sugestão: registrar no repositório a fonte/página consultada e os limites efetivos da conferência; para a figura, obter inspeção direta ou atribuir explicitamente a ordem à descrição textual do procedimento. Não declarar verificação integral enquanto persistirem essas lacunas.

## Tabela-resumo e veredito

| Achado | Gravidade | Situação de fechamento |
|---|---|---|
| C2-01 | importante | C-06 parcial: transparência corrigida; adequação da base normativa ainda não demonstrada. |
| C2-02 | menor | C-07 parcial: referência pertinente, mas frase precisa delimitar seu alcance. |
| C2-03 | menor | C-07 parcial: várias pendências confirmadas, outras explicitamente sem verificação. |

**Veredito: aprovado com ressalvas.** C-01 a C-04 estão resolvidos; C-05, C-06 e C-07 estão parcialmente resolvidos. Os novos números conferem com os artefatos indicados, e os requisitos de forma examinados foram atendidos. A incerteza quase externa permanece uma limitação declarada, com a alegação TRIPOD+AI agora restringida. Não há achado bloqueante novo; as ressalvas concentram-se na fundamentação normativa, no alcance da referência de balanceamento e nas verificações bibliográficas explicitamente incompletas. Este fechamento não certifica nova execução, compilação limpa ou conferência integral de todas as fontes.

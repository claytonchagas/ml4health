# Relatório C3: conformidade, referências e correções da B3

Auditoria independente em 02/11/2026, ramo `sbcas-2027`, HEAD `b243a74`. **Veredito: aprovado com ressalvas.** A redação corrigiu a maior parte dos problemas científicos da B3. Persistem uma atribuição excessivamente específica ao protocolo de Graf, atualização bibliográfica pendente, lacunas de relato e duas verificações operacionais inconclusivas: compilação limpa e anonimização do destino do repositório.

## Escopo e limites

Foram lidos `AUDITORIA.md`, `auditoria/relatorio_B3.md`, `sbcas/PLANO_ANALISE.md`, `sbcas/DESVIOS.md`, `sbcas/notas_literatura.md`, o `.tex`, os cinco arquivos de tabelas, as 28 entradas bibliográficas e o texto integral extraído das 12 páginas de `sbcas/artigo/main.pdf`. Consultaram-se também o texto de Dickson em `privado/Dickson1989.txt`, resultados salvos, o estilo SBC local e registros anteriores do repositório. As linhas citadas correspondem ao estado atual, não à numeração antiga da B3. Neste relatório, `main.tex`, `referencias.bib` e `tabelas/` são relativos a `sbcas/artigo/`.

Não houve retreino, reexecução da análise, geração de tabelas ou reprodução de bootstrap. Conferência de fontes numéricas significa leitura dos resultados existentes. A web foi usada apenas para referências e regras de submissão, inclusive a tentativa de conferir o link anonimizado. Nenhuma busca documental foi feita fora do repositório. A compilação autorizada executou o TeX instalado, com seus componentes de sistema, e gravou sua saída exclusivamente em diretório temporário, removido ao final. Apenas este relatório foi criado no repositório.

Nos quadros bibliográficos, **M** significa metadados e **S**, sustentação da citação. Foram comparados autores declarados, ano, título, veículo, volume, número e páginas quando aplicáveis. Omissão de volume/número/páginas de livro, conjunto de dados, competição e preprint não foi tratada como erro. Autores abreviados por `others` foram comparados pelos nomes explicitados; isso não certifica uma lista completa que o `.bib` não fornece. Resultado de busca indexado na própria fonte é distinguido de leitura integral. Bloqueios de acesso não são evidência de erro ou inexistência.

## 1. Situação de B3-01 a B3-12

| Achado anterior | Classificação | Evidência e avaliação atual |
|---|---|---|
| B3-01 | **Resolvido** | `main.tex:96` usa macros; `tabelas/numeros.tex:25–27` fornece 0,017, 0,018 e 0,0012. Compatíveis com `resultados_sbcas/valor_incremental.csv:2,4,6` e `resumo_cv.csv:6–7`. O texto agora compara expressamente médias do escore nativo. |
| B3-02 | **Resolvido** | `main.tex:31,35,175,183,188` explicita intervalos condicionais e resultado limítrofe da RSF17; `:96` preserva 0,0197 versus 0,0209. A estabilidade é atribuída à ausência de ganho demonstrado. A afirmação sobre o subgrupo ainda pede leitura estritamente descritiva, como ressalva `:135`. |
| B3-03 | **Resolvido** | `main.tex:77` informa a exceção binomial; `:117` distingue O/E global, padrões locais e IC, inclui Cox17 e aponta o suplementar. Os números 0,012–0,109, 0,712–0,888, 0,054, 0,171 e 0,748 são compatíveis com `resultados_sbcas/calibracao_quintis_ic.csv:2,7–8,11,21`. O limite binomial continua uma aproximação sob censura, agora identificada, e não se torna IC exato de KM. |
| B3-04 | **Resolvido** | `main.tex:77,117,129` define decisão hipotética, 46 limiares, escala de 1,5 por 100, ausência de equivalência demonstrada e possibilidade de otimismo por seleção. Não promete direção garantida do viés. |
| B3-05 | **Resolvido** | `main.tex:85` distingue ajuste integral em lifelines, empates Efron e imputação antes do log; `:137` distingue não detecção de comprovação; legenda `:141` identifica o ajuste descritivo. Formas funcionais e influência aparecem como não examinadas. |
| B3-06 | **Resolvido** | `main.tex:65,67,71` distingue 106 de 112 recusantes, último acompanhamento, Cox reestimado e censura por transplante no original. Dickson local: linhas 257–271, além das cinco variáveis em 21–28. Não se identificou nova contradição histórica. |
| B3-07 | **Resolvido** | `main.tex:47,71` restringe a igualdade às duas florestas e declara 50 configurações por RSF, 40 para Cox17 e nenhuma busca para Cox5. |
| B3-08 | **Resolvido** | `main.tex:85,155,159` identifica os comparadores, a diferença com/sem `N_Days`, o caráter descritivo, as escalas distintas e os níveis Bonferroni 99%/98,3%. A linha (d) em `tabelas/enquadramentos.tex:4` foi corrigida. |
| B3-09 | **Parcialmente resolvido** | `main.tex:45,54,179` qualifica o contraste e a sobreposição dos IC. Bootstrap .632+, números e seleção por AIC têm suporte primário. Contudo, as sete variáveis do diagnóstico não podem ser automaticamente atribuídas ao modelo que gerou o C de 0,776; e existe publicação final de 2026. Ver C3-01 e C3-02. |
| B3-10 | **Parcialmente resolvido** | `sbcas/DESVIOS.md:16` acrescenta D10; `main.tex:77,81,89` identifica G marginal, alcance dos IC do subgrupo e importância restrita. Permanece em `:89` a generalização de que os demais detalhes foram fixados antes dos resultados finais, que não documenta adequadamente a complementação posterior D10. Ver C3-07. |
| B3-11 | **Resolvido** | `referencias.bib:46` restaurou 1804–1812.e4, confirmado pela [fonte PubMed](https://pubmed.ncbi.nlm.nih.gov/26261009/). |
| B3-12 | **Parcialmente resolvido** | `main.tex:67,77,85,137` explica variáveis adicionais, biópsia, métricas, censura, decisão hipotética e distinção entre importância preditiva e eficácia. Melhorou substancialmente, mas ainda faltam unidades/codificações e ausências por variável em quadro compacto ou suplemento explicitamente indicado; ver C3-08. |

**Balanço: nove resolvidos, três parcialmente resolvidos, nenhum integralmente não resolvido.** Não encontrei novo número próprio divergente introduzido pelas correções examinadas. As pendências novas ou residuais são de atribuição documental, alcance e certificação, discriminadas abaixo.

## 2. Conferência das 28 referências

Todas as 28 entradas são citadas; todas as chaves citadas existem. Nas linhas a seguir, a indicação de título conferente refere-se ao título transcrito na entrada identificada.

| Entrada e linhas do `.bib` | Fonte consultada e metadados | Sustentação da frase atual e resultado |
|---|---|---|
| `dickson1989prognosis`, 4–12 | [PubMed 2737595](https://pubmed.ncbi.nlm.nih.gov/2737595/) bloqueou com verificação de navegador; a fonte primária local `privado/Dickson1989.txt:5–10` confirma os cinco autores, título, *Hepatology* 10(1):1–7, 1989. | **Confere M/S** pela cópia primária: cinco variáveis, dois ensaios, 312 e validação nos 106 (`:21–28,67–90,257–271`). Logs e tratamento histórico do transplante são compatíveis com a descrição em `main.tex:41,65,71`. Não se copiou texto extenso. |
| `uci878`, 14–19 | [UCI 878](https://archive.ics.uci.edu/dataset/878/cirrhosis+patient+survival+prediction+dataset-1): os cinco autores, título e DOI 10.24432/C5R02G conferem; a **citação recomendada usa 1989**, não 2023. | **Diverge M** no ano recomendado. Corrigir para 1989 e identificar `[Dataset]`; 2023 pode ser explicitado separadamente como disponibilização no portal. S confere para identificação, medidas, licença CC BY 4.0 e composição geral em `main.tex:43,65`. A identidade SHA-256 é afirmação sobre a cópia local, não algo demonstrado pela página web nesta passada. |
| `fleming1991counting`, 21–27 | [Wiley](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118150672) confirma autores, título e editora; sua data eletrônica não substitui a edição de 1991. [Catálogo institucional CiNii/NII](https://ci.nii.ac.jp/ncid/BA12189870?l=en) confirma **Wiley, 1991, New York, N.Y.** | **Confere M**, inclusive cidade. **S parcialmente verificável**: pertinência como obra clássica de sobrevivência confere; não foi aberto integralmente seu apêndice para atribuir a ele cada detalhe de recrutamento de `main.tex:65`. Esses detalhes têm corroboração independente em Dickson local. |
| `beuers2015nomenclature`, 29–37 | [PubMed 26372460](https://pubmed.ncbi.nlm.nih.gov/26372460/): Beuers, Gershwin, Gish et al.; título confere; *Hepatology* 62(5):1620–1622, 2015. | **Confere M/S** para mudança de nomenclatura em 2015 (`main.tex:41`). Não confundir com as publicações conjuntas em outros periódicos. |
| `lammers2015globe`, 39–47 | [PubMed 26261009](https://pubmed.ncbi.nlm.nih.gov/26261009/): Lammers, Hirschfield, Corpechot et al.; título confere; *Gastroenterology* 149(7):1804–1812.e4, 2015. | **Confere M/S** para GLOBE, Cox e exames após um ano de UDCA (`main.tex:53`). O composto do GLOBE inclui óbito ou transplante. |
| `carbone2016ukpbc`, 49–57 | [PubMed 26223498](https://pubmed.ncbi.nlm.nih.gov/26223498/): Carbone, Sharp, Flack et al.; título confere; *Hepatology* 63(3):930–950, **2016**, embora online em 2015. | **Confere M; S com ressalva** em `main.tex:53`: usa exames após tratamento e também variáveis basais. O desfecho é transplante ou morte relacionada ao fígado, não literalmente qualquer óbito. A formulação do artigo é aceitável como contexto, mas o plano `sbcas/PLANO_ANALISE.md:14` simplifica a identidade dos compostos. |
| `ishwaran2008rsf`, 59–67 | [Fonte do periódico/DOI](https://doi.org/10.1214/08-AOAS169): Ishwaran, Kogalur, Blackstone e Lauer; título confere; *Annals of Applied Statistics* 2(3):841–860, 2008. | **Confere M/S** para RSF com censura à direita em `main.tex:71`. Não implica que toda implementação ou todo orçamento de ajuste seja equivalente ao original. |
| `reade2023ps3e26`, 69–74 | [Kaggle, página da competição](https://www.kaggle.com/competitions/playground-series-s3e26): a versão indexada mostra citação recomendada de Walter Reade e Ashley Chow, título e ano 2023. A abertura inicial de `/overview` não forneceu texto; a página raiz indexada forneceu. | **Confere M/S** para competição multiclasse, três estados e dados sintéticos (`main.tex:43,45,57`). A tese de Tu também documenta o treinamento sintético a partir do original; não se baixaram CSVs da competição. |
| `shakir2025cirrhosis`, 76–84 | [PDF do próprio periódico](https://www.journal.irpi.or.id/index.php/predatecs/article/download/2015/1052), conteúdo indexado: Yasir Hussein Shakir, Eshaq Aziz Awadh AL Mandhari e Ali Alkhazraji; título confere; *Public Research Journal of Engineering, Data Technology and Computer Science* 3(1):22–30, 2025. Abertura direta repetidamente expirou. | **Confere M/S no conteúdo primário indexado**: p.23 enumera balanceamento antes de divisão; p.28 informa 90% para XGBoost e três classes. Sustenta `main.tex:57,179` como crítica ao protocolo descrito. Não se certificou visualmente o fluxograma nem ausência de calibração em todas as páginas pela abertura integral nesta passada. “Mandhari” pode ser normalizado para “AL Mandhari”, como na fonte. |
| `tu2025cirrhosis`, 86–91 | [Repositório UCLA](https://escholarship.org/uc/item/0d66m3m6) e [PDF institucional](https://escholarship.org/content/qt0d66m3m6/qt0d66m3m6_noSplash_ad8af2269f37db7bd78ab6ef175c0c40.pdf): Timothy Enoch Tu; título, UCLA, mestrado e 2025 conferem. | **Confere M/S**: acurácia 89% RF, classificação binária sem horizonte, treino sintético e teste nos 418 originais (cap.2 e §3.2.1), compatíveis com `main.tex:57,179`. A dependência entre fonte geradora e teste sustenta risco de contaminação, sem demonstrar quantitativamente quanto explica da acurácia. |
| `graf2025coxrsf`, 93–98 | [arXiv](https://arxiv.org/abs/2502.03119), [v2 integral](https://arxiv.org/pdf/2502.03119v2), [v1 HTML](https://arxiv.org/html/2502.03119v1), [PubMed final](https://pubmed.ncbi.nlm.nih.gov/42798169/): Graf, Todd, Baksh e título conferem. Existe versão publicada: **Biometrical Journal 68(5):e70171, 2026, DOI 10.1002/bimj.70171**. | **Diverge quanto à atualização do veículo; S parcial** em `main.tex:54`. Conferem 312, .632+, 1.000 bootstraps, 0,776/0,855 e respectivos IC, seis regras e ressalva da regra extratrees. A seleção retroativa por AIC está explícita na v1, §2.2. A lista de sete pertence ao diagnóstico de proporcionalidade, não prova a dimensão fixa do modelo avaliado. C3-01/02. |
| `christodoulou2019systematic`, 100–107 | [PubMed 30763612](https://pubmed.ncbi.nlm.nih.gov/?term=30763612): Christodoulou, Ma, Collins, Steyerberg, Verbakel e Van Calster; título confere; *Journal of Clinical Epidemiology* 110:12–22, 2019. | **Confere M/S** para 71 estudos e nenhuma vantagem demonstrada nas comparações de baixo risco de viés (`main.tex:43`). A revisão compara classificação binária/logística; `:175` é analogia contextual, não evidência direta sobre Cox/RSF. |
| `kapoor2023leakage`, 109–117 | [Texto primário no PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856/) e [cópia institucional NSF](https://par.nsf.gov/servlets/purl/10513990): Kapoor e Narayanan; título confere; *Patterns* 4(9):100804, 2023. | **Confere M/S** conceitual (`main.tex:45,179`). As constatações específicas sobre Shakir e Tu dependem das fontes desses autores, não de Kapoor. |
| `vancalster2019calibration`, 119–126 | [PubMed 31842878](https://pubmed.ncbi.nlm.nih.gov/31842878/): cinco autores nominais conferem; título confere; *BMC Medicine* **17(1):230**, 2019. Há também autoria coletiva STRATOS no registro. | **Confere M/S** para importância da calibração (`main.tex:57`), com incompletude bibliográfica menor: número 1 e grupo não constam da entrada. 230 é identificador, não intervalo de páginas. |
| `collins2024tripodai`, 128–135 | [BMJ original](https://www.bmj.com/content/385/bmj-2023-078378.abstract) e [PubMed original](https://pubmed.ncbi.nlm.nih.gov/38626948/): Collins, Moons, Dhiman, Riley, Beam et al.; título confere; *BMJ* 385:e078378, 2024. | **Confere M/S** para orientação de relato (`main.tex:61`), sem implicar adesão integral. Não substituir pelo erratum q902, que corrige afiliações. |
| `varma2006bias`, 137–144 | [PubMed 16504092](https://pubmed.ncbi.nlm.nih.gov/16504092/): Varma e Simon; título confere; *BMC Bioinformatics* 7:91, 2006. | **Confere M/S** para seleção interna/validação aninhada (`main.tex:75`). Não certifica por si só os IC condicionais deste artigo. |
| `cox1972regression`, 146–154 | [Sumário primário do fascículo](https://academic.oup.com/jrsssb/issue/34/2): D. R. Cox; título, ano e veículo histórico conferem; 34(2):**187–202**, seguido de discussão separada, 202–220. A abertura do DOI individual falhou no redirecionamento. | **Diverge na delimitação das páginas**: 187–220 é a convenção tradicional incluindo discussão; usar 187–202 para a entrada sem menção a discussão ou explicitar sua inclusão. S confere para o modelo em `main.tex:41`. C3-03. |
| `simon2011coxnet`, 156–164 | [JSS](https://www.jstatsoft.org/article/view/v039i05), DOI 10.18637/jss.v039.i05: Noah Simon, Jerome H. Friedman, Trevor Hastie, Rob Tibshirani; título confere; 39(5):1–13, 2011. | **Confere M/S** para Cox elastic net e descida coordenada (`main.tex:71`). A ausência do H. em Friedman é abreviação nominal menor, não troca de autor. |
| `uno2011cstat`, 166–174 | [PubMed 21484848](https://pubmed.ncbi.nlm.nih.gov/?term=21484848) e [manuscrito primário Wiley](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/sim.4154): Uno, Cai, Pencina, D'Agostino e Wei; título confere; *Statistics in Medicine* 30(10):1105–1117, 2011. | **Confere M/S** para concordância ponderada sob censura (`main.tex:77`), condicionada às hipóteses. A explicação didática do domínio do C exige ajuste: C3-06. |
| `uno2007auc`, 176–184 | [JASA/DOI](https://www.tandfonline.com/doi/abs/10.1198/016214507000000149): Uno, Cai, Tian e Wei; título confere; 102(478):527–537, 2007. A data de colocação online posterior não muda o ano do fascículo. | **Confere M/S** para avaliação de regras de risco em horizonte t com censura, pertinente à AUC cumulativa/dinâmica de `main.tex:77`; o texto disponível não certifica cada opção da implementação moderna. |
| `graf1999brier`, 186–194 | [PubMed 10474158](https://pubmed.ncbi.nlm.nih.gov/10474158/?dopt=Abstract): Graf, Schmoor, Sauerbrei e Schumacher; título confere; *Statistics in Medicine* 18(17–18):2529–2545, 1999. | **Confere M/S** para erro de previsão de probabilidades de sobrevivência sob censura (`main.tex:77`). A grade anual de cinco pontos é escolha deste estudo, declarada em `:183`, não exigência de Graf. |
| `harrell1982yield`, 196–204 | [PubMed 7069920](https://pubmed.ncbi.nlm.nih.gov/7069920/): **F. E. Harrell Jr**, Califf, Pryor, Lee e Rosati; título confere; *JAMA* 247(18):2543–2546, 1982. | **Confere M/S**, com omissão nominal menor do sufixo Jr. Referência pertinente ao C e valor prognóstico adicional (`main.tex:77`); a correção da dependência da censura é sustentada por Uno, não atribuível ao artigo de 1982. |
| `grambsch1994ph`, 206–214 | [Biometrika/DOI](https://doi.org/10.1093/biomet/81.3.515): Patricia M. Grambsch e Terry M. Therneau; título confere; 81(3):515–526, 1994. | **Confere M/S** para testes e resíduos ponderados (`main.tex:85,141`). O teste implementado e sua aproximação em lifelines não são prova de que todas as alternativas diagnósticas foram examinadas. |
| `vickers2006dca`, 216–224 | [PubMed 17099194](https://pubmed.ncbi.nlm.nih.gov/17099194/): Andrew J. Vickers e Elena B. Elkin; título confere; *Medical Decision Making* 26(6):565–574, 2006. | **Confere M/S** para benefício líquido e limiar (`main.tex:77`); não sustenta utilidade equivalente por inspeção visual, afirmação já retirada. |
| `vickers2008extensions`, 226–233 | [PubMed 19036144](https://pubmed.ncbi.nlm.nih.gov/19036144/) e [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2611975/): Vickers, Cronin, Elkin e Gonen; título confere; *BMC Medical Informatics and Decision Making* 8:53, 2008. | **Confere M/S** para extensão a dados censurados/KM (`main.tex:77`), sem dispensar pressupostos da censura e contexto dos limiares. |
| `putter2007competing`, 235–243 | [PubMed 17031868](https://pubmed.ncbi.nlm.nih.gov/17031868/) e [DOI Wiley](https://onlinelibrary.wiley.com/doi/10.1002/sim.2712/abstract): Putter, Fiocco e Geskus; título confere; *Statistics in Medicine* 26(11):2389–2430, 2007. | **Confere M/S** para distinguir causa específica de incidência cumulativa (`main.tex:183`). Interpretação causal da ausência de transplante exigiria hipóteses adicionais; o estudo não as testa. |
| `polsterl2020sksurv`, 245–253 | [JMLR](https://jmlr.org/papers/v21/20-729.html): Sebastian Pölsterl; título confere; 21(212):1–6, 2020. | **Confere M/S** para biblioteca de sobrevivência usada em `main.tex:89`. O artigo de software não comprova as versões efetivamente executadas, registradas nos manifestos locais. |
| `davidsonpilon2019lifelines`, 255–263 | [Citação oficial do lifelines](https://lifelines.readthedocs.io/en/latest/Citing%20lifelines.html): Cameron Davidson-Pilon; título confere; *JOSS* 4(40):1317, 2019, DOI 10.21105/joss.01317. Abertura direta do DOI/JOSS não foi acessível. | **Confere M/S pela documentação primária do projeto**, pertinente ao ajuste diagnóstico (`main.tex:85`). Não certifica equivalência entre Efron e Breslow, corretamente distinguida no texto. |

### Graf: protocolo e estado da publicação

A v2 confirma .632+, 1.000 reamostragens e a Tabela 2 com C 0,776/0,855. Na v1, §2.1.1 descreve sete variáveis para o diagnóstico de proporcionalidade; §2.2 descreve seleção retroativa por AIC na construção preditiva. Juntar as duas passagens não demonstra que o C publicado veio de um Cox fixo de sete variáveis em todas as reamostragens. O suplemento A da v2 não foi integralmente acessível. As ressalvas sobre IC e calibração encontram suporte. [Fontes: v1](https://arxiv.org/html/2502.03119v1), [v2](https://arxiv.org/pdf/2502.03119v2).

O registro final confirma publicação em outubro de 2026, com os mesmos autores e título, em *Biometrical Journal* 68(5):e70171. Logo, a afirmação local de ausência de veículo publicado está desatualizada. A identidade de todos os resultados entre preprint e versão final não foi certificada, pois Wiley/PMC bloquearam o texto integral final. [PubMed](https://pubmed.ncbi.nlm.nih.gov/42798169/).

## 3. Regras do SBCAS

Não localizei chamada oficial do SBCAS 2027 nas buscas realizadas em 02/11/2026. Isso não demonstra que não exista; aplico **provisoriamente a trilha principal de 2026**, sem transferir suas datas para 2027. Fonte: [chamada SBCAS 2026](https://www.sbcas2026.com/trilhaprincipal). A página é omissa sobre referências fora do limite, modalidade explicitamente duplo-cega e política específica para links de código; não invento essas cláusulas.

| Regra verificada | Resultado para o artigo |
|---|---|
| Trabalho completo: mínimo 8 e máximo 12 páginas | **Atende no PDF existente: 12 páginas**, contando as referências, que ocupam pp.11–12. A chamada não explicita exclusão das referências; contar o PDF inteiro é a interpretação conservadora. Não há folga para acréscimos. |
| Formato SBC, PDF | **Atende documentalmente**: `main.tex:1–12`, `sbc-template.sty:13,29–31`; A4, coluna única, Times 12 pt. Não houve auditoria dimensional de cada caixa do PDF. |
| Abstract e resumo: até dez linhas, ambos na primeira página | **Atende no PDF existente**: dez linhas em cada bloco, p.1; `main.tex:30–36`. A regra é do [modelo da SBC, atribuído à própria sociedade](https://www.overleaf.com/latex/templates/sbc-conferences-template/blbxwjwzdngr), não um limite de palavras nem de linhas do código-fonte. |
| Idioma português ou inglês | **Atende**: português com abstract em inglês. |
| Submissão anônima, sem dados que identifiquem autores | **Atende no texto e metadados examinados**: `main.tex:23–24`, PDF p.1, `pdfinfo` e `pdfinfo -custom`. O destino do repositório não pôde ser inspecionado. |
| Duplo-cego e link de repositório | A chamada exige anonimato, mas **não explicita “duplo-cego” nem regra específica de repositório**. Não é possível certificar esses dois detalhes como regras de 2027 ou cláusulas expressas de 2026. Um link continua sujeito ao requisito geral de não identificar autores; ver C3-05. |
| Declaração de IA generativa | **Atende à exigência encontrada**: `main.tex:190–192`, PDF p.10, identifica Claude, Codex e ChatGPT e responsabilidade humana. A chamada exige explicitar auxílio de IA à redação, excetuando correções linguísticas; não exige modelo específico de declaração, versões ou prompts. |
| Datas | Para **2026**: submissão prorrogada para 09/03/2026, notificação 15/04, versão final 30/04. **Não aplicáveis à submissão futura de 2027**; prazo de 2027 não verificado. Não há data no manuscrito que as contradiga. |
| Requisitos posteriores à aceitação | A chamada condiciona publicação a versão final, inscrição de ao menos um autor e cessão de direitos. Não são requisitos verificáveis pelo manuscrito nesta fase. |

O atendimento acima é ao documento disponível de 2026. Não equivale a certificação antecipada da chamada de 2027.

## 4. Cobertura dos itens essenciais de TRIPOD+AI

Esta é uma avaliação de cobertura solicitada, baseada no artigo e nos documentos locais, não uma pontuação formal dos 27 itens nem uma nova consulta web de conformidade. A referência à diretriz foi conferida bibliograficamente no item 2. O próprio manuscrito limita sua alegação em `main.tex:61`.

| Item | Cobertura | Onde e o que falta |
|---|---|---|
| Fonte de dados | **Coberto** | `main.tex:65`: centro, período, UCI, licença, cópia e checksum; `:183`: contexto histórico. |
| Participantes | **Parcial** | `:65,67,85`: 418, 312/106, sexo, idade e subgrupo. Faltam critérios clínicos de elegibilidade mais explícitos e síntese da distribuição de seguimento. Citar dois ensaios não relata todos os critérios. |
| Desfecho | **Coberto no essencial** | `:67,71,183`: composto, contagens, horizonte, censura e sensibilidade de óbito; distingue referência histórica e riscos competitivos. A forma de apuração/adjudicação histórica é pouco detalhada. |
| Preditores | **Parcial** | `:67,71`: lista das 17, disponibilidade basal, logs/imputação; `tabelas/cox.tex:1–5`: unidades dos efeitos. Faltam definição/codificação completa de categorias e unidades de todos os exames no artigo; podem ser remetidas a dicionário suplementar. |
| Tamanho amostral | **Parcial** | `:67,100`: 418/186 e 132 até cinco anos. Não há explicação explícita de que se usou toda a amostra pública disponível, sem dimensionamento prospectivo, nem justificativa de precisão para a margem. |
| Dados ausentes | **Parcial** | `:67,71,85,183`: nove ausências estruturais, 276 completos, dois sem protrombina, métodos e diferenças de escala. Falta tabela de ausências por variável/subgrupo e pressupostos/limitações da imputação. |
| Análise e validação | **Coberto no essencial** | `:71–89`: modelos, ajuste, partições comuns/aninhadas, métricas, G, bootstrap condicional, multiplicidade, margem e desvios. O protocolo integral está separado. |
| Discriminação | **Coberto** | `:96–113`, Tabela 1 e `tabelas/desempenho.tex:1–8`: medidas, dispersão e IC da diferença, com leitura delimitada. |
| Calibração | **Coberto no essencial** | `:77,117–123`: KM por quintil, O/E e incerteza; quatro modelos no suplementar. Não há intercepto/inclinação de calibração nem avaliação por grupos demográficos; não apresentar quintis como validação clínica completa. |
| Limitações | **Coberto** | `:175,179,181,183`: centro único, antiguidade, ausência de coorte externa, IC condicionais, censura, pré-processamento e busca restritos. |
| Código e dados | **Declarado; acesso não certificado** | `:89`: versões, sementes, manifesto, materiais e URL anonimizada. A documentação local existe; funcionamento e anonimato do destino permanecem inconclusivos. |

O artigo se apresenta corretamente como estudo de avaliação de modelos e caso metodológico. Não entrega um modelo final pronto para aplicação clínica com fórmula, sobrevivência basal e validação externa contemporânea; isso não deve ser inferido do título ou da conclusão. Relato essencial melhorou, mas não cabe declarar adesão integral a TRIPOD+AI.

## 5. Forma e compilação

### Compilação temporária

Foi criado um diretório temporário pelo equivalente Python de `mktemp -d` (`tempfile.mkdtemp`, prefixo `audit-c3-`). Com diretório de trabalho `sbcas/artigo`, executou-se:

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/audit-c3-3_iisu_a main.tex
```

Resultado: **latexmk terminou com código 12; não produziu PDF**. O log temporário, linha 127, informou:

```text
! Package babel Error: Unknown option 'brazil'. Either you misspelled it
(babel) or the language definition file brazil.ldf was not found
```

Na linha 146: erro fatal, sem saída PDF. O TeX instalado é 2022/dev; o PDF existente informa TeX Live 2023. Trata-se de dependência ambiental ausente, não de demonstração de defeito na opção `brazil`, também usada no modelo oficial. Não se instalaram pacotes, não se modificou o fonte e não se contornou o idioma para obter um PDF diferente. O temporário foi removido em bloco `finally`.

**Compilação sem erros e sem referências indefinidas pelo log: não certificada.** A execução nem chegou ao estágio necessário para essa verificação. A existência do PDF e a consistência estática não substituem esse teste.

### PDF existente e fontes

| Verificação | Resultado e evidência |
|---|---|
| Páginas | `pdfinfo sbcas/artigo/main.pdf`: **12**, A4. Dentro do teto provisório de 2026, incluindo referências. |
| Citações e referências internas | Zero `??` no texto extraído. 28 chaves, todas existentes e usadas. Todas as chamadas `ref` têm `label`. Isso é conferência estática e do PDF, não certificação do log. |
| Tabelas e figuras citadas | Tabela 1 em `main.tex:96`, Tabela 2 em `:137`, Tabela 3 em `:85,155`; Figuras 1 e 2 em `:117`. Rótulos em `:101,142,160,123,130`. `desempenho_obito.tex` é suplementar, não tabela órfã do PDF. |
| Travessão U+2014 | **Ausente** em `main.tex`, nos cinco `.tex` de tabelas e no texto extraído do PDF. Os `--` usados em intervalos ou separadores não são esse caractere. |
| Autoria no fonte e PDF | `main.tex:23–24` contém apenas marcadores de autoria e afiliação omitidas; nenhuma identificação de submetentes no texto extraído. Nomes em referências e instituições da coorte não foram confundidos com autoria. |
| Metadados | `pdfinfo` e `pdfinfo -custom`: Creator TeX, Producer pdfTeX, datas e `PTEX.Fullbanner`; sem campos Author, afiliação, e-mail ou identificação de submetentes. |
| Correspondência fonte/PDF | Trechos corrigidos, números, declaração de IA e bibliografia aparecem no PDF atual. Não é possível garantir igualdade de uma reconstrução que não terminou. |

## 6. Leitura como revisor do SBCAS

**A contribuição como estudo de caso está sustentada**, principalmente pelo pareamento dos modelos, controle de censura, avaliação além da discriminação, plano versionado e documentação dos desvios. O trabalho ganha ao formular ausência de vantagem demonstrada em vez de equivalência e ao reconhecer que o Cox17 ainda admite ganho relevante. O protocolo de cinco passos (`main.tex:177`) é uma proposta reutilizável descrita e implementada em um conjunto; sua replicabilidade efetiva em outras coortes não foi testada.

Para computação, as explicações em `main.tex:77` tornam sobrevivência e censura mais acessíveis. Para clínica, separar Mayo reestimado de escore original e mencionar a biópsia, a época da coorte e o uso hipotético do risco ajuda muito. Ainda há parágrafos longos com vários procedimentos em `:71,77,85,89,183`. A margem +0,02 é uma convenção prévia do estudo, não um limiar de benefício clínico universal validado.

Um revisor ainda criticaria, nesta ordem:

1. **Força da inferência negativa:** não há reamostragem do desenvolvimento inteiro; a exclusão para RSF17 é limítrofe e sensível ao protocolo de busca. As ressalvas estão presentes, mas impedem vender ausência de ganho como equivalência ou resultado universal.
2. **Comparação com o trabalho mais próximo:** atualizar Graf e distinguir modelo diagnóstico, seleção preditiva e versão publicada. A novidade depende de comparação bibliográfica fiel.
3. **Limite da novidade:** é comparação em uma coorte muito conhecida e histórica. A utilidade para o SBCAS é o caso metodológico auditável; não foi desenvolvido novo algoritmo, validado uso clínico atual ou isolado causalmente o efeito de cada escolha de protocolo.
4. **Relato de amostra/ausências/precisão:** explicitar o tamanho de conveniência e disponibilizar síntese de seguimento e ausências por variável. Isso ajuda a entender por que 17 variáveis e imputação estrutural podem não trazer ganho.
5. **Utilidade clínica exploratória:** há ação hipotética, mas faltam justificativa clínica dos limiares e incerteza da diferença de benefício líquido. O próprio texto já limita a interpretação.
6. **Reprodutibilidade verificável:** a documentação local é forte; faltam certificado de build limpo neste ambiente e inspeção do repositório anonimizado. A chamada de 2027 deverá ser conferida quando disponível.

Esses pontos não justificam reexecutar a análise nesta auditoria nem trocar o plano após resultados. Pedem delimitação das alegações, documentação e verificações de submissão.

## Achados

### C3-01  Detalhes distintos do protocolo de Graf foram fundidos
- Gravidade: importante
- Evidência: `sbcas/artigo/main.tex:54`, “O Cox usa sete variáveis escolhidas por seleção retroativa pelo critério de Akaike”; `sbcas/notas_literatura.md:9–10` atribui a verificação à v2. Na [v1 primária, §2.1.1 e §2.2](https://arxiv.org/html/2502.03119v1), a lista de sete caracteriza o diagnóstico de proporcionalidade; a seleção retroativa é descrita em outro procedimento. A [v2, §2.2](https://arxiv.org/html/2502.03119v2) remete a construção dos modelos ao suplemento A.
- Problema: a fonte consultada não demonstra que o C de 0,776 resulte de um único Cox fixo com essas sete variáveis, muito menos que essa dimensão seja mantida no bootstrap. A correção da B3 acrescentou especificidade maior que a evidência disponível. Não se deve declarar falsa a seleção AIC, que tem suporte na v1; a dificuldade é ligá-la à lista fixa e à versão apontada.
- Sugestão: descrever Cox com seleção de variáveis e bootstrap .632+, sem fixar sete na comparação preditiva, ou apontar a passagem do suplemento/versão final que estabeleça essa ligação. Corrigir a proveniência das notas.

### C3-02  Graf já tem publicação final de 2026
- Gravidade: importante
- Evidência: `sbcas/artigo/referencias.bib:93–98` registra apenas arXiv 2025; `sbcas/notas_literatura.md:9` diz “sem veículo publicado”. [PubMed 42798169](https://pubmed.ncbi.nlm.nih.gov/42798169/) registra *Biometrical Journal* 68(5):e70171, 2026, DOI 10.1002/bimj.70171.
- Problema: a referência é central para a motivação e seu estado de publicação está desatualizado. Citar o preprint não é inválido, mas afirmar que não existe veículo publicado é incorreto na data da auditoria.
- Sugestão: atualizar para a publicação de 2026; se os detalhes dependem da versão de 2025, indicar expressamente essa versão e conferir sua correspondência ao artigo final antes de transportar conclusões.

### C3-03  Ano recomendado da UCI e delimitação bibliográfica precisam ajuste
- Gravidade: menor
- Evidência: `referencias.bib:18` usa 2023; a [UCI](https://archive.ics.uci.edu/dataset/878/cirrhosis+patient+survival+prediction+dataset-1) recomenda 1989. `referencias.bib:153` usa 187–220 para Cox; o [sumário do periódico](https://academic.oup.com/jrsssb/issue/34/2) separa artigo 187–202 e discussão 202–220. `:197` omite Jr de Harrell; `:119–126` omite número 1/grupo STRATOS.
- Problema: o ano de depósito foi usado como ano da citação recomendada; a entrada de Cox não indica que inclui discussão. As outras omissões são de normalização, não comprometem os métodos citados.
- Sugestão: adotar a citação UCI recomendada, esclarecer artigo/discussão de Cox e completar os detalhes nominais/editoriais quando pertinente. New York para Fleming e Harrington está confirmado e não precisa correção.

### C3-04  Compilação limpa continua sem certificação por dependência ausente
- Gravidade: importante
- Evidência: `main.tex:5` carrega Babel `brazil`; log temporário `main.log:127,146`, transcrito no item 5, e retorno 12 de latexmk. O temporário foi removido. O PDF existente tem 12 páginas e nenhuma referência aparente indefinida.
- Problema: a compilação parou antes de BibTeX e das passagens finais. Não é possível responder afirmativamente “compila sem erros e referências indefinidas” com este ambiente. Isso não demonstra erro do manuscrito.
- Sugestão: conferir em ambiente com suporte português de Babel e dependências TeX completas, preservando o log final; repetir só a compilação temporária, sem reexecutar os experimentos. Conferir novamente teto de 12 páginas depois das alterações bibliográficas.

### C3-05  Anonimato do repositório vinculado não foi certificado
- Gravidade: importante
- Evidência: `main.tex:89` aponta [endereço anonimizado](https://anonymous.4open.science/r/ml4health-sbcas), que não foi acessível pela ferramenta web. A [chamada de 2026](https://www.sbcas2026.com/trilhaprincipal) exige não identificar autores. A cópia local contém identificação em `README.md:4,7` e URL identificadora em `AUDITORIA.md:8`; `main.tex:89,192` anuncia compartilhamento dos relatórios.
- Problema: o texto/PDF/metadados passam, mas não há evidência de que o espelho realmente funciona e remove nomes, URLs, histórico e documentos identificadores. A presença local não prova vazamento no espelho; impede certificar seu anonimato sem vê-lo.
- Sugestão: abrir o endereço como visitante e conferir o conteúdo efetivamente exposto, inclusive README, relatórios, caminhos, links e histórico. Usar um espelho que remova identificadores; verificar as regras específicas de 2027 quando publicadas.

### C3-06  Explicação nova apresenta 0,5 como limite inferior do C
- Gravidade: menor
- Evidência: `main.tex:77`, “varia de 0,5, o acaso, a 1, a ordenação perfeita”. A [referência de Uno](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/sim.4154) trata de probabilidade de concordância.
- Problema: o índice pode ser inferior a 0,5 quando a ordenação é pior que o acaso; seu domínio não começa em 0,5. É um erro didático introduzido na ampliação explicativa solicitada em B3-12, sem impacto nos números obtidos.
- Sugestão: dizer que varia de 0 a 1, com 0,5 indicando ordenação ao acaso e 1 concordância perfeita, sob a convenção de risco usada.

### C3-07  Cronologia dos complementos é generalizada além do registro
- Gravidade: menor
- Evidência: `main.tex:89`, “Os demais são complementações [...] fixadas antes dos resultados finais, exceto a regra de escolha da Tabela”; `sbcas/DESVIOS.md:16` acrescenta D10 em resposta à B3 de 02/11/2026, posterior aos resultados que aquela auditoria conferiu.
- Problema: D10 documenta escolhas/entregas existentes depois dos resultados e não é abrangido pela única exceção temporal declarada. Registrar posteriormente um procedimento já executado é diferente de o fixar prospectivamente.
- Sugestão: separar detalhes fixados antes da execução final de esclarecimentos posteriores sobre o que foi feito, identificando D9 e D10. Não alterar retrospectivamente o plano.

### C3-08  Relato essencial ainda incompleto para amostra e ausências
- Gravidade: menor
- Evidência: `main.tex:65,67,71` informa fonte, contagens e imputação; `:183` reconhece limitações. Não há justificativa explícita do tamanho amostral nem resumo do seguimento e das ausências por variável. A matriz de cobertura do item 4 identifica essas lacunas.
- Problema: o leitor não distingue de imediato amostra de conveniência integral de estudo dimensionado para excluir +0,02 e não dispõe de síntese suficiente para avaliar o custo da imputação estrutural. Dizer que o relato se orienta por TRIPOD+AI é aceitável; dizer que atende integralmente não seria.
- Sugestão: explicar o uso de todos os pacientes disponíveis, a ausência de dimensionamento prospectivo e a limitação de precisão; remeter a um quadro suplementar de seguimento, definições/codificações e ausências por variável/subgrupo, respeitando o teto de páginas.

## Tabela-resumo

| Achado | Gravidade | Providência principal |
|---|---|---|
| C3-01: atribuição do Cox de sete variáveis de Graf | importante | Separar modelo diagnóstico de construção preditiva e documentar a versão. |
| C3-02: veículo final de Graf | importante | Atualizar para *Biometrical Journal*, 2026. |
| C3-03: normalização bibliográfica | menor | Usar ano recomendado UCI e esclarecer páginas de Cox. |
| C3-04: compilação não certificada | importante | Completar dependência ambiental e conferir log final temporário. |
| C3-05: espelho anônimo não certificado | importante | Verificar acesso e remoção de identificadores no material exposto. |
| C3-06: domínio do C incorreto na explicação | menor | Distinguir domínio 0–1 de referência aleatória 0,5. |
| C3-07: cronologia de D10 | menor | Distinguir especificação prévia de documentação posterior. |
| C3-08: lacunas de relato | menor | Explicitar tamanho disponível, precisão, seguimento e ausências. |

## Veredito

**Aprovado com ressalvas: quatro achados importantes e quatro menores, nenhum bloqueante demonstrado.** Nove correções da B3 estão resolvidas e três parcialmente resolvidas. O estudo de caso e a proposta de protocolo reutilizável são defensáveis com o alcance atual; não sustentam equivalência entre modelos, prontidão clínica ou generalização para outras coortes.

Antes da submissão, recomenda-se corrigir atribuição/atualização de Graf e o domínio do C, ajustar a cronologia e a bibliografia, conferir build limpo e verificar o espelho anonimizado. O PDF existente atende ao teto provisório de 12 páginas e aos dois blocos de dez linhas. Regras e prazos definitivos do SBCAS 2027 permanecem não certificados; as verificações de evento usam explicitamente a chamada disponível de 2026. Nenhum insumo científico foi modificado.

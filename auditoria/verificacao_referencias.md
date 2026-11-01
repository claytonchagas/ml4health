# Conferência das referências do artigo

Registro de como cada referência de `artigo/referencias.bib` foi conferida: fonte consultada, quem conferiu, resultado e o que ainda não foi verificado. Consolida a verificação feita na escrita do artigo (Claude) e as passadas independentes C e C2 (Codex), de 01/11/2026. Detalhes e localizações nas fontes estão em [`relatorio_C.md`](relatorio_C.md) e [`relatorio_C2.md`](relatorio_C2.md).

Legenda: **M** = metadados (autores, ano, título, veículo, volume, número, páginas, DOI); **S** = sustentação das frases em que a referência é citada.

| Chave | Fonte consultada | Conferido por | Resultado | Ainda não verificado |
|---|---|---|---|---|
| dickson1989prognosis | [PubMed 2737595](https://pubmed.ncbi.nlm.nih.gov/2737595/); texto integral (cópia local, fora do git) | Claude; C | M e S conferem (dois ensaios, 312 e 418, 106 de 112, fórmula, exemplos, sobrevida basal) | nada |
| uci878 | [UCI 878](https://archive.ics.uci.edu/dataset/878/cirrhosis+patient+survival+prediction+dataset-1) | Claude; C; C2 | M confere (autores, 1989, DOI, CC BY 4.0, disponibilizado em 2023); identidade com a cópia local em [`comparacao_uci_rdatasets.txt`](comparacao_uci_rdatasets.txt) | nada |
| fleming1991counting | [Wiley](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118150672) | C; C2 | M confere (autores, título, Wiley, 1991; Apêndice D de dados) | cidade da editora (New York); conteúdo do apêndice sobre PBC |
| beuers2015nomenclature | [PubMed 26372460](https://pubmed.ncbi.nlm.nih.gov/26372460/); [versão conjunta, Amsterdam UMC](https://pure.amsterdamumc.nl/ws/portalfiles/portal/160708336/Changing-nomenclature-for-pbc-from-cirrhosis-to-cholangitis.pdf) | C; C2 | M confere; S confere (só uma minoria desenvolve cirrose) | nada |
| lammers2015globe | [PubMed 26261009](https://pubmed.ncbi.nlm.nih.gov/26261009/) | Claude; C | M confere (após correção para 1804–1812.e4); S confere (4.119 = 2.488 + 1.631; C de 0,82) | nada |
| carbone2016ukpbc | [PMC6984963](https://pmc.ncbi.nlm.nih.gov/articles/PMC6984963/) | Claude; C | M e S conferem (1.916 e 1.249; AUC acima de 0,90; exames aos 12 meses e basais; análise em não tratados) | nada |
| gerussi2022ml | [PubMed 34951722](https://pubmed.ncbi.nlm.nih.gov/34951722/); [pôster dos autores](https://www.postersessiononline.eu/173580348_eu/congresos/ILC2021/aula/-PO_376_ILC2021.pdf) | Claude; C; C2 | M confere; S confere quanto ao objetivo declarado (estratificação por agrupamento; 11.819 e 1.069) | texto integral da versão final (acesso restrito) |
| ishwaran2008rsf | [arXiv 0811.1645](https://arxiv.org/pdf/0811.1645) | Claude; C | M e S conferem (312 randomizados, 17 variáveis) | nada |
| reade2023ps3e26 | [Kaggle](https://www.kaggle.com/competitions/playground-series-s3e26/data) | Claude; C; C2 | M confere; S confere (três classes definidas por N_Days; dados sintéticos gerados por modelo treinado no original) | cabeçalho dos CSVs (exige login) |
| shakir2025cirrhosis | [página do periódico](https://journal.irpi.or.id/index.php/predatecs/article/view/2015); [reprodução integral](https://www.researchgate.net/publication/394892047_Leveraging_Machine_Learning_for_Early_Risk_Prediction_in_Cirrhosis_Outcome_Patients) | Claude; C; C2 | M confere; S confere no texto (N_Days removido, três classes, Kaggle, balanceamento antes da divisão, sem calibração) | imagem da Figura 1 (o artigo se apoia na descrição textual do procedimento) |
| tu2025cirrhosis | [PDF institucional UCLA](https://escholarship.org/content/qt0d66m3m6/qt0d66m3m6.pdf) | Claude; C | M e S conferem | nada |
| christodoulou2019systematic | [PubMed 30763612](https://pubmed.ncbi.nlm.nih.gov/30763612/) | Claude; C | M e S conferem (71 estudos, 282 pares, 79% sem calibração, diferença 0,00) | nada |
| vandengoorbergh2022harm | [UMC Utrecht](https://researchinformation.umcutrecht.nl/en/publications/the-harm-of-class-imbalance-corrections-for-risk-prediction-model/); [PubMed 35686364](https://pubmed.ncbi.nlm.nih.gov/35686364/) | Claude; C2 | M confere; S confere com o alcance delimitado (regressão logística) | nada |
| kapoor2023leakage | [PubMed 37720327](https://pubmed.ncbi.nlm.nih.gov/37720327/) | Claude; C | M e S conferem | nada |
| vancalster2019calibration | [BMC Medicine](https://link.springer.com/article/10.1186/s12916-019-1466-7) | Claude; C | M e S conferem | nada |
| steyerberg2014seven | [PubMed 24898551](https://pubmed.ncbi.nlm.nih.gov/24898551/) | C | M e S conferem | nada |
| collins2024tripodai | [PMC11019967](https://pmc.ncbi.nlm.nih.gov/articles/PMC11019967/) | C | M confere; o artigo declara não ter verificado formalmente todos os itens | nada |
| varma2006bias | [BMC Bioinformatics](https://link.springer.com/article/10.1186/1471-2105-7-91) | C | M e S conferem | nada |
| zou2005elasticnet | [JRSS B](https://doi.org/10.1111/j.1467-9868.2005.00503.x) | C | M e S conferem | nada |
| breiman2001random | [Springer](https://link.springer.com/article/10.1023/A:1010933404324) | C; C2 | M confere (volume 45, páginas 5–32, 2001) | número do fascículo (1) |
| chen2016xgboost | [arXiv 1603.02754](https://arxiv.org/abs/1603.02754) | C | M e S conferem | nada |
| vanbuuren2011mice | [JSS](https://www.jstatsoft.org/article/view/v045i03) | C; C2 | M confere (45(3):1–67); S confere quanto ao conceito | nada |
| pedregosa2011scikit | [JMLR](https://jmlr.org/papers/v12/pedregosa11a.html) | C | M e S conferem | nada |
| fawcett2006roc | [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S016786550500303X) | C | M e S conferem | nada |

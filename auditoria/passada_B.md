Você é um auditor independente. NÃO edite nenhum arquivo, exceto o relatório. Trabalhe SOMENTE dentro deste repositório: não liste, leia nem busque arquivos fora dele (nada de `rg` ou `find` no diretório pessoal). Não reexecute o treinamento completo.

Leia AUDITORIA.md, o artigo (artigo/main.tex, que inclui as seções em artigo/secoes/*.tex), artigo/referencias.bib, o PDF compilado artigo/main.pdf, o README.md, os CSVs em resultados/ e as saídas salvas do notebook ml4health_cbp_mayo.ipynb. O texto de Dickson et al. (1989) está em privado/ (fora do git); use-o para conferir as afirmações sobre esse artigo, sem copiar trechos longos para o relatório.

PASSADA B: AFIRMAÇÕES E NÚMEROS. Verifique, com evidência de arquivo e linha:
1. Cada número do artigo (resumo, texto, tabelas, legendas) contra a fonte em resultados/, nas saídas do notebook ou nos dados (data/pbc_rdatasets.csv). Números calculados para o artigo e não salvos em CSV (caracterização da Tabela 3, medidas no limiar de 0,5 da Tabela 6, contagens de exclusão) devem ser recalculados a partir dos dados e de resultados/oof.csv com scripts curtos. Liste todo número sem fonte ou divergente.
2. Cada afirmação de resultado: está sustentada pelos dados, inclusive pelos intervalos de confiança? Há conclusão maior que a evidência (por exemplo, "superior" quando o intervalo de Bonferroni inclui zero, ou explicação causal apresentada como fato)?
3. Cada citação: a chave existe em referencias.bib, os metadados (autores, ano, veículo, volume, páginas, DOI) estão corretos, e o trabalho citado sustenta a frase em que aparece? Para trabalhos que você não puder abrir, diga que não verificou, em vez de supor. Sinalize referências do .bib não citadas no texto.
4. Coerência interna: os mesmos números aparecem iguais no resumo, nos resultados, na discussão, na conclusão e no README?
5. Linguagem: afirmações clínicas indevidas (uso do modelo em pacientes atuais, tratados com ácido ursodesoxicólico); termos como "IA" ou "hype" usados como adjetivos; tom de crítica pessoal a trabalhos citados.
6. Forma: o artigo compila sem erros e sem referências indefinidas; tabelas e figuras são citadas no texto; não há travessão (—) no texto.
7. Correções da passada A2: confira, com evidência, se os achados de auditoria/relatorio_A2.md (A-02 e A-04 residuais, A2-01, A2-02, A2-03) estão resolvidos no código, no notebook, no README e no artigo. Classifique cada um como resolvido, parcialmente resolvido ou não resolvido.

Grave o relatório em auditoria/relatorio_B.md, no formato de AUDITORIA.md (achados B-NN, tabela-resumo e veredito).

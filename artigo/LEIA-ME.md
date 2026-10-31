# Modelo de artigo — Projeto de Aplicação em Aprendizado de Máquina para Saúde

**Instituto de Computação — Universidade Federal Fluminense (UFF)**

Este projeto apresenta um artigo em LaTeX com texto ilustrativo e aparência de artigo acadêmico. Não há campos com a marcação `PREENCHER`, caixas de orientação no PDF ou subdivisões na Introdução. Todos os parágrafos podem ser substituídos e adaptados ao problema desenvolvido pelo grupo.

## Como importar no Overleaf

1. Criar projeto em **New Project → Upload Project**.
2. Enviar o arquivo ZIP sem descompactá-lo.
3. Confirmar `main.tex` como documento principal e escolher **pdfLaTeX**.
4. Compilar normalmente. As referências serão processadas pelo BibTeX.

## Como editar

- **Título, autores e resumo:** substituir pelo problema clínico, objetivo, dados, métodos e principais resultados reais. No resumo do artigo final, relatar achados quantitativos efetivamente obtidos, não apenas procedimentos.
- **Introdução:** manter sem subdivisões; organizar os parágrafos em contexto, problema, lacuna, pergunta de pesquisa, objetivo e contribuições. Sustentar afirmações com bibliografia pertinente.
- **Trabalhos relacionados:** documentar o levantamento bibliográfico e comparar criticamente métodos, populações, bases, validação, resultados e limitações de pesquisas anteriores.
- **Materiais e métodos:** descrever dados, unidade de análise, critérios de seleção, alvo, análise exploratória, pipeline de transformações, particionamento, modelos, ajuste, métricas, reprodutibilidade e ética. Evitar vazamento de dados. Adicionar detalhes ou subseções conforme o problema.
- **Resultados:** substituir tabelas sem medidas e figura de dados fictícios por resultados reais. Indicar conjunto avaliado, número de observações, métricas, variabilidade e limitações relevantes.
- **Discussão e conclusão:** interpretar os resultados, contextualizar na literatura, expor limitações e evitar conclusões que excedam as evidências.
- **Bibliografia:** cadastrar fontes em `referencias.bib`, usar `\cite{chave}` para citação autor-data ou `\citeonline{chave}` para citação narrativa.
- **Figuras:** arquivos ficam na pasta `figuras/`. O arquivo atual ilustra a distribuição de classes com **dados fictícios**.

O estilo ABNT autor-data é aplicado por `abntex2cite` com BibTeX. A implementação disponível do pacote pode não refletir integralmente a versão mais recente de todas as normas da ABNT, sobretudo a NBR 10520:2023; quando for exigida adequação estrita, revisar as citações e referências geradas de acordo com as exigências institucionais.

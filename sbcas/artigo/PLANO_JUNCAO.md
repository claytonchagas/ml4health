# Plano da versão de junção (ramo `sbcas-2027-juncao`)

Base: versão B (commit `28ddaa9`). Fonte dos enxertos: versão A (commit `bf10357`, `main_A_bf10357.tex`). Pareceres: S = `1_sonnet.md`, O = `2_opus.md`, G = `3_gemini.txt`, C = `4_chatgpt.txt`. Os quatro preferem B e pedem junção com B como base.

Regras herdadas que continuam valendo: nenhum dado nem análise nova; nenhum número de resultado digitado à mão (só macros de `gerar_tabelas.py`); 12 páginas; abstract e resumo com no máximo 10 linhas; decisões congeladas de `sbcas/DECISOES_REVISAO.md`; limites da auditoria; anonimato; lição do CAIN; honestidade acima de persuasão.

## 1. Medição de partida

- B tem 12 páginas e a página 12 termina a cerca de 1,7 cm do fim do bloco de texto: folga de 3 a 4 linhas, nada mais.
- Abstract e resumo estão em exatamente 10 linhas cada: qualquer acréscimo neles exige corte interno.
- As figuras de B são ilegíveis sobretudo por escala, não só por tamanho: os PDFs foram gerados grandes e reduzidos a cerca de metade, de modo que fontes de 9 a 10 pt saem com 4,5 a 5,7 pt. A solução é gerar as figuras no tamanho impresso, com fontes reais de 7 a 8 pt, e só então aumentá-las um pouco.

## 2. Itens e custo estimado (linhas de texto de 12 pt)

### 2.1 Correções em B

| # | O que | Onde | Parecer | Custo |
|---|---|---|---|---|
| 1 | "responde 'não'" vira "descarta ganho de 0,02 ou mais, sem excluir ganhos menores"; mesmo cuidado na Discussão | Conclusão, Discussão par. 1 | C (B1), O | +0,5 |
| 2 | Reescrever "Para além do caso... não": efeito de reestimar a fórmula é local (estimada nestes pacientes); a semente mudou a leitura da RSF de 17 (Seção 4.1); vazamento medido em outra tarefa | Discussão par. 2 | G, C (B2), O (B1, B3) | +1 |
| 3 | Subgrupo: dizer que as diferenças pareadas são calculadas antes de arredondar (0,016 e 0,024 contra 0,017 e 0,025 por subtração dos C mostrados) | 4.3 | O (B4) | +0,5 |
| 4 | D13 explicado em uma oração (pergunta do plano sobre a origem do ganho ficou sem resposta: não houve ganho a decompor e o desenho não o isola) | 3.2 | O (B7) | +0,5 |
| 5 | O +0,043 no resumo: qualificar (nos 312 randomizados, sem intervalo) | Resumo e abstract | O, C (A6) | 0 (corte interno) |
| 6 | "nenhum superou a fórmula de 1989" sempre com "análise posterior" e "avaliada onde foi estimada" | Resumo, abstract, Discussão par. 1, Conclusão | C (B3), S | +0,5 |
| 7 | Lacuna de Trabalhos relacionados sem sugerir revisão sistemática; contribuição é o protocolo | Seção 2 | C (B4) | 0 |
| 8 | Plano complementar: "não é confirmação pré-especificada independente" explícito | 3.5 | C (B6) | +0,5 |
| 9 | SUS: "mais de 85% dos transplantes do país", fiel à fonte, como em A | Introdução | O (B6) | 0 |
| 10 | Legenda da Tabela 3: dizer por que o IC do teste corrigido não é simétrico em torno de ΔC | Tabela 3 | G (comum 3) | +0,5 |
| 11 | "um resultado nulo era o mais provável" acompanhado da justificativa (cenário real de adoção) | Discussão par. 1 | O (B5) | +0,5 |

### 2.2 Organização

| # | O que | Parecer | Custo |
|---|---|---|---|
| 12 | Métodos na ordem de A: parágrafo curto de abertura (TRIPOD+AI, data do registro, "o que mudou depois é desvio"); 3.1 Dados e desfechos; 3.2 Modelos e o alcance da comparação; 3.3 Validação e métricas; 3.4 Como se lê uma diferença entre modelos; 3.5 Análises complementares; 3.6 Desvios do plano e reprodutibilidade (com os três limites). Redação de B dentro de cada subseção. Nenhum conceito usado antes de apresentado: "desvio" é definido na abertura; D11 e D13 aparecem depois disso. Tabela 1 passa a remeter o passo 1 à abertura e à 3.6 | G, C, S, O | -2 (contabilidade dos desvios mais curta) |

### 2.3 Enxertos de A

| # | O que | Onde | Parecer | Custo |
|---|---|---|---|---|
| 13 | Tabela 3 com o bloco "Só óbito (sensibilidade)" (3 linhas + cabeçalho), legenda de B; texto de 4.1 passa a remeter ao bloco e encurta | Tabela 3, 4.1 | S, O, G, C | +3 na tabela, -2 no texto |
| 14 | Figuras geradas no tamanho impresso, com fontes reais: Figura 1 = calibração em três painéis (referência, Cox penalizado, RSF de 17), largura total; Figura 2 = curva de decisão e importância por permutação, largura total. O Cox penalizado entra por ser o desvio que o texto destaca (G); a legenda diz que foi acrescentado depois dos resultados | 4.2, 4.3 | S, O, G, C | +15 (cerca de 7,5 cm) |
| 15 | Introdução: frase de custo ("perdem a transparência de uma fórmula de cinco termos..."), junto da pergunta prática; contexto brasileiro compacto com coorte de 28 centros, "mais de 85%" e 2.454 transplantes de fígado em 2024, em uma frase; primeiro parágrafo de B mantido | Introdução | G, C, S, O | +2,5 |
| 16 | Censura explicada como em A ("sabe-se apenas que, se o evento ocorreu, foi depois"); estrutura dos dados com `N_Days`; licença CC BY 4.0 | 3.3, 3.1 | O, G, C | +2 |
| 17 | 4.2: a razão O/E global pode esconder erros em sentidos opostos | 4.2 | G | +1 |
| 18 | Trabalhos relacionados: sobreposição de intervalos por modelo não é intervalo para a diferença; derivados do Kaggle não avaliam calibração; mantido "cujo intervalo exclui o C pontual do Cox" | Seção 2 | C, G, S | +1 |
| 19 | Resumo: frase curta de que calibração e benefício líquido não mostraram vantagem | Resumo e abstract | G, S, O | 0 (corte interno) |
| 20 | Conclusão: estrutura de B, fecho de A ("com a mesma pergunta: quanto o novo modelo acrescenta") | Conclusão | G, S | 0 |

### 2.4 Conflitos (decisão e justificativa)

- **Importância por permutação (Fig. 2b de A).** Volta ao corpo, ao lado da curva de decisão. Motivo: uma curva de decisão legível sozinha ocuparia a mesma altura e deixaria metade da largura em branco, logo o painel (b) tem custo zero de página; três dos quatro leitores o querem; é o painel mais intuitivo para um comitê de computação. Condições pedidas pelo ChatGPT: a legenda diz que foi calculada só nas 5 partições da primeira repetição; o texto afirma só o que é robusto (bilirrubina no topo; da quarta posição em diante a ordem fica dentro do desvio entre partições) e não interpreta posições intermediárias nem diz que "as cinco de Mayo estão entre as oito primeiras" como estabilidade.
- **"Sobra pouco para a floresta aprender".** Volta em uma oração, marcada como hipótese não testada e ligada a trabalho futuro, no fim do primeiro parágrafo da Discussão, sem peso conclusivo. Motivo: é a única explicação de domínio que o artigo oferece e dialoga com a Figura 2b; a ressalva do ChatGPT (explicação causal não testada) fica atendida pela marcação explícita.
- **Commit `677a281` e data 01/11/2026.** Não decidido aqui: fica como em B (data, sem o hash), e a questão vai para `sbcas/artigo/PENDENCIAS_AUTOR.md`. A data é verdadeira e não se altera.

## 3. Orçamento de páginas

Acréscimos: figuras +15; Tabela 3 +3; texto (itens 1 a 11, 15 a 18) +11. Total: cerca de +29 linhas. Folga: 3 a 4 linhas. É preciso cortar cerca de 25 linhas sem perder conteúdo. De onde saem:

| Fonte do corte | Linhas |
|---|---|
| 4.1: a sensibilidade só óbito passa a estar na Tabela 3; o texto só remete e resume | 2 |
| 3.6: contabilidade dos dezessete desvios mais enxuta (sem a prosa de "um anterior, seis da auditoria, nove posteriores" em frase longa) | 2 |
| 4.3: frase da fórmula no desfecho só óbito mais curta (limites do teste corrigido sem repetir o intervalo inteiro) | 1,5 |
| 4.3: pressupostos da referência em uma frase | 1 |
| Discussão, parágrafo do contraste com Graf et al.: de 8 para cerca de 5,5 linhas, sem perder a ressalva do .632+ nem a do modelo não identificado | 2,5 |
| Discussão, parágrafo 2: reescrito sem repetir o que a Tabela 4 já diz | 1 |
| Legenda da Figura 1 de B (4 linhas) substituída por duas legendas mais curtas (3 + 3) | -2 (já contado nas figuras) |
| Tabela 4: primeira coluna da linha da fórmula sem "(muda também o modelo)", que já está na legenda; menos quebras de linha | 1,5 |
| Tabela 3: legenda reescrita em 5 linhas | 1 |
| 3.3: frase do C de Harrell encurtada | 0,5 |
| Introdução, parágrafo das contribuições: enxugar (i) | 1 |
| Conclusão: enxugar sem perder a distinção "descartado" e "não sabemos" | 1 |
| Declaração de IA: uma linha a menos, mantendo quem fez o quê | 1 |
| Trabalhos relacionados: parágrafo 3 enxuto ao acrescentar a calibração do Kaggle | 0,5 |
| 3.5: frases de ligação | 1 |
| Ajuste fino das alturas das figuras (de 5,0 cm para 4,6 cm cada) se faltar | até 2 |

Se, depois disso, ainda faltar espaço, a ordem de sacrifício é: (1) encurtar as alturas das figuras até 4,5 cm, mantendo as fontes reais; (2) reduzir o parágrafo brasileiro à frase única; (3) tirar do corpo o parágrafo da hipótese da floresta. Não se corta: Tabela 1, Tabela 4 em blocos, a seção 3.6 com os três limites, as limitações, a declaração completa das análises posteriores.

## 4. Mecânica

1. `gerar_tabelas.py`: `leitura.tex` volta a ter os três blocos (principal, só óbito, fórmula de 1989); `leitura_obito.tex` deixa de ser gerado (o bloco está no corpo); sem macros novas de resultado além das existentes.
2. Novo `sbcas/artigo/figuras_artigo.py` (substitui `figura_decisao_importancia.py`): lê só `calibracao_quintis_ic.csv`, `curva_decisao.csv` e `importancia_permutacao_rsf17.csv`, sem recomputar nada, e grava `figura_calibracao.pdf` (três painéis) e `figura_decisao_importancia.pdf`, ambos com largura de 16 cm e fontes reais. `figura_curva_decisao.pdf` sai do repositório por ficar sem uso.
3. Etapas com compilação e commit: (a) plano; (b) tabelas e figuras; (c) Métodos reordenados; (d) correções e enxertos de texto; (e) ajuste de páginas, changelog, pendências, suplementar e renderização final.

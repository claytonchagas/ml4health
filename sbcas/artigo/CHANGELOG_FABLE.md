# Registro de mudanças da reescrita (ramo `sbcas-2027-fable`)

Base: commit `bf10357` (versão avaliada pelos quatro pareceres). Pareceres citados: P1 = `1_fable_cego.md`, P2 = `2_revisorA_computacao.md`, P3 = `3_revisorB_bioestatistica.md`, P4 = `4_chatgpt.txt`; série H = itens H1 a H11 do briefing.

## Estratégia

1. Reorganizar o argumento em torno de três leituras (ganho não demonstrado; ganho relevante descartado; ganho aparente produzido pela avaliação) e dar a resposta por modelo ("não" para a RSF de 5 variáveis, "não sabemos" para os outros dois), do resumo à conclusão (P1 motivo 2; P2 motivo 2; P4 síntese).
2. Separar, em todo o texto, o que é do plano prévio do que é análise posterior (fórmula de 1989, fontes de ganho aparente, regra combinada), com uma subseção própria sobre o que o plano é e não é (P3 itens 3.a, 3.b, 4.2; P2 motivo 2; P4 6.11; H3).
3. Tirar a consequência das assimetrias do desenho: a comparação responde a uma pergunta de adoção, não a uma competição entre famílias de algoritmos (P1 motivo 3; P4 2.2).
4. Reduzir a densidade estatística para o público de computação: frases curtas, propósito antes do detalhe, cada termo explicado uma vez, números para as tabelas, mensagem para o texto; Tabela 3 só com o desfecho principal e a fórmula; Tabela 4 em blocos; contabilidade de desvios resumida (P1 seção 4; P2 motivo 3; P4 seção 4; lição do CAIN).
5. Nenhum número de resultado digitado à mão: todas as grandezas citadas no texto, inclusive no abstract em inglês, viraram macros geradas de `resultados_sbcas/*.csv` por `gerar_tabelas.py` (restrição 3 do briefing).

## Mudanças por seção

### Título
Mantido exatamente (decisão congelada).

### Abstract e resumo (10 linhas cada)
- Abrem pela pergunta de adoção ("julgados pelo que acrescentam ao modelo clínico"), sem afirmar que o Mayo é o padrão assistencial atual (P4 5.1).
- Dizem que o ganho de 0,02 foi descartado só para a RSF de 5 variáveis e que, para os outros dois, faltou precisão (H3; P1 motivo 2; P2 motivo 2).
- A fórmula de 1989 e o otimismo de treino aparecem como "análises posteriores" (H3; P3 3.a; P4 6.11).
- Todos os números vêm de macros (`\refAgr`, `\difMin`, `\difMax`, `\otimRSF`; versões `EN` com ponto decimal para o abstract).
- Calibração e benefício líquido saíram do resumo por falta de espaço nas 10 linhas; seguem na Seção 4.2 e na Tabela 1.

### 1. Introdução
- Abertura com a pergunta de adoção e com a lacuna apontada por um trabalho do próprio SBCAS, que declara como limitação não ter comparado seus modelos com as abordagens clínicas em uso (relevância para o comitê; P1 e P2, relevância 3 a 4).
- "Selecionadas em dois ensaios clínicos" em vez de "derivada de dois ensaios": a fórmula de uso foi estimada nos 418, como diz a Seção 3.6 (H5; P2 6.1; P3 2.5).
- Parágrafo Brasil/SUS encolhido a duas linhas, sem ser removido (decisão congelada atualizada em 02/11; P1 5.4; P2 5.5). A citação da coorte brasileira saiu por espaço.
- Contribuições reduzidas a três, começando pela reavaliação pareada da vantagem relatada para a RSF nesta coorte e pela medida das escolhas de avaliação; os cinco cuidados da Tabela 1 seguem como boas práticas conhecidas, não método novo (P1 motivo 1; P2 motivo 1; P4 3.1; decisão congelada).
- As três leituras passam a ser o eixo declarado do artigo.

### Tabela 1
- Linhas encurtadas; passo 3 remete às Seções 3.4 e 4.4; passo 5 remete à Tabela 4 "(classificação)", para não sugerir que o teste de vazamento foi feito nos modelos de sobrevivência (P1 6.7; P2 6.7).

### 2. Trabalhos relacionados
- Graf et al.: "exceto em uma de seis regras de divisão, cujo intervalo exclui o C pontual do Cox" (P3 3.h).
- Frase final da lacuna sem a reivindicação sobre "medir o ganho aparente", que era lida como exagero.

### 3.1 O plano prévio, seus limites e a reprodutibilidade (nova)
- Diz logo o que o plano é e não é: registro por `commit` no repositório da autoria, não registro independente (P1 motivo 3; P2 5.1; P3 4.1); escrito após a análise de classificação; regra de leitura mais exigente adotada depois dos resultados (P2 motivo 2, 6.4).
- A contabilidade dos dezessete desvios ficou em palavras ("um anterior a qualquer resultado, seis da auditoria, nove posteriores"), sem a enumeração D2, D4 a D8, D9 a D17 (P1 4.2; P2 motivo 3; P4 4.3). A lista completa está no repositório.
- Reprodutibilidade absorvida aqui (uma subseção a menos).

### 3.2 Dados e desfechos
- Variáveis e ausências reescritas em frases curtas (P2 4.5). 132 eventos até cinco anos mantidos e levados à legenda da Tabela 2 (P4 6.3).

### 3.3 Modelos e o alcance da comparação
- Assimetrias mantidas antes dos resultados (decisão congelada) e seguidas do parágrafo "o que a comparação pode dizer": pergunta de adoção, não competição entre famílias; um empate é compatível com as duas hipóteses; D13 citado (P1 motivo 3; P3 4.1; P4 3.2).

### 3.4 Validação e métricas
- C de Uno explicado "como a AUC", com a diferença para o C de Harrell em uma frase (P1 4.5). Secundárias, calibração e curva de decisão explicadas em linguagem direta.

### 3.5 Como se lê uma diferença entre modelos
- Bootstrap e teste corrigido explicados pelo que cada um captura (pacientes e retreino); "depois de conhecidos os resultados" em vez de "posterior à auditoria" (P3 2.3); regra combinada declarada como posterior e mais exigente, com a leitura só pelo plano mantida (decisão congelada; P1 4.1; P2 4.1; P4 4.1).

### 3.6 Análises complementares
- Separa as quatro análises de apoio previstas no plano das duas do plano complementar, "registrado antes de ser executado, mas depois dos resultados principais" (P3 3.a, 4.2; P4 4.2).
- Fórmula de 1989: duas versões explicadas (final, estimada nos 418, usada na coorte e avaliada onde foi estimada; inicial, estimada nos 312, usada nos 106) (P1 4.4; P2 4.2; P4 4.2); não cega.
- Declara a emenda após a auditoria da primeira execução e a troca de métrica do otimismo: previsto C de Harrell (`\otimRSFHarrell`), relatado C de Uno (`\otimRSF`) (H6; P3 2.6, 4.2, 4.5). Registrado também em `sbcas/DESVIOS.md` (D16, complemento).

### 4.1 Discriminação: a resposta para cada modelo
- Resposta por modelo, em frases curtas (P1 4.3; P2 4.3; P4 4.4).
- Precisão alcançada como macro: meia-largura dos intervalos pareados pelo plano (`\meiaLargPlanoMin/Max`) e pelo teste corrigido (`\meiaLargTcMin/Max`), com 132 eventos até cinco anos (H9; P1 6.2; P3 1.7).
- Sensibilidade só óbito resumida no texto por macros (`\obitoDif*`, `\obitoSupPlano*`, `\nbSupObito*`); o bloco completo foi para `tabelas/leitura_obito.tex` (suplementar) (P2 motivo 3).
- Escopo "no C de Uno" explicitado antes da frase sobre a AUC (P2 6.3); "as demais não diferiram no desfecho principal" (P3 3.g).

### Tabela 2
- Uma linha por modelo, "média (desvio)"; legenda com 186 eventos no seguimento e 132 até cinco anos (P4 6.3).

### Tabela 3
- Só desfecho principal: bloco contra o Cox reestimado (referência do plano) e bloco contra a fórmula de 1989 (análise posterior).
- Legenda diz como ler, explica o asterisco (comparação à parte, IC 95%) e o Bonferroni das três comparações de AM, e que o teste corrigido é centrado na média por partição (H8; P1 6.3; P2 motivo 3; P3 1.3 e 2.2; P4 6.7).

### 4.2 Calibração e utilidade clínica
- Cox penalizado identificado como "o modelo de maior C" ao relatar sua calibração (P2 5.7); Brier "maior, de modo mais nítido na RSF de 5 variáveis" (P3 3.e); curva de decisão reescrita (P2 4.4; P4 4.5). Números por macro (`\oeMin/Max`, `\rsfDezQuintilPrev/Obs`, `\dcMaxDifPorCem`).

### Figura 1 (única)
- Calibração (referência e RSF) e curva de decisão lado a lado, com uma só descrição da regra de seleção da RSF (P1 6.8). O painel de importância por permutação saiu do artigo (figura no suplementar); os valores seguem no texto.

### 4.3 Contra a fórmula de 1989 e fora do treino (análises posteriores)
- Fórmula no desfecho principal e, com honestidade, no desfecho só óbito: fórmula nominalmente à frente do Cox reestimado (bootstrap sem zero, teste corrigido com zero) e da RSF de 5 variáveis só no bootstrap, "indício, não demonstração" (H1; P2 5.3 e 6.5; P3 2.5 e 5.2; P4 6.1; limite da auditoria D14-D16, item c).
- Subgrupo: "até +0,016 contra o Cox reestimado e até +0,024 contra a fórmula inicial" (H4; P1 6.1; P2 5.6 e 6.2).
- Riscos proporcionais sem a insinuação de que a flexibilidade da floresta deveria ter ajudado (P1 5.7); importância por permutação: bilirrubina domina e, da quarta posição em diante, a ordem está dentro do desvio (P2 5.4; P3 3.f).

### 4.4 De onde vêm os ganhos aparentes?
- "Entre os contrastes em C de Uno, o maior foi..." (H10; P4 5.4); populações declaradas (312 para o otimismo, 418 para as diferenças) (P1 5.2 e 6.6; P3 2.6).
- A linha da fórmula "muda também o modelo, e por isso não isola o efeito de avaliar na amostra de derivação" (H2; P4 2.3 e 6.2).
- Vazamento identificado como medido na classificação anterior ao plano (P2 6.7); IC da classificação com o nível declarado ("intervalo de Bonferroni para 5 comparações") (P3 3.i).

### Tabela 4
- Três blocos: fontes de ganho aparente (sem IC pareado), escolhas que pouco mudaram o resultado (IC 95% pareado; a linha da fórmula rotulada "muda também o modelo") e sensibilidade da inferência ("não é ganho") (H2; P1 6.5; P3 3.j; P4 2.3, 3.3 e 6.9).
- Linha da fórmula: comparador identificado como o Cox ajustado só nos 312, fora da partição (P2 6.8).

### 5. Discussão
- Abre com "a resposta é 'não demonstrado', e não 'não supera'"; precisão com 132 eventos (H9); regra combinada posterior; nulo era o mais provável dado o desenho, logo não é prova de equivalência e vale para o cenário de adoção (P2 3 motivo 2; P1 motivo 3; limite da auditoria, item b).
- "Quantifica quais escolhas de avaliação importam e quais não" em vez de "mostra por que a forma de avaliar importa" (P1 5.1 e 3 motivo 1); diz que Graf et al. não avaliam no treino (.632+) e que o otimismo medido não explica o 0,855 (P2 5.2; limite da auditoria, item d).
- Graf et al.: "o 0,776 relatado lá vem de outro protocolo e de um modelo que o texto não identifica, e não é diretamente comparável" (H7; P3 3.d).
- "Acurácias próximas de 90% em dados sintéticos derivados da coorte", sem "neste mesmo conjunto" (H11; P4 5.3).
- Frase sobre o SUS como destino de transferência retirada (P2 5.5); recado geral fala em "modelo clínico pertinente à população e ao momento da predição" (P4 3.2).
- Limitações incluem as análises posteriores, a falta de cegamento e a regra combinada (P3 4.6).
- A hipótese "sobra pouco para a floresta aprender" saiu por espaço.

### 6. Conclusão
- Separa plano prévio de análises posteriores (H3; P3 3.b); "não" e "não sabemos" por modelo; cenário de adoção que favorece a referência (P1 3 motivo 2 e 3).

### Declaração de uso de IA
- Uma frase sobre as decisões humanas (pergunta, desenho, plano, regra de leitura, desvios, interpretação) (P1 observações finais).

### Arquivos
- `gerar_tabelas.py`: macros novas (ver cabeçalho das linhas "Fable" na função `macros`), `fe()` para o abstract, `tabela_fontes()` em blocos, `tabela_leitura()` parametrizada (principal e fórmula no artigo; só óbito em `leitura_obito.tex`), `tabela_desempenho()` em uma linha por modelo.
- `referencias.bib`: retirada a nota "Com discussão" da entrada de Cox (1972); a entrada de Beuers et al. (2015) deixou de ser citada (nomenclatura dita sem citação) e a de Cançado et al. (2022) também, ambas por espaço; as entradas permanecem no `.bib`.
- `sbcas/DESVIOS.md`: complementos em D14 (resultado do óbito contra a fórmula) e D16 (troca de métrica do otimismo), sem apagar linhas.
- `sbcas/MATERIAL_SUPLEMENTAR.md`: apontadores para `leitura_obito.tex` e para a figura de importância.

## Decisões congeladas: confirmação

| Decisão | Situação |
|---|---|
| Título T1 exato | Mantido, caractere a caractere. |
| Leitura conservadora da margem (regra combinada no resumo, discussão e conclusão; leitura só do plano relatada) | Mantida: "não (só no plano)" na Tabela 3, limite de 0,0197 e sementes na Seção 4.1, "pela regra só do plano, a RSF de 17 também teria o ganho descartado" na Discussão. |
| Parágrafo Brasil/SUS | Encolhido a duas linhas, não removido. |
| Cinco passos como boas práticas conhecidas, sem "replicável" | Mantido; Tabela 1 compacta; sem reivindicação de método novo. |
| Cronologia honesta (plano após classificação; D2 a D8 entre execuções; D9 a D17 após; plano complementar posterior e não cego) | Mantida e concentrada na Seção 3.1 e na 3.6; emenda após a primeira execução de D16 declarada. |
| Assimetrias antes dos resultados | Seção 3.3, agora com o alcance da comparação. |
| Sem boosting nem redes neurais na sobrevivência | Mantido nas Limitações. |

## Limites da auditoria e das notas de literatura: confirmação

- Não se diz que a vantagem de derivação "vale zero"; a Tabela 4 rotula o contraste como não isolado e a Seção 3.3 mantém a seleção das variáveis como assimetria.
- "Nenhum ganho demonstrado", nunca equivalência (Discussão e Conclusão).
- No óbito, RSF de 5 abaixo da fórmula é "indício, não uma demonstração".
- O otimismo medido "não explica o C de 0,855" de Graf et al. (.632+).
- "O 0,776 relatado lá vem de outro protocolo e de um modelo que o texto não identifica".
- Fórmula de uso (final) estimada nos 418; inicial nos 312 (Seção 3.6).

## Conferências finais
- Contagem do caractere travessão (U+2014) em `main.tex`: 0 (linha "Travessões" do `log_compilacao.txt`).
- Números de resultado no texto: todos por macro; os únicos decimais literais são 0,855 e 0,776 (de Graf et al.), 0,02 (margem) e versões de software.
- `log_compilacao.txt`: 12 páginas, 0 erros, 0 caixas fora da margem, abstract e resumo com 10 linhas.
- Revisão duplo-cega: sem nomes, instituições, disciplina ou URL identificável (só o endereço anonimizado).

# Pendências para decisão do autor (versão de junção, ramo `sbcas-2027-juncao`)

Questões que os pareceres levantaram e que a junção, por instrução do briefing, não decidiu. O texto ficou como em B.

## 1. Identificador do commit do plano (`677a281`) e a data 01/11/2026 na Seção 3

- **Como está:** a Seção 3 diz que o plano "foi registrado em 01/11/2026 no controle de versões do repositório", sem o hash do commit (como em B). A versão A trazia "(commit `677a281`)".
- **O que o ChatGPT pede:** incluir o identificador exato do commit, por rastreabilidade (parecer `4_chatgpt.txt`, seção 7, Métodos).
- **O que o Gemini alerta:** (a) o hash permite localizar o repositório original fora do espelho anônimo, se ele estiver indexado, o que pode quebrar o duplo-cego; (b) a data 01/11/2026 pode surpreender um revisor cético, porque plano, execuções, auditorias, plano complementar, dezessete desvios e redação cabem em poucos dias, e alguém pode até ler a data no formato norte-americano (parecer `3_gemini.txt`, seção 5, problema comum 1).
- **O que não pode mudar:** a data é verdadeira e fica. A cronologia está em `sbcas/CRONOLOGIA.md` e `sbcas/DESVIOS.md`.
- **Opções para o autor:** (i) manter como está (data, sem hash); (ii) acrescentar o hash curto, aceitando o risco de identificação apontado pelo Gemini; (iii) manter sem hash e acrescentar meia frase de contexto, por exemplo "a cronologia completa, com os identificadores dos commits, está no repositório anonimizado", que dá rastreabilidade sem expor o hash no PDF. A opção (iii) custa cerca de uma linha; a página 12 tem folga de duas a três linhas.

## 2. Hipótese "sobra pouco para a floresta aprender" (A, Discussão)

- **Como está:** fora do corpo. O Gemini a queria; o ChatGPT a considera explicação causal não testada. O plano da junção previa recolocá-la como hipótese marcada e ligada a trabalho futuro, mas ela não coube: no ajuste de páginas foi o conteúdo de menor custo de remoção entre os que restavam, e nenhuma versão comitada da junção a contém.
- **Se o autor quiser recolocá-la:** a forma redigida é "e testar a hipótese, aqui não verificada, de que uma referência com relações já em logaritmo e informação concentrada na bilirrubina (Figura 1e) deixe pouco para a floresta aprender", no último período da Conclusão. Custa cerca de uma linha e meia; exige tirar outra linha e meia em algum lugar.

## 3. Calibração e benefício líquido no resumo

- **Como está:** o resumo e o abstract não mencionam calibração nem benefício líquido (como em B). O Gemini, o Sonnet e o Opus pediam uma frase curta "se coubesse"; não coube nas 10 linhas junto com as qualificações exigidas pelo Opus e pelo ChatGPT para o +0,043 (sem intervalo) e para a fórmula de 1989 (análise posterior, avaliada onde foi estimada), que têm prioridade por serem correções de alcance e não preferências.
- **Se o autor preferir a frase de calibração:** o resumo e o abstract estão em exatamente 10 linhas, então a frase só entra se outra sair. A troca viável é retirar "mais que qualquer diferença entre modelos" (fim do resumo) e acrescentar ", nem em calibração ou benefício líquido" logo após "(0,831; diferenças de −0,014 a +0,015)"; o mesmo no abstract. É uma escolha entre duas frases de peso parecido: a comparação de grandezas do otimismo de treino ou a cobertura das três dimensões avaliadas.

## 4. Referências retiradas por espaço

Para fechar em 12 páginas saíram do texto, e portanto da lista, cinco citações de apoio, nenhuma de resultado: Fleming e Harrington (1991, livro clássico sobre a coorte), Davidson-Pilon (2019, `lifelines`, que segue citado no suplementar), Varma e Simon (2006, validação aninhada), Harrell et al. (1982, C de Harrell) e Cox (1972, regressão de Cox; o modelo de Mayo segue citado por Dickson et al. 1989). As entradas continuam em `referencias.bib`. Se o autor quiser qualquer uma de volta, cada entrada custa duas a três linhas.

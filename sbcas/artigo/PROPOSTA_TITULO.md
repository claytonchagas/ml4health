# Proposta de título (decisão do autor: mudar; rodada de fluidez)

Título atual: "O aprendizado de máquina realmente supera o modelo clínico? Um estudo de caso com plano prévio na colangite biliar primária".

Por que mudar: os quatro pareceres isolados da versão `7c1e9ed` apontaram "com plano prévio" como mais forte que a cronologia (Sonnet X1, Opus 6 e 14, ChatGPT 04, Gemini crítica 1). Os fatos: o registro é um commit no repositório da autoria; o plano foi escrito depois de uma análise de classificação nos mesmos dados; há dezessete desvios, nove posteriores aos resultados; a regra de leitura que produz a manchete é posterior. Todos elogiaram a pergunta inicial e a franqueza do relato.

Restrições: honesto quanto ao que foi pré-especificado; legível para computação; sem prometer decisão clínica atual; de preferência mantendo a pergunta inicial.

Como trocar: o título está na macro `\titulo`, no início de `main.tex` (um único lugar). As quebras de linha (`\\`) são manuais e devem ser conferidas na página 1 depois da troca.

## Candidatos

| # | Título | Prós | Contras |
|---|---|---|---|
| T1 (recomendado, aplicado) | O aprendizado de máquina realmente supera o modelo clínico? Um estudo de caso com plano registrado e desvios declarados na colangite biliar primária | Mantém a pergunta. "Registrado" descreve o que existe (um commit datado), sem prometer registro independente nem anterioridade a toda exploração. "Desvios declarados" antecipa o que o revisor vai encontrar na Seção 3.6 e transforma a franqueza, o argumento a favor mais citado pelos quatro leitores, em parte da proposta. Nenhum leitor que ler o título e depois os dezessete desvios se sentirá enganado. | Mais longo que o atual (três linhas na página 1, como hoje). "Desvios declarados" pode soar defensivo a um revisor apressado; a aposta é que, no SBCAS, o relato honesto pesa mais que a aparência de perfeição. |
| T2 | O aprendizado de máquina realmente supera o modelo clínico? Um estudo de caso com plano registrado na colangite biliar primária | Mudança mínima e discreta; resolve a objeção literal a "prévio"; cabe em duas ou três linhas. | "Plano registrado" ainda pode ser lido como pré-registro formal; a honestidade fica só no corpo. Foi a sugestão do Opus (crítica 6). |
| T3 | O aprendizado de máquina realmente supera o modelo clínico? Comparação pareada, com protocolo registrado e auditável, na colangite biliar primária | Destaca o que o estudo tem de melhor no desenho (pareamento, protocolo público e auditado); "auditável" foi a palavra do Gemini. | Perde "estudo de caso", que delimita o alcance; "auditável" promete que o revisor vai ao repositório, o que raramente acontece; o título fica mais técnico. |
| T4 | Florestas de sobrevivência superam o modelo de Mayo? Um estudo de caso com plano registrado na colangite biliar primária | Escopo exato (sugestão do Opus, crítica 14): nomeia a família de modelos e a referência, sem generalizar para "o aprendizado de máquina". | Perde a pergunta geral que os leitores elogiaram e o alcance ao Cox penalizado; "modelo de Mayo" não diz nada a um leitor de computação sem o subtítulo; a mensagem do artigo (julgar o AM pelo que acrescenta ao modelo clínico) fica menos visível. |
| T5 | O aprendizado de máquina acrescenta algo ao modelo clínico? Um estudo de caso de avaliação incremental, com plano registrado, na colangite biliar primária | Formula a pergunta como o artigo a responde (ganho incremental, não "superar"); "avaliação incremental" é o termo do ChatGPT. | Troca a pergunta que os leitores já conhecem e elogiaram; "avaliação incremental" não é termo corrente em computação; título longo. |

## Recomendação

T1. Se o autor preferir discrição, T2 é a alternativa segura e mais curta. Em qualquer caso, o resumo e o abstract já dizem que o plano foi registrado antes da análise de sobrevivência e depois de uma classificação exploratória, e a Seção 3 explica o que o registro é e o que não é.

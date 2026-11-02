# Roteiro de auditoria independente (Codex)

Este repositório é construído por um agente (Claude) e auditado por outro (Codex), executado localmente pelo autor. O auditor **não corrige nada**: produz um relatório com achados, cada um com evidência (arquivo e linha, ou célula do notebook), gravidade e sugestão. As correções são feitas depois, uma por vez.

## Como rodar

```bash
git clone <endereço do repositório> && cd ml4health
pip install -r requirements.txt
# Em um terminal: o painel de acompanhamento
bash auditoria/painel.sh
# Em outro terminal: o Codex, com o prompt da passada desejada
codex "$(cat auditoria/passada_A.md)"
```

Cada passada grava seu relatório em `auditoria/relatorio_<passada>.md`. O painel mostra, a cada 2 segundos, o tempo decorrido, os arquivos alterados no repositório e o tamanho e as últimas linhas do relatório em produção.

## Formato obrigatório de cada achado

```
### [A|B|C]-NN  Título curto
- Gravidade: bloqueante | importante | menor
- Evidência: arquivo:linha (ou célula N do notebook), trecho citado
- Problema: o que está errado e por quê
- Sugestão: o que mudar (sem aplicar)
```

Ao final, uma tabela-resumo com todos os achados e um veredito: "aprovado", "aprovado com ressalvas" ou "reprovado".

## Passadas

| Passada | Quando | Prompt |
|---|---|---|
| A. Método e código | Antes do artigo | [`auditoria/passada_A.md`](auditoria/passada_A.md) |
| A2. Reauditoria de método e código | Após corrigir os achados da passada A | [`auditoria/passada_A2.md`](auditoria/passada_A2.md) |
| B. Afirmações e números | Após o rascunho do artigo | [`auditoria/passada_B.md`](auditoria/passada_B.md) |
| C. Conformidade e referências | No fim | [`auditoria/passada_C.md`](auditoria/passada_C.md) |
| C2. Fechamento | Após corrigir os achados da passada C | [`auditoria/passada_C2.md`](auditoria/passada_C2.md) |
| A3. Análise de sobrevivência (versão SBCAS, ramo `sbcas-2027`) | Após executar o plano registrado | [`auditoria/passada_A3.md`](auditoria/passada_A3.md) |

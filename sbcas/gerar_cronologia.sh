#!/usr/bin/env bash
# Gera sbcas/CRONOLOGIA.md: todos os commits do repositório (hash curto, data e hora, mensagem), em ordem.
# Motivo: o espelho anonimizado para a revisão serve só os arquivos, sem o histórico do git; esta lista permite
# conferir que o plano (commit 677a281) antecede os resultados da análise de sobrevivência.
# Uso, na raiz do repositório: bash sbcas/gerar_cronologia.sh
set -eu
cd "$(git rev-parse --show-toplevel)"
{
  echo "# Cronologia do repositório"
  echo
  echo "Gerado por \`sbcas/gerar_cronologia.sh\` a partir do histórico do git (horário de Brasília, UTC-3)."
  echo "Marcos: plano registrado em \`677a281\`; primeira execução em \`70cc304\` e \`859b37d\`; auditoria A3 e desvios D1 a D8 de \`f544959\` a \`012bfaa\`; execução final em \`ebcc88c\` e \`bbcf04d\`."
  echo
  echo "| Commit | Data e hora | Mensagem |"
  echo "|---|---|---|"
  git log --reverse --format="| \`%h\` | %ad | %s |" --date=format:'%Y-%m-%d %H:%M'
} > sbcas/CRONOLOGIA.md
echo "sbcas/CRONOLOGIA.md: $(git rev-list --count HEAD) commits"

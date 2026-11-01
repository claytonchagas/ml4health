#!/usr/bin/env bash
# Painel de acompanhamento da auditoria: atualiza a cada 2 s. Uso: bash auditoria/painel.sh
inicio=$(date +%s)
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
while true; do
  clear
  agora=$(date +%s); dec=$((agora - inicio))
  printf "\033[1m=== Auditoria ml4health ===\033[0m   %s   decorrido: %02d:%02d\n\n" "$(date +%H:%M:%S)" $((dec/60)) $((dec%60))
  echo "Relatórios:"
  for r in A A2 B C; do
    f="auditoria/relatorio_$r.md"
    if [ -f "$f" ]; then
      n=$(grep -c '^### ' "$f"); b=$(grep -ci 'Gravidade: bloqueante' "$f"); i=$(grep -ci 'Gravidade: importante' "$f")
      printf "  %-2s %6s bytes  achados: %-3s (bloqueantes: %s, importantes: %s)\n" "$r" "$(wc -c <"$f")" "$n" "$b" "$i"
    else
      printf "  %-2s (ainda não iniciado)\n" "$r"
    fi
  done
  echo; echo "Arquivos alterados no repositório (não deveria haver nada além de auditoria/):"
  git status --short | sed 's/^/  /' | head -15
  ultimo=$(ls -t auditoria/relatorio_*.md 2>/dev/null | head -1)
  if [ -n "$ultimo" ]; then echo; echo "Últimas linhas de $ultimo:"; tail -12 "$ultimo" | sed 's/^/  /'; fi
  sleep 2
done

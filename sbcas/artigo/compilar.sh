#!/usr/bin/env bash
# Compila o artigo SBCAS num diretório temporário (sem sujar a pasta) e grava log_compilacao.txt
# com versão do TeX, páginas, erros, citações/referências indefinidas, caixas fora da margem e
# linhas do abstract e do resumo na página 1 (o modelo da SBC limita cada um a 10 linhas).
# Uso, na raiz do repositório: bash sbcas/artigo/compilar.sh
set -u
cd "$(dirname "$0")"
T=$(mktemp -d)
latexmk -pdf -interaction=nonstopmode -outdir="$T" main.tex >/dev/null 2>&1
saida=$?
L="$T/main.log"
contar() { grep -cE "$1" "$L" 2>/dev/null || true; }
linhas_bloco() {  # linhas de um bloco da página 1, de "$1" até a primeira linha em branco
  pdftotext -layout -f 1 -l 1 "$T/main.pdf" - 2>/dev/null | awk -v ini="$1" '
    index($0, ini) {em=1} em && /^[[:space:]]*$/ {exit} em {n++} END {print n+0}'
}
{
  echo "Compilação do artigo SBCAS ($(date '+%Y-%m-%d %H:%M'))"
  echo "TeX: $(pdflatex --version | head -1)"
  echo "Código de saída do latexmk: $saida"
  echo "Páginas: $(pdfinfo "$T/main.pdf" 2>/dev/null | awk '/^Pages/ {print $2}')"
  echo "Erros (linhas iniciadas por !): $(contar '^!')"
  echo "Citações indefinidas: $(contar 'Citation .* undefined')"
  echo "Referências indefinidas: $(contar 'Reference .* undefined')"
  echo "Caixas fora da margem (Overfull hbox): $(contar 'Overfull \\hbox')"
  echo "Linhas do abstract: $(linhas_bloco 'Abstract.')"
  echo "Linhas do resumo: $(linhas_bloco 'Resumo.')"
  echo "Travessões (U+2014) no main.tex: $(grep -c '—' main.tex)"
} | tee log_compilacao.txt
cp "$T/main.pdf" main.pdf 2>/dev/null
rm -rf "$T"

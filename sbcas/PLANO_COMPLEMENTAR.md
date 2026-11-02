# Plano complementar (análises D14 a D17), registrado antes de executá-las

Data: 02/11/2026. Origem: terceira revisão tripla e consulta independente (modelo de IA externo), depois dos resultados finais do plano de 01/11/2026 (commit `677a281`). O plano original não é alterado: a referência principal continua o Cox reestimado com as cinco variáveis de Mayo, e a regra de leitura (bootstrap pareado, teste t corrigido e regra combinada de D11) é a mesma. Todas as análises abaixo são posteriores aos resultados e serão relatadas como tais, qualquer que seja o resultado. Um cálculo exploratório da fórmula de 1989, feito fora do repositório pelo consultor, já é conhecido; por isso D14 não é cego e é declarado assim.

## D14. Fórmula de Mayo publicada em 1989 como segunda referência (só discriminação)

- Escore: R = coeficientes publicados por Dickson et al. (1989) para idade, ln bilirrubina, ln albumina, ln tempo de protrombina e edema, conferidos no artigo original antes de rodar; sem reajuste. Ausentes (2 pacientes): mediana do treino de cada partição, como no pipeline.
- Desfechos: principal (óbito ou transplante) e sensibilidade (só óbito).
- Métrica: C de Uno em 5 anos sobre o escore (só a ordenação; sem sobrevida basal publicada, sem calibração nem curva de decisão).
- Comparações: cada um dos três modelos de AM e o Cox reestimado contra a fórmula, com o mesmo bootstrap pareado (2.000, semente 2026, Bonferroni para 3 comparações de AM) e o mesmo teste t corrigido (C da fórmula em cada uma das 25 partições de teste; variância de retreino da fórmula nula por construção). A diferença Cox reestimado menos fórmula é relatada à parte, com IC 95%.
- Vantagem de derivação: nos 312 randomizados, C da fórmula fixa (avaliada na amostra de derivação) contra C do Cox reestimado fora da partição.
- Leitura: a mesma regra combinada de D11. Nenhum resultado muda a referência principal.

## D15. Comparação pareada no subgrupo dos 106 não randomizados (completa D10)

- Treino nos 312, teste nos 106 (42 eventos), predições já salvas.
- Diferenças de C de Uno de cada modelo contra o Cox reestimado e contra a fórmula de 1989, bootstrap pareado de pacientes (2.000, semente 2026), IC 95%. Leitura descritiva; não entra na regra da margem.

## D16. Comparador alternativo e avaliação dentro da amostra nos 312 randomizados (exploratório)

- Ressalva de fonte: Graf et al. não dizem explicitamente que o C de 0,776 vem do modelo de 7 variáveis (notas_literatura.md). Por isso não se fala em reproduzir Graf: o modelo é "Cox com as sete variáveis do conjunto final de Graf et al." (idade, bilirrubina, albumina, fosfatase alcalina, plaquetas, protrombina, estágio), na mesma validação cruzada 5×5 e nas mesmas partições restritas aos 312.
- Métricas: C de Harrell e C de Uno, pareados (bootstrap, IC 95%) com o Cox de Mayo reestimado e com a RSF de 17 variáveis nos mesmos 312.
- Otimismo de avaliação: C de Harrell da RSF de 17 variáveis com treino igual ao teste nos 312, contra o valor fora da partição.
- Critério de parada: se o modelo de 7 variáveis não puder ser ajustado de forma estável (convergência ou ausências) até terça às 18h, D16 é abandonado e registrado como tal.

## D17. Importância por permutação nas 25 partições (completa D10)

- Mesmo procedimento atual, estendido às 25 partições com os hiperparâmetros salvos. Opcional; executado só se o tempo de máquina permitir até terça às 18h.

## Apresentação prevista

- Tabela 3 ganha a fórmula de 1989 como segunda referência.
- Tabela 4 passa a "Fontes de ganho aparente medidas neste conjunto": vazamento (linha d atual), classificação com exclusão de censurados (linha a atual), reajuste da referência (D14), comparador alternativo e avaliação dentro da amostra (D16), semente do bootstrap (D12). Cada linha diz como foi medida e o tamanho; métricas em escalas diferentes não são somadas nem comparadas.
- Seção 3.4 ou 4.1: frase sobre a precisão alcançada (meia-largura dos intervalos pareados da ordem da margem).
- Tudo gerado por script a partir de CSV, com macros; auditoria independente antes de entrar no texto.

## Emenda 1 (02/11/2026, antes de executar D14 e D15)

Ao preparar o script, conferiu-se em `experimento.py` e no relatório de auditoria A (verificado contra o artigo original) que Dickson et al. (1989) publicam duas versões: o modelo **final**, cuja fórmula de uso (p. 6) foi estimada com os **418** pacientes desta coorte, e o modelo **inicial** (Tabela 2, p. 4), estimado só com os **312** randomizados. Isso corrige a premissa do consultor de que a fórmula de uso foi derivada nos 312. Consequências, fixadas antes de rodar:

- D14 na coorte inteira usa a fórmula **final** (a que a clínica usa). Ela é avaliada dentro da própria amostra de estimação, logo seu C é otimista; os modelos de AM e o Cox reestimado são avaliados fora da partição. A comparação favorece a fórmula e será descrita assim.
- A medida da vantagem de derivação nos 312 usa a fórmula **inicial** (estimada nos 312), avaliada nos 312, contra o Cox reestimado fora da partição nos mesmos 312; a final é relatada ao lado.
- D15 (106 não randomizados) usa a fórmula **inicial**, que não viu esses pacientes: é a única comparação em que a fórmula publicada e os modelos treinados nos 312 são avaliados fora da amostra de estimação de ambos. A final é relatada ao lado, como contaminada.
- Imputação dos 2 tempos de protrombina ausentes: mediana do treino de cada partição (D14) ou dos 312 (D15).

## Emenda 2 (02/11/2026, após a auditoria independente de D14 a D16 e antes de qualquer texto do artigo)

Correções de procedimento apontadas pela auditoria, aplicadas em `comparador_graf.py` e reexecutadas:
- RSF de 17 variáveis em D16: os hiperparâmetros passam a ser, em cada partição, os escolhidos no treino da mesma partição da validação principal (`hiperparametros.csv`); antes vinham de uma busca nos mesmos 312 (vazamento leve, cerca de 0,003 no C).
- Otimismo de avaliar dentro da amostra: C agregado fora da partição contra C dentro da amostra (mesma base de cálculo); antes comparava com a média de C por partição.
- Vantagem de derivação: comparada com o Cox de Mayo reestimado só nos 312 (`graf312_derivacao.csv`); `mayo1989_derivacao.csv`, com o Cox treinado nas partições dos 418, fica como registro.
A auditoria também fixou a leitura: (a) D14 mede o efeito de reestimar os coeficientes, não o da seleção das variáveis; (b) "nenhum ganho demonstrado sobre a fórmula", sem leitura de equivalência; (c) no óbito, a RSF de 5 variáveis abaixo da fórmula é só indício (o teste corrigido não confirma); (d) o otimismo medido aqui não explica o C de 0,855 de Graf et al., obtido por bootstrap .632+.

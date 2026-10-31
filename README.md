# Aprendizado de Máquina versus Escore de Mayo: qual vale mais a pena na predição de óbito em cirrose biliar primária?

**Disciplina:** TCC00367, Introdução ao Aprendizado de Máquina para Saúde (PGC/UFF)
**Autor:** Clayton Escouper das Chagas
**Notebook de demonstração:** [`ml4health_cbp_mayo.ipynb`](ml4health_cbp_mayo.ipynb)

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/claytonchagas/ml4health/blob/main/ml4health_cbp_mayo.ipynb)

---

## 1. Motivação e objetivo

A cirrose biliar primária (CBP; desde 2015, colangite biliar primária) é uma doença hepática crônica e autoimune, de progressão muito variável entre pacientes. Estimar o risco individual de óbito na primeira avaliação orienta a intensidade do acompanhamento e o momento de encaminhamento ao transplante.

Desde 1989 existe o **Escore de Risco de Mayo** (Dickson et al., 1989), uma regressão com cinco variáveis de rotina (idade, bilirrubina, albumina, tempo de protrombina e edema), derivada exatamente nos dados usados aqui. Modelos de aprendizado de máquina (AM) prometem mais precisão, mas exigem mais variáveis, mais pacientes com dados completos e mais infraestrutura, e perdem a transparência de uma fórmula. Revisões sistemáticas não encontraram vantagem do AM sobre a regressão logística em predição clínica quando a comparação é metodologicamente limpa (Christodoulou et al., 2019).

**Objetivo.** Medir o **valor incremental** do AM sobre o Escore de Mayo na predição de óbito em até 5 anos, e o custo desse ganho. *Valor incremental* é o benefício adicional que um novo modelo traz em comparação com o método clínico já usado na rotina: não basta o modelo ser preciso, ele precisa ser melhor do que o que os médicos já fazem para justificar custo, tempo e mudança no fluxo de trabalho.

**Perguntas.**

1. Em que condições random forest e XGBoost superam, empatam ou perdem para o Escore de Mayo, em discriminação e em calibração?
2. O ganho, se houver, vem do algoritmo ou das variáveis extras?
3. Quanto o enquadramento da competição Kaggle PS3E26 (prever `Status` com `N_Days` como entrada) infla o desempenho?

**Desenho 2 x 2.** Duas famílias de métodos (regressão e AM), cada uma com as 5 variáveis de Mayo e com as 17 variáveis do dataset, nos mesmos folds. A leitura vertical (mesmas variáveis) isola o efeito do algoritmo; a horizontal (mesmo algoritmo), o efeito das variáveis extras.

---

## 2. Descrição do dataset

### 2.1 Dados

- **Fonte:** UCI Machine Learning Repository, dataset 878, *Cirrhosis Patient Survival Prediction*, DOI [10.24432/C5R02G](https://doi.org/10.24432/C5R02G), licença CC BY 4.0. Link: <https://archive.ics.uci.edu/dataset/878/cirrhosis+patient+survival+prediction+dataset-1>
- **Origem:** ensaio clínico da Mayo Clinic (1974 a 1984) sobre D-penicilamina em CBP; base do artigo de Dickson et al. (1989). É o mesmo conjunto disponível como `survival::pbc` no R.
- **População:** 418 pacientes (312 randomizados no ensaio, com exames completos; 106 elegíveis que recusaram a randomização e só têm as medidas de rotina). Mais de 90% mulheres.
- **Unidade de observação:** paciente; todas as variáveis medidas na data de registro (linha de base).
- **Variáveis de entrada (17):** idade, sexo, tratamento (D-penicilamina ou placebo), ascite, hepatomegalia, aranhas vasculares, edema (3 níveis), bilirrubina, colesterol, albumina, cobre urinário, fosfatase alcalina, AST (SGOT/TGO), triglicerídeos, plaquetas, tempo de protrombina, estágio histológico.
- **Variáveis de desfecho:** `Status` (C: censurado, 232; D: óbito, 161; CL: transplante, 25) e `N_Days` (dias até óbito, transplante ou fim do estudo em julho de 1986).

**Dados ausentes (418 pacientes):**

| Variável | Ausentes | Motivo |
|---|---|---|
| Triglicerídeos | 136 | 106 fora do ensaio + 30 no ensaio |
| Colesterol | 134 | 106 fora do ensaio + 28 no ensaio |
| Cobre urinário | 108 | 106 fora do ensaio + 2 no ensaio |
| Tratamento, ascite, hepatomegalia, aranhas, fosfatase alcalina, AST | 106 | fora do ensaio (ausência por desenho) |
| Plaquetas | 11 | |
| Estágio | 6 | |
| Tempo de protrombina | 2 | |

### 2.2 Preparação e pré-processamento

1. **Rótulo de 5 anos (1.826 dias).** `Status = D` e `N_Days ≤ 1826` → 1 (óbito); `N_Days > 1826` → 0 (vivo aos 5 anos); `Status ∈ {C, CL}` e `N_Days ≤ 1826` → excluído (saiu antes dos 5 anos sem óbito observado; censura). Resultado: **312 pacientes rotulados, 115 óbitos (36,9%), 106 excluídos.**
2. **`N_Days` nunca é variável de entrada.** É o tempo até o desfecho, conhecido só depois dele. Entra apenas na construção do rótulo, e no braço de controle de vazamento, rodado de propósito.
3. **Codificação:** idade em anos; sexo e sinais clínicos em 0/1; edema em 0, 0,5 e 1, como no Escore de Mayo; tratamento em 0/1 com ausência mantida.
4. **Transformação:** na regressão logística, laboratórios assimétricos em logaritmo (bilirrubina, albumina e protrombina na especificação de Mayo; também colesterol, cobre, fosfatase alcalina, AST e triglicerídeos no modelo de 17 variáveis). Árvores não precisam de transformação.
5. **Imputação, dentro de cada partição de treino:** mediana para as 5 variáveis de Mayo (só 2 pacientes rotulados têm algum ausente); imputação iterativa para as 17 variáveis; o XGBoost trata ausentes nativamente.
6. **Sem balanceamento artificial de classes**, porque distorce as probabilidades previstas (Christodoulou et al., 2019).

### 2.3 Link para a versão usada

O notebook baixa o dataset oficial pelo pacote `ucimlrepo` (id 878). Se o servidor do UCI não responder, usa automaticamente o espelho Rdatasets do mesmo conjunto: <https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/survival/pbc.csv>. Os resultados deste README foram obtidos com o espelho; as contagens (418 pacientes, 232/161/25 por `Status`, 106 sem tratamento) coincidem com o UCI 878.

---

## 3. Modelo de aprendizado de máquina

### 3.1 Formalização matemática

Seja $\mathbf{x}_i \in \mathbb{R}^p$ o vetor de variáveis de linha de base do paciente $i$ ($p = 5$ ou $p = 17$) e $y_i \in \{0, 1\}$ o indicador de óbito em até 5 anos. Cada modelo estima $\hat{\pi}(\mathbf{x}) = \hat{P}(y = 1 \mid \mathbf{x})$.

**Escore de Risco de Mayo (1989), coeficientes publicados:**

$$R = 0{,}039\,\text{idade} + 0{,}871\ln(\text{bilirrubina}) - 2{,}53\ln(\text{albumina}) + 2{,}38\ln(\text{protrombina}) + 0{,}859\,\text{edema}$$

Os coeficientes não são reestimados. Para converter $R$ em probabilidade, só intercepto e inclinação são recalibrados no treino: $\hat{\pi} = \sigma(a + bR)$, com $\sigma(z) = 1/(1 + e^{-z})$. A ordenação, e portanto o AUROC, é exatamente a do escore original.

**Regressão logística.** $\hat{\pi}(\mathbf{x}) = \sigma(\beta_0 + \boldsymbol{\beta}^\top \tilde{\mathbf{x}})$, em que $\tilde{\mathbf{x}}$ são as variáveis transformadas e padronizadas. Com 5 variáveis, $\boldsymbol{\beta}$ é estimado por máxima verossimilhança (é o escore de Mayo reestimado). Com 17, por *elastic net*:

$$\min_{\beta_0, \boldsymbol{\beta}} \; -\sum_i \left[y_i \ln \hat{\pi}_i + (1 - y_i)\ln(1 - \hat{\pi}_i)\right] + \frac{1}{C}\left(\alpha\|\boldsymbol{\beta}\|_1 + \frac{1 - \alpha}{2}\|\boldsymbol{\beta}\|_2^2\right)$$

**Random forest.** $\hat{\pi}(\mathbf{x}) = \frac{1}{B}\sum_{b=1}^{B} T_b(\mathbf{x})$, média de $B = 300$ árvores de classificação, cada uma treinada numa amostra bootstrap e escolhendo, em cada nó, a melhor divisão (índice de Gini) entre um subconjunto aleatório de variáveis.

**XGBoost.** Modelo aditivo $F_M(\mathbf{x}) = \sum_{m=1}^{M} \eta f_m(\mathbf{x})$, com $\hat{\pi} = \sigma(F_M)$. Cada árvore $f_m$ minimiza uma aproximação de segunda ordem da perda logística mais a penalização $\gamma T + \frac{\lambda}{2}\|\mathbf{w}\|_2^2$ ($T$ folhas, pesos $\mathbf{w}$).

**Desenho 2 x 2:**

| | 5 variáveis de Mayo | 17 variáveis |
|---|---|---|
| **Regressão** | Mayo 1989; regressão logística | Regressão logística *elastic net* |
| **Aprendizado de máquina** | Random forest; XGBoost | Random forest; XGBoost |

### 3.2 Método de validação

- **Externa ao ajuste:** validação cruzada estratificada repetida, 5 repetições de 5 folds (25 avaliações).
- **Ajuste de hiperparâmetros aninhado:** `RandomizedSearchCV` com 3 folds internos, critério AUROC, 12 configurações (8 para o random forest), somente no treino de cada fold externo. Imputação, padronização e ajuste ficam dentro de um `Pipeline`, refeitos em cada partição.
- **Grades:** regressão *elastic net*: $C \in \{0{,}01; 0{,}03; 0{,}1; 0{,}3; 1; 3\}$, $\alpha \in \{0; 0{,}5; 1\}$. Random forest: folha mínima $\in \{3, 5, 10, 20\}$, variáveis por divisão $\in \{\sqrt{p}, 0{,}5p, p\}$, profundidade $\in \{\text{livre}, 4, 6\}$. XGBoost: árvores $\in \{100, 200, 400\}$, taxa $\eta \in \{0{,}02; 0{,}05; 0{,}1\}$, profundidade $\in \{1, 2, 3\}$, peso mínimo $\in \{1, 5\}$, $\lambda \in \{1, 5\}$.
- **Validação quase externa:** desenvolvimento nos pacientes do ensaio randomizado, teste nos não randomizados.
- **Braço de controle de vazamento:** classificação de `Status` em 3 classes (enquadramento da PS3E26), XGBoost com 17 variáveis, com e sem `N_Days`, mesma validação 5 x 5.
- **Semente:** 2026.

### 3.3 Medidas de desempenho

- **AUROC** (principal): probabilidade de o modelo dar risco maior a quem morreu do que a quem sobreviveu, num par sorteado.
- **Valor incremental:** $\Delta\text{AUROC}$ em relação ao Escore de Mayo, com IC 95% por *bootstrap* de pacientes (2.000 reamostragens) sobre as predições fora-do-fold, médias das 5 repetições.
- **AUPRC:** área sob a curva precisão-revocação.
- **Brier:** $\frac{1}{n}\sum_i (\hat{\pi}_i - y_i)^2$; menor é melhor.
- **Calibração no geral (CITL):** intercepto $a$ em $\text{logit}\,P(y=1) = a + \text{logit}(\hat{\pi})$, isto é, com o logit da predição como *offset* (Van Calster et al., 2019); ideal 0. Positivo: o modelo subestima o risco; negativo: superestima.
- **Inclinação de calibração:** coeficiente $b$ em $\text{logit}\,P(y=1) = a + b\,\text{logit}(\hat{\pi})$; ideal 1. Abaixo de 1, probabilidades extremas demais; acima de 1, comprimidas demais.
- **Custo de dados:** número de variáveis exigidas e pacientes elegíveis sem imputação.
- **Braço de vazamento:** *log loss* multiclasse, AUROC macro (um contra todos) e acurácia.

---

## 4. Avaliação

### 4.1 Amostras

| Uso | Pacientes | Óbitos em 5 anos |
|---|---|---|
| Coorte completa | 418 | |
| Rotulados para 5 anos (análise principal) | 312 | 115 (36,9%) |
| Cada fold externo: treino / teste | ≈ 250 / ≈ 62 | ≈ 92 / ≈ 23 |
| Cada fold interno (ajuste): treino / validação | ≈ 166 / ≈ 83 | |
| Quase externa: treino (randomizados) | 244 | |
| Quase externa: teste (não randomizados) | 68 | 30 |
| Braço de vazamento (3 classes) | 418 | 161 D, 25 CL, 232 C |

**Custo de dados:** dos 312 rotulados, **310 têm as 5 variáveis de Mayo completas e só 210 têm as 17 completas**. Exigir o conjunto completo sem imputação custa um terço dos pacientes.

### 4.2 Desempenho na validação cruzada 5 x 5 (média ± desvio entre os 25 folds)

| Modelo | AUROC | AUPRC | Brier | CITL | Incl. calibração |
|---|---|---|---|---|---|
| Mayo 1989 (coef. publicados) | 0,910 ± 0,040 | 0,879 ± 0,054 | 0,112 ± 0,028 | 0,00 ± 0,31 | 1,10 ± 0,33 |
| Regressão logística, 5 var. (Mayo reestimado) | 0,906 ± 0,044 | 0,871 ± 0,061 | 0,115 ± 0,032 | −0,01 ± 0,33 | 1,04 ± 0,36 |
| Regressão logística *elastic net*, 17 var. | 0,915 ± 0,035 | 0,880 ± 0,051 | 0,121 ± 0,024 | 0,00 ± 0,25 | 1,74 ± 0,91 |
| Random forest, 5 var. | 0,893 ± 0,047 | 0,852 ± 0,066 | 0,130 ± 0,030 | 0,01 ± 0,27 | 1,26 ± 0,60 |
| Random forest, 17 var. | 0,903 ± 0,044 | 0,862 ± 0,068 | 0,124 ± 0,026 | 0,02 ± 0,21 | 1,54 ± 0,52 |
| XGBoost, 5 var. | 0,891 ± 0,051 | 0,852 ± 0,072 | 0,126 ± 0,033 | 0,04 ± 0,26 | 1,09 ± 0,34 |
| XGBoost, 17 var. | 0,895 ± 0,042 | 0,854 ± 0,064 | 0,126 ± 0,028 | 0,04 ± 0,26 | 1,15 ± 0,41 |

**Tabela 2 x 2 (AUROC médio):**

| | 5 variáveis (310 elegíveis) | 17 variáveis (210 elegíveis) |
|---|---|---|
| **Regressão** | 0,906 (Mayo 1989: 0,910) | 0,915 |
| **Random forest** | 0,893 | 0,903 |
| **XGBoost** | 0,891 | 0,895 |

**Valor incremental sobre o Escore de Mayo 1989 ($\Delta$AUROC, IC 95% bootstrap):**

| Modelo | ΔAUROC | IC 95% |
|---|---|---|
| Regressão logística, 5 var. (reestimado) | −0,005 | [−0,012; +0,003] |
| Regressão logística *elastic net*, 17 var. | +0,004 | [−0,015; +0,023] |
| Random forest, 5 var. | −0,018 | [−0,034; −0,002] |
| Random forest, 17 var. | −0,003 | [−0,021; +0,014] |
| XGBoost, 5 var. | −0,018 | [−0,031; −0,006] |
| XGBoost, 17 var. | −0,011 | [−0,030; +0,007] |

### 4.3 Validação quase externa (treino em 244 randomizados, teste em 68 não randomizados)

| Modelo | AUROC | Brier | CITL | Incl. calibração |
|---|---|---|---|---|
| Mayo 1989 | 0,873 | 0,149 | 0,29 | 0,89 |
| Regressão logística, 5 var. | 0,878 | 0,144 | 0,30 | 0,88 |
| Regressão logística *elastic net*, 17 var. | 0,874 | 0,172 | 0,46 | 2,27 |
| Random forest, 5 var. | 0,882 | 0,145 | 0,41 | 1,15 |
| Random forest, 17 var. | 0,896 | 0,145 | 0,30 | 1,49 |
| XGBoost, 5 var. | 0,879 | 0,145 | 0,38 | 0,99 |
| XGBoost, 17 var. | 0,845 | 0,179 | −0,81 | 1,00 |

Com só 68 pacientes e 30 óbitos no teste, diferenças de alguns centésimos de AUROC estão dentro do ruído; o que esta análise mostra com segurança são as quedas grandes e os desvios de calibração.

### 4.4 Braço de controle: vazamento por `N_Days` (3 classes, XGBoost, 17 variáveis)

| Entrada | *Log loss* | AUROC macro | Acurácia |
|---|---|---|---|
| Sem `N_Days` | 0,753 ± 0,089 | 0,788 ± 0,043 | 0,721 ± 0,037 |
| Com `N_Days` | 0,645 ± 0,086 | 0,822 ± 0,045 | 0,763 ± 0,032 |

---

## 5. Conclusão

1. **Nenhum modelo de aprendizado de máquina superou o Escore de Mayo de 1989.** O melhor resultado foi a regressão logística com 17 variáveis (+0,004 de AUROC, intervalo que inclui zero). Random forest e XGBoost com as 5 variáveis de Mayo ficaram **abaixo** do escore, com intervalos que excluem zero (−0,018). Com 17 variáveis, os dois empataram com o escore.
2. **Desenho 2 x 2.** Na leitura vertical, a regressão ficou à frente do AM nas duas colunas: com as mesmas variáveis, o algoritmo flexível não acrescentou nada, e as transformações logarítmicas escolhidas em 1989 já capturavam o que as árvores precisariam aprender. Na leitura horizontal, as 12 variáveis extras acrescentaram cerca de 0,01 de AUROC em todas as famílias, ao custo de um terço dos pacientes elegíveis sem imputação (310 para 210).
3. **Calibração.** O escore de Mayo e o XGBoost tiveram inclinação próxima de 1. A regressão penalizada com 17 variáveis (1,74) e o random forest (1,26 e 1,54) produziram probabilidades comprimidas demais. Na validação quase externa, a mortalidade em 5 anos dos pacientes fora do ensaio (44%, 30 de 68) foi maior que a dos randomizados usados no treino (35%, 85 de 244), e quase todos os modelos passaram a subestimar o risco (CITL entre 0,29 e 0,46). A exceção foi o XGBoost com 17 variáveis, que perdeu discriminação (0,845) e passou a superestimar o risco (CITL −0,81): nos pacientes fora do ensaio, as variáveis ausentes deixam de ser exceção, e a regra aprendida para ausentes deixa de valer. Os modelos de 5 variáveis, cujos dados existem para todos, mantiveram a discriminação.
4. **Vazamento.** Incluir `N_Days` como entrada, como no enquadramento da PS3E26, reduziu o *log loss* de 0,753 para 0,645 e elevou o AUROC macro de 0,788 para 0,822, com uma informação que não existe no momento da predição.
5. **Resposta à pergunta do título.** Neste dataset, o Escore de Mayo vale mais a pena: discrimina tão bem ou melhor que os modelos de AM, é bem calibrado, exige 5 variáveis de rotina disponíveis para quase todos os pacientes, e é uma fórmula interpretável. O resultado está alinhado com Christodoulou et al. (2019).

**Limitações.** Centro único, década de 1970/80, população anterior ao ácido ursodesoxicólico; sem coorte externa verdadeira; classificação em horizonte fixo exclui 106 pacientes censurados ou transplantados antes de 5 anos (análise de sobrevivência com riscos competitivos é a extensão natural); os coeficientes de Mayo foram derivados nestes mesmos dados, o que favorece o escore original (o escore reestimado na validação cruzada, sem essa vantagem, ficou 0,005 abaixo); grades de hiperparâmetros reduzidas por limite computacional; validação quase externa com amostra pequena.

---

## Como executar

```bash
pip install ucimlrepo xgboost scikit-learn pandas numpy matplotlib jupyter
jupyter nbconvert --to notebook --execute ml4health_cbp_mayo.ipynb
```

Tempo de execução: cerca de 20 minutos em CPU com 2 núcleos. Para um teste rápido, mude `N_REP = 1` no notebook.

## Referências

- Christodoulou, E. et al. A systematic review shows no performance benefit of machine learning over logistic regression for clinical prediction models. *Journal of Clinical Epidemiology*, 110:12-22, 2019.
- Dickson, E. R. et al. Prognosis in primary biliary cirrhosis: model for decision making. *Hepatology*, 10(1):1-7, 1989.
- Kapoor, S.; Narayanan, A. Leakage and the reproducibility crisis in machine-learning-based science. *Patterns*, 4(9):100804, 2023.
- Steyerberg, E. W.; Vergouwe, Y. Towards better clinical prediction models: seven steps for development and an ABCD for validation. *European Heart Journal*, 35(29):1925-1931, 2014.
- Van Calster, B. et al. Calibration: the Achilles heel of predictive analytics. *BMC Medicine*, 17:230, 2019.
- UCI Machine Learning Repository. Cirrhosis Patient Survival Prediction [dataset], 2023. DOI 10.24432/C5R02G.

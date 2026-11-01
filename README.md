# Aprendizado de Máquina versus Escore de Mayo: qual vale mais a pena na predição de óbito em cirrose biliar primária?

**Disciplina:** TCC00367, Introdução ao Aprendizado de Máquina para Saúde (PGC/UFF)
**Autor:** Clayton Escouper das Chagas
**Notebook de demonstração:** [`ml4health_cbp_mayo.ipynb`](ml4health_cbp_mayo.ipynb)

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/claytonchagas/ml4health/blob/main/ml4health_cbp_mayo.ipynb)

**Auditoria independente.** O código, o notebook e este documento foram auditados por um segundo agente ([`AUDITORIA.md`](AUDITORIA.md)). Os sete achados da primeira passada ([`auditoria/relatorio_A.md`](auditoria/relatorio_A.md)) foram tratados nesta versão; a seção 6 resume cada um.

---

## 1. Motivação e objetivo

A cirrose biliar primária (CBP; desde 2015, colangite biliar primária) é uma doença hepática crônica e autoimune, de progressão muito variável entre pacientes. Estimar o risco individual de óbito na primeira avaliação orienta a intensidade do acompanhamento e o momento de encaminhamento ao transplante.

Desde 1989 existe o **Escore de Risco de Mayo** (Dickson et al., 1989), um modelo de Cox com cinco variáveis de rotina (idade, bilirrubina, albumina, tempo de protrombina e edema), derivado exatamente nos dados usados aqui. Modelos de aprendizado de máquina (AM) prometem mais precisão, mas costumam trazer custos: perdem a transparência de uma fórmula, exigem mais infraestrutura e, quando usam variáveis além das cinco de Mayo, exigem também mais exames e mais pacientes com dados completos. Revisões sistemáticas não encontraram vantagem do AM sobre a regressão logística em predição clínica quando a comparação é metodologicamente limpa (Christodoulou et al., 2019).

**Objetivo.** Medir o **valor incremental** do AM sobre um modelo de regressão com as 5 variáveis do Escore de Mayo, na predição de óbito em até 5 anos, e o custo desse ganho. *Valor incremental* é o benefício adicional que um novo modelo traz em comparação com o método clínico já usado na rotina: não basta o modelo ser preciso, ele precisa ser melhor do que o que os médicos já fazem para justificar custo, tempo e mudança no fluxo de trabalho.

**Perguntas.**

1. Em que condições random forest e XGBoost mostram ganho, ausência de diferença ou perda em relação à regressão com as 5 variáveis de Mayo, em discriminação e em calibração?
2. O ganho, se houver, vem do algoritmo ou das variáveis extras?
3. Quanto o enquadramento da competição Kaggle PS3E26 (prever `Status` com `N_Days` como entrada) infla o desempenho?

**Desenho 2 x 2.** Duas famílias de métodos (regressão e AM), cada uma com as 5 variáveis de Mayo e com as 17 variáveis do dataset, nos mesmos pacientes e nos mesmos folds. A leitura horizontal (mesma família) mede o efeito das variáveis extras. A leitura vertical (mesmas variáveis) compara os **pipelines** de cada família, que diferem também no tratamento dos dados; uma análise de sensibilidade dá às árvores o mesmo pré-processamento da regressão, aproximando a comparação do efeito do algoritmo.

---

## 2. Descrição do dataset

### 2.1 Dados

- **Fonte:** UCI Machine Learning Repository, dataset 878, *Cirrhosis Patient Survival Prediction*, DOI [10.24432/C5R02G](https://doi.org/10.24432/C5R02G), licença CC BY 4.0. Link: <https://archive.ics.uci.edu/dataset/878/cirrhosis+patient+survival+prediction+dataset-1>
- **Origem:** ensaio clínico da Mayo Clinic (1974 a 1984) sobre D-penicilamina em CBP; base do artigo de Dickson et al. (1989). É o mesmo conjunto disponível como `survival::pbc` no R.
- **População:** 418 pacientes (312 randomizados no ensaio, com o painel completo de exames, ainda que com alguns valores ausentes; 106 elegíveis que recusaram a randomização e só têm as medidas de rotina). São 374 mulheres (89,5%).
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

1. **Rótulo de 5 anos (1.826 dias).** `Status = D` e `N_Days ≤ 1826` → 1 (óbito); `N_Days > 1826` → 0 (vivo aos 5 anos); `Status ∈ {C, CL}` e `N_Days ≤ 1826` → excluído (saiu antes dos 5 anos sem óbito observado; censura). Resultado: **312 pacientes rotulados, 115 óbitos (36,9%), 106 excluídos.** Esses 106 excluídos e os 106 não randomizados são conjuntos distintos; a coincidência é numérica.
2. **`N_Days` nunca é variável de entrada.** É o tempo até o desfecho, conhecido só depois dele. Entra apenas na construção do rótulo, e no braço de controle de vazamento, rodado de propósito.
3. **Codificação:** idade em anos; sexo e sinais clínicos em 0/1; edema em 0, 0,5 e 1, como no Escore de Mayo; tratamento em 0/1 com ausência mantida.
4. **Transformação:** na regressão logística, laboratórios assimétricos em logaritmo natural (bilirrubina, albumina e protrombina na especificação de Mayo; também colesterol, cobre, fosfatase alcalina, AST e triglicerídeos no modelo de 17 variáveis), seguidos de padronização.
5. **Imputação, dentro de cada partição de treino:** mediana para as 5 variáveis de Mayo (só 2 pacientes rotulados têm algum ausente); imputação iterativa para as 17 variáveis (na escala logarítmica, na regressão; na escala original, no random forest); o XGBoost trata ausentes nativamente.
6. **Sem balanceamento artificial de classes**, porque distorce as probabilidades previstas (Christodoulou et al., 2019).

### 2.3 Link para a versão usada

A execução oficial usa a cópia versionada em [`data/pbc_rdatasets.csv`](data/pbc_rdatasets.csv), obtida do espelho Rdatasets do `survival::pbc` (<https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/survival/pbc.csv>), com verificação de checksum SHA-256 (`797ea9b6abfe...`). As contagens (418 pacientes, 232/161/25 por `Status`, 106 sem tratamento) coincidem com o UCI 878. No notebook, `FONTE_DADOS = "uci"` baixa o dataset oficial pelo pacote `ucimlrepo` (id 878).

---

## 3. Modelo de aprendizado de máquina

### 3.1 Formalização matemática

Seja $\mathbf{x}_i \in \mathbb{R}^p$ o vetor de variáveis de linha de base do paciente $i$ ($p = 5$ ou $p = 17$) e $y_i \in \{0, 1\}$ o indicador de óbito em até 5 anos. Cada modelo estima $\hat{\pi}(\mathbf{x}) = \hat{P}(y = 1 \mid \mathbf{x})$.

**Escore de Risco de Mayo (Dickson et al., 1989).** O modelo final, estimado com os 418 pacientes, define

$$R = 0{,}039\,\text{idade} + 0{,}871\ln(\text{bilirrubina}) - 2{,}53\ln(\text{albumina}) + 2{,}38\ln(\text{protrombina}) + 0{,}859\,\text{edema}$$

A implementação reproduz os dois exemplos resolvidos do artigo ($R = 3{,}12$ e $R = 8{,}39$). Como esses coeficientes foram estimados nesta mesma coorte, o escore publicado é apresentado só como **referência histórica**, em duas versões:

- **probabilidade original** do modelo de Cox, sem nenhum ajuste: $\hat{\pi} = 1 - S_0(5)^{\exp(R - 5{,}07)}$, com $S_0(5) = 0{,}774$ (Tabela 4 do artigo) e 5,07 a média de $R$ nos 418 pacientes;
- **recalibrado no treino:** $\hat{\pi} = \sigma(a + bR)$, com $\sigma(z) = 1/(1 + e^{-z})$ e $a, b$ estimados no treino.

Na validação quase externa, entra também o **modelo inicial** de Dickson (Tabela 2), estimado só com os 312 pacientes randomizados: coeficientes 0,0333 (idade), 0,8792 (ln bilirrubina), −3,053 (ln albumina), 3,016 (ln protrombina), 0,7847 (edema), recalibrado no treino.

**Regressão logística.** $\hat{\pi}(\mathbf{x}) = \sigma(\beta_0 + \boldsymbol{\beta}^\top \tilde{\mathbf{x}})$, em que $\tilde{\mathbf{x}}$ são as variáveis transformadas e padronizadas. Com 5 variáveis, $\boldsymbol{\beta}$ é estimado por máxima verossimilhança em cada fold: é o Escore de Mayo reestimado, e a **referência principal** do valor incremental. Com 17, por *elastic net*:

$$\min_{\beta_0, \boldsymbol{\beta}} \; -\sum_i \left[y_i \ln \hat{\pi}_i + (1 - y_i)\ln(1 - \hat{\pi}_i)\right] + \frac{1}{C}\left(\alpha\|\boldsymbol{\beta}\|_1 + \frac{1 - \alpha}{2}\|\boldsymbol{\beta}\|_2^2\right)$$

**Random forest.** $\hat{\pi}(\mathbf{x}) = \frac{1}{B}\sum_{b=1}^{B} T_b(\mathbf{x})$, média de $B = 300$ árvores de classificação, cada uma treinada numa amostra *bootstrap* e escolhendo, em cada nó, a melhor divisão (índice de Gini) entre um subconjunto aleatório de variáveis.

**XGBoost.** Modelo aditivo $F_M(\mathbf{x}) = \sum_{m=1}^{M} \eta f_m(\mathbf{x})$, com $\hat{\pi} = \sigma(F_M)$. Cada árvore $f_m$ minimiza uma aproximação de segunda ordem da perda logística mais a penalização $\gamma T + \frac{\lambda}{2}\|\mathbf{w}\|_2^2$ ($T$ folhas, pesos $\mathbf{w}$).

**Desenho 2 x 2:**

| | 5 variáveis de Mayo | 17 variáveis |
|---|---|---|
| **Regressão** | Regressão logística (Mayo reestimado) | Regressão logística *elastic net* |
| **Aprendizado de máquina** | Random forest; XGBoost | Random forest; XGBoost |

**Análise de sensibilidade do pré-processamento.** Random forest e XGBoost com 17 variáveis recebendo exatamente as etapas da regressão com 17 variáveis (logaritmo, imputação iterativa e padronização). Árvores são invariantes a transformações monotônicas; a diferença restante em relação à regressão é o algoritmo e seus hiperparâmetros.

### 3.2 Método de validação

- **Validação cruzada:** estratificada repetida, 5 repetições de 5 folds (25 avaliações), com as mesmas divisões para todos os modelos.
- **Ajuste de hiperparâmetros aninhado:** `RandomizedSearchCV` com 3 folds internos, critério AUROC, **12 configurações sorteadas para todos os modelos ajustáveis**, somente no treino de cada fold externo. Imputação, padronização e ajuste ficam dentro de um `Pipeline`, refeitos em cada partição. Os hiperparâmetros escolhidos em cada fold estão em [`resultados/hiperparametros.csv`](resultados/hiperparametros.csv).
- **Grades** (definidas antes de qualquer resultado e não alteradas depois): regressão *elastic net*: $C \in \{0{,}01; 0{,}03; 0{,}1; 0{,}3; 1; 3\}$, $\alpha \in \{0; 0{,}5; 1\}$. Random forest: folha mínima $\in \{3, 5, 10, 20\}$, variáveis por divisão $\in \{\sqrt{p}, 0{,}5p, p\}$, profundidade $\in \{\text{livre}, 4, 6\}$. XGBoost: árvores $\in \{100, 200, 400\}$, taxa $\eta \in \{0{,}02; 0{,}05; 0{,}1\}$, profundidade $\in \{1, 2, 3\}$, peso mínimo $\in \{1, 5\}$, $\lambda \in \{1, 5\}$.
- **Validação quase externa:** desenvolvimento nos 244 pacientes rotulados do ensaio randomizado, teste nos 68 rotulados não randomizados.
- **Braço de controle de vazamento:** classificação de `Status` em 3 classes (enquadramento da PS3E26), XGBoost com 17 variáveis, com e sem `N_Days`, mesma validação 5 x 5.
- **Reprodutibilidade:** semente 2026 em todos os componentes aleatórios (divisões, buscas, florestas, XGBoost e o *solver* `saga` da regressão penalizada); avisos de convergência registrados (nenhum ocorreu); versões exatas em [`requirements.txt`](requirements.txt).

### 3.3 Medidas de desempenho

- **AUROC** (principal): probabilidade de o modelo dar risco maior a quem morreu do que a quem sobreviveu, num par sorteado.
- **Valor incremental:** $\Delta\text{AUROC}$ em relação à regressão logística com as 5 variáveis de Mayo, sobre as predições fora-do-fold de cada paciente (média das 5 repetições). Intervalos por *bootstrap* **pareado** de pacientes (2.000 reamostragens): IC 95% e, para as cinco comparações principais, IC simultâneo de **Bonferroni** (99%). Só se afirma "maior" ou "menor" quando o IC de Bonferroni exclui zero. Os intervalos são **condicionais** às predições já obtidas (não incorporam a variação de refazer o treino e a busca), portanto **exploratórios**; "sem evidência de diferença" não significa equivalência, pois nenhuma margem foi definida a priori. Complementam: a média e o desvio da diferença de AUROC dentro de cada um dos 25 folds e a fração de folds com ganho.
- **AP** (*average precision*, precisão média): soma da precisão ponderada pelos incrementos de revocação, estimador usual da área sob a curva precisão-revocação (não é a integração trapezoidal).
- **Brier:** $\frac{1}{n}\sum_i (\hat{\pi}_i - y_i)^2$; menor é melhor.
- **Calibração no geral (CITL):** intercepto $a$ em $\text{logit}\,P(y=1) = a + \text{logit}(\hat{\pi})$, isto é, com o logit da predição como *offset* (Van Calster et al., 2019); ideal 0. Positivo: o modelo subestima o risco; negativo: superestima.
- **Inclinação de calibração:** coeficiente $b$ em $\text{logit}\,P(y=1) = a + b\,\text{logit}(\hat{\pi})$; ideal 1. Abaixo de 1, probabilidades extremas demais; acima de 1, comprimidas demais.
- **Custo de dados:** número de variáveis exigidas e pacientes elegíveis sem imputação.
- **Braço de vazamento:** *log loss* multiclasse, AUROC macro (um contra todos) e acurácia.

A AUROC das tabelas é a média dos 25 folds; a das curvas ROC do notebook é calculada sobre as predições fora-do-fold médias (por exemplo, 0,910 e 0,908 para o Mayo publicado). São estimadores diferentes, ambos corretos.

---

## 4. Avaliação

### 4.1 Amostras

| Uso | Pacientes | Óbitos em 5 anos |
|---|---|---|
| Coorte completa | 418 | |
| Rotulados para 5 anos (análise principal) | 312 | 115 (36,9%) |
| Cada fold externo: treino / teste | ≈ 250 / ≈ 62 | ≈ 92 / ≈ 23 |
| Cada fold interno (ajuste): treino / validação | ≈ 166 / ≈ 83 | |
| Quase externa: treino (randomizados) | 244 | 85 (34,8%) |
| Quase externa: teste (não randomizados) | 68 | 30 (44,1%) |
| Braço de vazamento (3 classes) | 418 | 161 D, 25 CL, 232 C |

**Custo de dados:** dos 312 rotulados, **310 têm as 5 variáveis de Mayo completas e só 210 têm as 17 completas**. Todos os modelos foram avaliados nos 312, com imputação ou tratamento nativo de ausentes; a contagem mostra quantos pacientes seriam elegíveis se cada modelo exigisse dados completos na aplicação.

### 4.2 Desempenho na validação cruzada 5 x 5 (média ± desvio entre os 25 folds)

| Modelo | AUROC | AP | Brier | CITL | Incl. calibração |
|---|---|---|---|---|---|
| *Mayo 1989 final, probabilidade original (ref. histórica)* | *0,910 ± 0,040* | *0,879 ± 0,054* | *0,121 ± 0,023* | *0,33 ± 0,18* | *1,56 ± 0,44* |
| *Mayo 1989 final, recalibrado (ref. histórica)* | *0,910 ± 0,040* | *0,879 ± 0,054* | *0,112 ± 0,028* | *0,00 ± 0,31* | *1,10 ± 0,33* |
| **Regressão logística, 5 var. (Mayo reestimado; referência)** | **0,906 ± 0,044** | **0,871 ± 0,061** | **0,115 ± 0,032** | **−0,01 ± 0,33** | **1,04 ± 0,36** |
| Regressão logística *elastic net*, 17 var. | 0,915 ± 0,035 | 0,880 ± 0,051 | 0,121 ± 0,024 | 0,00 ± 0,25 | 1,74 ± 0,91 |
| Random forest, 5 var. | 0,893 ± 0,047 | 0,852 ± 0,066 | 0,130 ± 0,030 | 0,01 ± 0,27 | 1,27 ± 0,60 |
| Random forest, 17 var. | 0,903 ± 0,044 | 0,862 ± 0,069 | 0,124 ± 0,026 | 0,02 ± 0,21 | 1,57 ± 0,58 |
| XGBoost, 5 var. | 0,891 ± 0,051 | 0,852 ± 0,072 | 0,126 ± 0,033 | 0,04 ± 0,26 | 1,09 ± 0,34 |
| XGBoost, 17 var. | 0,895 ± 0,042 | 0,854 ± 0,064 | 0,126 ± 0,028 | 0,04 ± 0,26 | 1,15 ± 0,41 |
| Random forest, 17 var., pré-proc. da regressão | 0,907 ± 0,042 | 0,868 ± 0,063 | 0,122 ± 0,024 | 0,00 ± 0,20 | 1,52 ± 0,60 |
| XGBoost, 17 var., pré-proc. da regressão | 0,899 ± 0,039 | 0,855 ± 0,053 | 0,126 ± 0,027 | 0,07 ± 0,33 | 1,04 ± 0,46 |

**Tabela 2 x 2 (AUROC médio):**

| | 5 variáveis (310 com dados completos) | 17 variáveis (210 com dados completos) |
|---|---|---|
| **Regressão** | 0,906 | 0,915 |
| **Random forest** | 0,893 | 0,903 (0,907 com o pré-proc. da regressão) |
| **XGBoost** | 0,891 | 0,895 (0,899 com o pré-proc. da regressão) |

**Valor incremental sobre a regressão com as 5 variáveis de Mayo (exploratório):**

| Modelo | ΔAUROC | IC 95% | IC 99% (Bonferroni) | Leitura | Δ por fold (média ± desvio) | Folds com ganho |
|---|---|---|---|---|---|---|
| Regressão *elastic net*, 17 var. | +0,009 | [−0,010; +0,030] | [−0,017; +0,035] | sem evidência de diferença | +0,009 ± 0,027 | 60% |
| Random forest, 5 var. | −0,013 | [−0,029; +0,003] | [−0,035; +0,009] | sem evidência de diferença | −0,013 ± 0,019 | 24% |
| Random forest, 17 var. | −0,000 | [−0,018; +0,016] | [−0,022; +0,024] | sem evidência de diferença | −0,003 ± 0,018 | 40% |
| XGBoost, 5 var. | −0,013 | [−0,027; −0,001] | [−0,031; +0,003] | sem evidência de diferença | −0,016 ± 0,019 | 20% |
| XGBoost, 17 var. | −0,006 | [−0,025; +0,012] | [−0,030; +0,017] | sem evidência de diferença | −0,011 ± 0,019 | 24% |

**Sensibilidade do pré-processamento (referência: regressão *elastic net* com 17 variáveis; IC de Bonferroni para 2 comparações):**

| Modelo | ΔAUROC | IC 95% | IC 97,5% (Bonferroni) | Leitura | Folds com ganho |
|---|---|---|---|---|---|
| Random forest, 17 var., pré-proc. da regressão | −0,006 | [−0,022; +0,009] | [−0,023; +0,011] | sem evidência de diferença | 40% |
| XGBoost, 17 var., pré-proc. da regressão | −0,013 | [−0,028; +0,002] | [−0,030; +0,004] | sem evidência de diferença | 16% |

**Referência histórica (exploratória).** Contra a probabilidade original do Mayo publicado, a regressão reestimada com 5 variáveis ficou em −0,007 [−0,016; +0,000], e random forest e XGBoost com 5 variáveis ficaram abaixo (−0,021 cada, com IC de Bonferroni que exclui zero). Essa comparação favorece o escore, cujos coeficientes viram os pacientes do teste, e por isso não sustenta inferências (tabela completa em [`resultados/valor_incremental_vs_mayo_publicado.csv`](resultados/valor_incremental_vs_mayo_publicado.csv)).

### 4.3 Validação quase externa (treino em 244 randomizados, teste em 68 não randomizados)

| Modelo | AUROC | AP | Brier | CITL | Incl. calibração |
|---|---|---|---|---|---|
| **Mayo 1989 inicial (n = 312), recalibrado** | **0,865** | **0,847** | **0,155** | **0,33** | **0,83** |
| *Mayo 1989 final, probabilidade original (viu o teste)* | *0,873* | *0,856* | *0,161* | *0,58* | *1,25* |
| *Mayo 1989 final, recalibrado (viu o teste)* | *0,873* | *0,856* | *0,149* | *0,29* | *0,89* |
| Regressão logística, 5 var. | 0,878 | 0,844 | 0,144 | 0,30 | 0,88 |
| Regressão logística *elastic net*, 17 var. | 0,874 | 0,859 | 0,172 | 0,46 | 2,27 |
| Random forest, 5 var. | 0,882 | 0,876 | 0,145 | 0,41 | 1,15 |
| Random forest, 17 var. | 0,896 | 0,876 | 0,145 | 0,30 | 1,49 |
| XGBoost, 5 var. | 0,879 | 0,870 | 0,145 | 0,38 | 0,99 |
| XGBoost, 17 var. | 0,845 | 0,842 | 0,179 | −0,81 | 1,00 |
| Random forest, 17 var., pré-proc. da regressão | 0,897 | 0,882 | 0,149 | 0,79 | 0,98 |
| XGBoost, 17 var., pré-proc. da regressão | 0,888 | 0,878 | 0,150 | 0,85 | 0,66 |

Os coeficientes finais de Mayo foram estimados com os 418 pacientes, inclusive os 68 do teste; por isso, o comparador histórico válido aqui é o **modelo inicial** (n = 312). Com só 68 pacientes e 30 óbitos no teste, diferenças de alguns centésimos de AUROC não devem ser interpretadas, e nenhum intervalo de confiança foi calculado para esta análise; ela serve para sinalizar quedas grandes de discriminação e desvios de calibração, de forma descritiva.

### 4.4 Braço de controle: vazamento por `N_Days` (3 classes, XGBoost, 17 variáveis)

| Entrada | *Log loss* | AUROC macro | Acurácia |
|---|---|---|---|
| Sem `N_Days` | 0,753 ± 0,089 | 0,788 ± 0,043 | 0,721 ± 0,037 |
| Com `N_Days` | 0,645 ± 0,086 | 0,822 ± 0,045 | 0,763 ± 0,032 |

---

## 5. Conclusão

1. **O aprendizado de máquina não demonstrou ganho sobre a regressão com as 5 variáveis de Mayo.** Em nenhuma das cinco comparações principais o IC de Bonferroni excluiu zero. A maior diferença nominal foi a da regressão *elastic net* com 17 variáveis (+0,009). Random forest e XGBoost superaram a regressão em apenas 20% a 40% dos folds. Nominalmente, os modelos de AM com 5 variáveis ficaram abaixo (−0,013), sem significância após a correção para comparações múltiplas.
2. **Desenho 2 x 2.** Na leitura horizontal, as 12 variáveis extras acrescentaram cerca de 0,01 de AUROC nominal em cada família; esse contraste não teve intervalo de confiança próprio. O custo dessa coluna vale para regressão e AM: exigir as 17 variáveis completas, sem imputação, reduziria os elegíveis de 310 para 210. Na leitura vertical, a regressão teve a maior AUROC nominal nas duas colunas. Com o mesmo pré-processamento da regressão, random forest e XGBoost com 17 variáveis também não mostraram ganho sobre a regressão penalizada (−0,006 e −0,013; sem evidência de diferença). Nominalmente, esse pré-processamento elevou a AUROC das árvores (RF de 0,903 para 0,907; XGBoost de 0,895 para 0,899; na quase externa, XGBoost de 0,845 para 0,888); o efeito do pré-processamento não foi testado diretamente. A conclusão vale para os pipelines e o orçamento de busca avaliados.
3. **Calibração.** Na validação cruzada, a regressão com 5 variáveis e o XGBoost tiveram inclinação próxima de 1; a regressão penalizada com 17 variáveis (1,74) e o random forest (1,27 e 1,57) produziram probabilidades comprimidas demais. A probabilidade original do modelo de Cox de 1989, sem ajuste, **subestimou** o risco nesta análise (CITL +0,33; inclinação 1,56), possivelmente porque o rótulo de 5 anos exclui pacientes que saíram vivos antes do horizonte (hipótese não testada); recalibrada no treino, teve estimativas de calibração próximas das ideais (CITL 0,00; inclinação 1,10). Na validação quase externa, a mortalidade do teste (44%) foi maior que a do treino (35%), e quase todos os modelos subestimaram o risco; o XGBoost com 17 variáveis, ao contrário, perdeu discriminação (0,845) e superestimou o risco (CITL −0,81). Uma hipótese é que, fora do ensaio, as variáveis ausentes deixam de ser exceção; o desenho não separa esse efeito da diferença de população nem da variabilidade de uma amostra de 68 pacientes.
4. **Vazamento.** Incluir `N_Days` como entrada, como no enquadramento da PS3E26, reduziu o *log loss* de 0,753 para 0,645 e elevou o AUROC macro de 0,788 para 0,822, com uma informação que não existe no momento da predição.
5. **Resposta à pergunta do título.** Neste estudo de caso, um modelo de regressão com as 5 variáveis de rotina do Escore de Mayo vale mais a pena: o ganho do AM não foi demonstrado, nem com as 5 variáveis de Mayo nem com as 17. Com as mesmas 5 variáveis, o AM não exige dados extras, mas perde a transparência de uma fórmula; passar para 17 variáveis acrescenta, a qualquer família, o custo de coleta e a menor elegibilidade sem imputação, sem ganho demonstrado. Na validação quase externa, o XGBoost com 17 variáveis teve a maior perda de discriminação e de calibração (descritiva). O resultado está alinhado com Christodoulou et al. (2019).

**Limitações.** Centro único, década de 1970/80, população anterior ao ácido ursodesoxicólico; sem coorte externa verdadeira; os coeficientes publicados de Mayo foram estimados nesta coorte, e por isso o escore publicado só serve como referência histórica; a classificação em horizonte fixo exclui 106 pacientes censurados ou transplantados antes de 5 anos (análise de sobrevivência com riscos competitivos é a extensão natural); os intervalos de confiança são condicionais às predições fora-do-fold e não incorporam a variação de refazer o treino (uma reamostragem do procedimento completo não foi feita por custo computacional); não houve teste de equivalência; orçamento de busca modesto (12 configurações); validação quase externa com amostra pequena.

---

## 6. Auditoria independente: achados da passada A e como foram tratados

| Achado | Gravidade | Tratamento |
|---|---|---|
| A-01: coeficientes de Mayo estimados com os pacientes de teste | bloqueante | Referência principal passou a ser a regressão com as 5 variáveis de Mayo reestimada em cada fold; Mayo publicado só como referência histórica; na validação quase externa, comparador histórico é o modelo inicial de Dickson (n = 312) |
| A-02: semente e ambiente não garantiam reprodução | importante | Semente no *solver* `saga`; avisos de convergência registrados (nenhum); versões fixadas; fonte de dados selecionável, com padrão local e checksum SHA-256; hiperparâmetros escolhidos salvos |
| A-03: intervalos com interpretação mais ampla que o procedimento permite | importante | Intervalos descritos como condicionais e exploratórios; IC de Bonferroni; "maior/menor" só quando ele exclui zero; "sem evidência de diferença" em vez de "empate"; dispersão fold a fold |
| A-04: leitura vertical não isolava o algoritmo | importante | Leitura vertical descrita como comparação de pipelines; análise de sensibilidade com o mesmo pré-processamento; orçamento de busca igual (12) para todos |
| A-05: texto do notebook divergia do código | menor | Descrições corrigidas; calibração em decis de fato; curvas de iteração identificadas como demonstrativas |
| A-06: convenção de AP/AUPRC | menor | Métrica renomeada para AP, com a definição explícita |
| A-07: calibração atribuída às probabilidades originais de Mayo | importante | Separação entre probabilidade original do modelo de Cox ($1 - 0{,}774^{\exp(R - 5{,}07)}$) e versão recalibrada; conclusão sobre calibração restrita ao que foi medido |

---

## Como executar

Requer **Python 3.11 ou mais novo** (a execução oficial usou o 3.13); com Python 3.10, as versões fixadas não instalam. Com o [`uv`](https://docs.astral.sh/uv/), que baixa o Python sozinho:

```bash
uv venv --python 3.13 .venv && source .venv/bin/activate
uv pip install -r requirements.txt
jupyter nbconvert --to notebook --execute ml4health_cbp_mayo.ipynb
```

Quem já tem o Python 3.13 pode usar `python3.13 -m venv .venv && source .venv/bin/activate` e `pip install -r requirements.txt`.

Com as versões do `requirements.txt` e `FONTE_DADOS = "local"` (padrão), a execução reproduz os números deste documento. No Colab (botão no topo), a primeira célula instala apenas os pacotes ausentes e usa as versões do Colab, de modo que os resultados podem diferir na terceira casa decimal. Duas execuções completas, guardadas nos commits `00d1773` e `0fb5b54`, produziram os mesmos resultados (diferença absoluta máxima de 1,6e-13); a comparação pode ser refeita, sem treinar nada, com `python auditoria/comparar_execucoes.py`, e a saída está em [`auditoria/comparacao_execucoes.txt`](auditoria/comparacao_execucoes.txt). Tempo de execução: cerca de 35 a 40 minutos em CPU com 2 núcleos; para um teste rápido, use `N_REP = 1`.

## Referências

- Christodoulou, E. et al. A systematic review shows no performance benefit of machine learning over logistic regression for clinical prediction models. *Journal of Clinical Epidemiology*, 110:12-22, 2019.
- Dickson, E. R. et al. Prognosis in primary biliary cirrhosis: model for decision making. *Hepatology*, 10(1):1-7, 1989.
- Kapoor, S.; Narayanan, A. Leakage and the reproducibility crisis in machine-learning-based science. *Patterns*, 4(9):100804, 2023.
- Steyerberg, E. W.; Vergouwe, Y. Towards better clinical prediction models: seven steps for development and an ABCD for validation. *European Heart Journal*, 35(29):1925-1931, 2014.
- Van Calster, B. et al. Calibration: the Achilles heel of predictive analytics. *BMC Medicine*, 17:230, 2019.
- UCI Machine Learning Repository. Cirrhosis Patient Survival Prediction [dataset], 2023. DOI 10.24432/C5R02G.

# Auditoria independente das análises D14 a D16 (plano complementar, com a Emenda 1)

Data: 02/11/2026. Auditor: agente independente. Escopo: `sbcas/PLANO_COMPLEMENTAR.md` (com a Emenda 1), `mayo1989.py` (D14, D15), `comparador_graf.py` (D16), resultados `resultados_sbcas/mayo1989_*.csv` e `graf312_*.csv`, infraestrutura `sobrevivencia.py` e `experimento.py`. Nenhum arquivo do repositório foi alterado. Recálculo independente em `/tmp/claude-0/-home-claude/54a8d552-1224-58f3-8df0-58e6f9325be5/scratchpad/aud14/recalculo.py` (saída em `saida.txt`, tabelas `recalc_D14.csv` e `recalc_D16_particoes.csv`, no mesmo diretório). Commits auditados: `86a5386` (scripts), `db7950b` (D16), `acd6fca` (D14 e D15).

Classificação: **bloqueante** (impede usar o número ou a frase como está), **importante** (exige mudança de redação ou ressalva explícita), **menor** (registro ou melhoria).

## 1. Resumo executivo

Todos os números dos quatro CSV de D14/D15 e dos três de D16 foram reproduzidos de forma independente, com coincidência até a quarta casa (bootstrap com a mesma semente reproduzido exatamente; RSF por partição reproduzida exatamente). A reconstrução das 25 partições a partir de `particoes*.csv` coincide com o `RepeatedStratifiedKFold(5, 5, random_state=2026)` original nas 25 partições, para os dois desfechos, e o índice `Fold` de `folds*.csv` corresponde à partição `k` com `rep, f = divmod(k, 5)` (três partições reajustadas dão o mesmo C de Uno de `folds.csv` até a 6ª casa). Os scripts seguem o plano e a Emenda 1 sem divergência de procedimento. Os problemas encontrados são de interpretação e de desenho da medida de otimismo em D16, não de cálculo. Não há achado bloqueante nos números; há dois bloqueantes de redação (conclusões (a) e (d) como enunciadas) e vários importantes.

## 2. Conformidade com o plano (pergunta 1)

| Item do plano / Emenda 1 | Script | Situação |
|---|---|---|
| D14: coeficientes publicados sem reajuste; fórmula final (418) na coorte inteira | `coorte()` usa `COEF_MAYO` | Conforme. Coeficientes iguais aos verificados no relatório A (fórmula de uso, p. 6). |
| D14: ausentes (2 pacientes) imputados pela mediana do treino de cada partição | `escore(X[te], X.loc[tr,"Prothrombin"].median(), ...)` | Conforme. Os 2 ausentes estão ambos nos 106 não randomizados; a imputação não afeta a derivação nos 312. Efeito nulo no C agregado (0,8307 com imputação global ou por partição). |
| D14: C de Uno em 5 anos sobre o escore; sem calibração | `cuno(..., tau=1826)` | Conforme. |
| D14: bootstrap pareado 2.000, semente 2026, Bonferroni 98,3% para os 3 de AM, 95% para a referência | `NIVEL = 1 - 0.05/3`; `boot_dif(None, ...)` | Conforme. Censura reestimada em cada reamostra, como em `valor_incremental` (D10 i). |
| D14: teste t corrigido com C da fórmula em cada uma das 25 partições de teste | `c_fold`, `d = C_modelo_k - C_formula_k`, `sqrt(1/25 + 1/4) * sd`, t com 24 g.l. | Conforme. Fator e graus de liberdade corretos para 5x5 (Nadeau e Bengio, 2003; Bouckaert e Frank, 2004). |
| Emenda 1: vantagem de derivação nos 312 com a fórmula inicial (312) e a final ao lado, contra o Cox reestimado fora da partição | `derivacao()` | Conforme, com uma ressalva de redação (achado 3). |
| Emenda 1: D15 com a fórmula inicial, final ao lado, imputação pela mediana dos 312; bootstrap 2.000, semente 2026, IC 95% | `subgrupo()` | Conforme. Censura estimada nos 312, como em `validacao_subgrupo`. |
| D16: Cox de 7 variáveis do conjunto final de Graf, Cox de Mayo e RSF de 17 nas mesmas partições restritas aos 312; Harrell e Uno; bootstrap pareado | `comparador_graf.main()` | Conforme. |
| D16: RSF com os hiperparâmetros já escolhidos no treino dos 312, sem nova busca | `hiperparametros_subgrupo.csv` | Conforme ao plano; mas ver achado 6 (vazamento de seleção). |
| D16: otimismo = C de Harrell da RSF de 17 com treino igual ao teste nos 312, contra o valor fora da partição | `dentro` compara com a **média por partição** | Conforme à letra do plano, que não fixou qual "valor fora da partição". Ver achado 5. |
| Plano: D14 não é cego (cálculo exploratório prévio do consultor) | Declarado no plano | Registrar no artigo. |

Divergência de procedimento: **nenhuma**. Divergências de leitura e de desenho: achados 3, 5 e 6.

## 3. Achados

### Achado 1 (menor). Reprodução integral dos números
Recalculados de forma independente, sem reutilizar funções de `mayo1989.py` ou `comparador_graf.py`:

| Quantidade | CSV do repositório | Recálculo |
|---|---|---|
| C da fórmula final na coorte, principal (418) | 0,8307 (agregado); 0,8317 (média por partição) | 0,8307; 0,8317 |
| C da fórmula final na coorte, só óbito | 0,8546; 0,8570 | 0,8546; 0,8570 |
| Cox reestimado menos fórmula, principal | +0,0007; IC95 bootstrap [-0,0054; +0,0066]; t corrigido [-0,0067; +0,0098] | idênticos |
| Cox reestimado menos fórmula, só óbito | -0,0049; IC95 [-0,0079; -0,0023]; t corrigido [-0,0079; +0,0010] | idênticos |
| Cox penalizado menos fórmula, principal | +0,0155; IC 98,3% [-0,0046; +0,0357]; t corr. [-0,0170; +0,0465] | idênticos |
| RSF 5 menos fórmula, só óbito | -0,0181; IC 98,3% [-0,0361; -0,0024]; t corr. [-0,0529; +0,0021] | idênticos; t = -2,37, p bicaudal 0,026 (limiar Bonferroni 0,0167) |
| C das fórmulas nos 106 (censura nos 312) | inicial 0,7824; final 0,7857 | idênticos |
| Cox penalizado menos fórmula inicial nos 106 | +0,0238; IC95 [-0,0113; +0,0607] | idêntico |
| Otimismo RSF 17 nos 312 (Harrell dentro menos média por partição) | 0,8594 - 0,8269 = +0,0325 | idêntico; RSF por partição reproduzida exatamente |
| Otimismo Cox 5 nos 312 | 0,8238 - 0,8238 = -0,0000 | idêntico |

### Achado 2 (menor). Ordem das partições e estimativa da censura
Verificado: `particoes*.csv` reconstrói exatamente as 25 partições do `RepeatedStratifiedKFold` original, na ordem `k = 5*rep + f`, para os dois desfechos; `Fold k` de `folds*.csv` é essa partição. O C de Uno usa `concordance_index_ipcw` com censura estimada por Kaplan-Meier no treino (por partição e no subgrupo) ou na própria amostra avaliada (predições agregadas e reamostras), coerente com D10 (i). Sensibilidade feita no subgrupo: estimando a censura nos próprios 106 em vez dos 312, o C das fórmulas cai para 0,768 (inicial) e 0,772 (final) e os IC pareados alargam (Cox penalizado menos inicial: [-0,005; +0,074]); nenhuma leitura muda.

### Achado 3 (importante). "Cox reestimado fora da partição nos 312" foi treinado em partições dos 418
Em `derivacao()`, `ref = oof[REFERENCIA][rand]` são as predições fora da partição da validação cruzada feita nos **418** (cada modelo foi treinado em cerca de 334 pacientes, que incluem os 106 não randomizados), apenas **avaliadas** nos 312. A Emenda 1 fala em "Cox reestimado fora da partição nos mesmos 312", o que pode ser lido como treino restrito aos 312 (como em D16, onde esse Cox restrito existe e dá C de Uno agregado 0,8427). O número relatado (0,8454) é legítimo, mas o texto deve dizer que o treino foi nos 418 menos a partição. Com o Cox restrito aos 312 (D16), a "vantagem" da fórmula inicial subiria de 0,002 para cerca de 0,005 (0,8475 contra 0,8427), ainda abaixo da margem.

### Achado 4 (bloqueante, redação). A medida de "vantagem de derivação" não mede o que a frase sugere
A comparação fórmula inicial (avaliada nos 312 onde foi estimada) contra Cox de 5 variáveis reestimado fora da partição isola **apenas** o custo de reestimar cinco coeficientes já escolhidos (correlação de Spearman entre os dois escores: 0,993). Não mede a parte principal da vantagem de derivação: a **seleção das cinco variáveis** nesta mesma coorte (Dickson et al., p. 3), que a referência reestimada compartilha com a fórmula. Portanto a frase "a vantagem de derivação da referência vale zero em discriminação" não é sustentada; o que é sustentado é: "reestimar os coeficientes das cinco variáveis publicadas, fora da partição, não custa discriminação mensurável nesta coorte (diferença de -0,002, IC95 [-0,008; +0,003] no desfecho principal)". Além disso, no desfecho só óbito, a fórmula é **melhor** que o Cox reestimado por 0,004 a 0,005 com IC bootstrap que exclui zero (coorte: [-0,0079; -0,0023]; derivação com a final: [-0,0066; -0,0010]); logo "vale zero" é falso nesse desfecho, embora a diferença seja clinicamente irrelevante (um quarto da margem). Explicação plausível, a conferir no artigo original: o modelo de Mayo foi derivado para **óbito** (transplante censurado), e a fórmula final foi ajustada nestes mesmos 418; a vantagem dentro da amostra aparece justamente no desfecho para o qual foi derivada e some no desfecho composto.

### Achado 5 (importante). O otimismo em D16 compara duas quantidades não comparáveis e o "zero" do Cox é coincidência
`graf312_dentro_amostra.csv` compara o C de Harrell **agregado** dentro da amostra (um escore para 312 pacientes) com a **média de 25 valores por partição** (cada um sobre cerca de 62 pacientes). São estimandos diferentes: a média por partição é sistematicamente maior que o C das predições agregadas (para o Cox de 5 variáveis fora da partição: 0,8238 por partição contra 0,8170 agregado; para a RSF: 0,8269 contra 0,8213). O otimismo "-0,0000" do Cox é uma coincidência numérica dessa mistura, não uma medida. Recálculo com a comparação homogênea (dentro da amostra agregado menos fora da partição agregado, ambos nos 312):

| Modelo | Dentro (Harrell) | Fora, agregado | Otimismo homogêneo | Otimismo do CSV |
|---|---|---|---|---|
| Cox, 5 var. | 0,8238 | 0,8170 | **+0,0068** | -0,0000 |
| RSF, 17 var. | 0,8594 | 0,8213 | **+0,0381** | +0,0325 |

A conclusão qualitativa se mantém (otimismo da RSF cinco a seis vezes o do Cox), mas "o Cox quase nada" deve virar "cerca de 0,007" e a RSF "cerca de 0,03 a 0,04", com a base de comparação declarada. Em C de Uno, a RSF dentro da amostra dá 0,884 contra 0,845 fora (agregado): otimismo de 0,039, mesma ordem.

### Achado 6 (importante). Hiperparâmetros da RSF escolhidos nos mesmos 312 inflam a validação cruzada de D16, pouco
Os hiperparâmetros de `hiperparametros_subgrupo.csv` foram escolhidos por busca aninhada em **todos** os 312 e depois reutilizados em cada partição dos 312: cada partição de teste participou da escolha. É vazamento de seleção, de magnitude pequena em uma grade de 50 configurações. Sensibilidade sem vazamento (hiperparâmetros da partição `k` de `hiperparametros.csv`, escolhidos no treino da partição `k` dos 418, que não contém o teste): C de Harrell agregado da RSF cai de 0,8213 para 0,8187 e o C de Uno agregado de 0,8449 para 0,8413 (menos 0,003 a 0,004); a diferença RSF 17 menos Cox 5 nos 312 passa de +0,0022 para -0,0014 em Uno (IC95 [-0,020; +0,017]) e de +0,0043 para +0,0018 em Harrell (IC95 [-0,014; +0,019]). Nenhuma leitura muda, mas o artigo deve declarar o vazamento e, de preferência, relatar a versão sem vazamento. O mesmo vazamento infla o otimismo medido no achado 5 em sentido contrário (torna o "fora" maior e o otimismo menor), também em cerca de 0,003.

### Achado 7 (menor). Pré-processamento do Cox de 7 variáveis
`_preproc_cox(GRAF7)`: logaritmo em bilirrubina, albumina, fosfatase alcalina e protrombina (as de `LOG_LAB`), **sem** logaritmo em plaquetas (razoável, distribuição pouco assimétrica) e estágio tratado como numérico ordinal 1 a 4 (razoável e usual; Graf et al. não dizem como codificaram). Imputação iterativa no treino e padronização. Convergiu em todas as 25 partições. É razoável como "Cox com as sete variáveis", desde que o artigo não o chame de reprodução de Graf, o que o plano já veda.

### Achado 8 (importante). Comparação da fórmula final na coorte favorece a fórmula menos do que se temia, e isso pode ser dito
A Emenda 1 diz que a fórmula final é avaliada dentro da amostra e por isso "a comparação favorece a fórmula". Os próprios dados permitem dimensionar esse favorecimento: para um Cox de 5 variáveis nesta coorte, o otimismo dentro da amostra é de cerca de 0,007 em Harrell (achado 5) e, no desfecho principal, o Cox reestimado fora da partição iguala a fórmula (+0,0007). Portanto o viés a favor da fórmula é de no máximo poucos milésimos no desfecho principal, e de cerca de 0,004 a 0,005 no desfecho só óbito. Vale registrar isso em vez de deixar a ressalva sem tamanho.

### Achado 9 (menor). Leitura mecânica dos IC do teste corrigido
Em `coorte()`, o IC do teste corrigido para a referência usa nível 95% e para os modelos de AM 98,3%, como previsto. O erro padrão corrigido é cerca de 2,7 vezes o ingênuo (sd/5), o que é esperado para 5x5. Os IC são 1,3 a 2,5 vezes mais largos que os do bootstrap. Nenhuma comparação de AM contra a fórmula fica com p corrigido abaixo do limiar de Bonferroni (0,0167); a menor é RSF 5 no óbito (p = 0,026).

## 4. Respostas às perguntas 3 e 5

### Pergunta 3 (D16)
- **C dentro da amostra contra média por partição é justo?** Não como está (achado 5): mistura C agregado com média de C por partição de 62 pacientes. Justa é a comparação agregado contra agregado nos mesmos 312, que dá 0,007 (Cox) e 0,038 (RSF). Ambas as versões dão a mesma ordem de grandeza para a RSF.
- **Hiperparâmetros da RSF da busca nos mesmos 312 inflam a RSF na validação cruzada?** Sim, em direção conhecida e magnitude medida de 0,003 a 0,004 (achado 6). Não muda nenhuma conclusão; deve ser declarado.
- **Pré-processamento do Cox de 7 variáveis é razoável?** Sim (achado 7), com estágio numérico e sem logaritmo em plaquetas, ambos defensáveis.

### Pergunta 5 (conclusões)
**(a) "A vantagem de derivação da referência vale zero em discriminação."** Não sustentada como enunciada (achado 4, bloqueante). Sustentada: "reestimar os coeficientes das cinco variáveis fora da partição custa menos de 0,01 de C de Uno (desfecho principal: -0,002, IC95 [-0,008; +0,003]); no desfecho só óbito a fórmula publicada mantém uma vantagem de cerca de 0,004 (IC bootstrap exclui zero; teste corrigido não), um quarto da margem." A seleção das variáveis nesta coorte, compartilhada pela referência, não é medida por D14 e deve continuar como limitação (como já está em D13).

**(b) "Nenhum modelo de AM supera a fórmula publicada."** Sustentada apenas na forma "nenhum ganho sobre a fórmula publicada foi demonstrado nos 418, nos dois desfechos, nas duas inferências" (todos os IC de Bonferroni contêm zero). Não sustentada como afirmação de equivalência: para o Cox penalizado o limite superior é +0,036 (bootstrap) e +0,047 (t corrigido) no desfecho principal, acima da margem de 0,02, logo um ganho relevante não está excluído; a margem só é excluída, pela regra combinada de D11, para nenhum modelo contra a fórmula (RSF 5: limite superior 0,009 no bootstrap, mas 0,019 no t corrigido, portanto também não excluída pelas duas). Nos 106 do subgrupo, Cox penalizado e RSF 17 têm +0,024 contra a fórmula inicial com IC até +0,06 e +0,07: a frase não pode ser estendida ao subgrupo. Recomenda-se "não há evidência de que algum modelo de AM supere a fórmula publicada; os intervalos não excluem ganhos da ordem da margem para o Cox penalizado e a RSF de 17".

**(c) RSF de 5 variáveis inferior à fórmula no desfecho só óbito.** Bootstrap pareado (condicional às predições) exclui zero com Bonferroni ([-0,036; -0,002]); teste corrigido não ([-0,053; +0,002], p = 0,026 contra limiar 0,0167). Pela regra combinada adotada em D11 (declarar só quando as duas inferências concordam), a inferioridade **não** deve ser declarada; relatar como "indício de inferioridade, não confirmado quando se inclui a variação de retreino", a mesma situação já observada contra o Cox reestimado no óbito (IC Bonferroni [-0,031; +0,003]). Observação: a estimativa pontual é consistente nos dois desfechos (-0,013 e -0,018), e o padrão é coerente com o achado de D1 (florestas pequenas de 5 variáveis ordenam pior que o Cox nas mesmas variáveis), mas isso é descrição, não inferência.

**(d) "A avaliação dentro da amostra infla a RSF em cerca de 0,03 e o Cox quase nada."** Parcialmente sustentada e com base de comparação errada (achado 5, bloqueante na redação atual). Corrigir para: "nos 312, o C de Harrell dentro da amostra excede o das predições fora da partição em cerca de 0,04 para a RSF de 17 variáveis (0,859 contra 0,821) e em cerca de 0,007 para o Cox de 5 variáveis (0,824 contra 0,817)". Quanto a Graf et al. (2026): o C de 0,855 deles vem de **bootstrap .632+**, que é um estimador com correção de otimismo, não uma avaliação dentro da amostra; o otimismo medido aqui **não explica** aquele valor e o artigo não deve insinuar que explica. O que se pode dizer: (i) o nosso C de Harrell fora da partição da RSF nos 312 (0,82 a 0,83) está dentro do IC de Graf (0,778 a 0,932); (ii) o .632+ incorpora uma fração do erro dentro da amostra, de modo que um otimismo grande da RSF pode contribuir para o valor pontual, mas a magnitude dessa contribuição não foi medida aqui; (iii) outras diferenças (desfecho, variáveis, ajuste por erro fora da sacola em todos os 312 antes do bootstrap, seguimento completo em vez de 5 anos) são candidatas igualmente plausíveis, e o C do Cox de Graf (0,776) é **menor** que o nosso Cox nos 312 (0,817), o que o otimismo da RSF não explica. Qualquer frase ligando 0,03 a 0,855 deve ser removida ou reduzida a "mecanismo possível, não medido".

## 5. Recomendações, em ordem
1. (Bloqueante) Reescrever (a) e (d) como no item 4; não usar "vale zero" nem "o Cox quase nada".
2. (Importante) Trocar a base do otimismo em D16 para agregado contra agregado, ou relatar as duas, declarando qual é qual. Isso exige só mudar `fora` em `comparador_graf.py` para o C de Harrell de `agg[nome]` (não executado aqui, por instrução).
3. (Importante) Declarar o vazamento de seleção de hiperparâmetros em D16 e, se possível, relatar a versão com hiperparâmetros por partição (números no achado 6).
4. (Importante) Em D14 derivação, dizer que o Cox fora da partição foi treinado nos 418 menos a partição; opcionalmente relatar a versão restrita aos 312 (0,8427), já disponível em D16.
5. (Importante) Restringir (b) à ausência de demonstração nos 418 e explicitar que a margem não é excluída contra a fórmula para nenhum modelo nas duas inferências; não estender ao subgrupo.
6. (Importante) Em (c), seguir a regra de D11 e não declarar inferioridade.
7. (Menor) Registrar no artigo que D14 não foi cega e que a fórmula final é avaliada dentro da amostra, com o tamanho do favorecimento (achado 8).
8. (Menor) Conferir no artigo de Dickson et al. se o transplante foi censurado na derivação; se sim, usar isso para explicar por que a fórmula ganha só no desfecho óbito.

## 6. Arquivos do recálculo
- `/tmp/claude-0/-home-claude/54a8d552-1224-58f3-8df0-58e6f9325be5/scratchpad/aud14/recalculo.py`
- `/tmp/claude-0/-home-claude/54a8d552-1224-58f3-8df0-58e6f9325be5/scratchpad/aud14/saida.txt`
- `/tmp/claude-0/-home-claude/54a8d552-1224-58f3-8df0-58e6f9325be5/scratchpad/aud14/recalc_D14.csv`
- `/tmp/claude-0/-home-claude/54a8d552-1224-58f3-8df0-58e6f9325be5/scratchpad/aud14/recalc_D16_particoes.csv`

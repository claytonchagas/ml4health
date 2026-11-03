# Análises que eu recomendaria e não executei

Regra do briefing: análises novas exigem registro prévio (em `sbcas/DESVIOS.md` ou num plano complementar) e aprovação do autor. Nenhuma das propostas abaixo foi executada; os números citados são apenas os que já existem no repositório. Em ordem de relação efeito/custo.

## 1. Brier por partição com o teste corrigido (sem retreino)

- O quê: aplicar o mesmo teste t corrigido de Nadeau e Bengio, já usado para o C de Uno, às diferenças de Brier em 5 anos e de Brier integrado por partição (`folds.csv`), modelo contra referência, com Bonferroni para 3 comparações; opcionalmente, bootstrap pareado do Brier nas predições agregadas, como já se faz para o C de Uno.
- Por quê: o revisor de bioestatística (parecer 3, item 3.e) recalculou isso e encontrou, para a RSF de 5 variáveis, erro maior em 23 de 25 partições com IC corrigido que exclui zero; hoje o artigo só diz "erro maior, de modo mais nítido na RSF de 5 variáveis". Um resultado demonstrado de inferioridade em calibração global reforçaria a leitura "não há ganho" sem mudar a conclusão.
- Custo: baixo (uma função em `gerar_tabelas.py`, lendo `folds.csv`; sem retreino). Duas linhas no texto.
- Risco: ser lido como "mais um teste" (densidade); exigiria registrar como desvio posterior aos resultados, o que já é o caso de D11.
- Efeito esperado na avaliação: pequeno (1 a 2 pontos); ajuda mais na qualidade técnica do que na originalidade.

## 2. Importância por permutação nas 25 partições (D17, já previsto e não executado)

- O quê: executar `importancia_permutacao.py` nas 25 partições com os hiperparâmetros salvos, como previa D17.
- Por quê: remove um "ficou aquém do plano" declarado na Seção 3.1 e permite dizer com desvio adequado que só a bilirrubina (e talvez o cobre) se destaca. Dois pareceres (2 e 3) apontaram que a ordem após a terceira posição é ruído com 5 partições.
- Custo: tempo de máquina (25 reajustes de RSF com 30 permutações por variável), sem decisão metodológica nova.
- Risco: nenhum para as conclusões; a figura voltou ao suplementar nesta versão, então o ganho é de completude.
- Efeito esperado: pequeno.

## 3. Intervalo pareado para a diferença de benefício líquido

- O quê: bootstrap pareado de pacientes (2.000, semente 2026) para a diferença de benefício líquido entre a RSF de 17 variáveis e a referência em cada limiar de 5% a 50%, sobre as predições fora da partição já salvas (`oof_risco5.csv`), com a censura tratada como em `curva_decisao.py`.
- Por quê: hoje a Seção 4.2 diz que "sem intervalo para essa diferença, a figura não permite afirmar utilidade igual". Com intervalo, a curva de decisão passaria de descritiva a comparável com o resto do artigo, e a crítica "calibração e benefício líquido não foram comparados inferencialmente" (parecer 1, item 5.3) deixaria de existir.
- Custo: médio-baixo (reamostragem sobre predições salvas; a estimação Kaplan-Meier por reamostra e por limiar é o que pesa).
- Risco: a RSF exibida foi escolhida pelo maior C de Uno nesta coorte (seleção declarada); o intervalo herdaria esse otimismo e isso teria de ser dito.
- Efeito esperado: pequeno a médio.

## 4. Sensibilidade do C de Uno à estimação da censura nos 106

- O quê: repetir o C de Uno do subgrupo estimando a distribuição de censura nos próprios 106 em vez de nos 312, como a auditoria D14-D16 fez em caráter exploratório (achado 2: os C das fórmulas caem para cerca de 0,77 e os intervalos alargam; nenhuma leitura muda).
- Por quê: fecha uma pergunta que um revisor de bioestatística pode fazer sobre o teste de transporte.
- Custo: baixo. Risco: nenhum. Efeito esperado: muito pequeno; só se sobrar espaço no suplementar.

## 5. O que não recomendo

- Riscos competitivos para o desfecho óbito: fora do escopo declarado, abriria outra frente de crítica e não muda a pergunta.
- Boosting ou redes neurais na sobrevivência: decisão congelada; com 186 eventos, uma família a mais não muda a conclusão nem a originalidade percebida.
- Cálculo de "quantos eventos seriam necessários" para decidir a margem para o Cox penalizado: é tentador para a Discussão, mas é um cálculo de poder pós-hoc com suposições que o comitê contestaria; a meia-largura observada, já relatada por macro, diz o essencial.

# Notas de literatura para a versão SBCAS

## Trabalho diretamente comparável, a citar e contrastar
- Graf, R.; Todd, S.; Baksh, M. F. "Comparison of the Cox proportional hazards model and Random Survival Forest algorithm for predicting patient-specific survival probabilities in clinical trial data". arXiv:2502.03119 (2025). Veículo final a confirmar.
  - Usa os 312 pacientes randomizados da Mayo (CBP) e um ensaio de câncer de próstata.
  - CBP: C de Cox 0,776 (0,735 a 0,817) contra RSF com divisão log-rank 0,855 (0,778 a 0,932); IBS 0,131 contra 0,116. Intervalos com sobreposição.
  - Simulações: Cox melhor calibrado, sobretudo com riscos não proporcionais; RSF com curvas de calibração muito inclinadas.
  - Teste global de Grambsch-Therneau significativo na CBP (qui-quadrado 20,86, gl 8, p = 0,0075); edema retirado do modelo final.
  - Verificado em 02/11/2026 no texto completo (arXiv:2502.03119v2, revisado em 27/05/2025; sem veículo publicado):
    - CBP: 312 randomizados; Cox final com 7 variáveis (idade, bilirrubina, albumina, fosfatase alcalina, plaquetas, protrombina, estágio), escolhidas por seleção retroativa pelo AIC (stepAIC); edema fora.
    - Validação por bootstrap .632+ (Wahl et al., 2016), 1.000 reamostragens, IC por percentis.
    - Discriminação pelo C de Harrell (Uno não é usado). RSF ajustada por grade, minimizando o erro fora da sacola (1 − C).
    - Intervalos relatados por modelo; não há intervalo para a diferença entre modelos.
    - Conclusão dos autores: RSF "tends to perform better but the confidence intervals are still overlapping"; só a regra extremely randomized trees (C 0,844; IC 0,819 a 0,869) tem IC que exclui o C do Cox.
    - Fonte: https://arxiv.org/html/2502.03119v2
  - Contraste com o nosso trabalho: lá a RSF parece superior em valor pontual; aqui, com validação cruzada aninhada, mesmas partições, comparação pareada e margem pré-especificada, não há ganho. Verificar se o protocolo deles é comparável (bootstrap, ajuste de hiperparâmetros, variáveis).

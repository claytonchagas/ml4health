# Notas de literatura para a versão SBCAS

## Trabalho diretamente comparável, a citar e contrastar
- Graf, R.; Todd, S.; Baksh, M. F. "Comparison of the Cox proportional hazards model and Random Survival Forest algorithm for predicting patient-specific survival probabilities in clinical trial data". arXiv:2502.03119 (2025). Veículo final a confirmar.
  - Usa os 312 pacientes randomizados da Mayo (CBP) e um ensaio de câncer de próstata.
  - CBP: C de Cox 0,776 (0,735 a 0,817) contra RSF com divisão log-rank 0,855 (0,778 a 0,932); IBS 0,131 contra 0,116. Intervalos com sobreposição.
  - Simulações: Cox melhor calibrado, sobretudo com riscos não proporcionais; RSF com curvas de calibração muito inclinadas.
  - Teste global de Grambsch-Therneau significativo na CBP (qui-quadrado 20,86, gl 8, p = 0,0075); edema retirado do modelo final.
  - Verificado em 02/11/2026 no PDF do preprint (arXiv:2502.03119; v1 de 05/02/2025 e v2 de 27/05/2025):
    - CBP: 312 randomizados. Seção 2.1.1: variáveis escolhidas comparando modelos por AIC e BIC; o "final dataset, in which the proportional hazards assumption was tested" tem 7 variáveis (idade, bilirrubina, albumina, fosfatase alcalina, plaquetas, protrombina, estágio); teste de Grambsch-Therneau com qui-quadrado 20,86, gl 8, p = 0,0075.
    - O texto não diz explicitamente que o C de 0,776 vem desse modelo de 7 variáveis, nem se a seleção foi repetida no bootstrap.
    - Seleção retroativa por AIC: descrita para o Cox do estudo de simulação (Seção 2.2.2).
    - Validação por bootstrap .632+, 1.000 reamostragens, IC por percentis. C de Harrell. RSF ajustada por grade pelo erro fora da sacola.
    - Intervalos por modelo; nenhum intervalo para a diferença. Conclusão: "tends to perform better but the confidence intervals are still overlapping"; só a regra extremely randomized trees tem IC que exclui o C do Cox.
    - Fontes: https://arxiv.org/pdf/2502.03119 e https://arxiv.org/html/2502.03119v2
  - Contraste com o nosso trabalho: lá a RSF parece superior em valor pontual; aqui, com validação cruzada aninhada, mesmas partições, comparação pareada e margem pré-especificada, não há ganho. Verificar se o protocolo deles é comparável (bootstrap, ajuste de hiperparâmetros, variáveis).

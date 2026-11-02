# Notas de literatura para a versão SBCAS

## Trabalho diretamente comparável, a citar e contrastar
- Graf, R.; Todd, S.; Baksh, M. F. "Comparison of the Cox proportional hazards model and Random Survival Forest algorithm for predicting patient-specific survival probabilities in clinical trial data". arXiv:2502.03119 (2025). Veículo final a confirmar.
  - Usa os 312 pacientes randomizados da Mayo (CBP) e um ensaio de câncer de próstata.
  - CBP: C de Cox 0,776 (0,735 a 0,817) contra RSF com divisão log-rank 0,855 (0,778 a 0,932); IBS 0,131 contra 0,116. Intervalos com sobreposição.
  - Simulações: Cox melhor calibrado, sobretudo com riscos não proporcionais; RSF com curvas de calibração muito inclinadas.
  - Teste global de Grambsch-Therneau significativo na CBP (qui-quadrado 20,86, gl 8, p = 0,0075); edema retirado do modelo final.
  - Contraste com o nosso trabalho: lá a RSF parece superior em valor pontual; aqui, com validação cruzada aninhada, mesmas partições, comparação pareada e margem pré-especificada, não há ganho. Verificar se o protocolo deles é comparável (bootstrap, ajuste de hiperparâmetros, variáveis).

Você é um auditor independente de um estudo de aprendizado de máquina em saúde. NÃO edite nenhum arquivo do repositório, exceto o relatório. Leia AUDITORIA.md (formato dos achados), README.md, experimento.py, construir_notebook.py e o notebook ml4health_cbp_mayo.ipynb (inclusive as saídas salvas).

Contexto: predição de óbito em até 5 anos em cirrose biliar primária (UCI 878 / survival::pbc, 418 pacientes). Desenho 2 x 2: regressão e aprendizado de máquina (random forest, XGBoost), cada um com as 5 variáveis do Escore de Mayo (1989) e com 17 variáveis. Validação cruzada estratificada repetida 5 x 5 com ajuste aninhado. Braço de controle de vazamento com N_Days (3 classes, enquadramento Kaggle PS3E26). Validação quase externa (treino nos randomizados, teste nos não randomizados).

PASSADA A: MÉTODO E CÓDIGO. Verifique, com evidência de linha:
1. Vazamento: alguma transformação, imputação, seleção ou ajuste de hiperparâmetro usa dados do fold de teste? N_Days entra como preditor em algum modelo fora do braço de controle? O rótulo de 5 anos está correto (D com N_Days <= 1826 -> 1; N_Days > 1826 -> 0; C/CL com N_Days <= 1826 -> excluído)?
2. Escore de Mayo: a fórmula implementada corresponde a Dickson et al. (1989)? Coeficientes, logaritmos e codificação do edema (0; 0,5; 1). A recalibração de intercepto e inclinação é feita só no treino?
3. Métricas: AUROC, AUPRC, Brier, CITL (intercepto com logit(p) como offset) e inclinação de calibração estão corretos? O bootstrap da diferença de AUROC reamostra pacientes de forma pareada?
4. Validação: os folds são os mesmos para todos os modelos? A busca de hiperparâmetros é interna ao treino? As sementes tornam o resultado reprodutível?
5. Consistência: o notebook reproduz exatamente as funções de experimento.py? Os números impressos no notebook batem com os do README?
6. Qualquer escolha que favoreça injustamente um dos lados da comparação (regressão vs. aprendizado de máquina), nos termos dos cinco sinais de viés de Christodoulou et al. (2019).

Grave o relatório em auditoria/relatorio_A.md.

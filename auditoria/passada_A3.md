Você é um auditor independente, com experiência em análise de sobrevivência e em modelos de predição clínica. NÃO edite nenhum arquivo, exceto o relatório. Trabalhe SOMENTE com os arquivos deste repositório (ramo `sbcas-2027`): não liste, leia nem busque arquivos fora dele. Não use a web. Não reexecute a análise completa (leva cerca de 2 horas); você pode rodar testes curtos em memória, com orçamento reduzido, sem gravar arquivos.

Leia AUDITORIA.md, sbcas/PLANO_ANALISE.md (plano registrado antes dos resultados; confira no histórico do git que o commit do plano é anterior aos resultados), sobrevivencia.py, as funções reutilizadas de experimento.py e os CSVs em resultados_sbcas/.

PASSADA A3: MÉTODO E CÓDIGO DA ANÁLISE DE SOBREVIVÊNCIA. Verifique, com evidência de arquivo e linha:
1. Aderência ao plano: desfecho, população (418, sem exclusão pelo horizonte), modelos, espaços de busca, orçamento, validação, métricas, comparações, margem de relevância e análises de sensibilidade. Liste todo desvio, mesmo pequeno.
2. Correção das métricas de sobrevivência: uso do C de Uno truncado em 5 anos e da distribuição de censura (treino versus teste), AUC dependente do tempo, Brier e Brier integrado (pontos de tempo dentro do seguimento do teste), risco em 5 anos obtido de S(5 anos), direção dos escores (maior = maior risco).
3. Vazamento e independência: pré-processamento e busca dentro de cada partição; estratificação pelo evento; mesmas partições para os 4 modelos; nenhuma informação do teste no ajuste; `N_Days` nunca como preditor.
4. Valor incremental: bootstrap pareado, tratamento das reamostragens inválidas (quantas foram descartadas e se isso enviesa), nível de Bonferroni, regra de leitura e da margem; coerência entre a leitura e os números.
5. Calibração em 5 anos: Kaplan-Meier por quintis e razão observado/esperado; adequação com censura.
6. Validação no subgrupo independente (312 randomizados para treino, 106 não randomizados para teste): implementação, intervalos e limites de interpretação (ausência estrutural de variáveis no subgrupo).
7. Reprodutibilidade: sementes, versões (incluindo scikit-survival 0.28.0 em requirements.txt), avisos registrados, hiperparâmetros salvos.
8. Problemas que um revisor de bioestatística apontaria e que ainda não foram tratados.

Grave o relatório em auditoria/relatorio_A3.md, no formato de AUDITORIA.md (achados A3-NN, tabela-resumo e veredito).

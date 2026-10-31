"""Gera o notebook de demonstracao a partir do modulo experimento.py (mantem uma unica fonte de verdade)."""
import re
import nbformat as nbf

src = open("experimento.py", encoding="utf-8").read()
src = src.split('if __name__ == "__main__":')[0]
blocos = re.split(r"\n# -{20,} ?", src)
cab, resto = blocos[0], blocos[1:]
imports = cab.split('"""', 2)[2].strip()  # remove docstring
secoes = {}
for b in resto:
    titulo, corpo = b.split("\n", 1)
    secoes[titulo.strip()] = corpo.strip()

md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell
nb = nbf.v4.new_notebook()
C = []

C.append(md("""# Aprendizado de Máquina versus Escore de Mayo: qual vale mais a pena na predição de óbito em cirrose biliar primária?

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/claytonchagas/ml4health/blob/main/ml4health_cbp_mayo.ipynb)

**TCC00367, Introdução ao Aprendizado de Máquina para Saúde (PGC/UFF).** Clayton Escouper das Chagas.

Notebook de demonstração do projeto. Pergunta: quanto o aprendizado de máquina acrescenta ao Escore de Risco de Mayo (1989, 5 variáveis de rotina) na predição de óbito em até 5 anos, e a que custo? O desenho é 2 x 2: **regressão** e **aprendizado de máquina**, cada um com as **5 variáveis de Mayo** e com as **17 variáveis** do dataset, nos mesmos folds. A leitura vertical isola o efeito do algoritmo; a horizontal, o efeito das variáveis extras.

Tempo de execução: cerca de 10 a 20 minutos em CPU (Colab gratuito serve). Para uma execução rápida de teste, mude `N_REP` para 1 na seção de hiperparâmetros."""))

C.append(md("## 1. Dependências do ambiente de execução"))
C.append(code("""# Instala apenas o que faltar (funciona no Colab e em ambiente local)
import importlib.util, subprocess, sys
faltando = [p for p in ["ucimlrepo", "xgboost", "sklearn", "pandas", "numpy", "matplotlib"] if importlib.util.find_spec(p) is None]
if faltando:
    nomes_pip = {"sklearn": "scikit-learn"}
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *[nomes_pip.get(p, p) for p in faltando]])

import os
os.makedirs("resultados", exist_ok=True); os.makedirs("figs", exist_ok=True)

import sys, sklearn, xgboost, pandas, numpy, matplotlib
print("Python", sys.version.split()[0])
for m in (sklearn, xgboost, pandas, numpy, matplotlib):
    print(f"{m.__name__:12s} {m.__version__}")"""))

C.append(md("## 2. Etapas de execução\n\n### 2.1 Bibliotecas utilizadas"))
C.append(code(imports + "\n\nimport matplotlib.pyplot as plt\nfrom sklearn.calibration import calibration_curve\nfrom sklearn.metrics import roc_curve\nplt.rcParams.update({'figure.dpi': 110, 'axes.spines.top': False, 'axes.spines.right': False})"))

C.append(md("""### 2.2 Funções de apoio

As funções estão agrupadas por papel: carga e codificação dos dados, Escore de Mayo, pipelines dos modelos, métricas e validação, experimento de vazamento e validação quase externa. Todo pré-processamento que aprende com os dados (imputação, padronização, ajuste de hiperparâmetros) fica **dentro** de um `Pipeline`, e portanto é refeito em cada partição de treino; o conjunto de teste nunca influencia nenhuma decisão."""))
nomes = {"dados": "Carga e codificação dos dados", "Escore de Mayo": "Escore de Risco de Mayo (Dickson et al., 1989)",
         "pipelines": "Pipelines dos modelos e grades de hiperparâmetros", "metricas": "Métricas, validação cruzada e bootstrap",
         "vazamento (enquadramento PS3E26)": "Experimento de vazamento (enquadramento da competição Kaggle PS3E26)",
         "validacao quase externa": "Validação quase externa"}
for k, v in secoes.items():
    C.append(md(f"#### {nomes.get(k, k)}"))
    C.append(code(v))

C.append(md("""### 2.3 Carregamento e pré-processamento do dataset

O notebook tenta baixar o dataset oficial do UCI (id 878). Se o servidor não responder, usa o espelho Rdatasets do `survival::pbc` do R, que é a mesma coorte de 418 pacientes com as mesmas variáveis (o UCI 878 foi derivado dele). A idade é convertida para anos.

**Rótulo.** Óbito em até 5 anos (1.826 dias):
- `Status = D` e `N_Days ≤ 1826` → 1;
- `N_Days > 1826` (qualquer status) → 0 (vivo aos 5 anos, com certeza);
- `Status ∈ {C, CL}` e `N_Days ≤ 1826` → sem rótulo, excluído (saiu antes dos 5 anos sem óbito observado).

`N_Days` é usado **apenas** para construir o rótulo; nunca é variável de entrada (exceto no braço de controle de vazamento, rodado de propósito)."""))
C.append(code("""df, ORIGEM = carregar_dados()
X = codificar(df)
y = rotulo_5anos(df)
rot = y.notna()
print("Origem dos dados:", ORIGEM)
print("Pacientes:", len(df))
print("Status:", df["Status"].value_counts().to_dict())
print("Randomizados no ensaio (Drug presente):", int(df["Drug"].notna().sum()), "| não randomizados:", int(df["Drug"].isna().sum()))
print(f"Rotulados para 5 anos: {int(rot.sum())} | óbitos em 5 anos: {int(y.sum())} ({y[rot].mean():.1%}) | excluídos por censura/transplante antes de 5 anos: {int((~rot).sum())}")"""))
C.append(code("""# Ausentes por variável (coorte completa) e custo de dados de cada coluna do desenho 2 x 2
aus = X[TODAS17].isna().sum().sort_values(ascending=False)
print(aus[aus > 0].to_string())
comp5 = int(X.loc[rot, MAYO5].notna().all(1).sum()); comp17 = int(X.loc[rot, TODAS17].notna().all(1).sum())
print(f"\\nPacientes rotulados com dados completos, sem imputação: 5 variáveis = {comp5} de {int(rot.sum())}; 17 variáveis = {comp17} de {int(rot.sum())}")"""))
C.append(code("""# Por que N_Days não pode ser entrada: ele separa as classes de Status quase sozinho
fig, ax = plt.subplots(figsize=(6, 3.2))
ordem = ["D", "CL", "C"]
ax.boxplot([df.loc[df.Status == s, "N_Days"] for s in ordem], tick_labels=["Óbito (D)", "Transplante (CL)", "Censurado (C)"], vert=False)
ax.axvline(HORIZONTE, ls="--", c="gray", lw=1); ax.text(HORIZONTE + 40, 3.35, "5 anos", color="gray", fontsize=8)
ax.set_xlabel("N_Days (dias até óbito, transplante ou fim do estudo)"); ax.set_title("Distribuição de N_Days por Status")
plt.tight_layout(); plt.savefig("figs/n_days_por_status.png", dpi=200, bbox_inches="tight"); plt.show()"""))

C.append(md("""### 2.4 Hiperparâmetros utilizados

- **Validação externa ao ajuste:** validação cruzada estratificada repetida, `N_REP` repetições de 5 folds (padrão 5 x 5 = 25 avaliações).
- **Ajuste aninhado:** `RandomizedSearchCV` com 12 configurações sorteadas, 3 folds internos, critério AUROC, somente no treino de cada fold externo.
- **Escore de Mayo (1989):** coeficientes publicados, sem reestimar; para converter o escore em probabilidade, só intercepto e inclinação são recalibrados no treino. A ordenação (AUROC) é exatamente a do escore original.
- **Regressão logística com 5 variáveis:** mesma especificação de Mayo (log de bilirrubina, albumina e protrombina), sem penalização; é o escore reestimado.
- **Regressão logística com 17 variáveis:** elastic net, laboratórios assimétricos em log, imputação iterativa.
- **Random forest:** 500 árvores; grade sobre folhas mínimas, variáveis por divisão e profundidade.
- **XGBoost:** ausentes tratados nativamente; grade sobre número de árvores, taxa de aprendizado, profundidade, peso mínimo e regularização L2.
- **Sem balanceamento artificial de classes:** distorceria as probabilidades (Christodoulou et al., 2019)."""))
C.append(code("""N_REP = 5      # repetições da validação cruzada (use 1 para um teste rápido)
N_FOLDS = 5
print("Semente:", SEMENTE, "| horizonte:", HORIZONTE, "dias")
for nome, cols, est, grade in modelos():
    print(f"- {nome:32s} {len(cols):2d} variáveis | grade: {grade if grade else 'sem ajuste'}")
print("\\nGrades:")
for k, g in GRADES.items():
    print(" ", k, g)"""))

C.append(md("""## 3. Execução

### 3.1 Curvas de iteração

Antes da avaliação principal, curvas de treinamento num único corte treino/teste (80/20 estratificado), para mostrar como cada modelo aprende: perda logarítmica do XGBoost por rodada de boosting, erro fora-da-bolsa (OOB) do random forest por número de árvores, e o caminho de regularização da regressão logística penalizada."""))
C.append(code("""from sklearn.model_selection import train_test_split
Xr, yr = X[rot], y[rot].astype(int)
Xtr, Xte, ytr, yte = train_test_split(Xr, yr, test_size=0.2, stratify=yr, random_state=SEMENTE)

fig, axs = plt.subplots(1, 3, figsize=(14, 3.6))

# (a) XGBoost: log loss por rodada
for cols, nome in [(MAYO5, "5 var."), (TODAS17, "17 var.")]:
    m = XGBClassifier(n_estimators=400, learning_rate=0.05, max_depth=2, subsample=0.8, colsample_bytree=0.8,
                      eval_metric="logloss", random_state=SEMENTE, verbosity=0)
    m.fit(Xtr[cols], ytr, eval_set=[(Xtr[cols], ytr), (Xte[cols], yte)], verbose=False)
    ev = m.evals_result()
    axs[0].plot(ev["validation_0"]["logloss"], ls="--", lw=1, label=f"treino, {nome}")
    axs[0].plot(ev["validation_1"]["logloss"], lw=1.6, label=f"teste, {nome}")
axs[0].set_title("XGBoost: log loss por rodada"); axs[0].set_xlabel("rodada de boosting"); axs[0].set_ylabel("log loss"); axs[0].legend(fontsize=7)

# (b) Random forest: erro OOB por número de árvores
for cols, nome in [(MAYO5, "5 var."), (TODAS17, "17 var.")]:
    Xi = SimpleImputer(strategy="median").fit(Xtr[cols]).transform(Xtr[cols])
    rf = RandomForestClassifier(warm_start=True, oob_score=True, min_samples_leaf=5, random_state=SEMENTE, n_jobs=-1)
    ns, err = list(range(25, 525, 25)), []
    for n in ns:
        rf.set_params(n_estimators=n); rf.fit(Xi, ytr); err.append(1 - rf.oob_score_)
    axs[1].plot(ns, err, marker="o", ms=3, label=nome)
axs[1].set_title("Random forest: erro OOB"); axs[1].set_xlabel("número de árvores"); axs[1].set_ylabel("erro OOB"); axs[1].legend(fontsize=7)

# (c) Regressão logística penalizada: AUROC de teste ao longo de C
Cs = np.logspace(-3, 1, 15); auc_tr, auc_te = [], []
for c in Cs:
    p = pipe_regressao(TODAS17, True).set_params(clf__C=c, clf__l1_ratio=0.5).fit(Xtr[TODAS17], ytr)
    auc_tr.append(roc_auc_score(ytr, p.predict_proba(Xtr[TODAS17])[:, 1])); auc_te.append(roc_auc_score(yte, p.predict_proba(Xte[TODAS17])[:, 1]))
axs[2].semilogx(Cs, auc_tr, "--", label="treino"); axs[2].semilogx(Cs, auc_te, label="teste")
axs[2].set_title("RL elastic net, 17 var.: AUROC vs. C"); axs[2].set_xlabel("C (inverso da regularização)"); axs[2].set_ylabel("AUROC"); axs[2].legend(fontsize=7)
plt.tight_layout(); plt.savefig("figs/curvas_iteracao.png", dpi=200, bbox_inches="tight"); plt.show()"""))

C.append(md("### 3.2 Avaliação principal: desenho 2 x 2 em validação cruzada 5 x 5 aninhada"))
C.append(code("""import time
t0 = time.time()
folds, oof = validacao_cruzada(X[rot], y[rot], n_rep=N_REP, n_folds=N_FOLDS)
folds.to_csv("resultados/folds.csv", index=False); oof.to_csv("resultados/oof.csv")
print(f"Tempo: {time.time() - t0:.0f} s")"""))
C.append(code("""resumo = folds.drop(columns="Fold").groupby("Modelo", sort=False).agg(["mean", "std"])
fmt = resumo.copy()
tab = pd.DataFrame({c: [f"{m:.3f} ± {s:.3f}" for m, s in zip(resumo[(c, 'mean')], resumo[(c, 'std')])] for c in ["AUROC", "AUPRC", "Brier", "CITL", "Incl. calibr."]}, index=resumo.index)
tab"""))
C.append(code("""# Valor incremental: diferença de AUROC em relação ao Escore de Mayo, com IC 95% por bootstrap de pacientes
yy = y[rot].to_numpy()
linhas = []
for ref in ["Mayo 1989 (coef. publicados)", "RL, 5 var. (Mayo reestimado)"]:
    for nome in oof.columns:
        if nome == ref: continue
        d, lo, hi = bootstrap_diferenca(yy, oof[ref].to_numpy(), oof[nome].to_numpy())
        linhas.append({"Referência": ref, "Modelo": nome, "ΔAUROC": round(d, 3), "IC 95%": f"[{lo:+.3f}; {hi:+.3f}]", "Inclui zero?": "sim" if lo <= 0 <= hi else "não"})
incremental = pd.DataFrame(linhas); incremental.to_csv("resultados/valor_incremental.csv", index=False)
resumo.to_csv("resultados/resumo_cv.csv")
incremental"""))
C.append(code("""# Tabela 2 x 2: AUROC médio (desvio) e custo de dados
celula = lambda n: f"{resumo.loc[n, ('AUROC','mean')]:.3f} ± {resumo.loc[n, ('AUROC','std')]:.3f}"
t22 = pd.DataFrame({
    f"5 variáveis (elegíveis sem imputação: {comp5})": [celula("RL, 5 var. (Mayo reestimado)") + "  [Mayo 1989: " + celula("Mayo 1989 (coef. publicados)") + "]",
                                                        celula("Random forest, 5 var.") + " (RF) / " + celula("XGBoost, 5 var.") + " (XGB)"],
    f"17 variáveis (elegíveis sem imputação: {comp17})": [celula("RL penalizada, 17 var."),
                                                          celula("Random forest, 17 var.") + " (RF) / " + celula("XGBoost, 17 var.") + " (XGB)"]},
    index=["Regressão", "Aprendizado de máquina"])
t22"""))
C.append(code("""cores = {"Mayo 1989 (coef. publicados)": "#444444", "RL, 5 var. (Mayo reestimado)": "#1f77b4", "RL penalizada, 17 var.": "#6baed6",
         "Random forest, 5 var.": "#2ca02c", "Random forest, 17 var.": "#98df8a", "XGBoost, 5 var.": "#d62728", "XGBoost, 17 var.": "#ff9896"}
fig, axs = plt.subplots(1, 3, figsize=(15, 4.3))
# (a) AUROC por fold
dados = [folds.loc[folds.Modelo == n, "AUROC"] for n in oof.columns]
bp = axs[0].boxplot(dados, vert=False, patch_artist=True, tick_labels=list(oof.columns))
for patch, n in zip(bp["boxes"], oof.columns): patch.set_facecolor(cores[n]); patch.set_alpha(.7)
axs[0].set_xlabel("AUROC (25 folds)"); axs[0].set_title("Discriminação"); axs[0].invert_yaxis(); axs[0].tick_params(axis="y", labelsize=8)
# (b) curvas ROC (predições fora-do-fold médias)
for n in oof.columns:
    f, t, _ = roc_curve(yy, oof[n]); axs[1].plot(f, t, c=cores[n], lw=1.3, label=f"{n} ({roc_auc_score(yy, oof[n]):.3f})")
axs[1].plot([0, 1], [0, 1], ":", c="gray"); axs[1].set_xlabel("1 - especificidade"); axs[1].set_ylabel("sensibilidade"); axs[1].set_title("Curvas ROC"); axs[1].legend(fontsize=6.5, loc="lower right")
# (c) curvas de calibração
for n in oof.columns:
    fo, mp = calibration_curve(yy, oof[n], n_bins=8, strategy="quantile"); axs[2].plot(mp, fo, marker="o", ms=3, c=cores[n], lw=1.2, label=n)
axs[2].plot([0, 1], [0, 1], ":", c="gray"); axs[2].set_xlabel("probabilidade prevista"); axs[2].set_ylabel("frequência observada"); axs[2].set_title("Calibração (decis de risco)"); axs[2].legend(fontsize=6.5)
plt.tight_layout(); plt.savefig("figs/discriminacao_roc_calibracao.png", dpi=200, bbox_inches="tight"); plt.show()"""))

C.append(md("### 3.3 Validação quase externa: desenvolvimento nos pacientes do ensaio, teste nos não randomizados"))
C.append(code("""qe, ntr, nte, nev = validacao_quase_externa(df, X, y)
qe.to_csv("resultados/quase_externa.csv", index=False)
print(f"Treino: {ntr} pacientes randomizados | Teste: {nte} não randomizados ({nev} óbitos em 5 anos)")
print("No teste, as variáveis exclusivas do ensaio estão ausentes e são imputadas (17 var.) ou tratadas nativamente (XGBoost).")
qe.set_index("Modelo").round(3)"""))

C.append(md("### 3.4 Braço de controle: vazamento por `N_Days` no enquadramento da PS3E26 (3 classes)"))
C.append(code("""vz = experimento_vazamento(df, X, n_rep=N_REP)
vz.to_csv("resultados/vazamento.csv", index=False)
vz_res = vz.drop(columns="Fold").groupby("Entrada").agg(["mean", "std"]).round(3)
vz_res"""))
C.append(code("""fig, axs = plt.subplots(1, 2, figsize=(9, 3.2))
for ax, met in zip(axs, ["AUROC macro (OvR)", "Log loss"]):
    d = [vz.loc[vz.Entrada == e, met] for e in ["sem N_Days", "com N_Days"]]
    ax.boxplot(d, tick_labels=["sem N_Days", "com N_Days"]); ax.set_title(met)
plt.suptitle("XGBoost, 17 variáveis, Status em 3 classes (C, CL, D)", fontsize=10); plt.tight_layout(); plt.savefig("figs/vazamento_n_days.png", dpi=200, bbox_inches="tight"); plt.show()"""))

C.append(md("""## 4. Leitura dos resultados

- **Discriminação:** compare cada célula com o Escore de Mayo pela tabela de valor incremental; intervalos que incluem zero indicam ausência de evidência de ganho.
- **Desenho 2 x 2:** a leitura vertical (mesma coluna) isola o algoritmo; a horizontal (mesma linha), as variáveis extras, que custam pacientes elegíveis.
- **Calibração:** inclinação próxima de 1 e CITL próximo de 0 indicam probabilidades confiáveis.
- **Vazamento:** a diferença entre os braços com e sem `N_Days` mede o quanto o enquadramento da PS3E26 infla o desempenho.

As conclusões e a discussão estão no `README.md` e no artigo."""))

nb["cells"] = C
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nb["metadata"]["language_info"] = {"name": "python"}
nbf.write(nb, "ml4health_cbp_mayo.ipynb")
print("ok", len(C), "celulas")

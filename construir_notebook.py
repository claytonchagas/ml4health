"""Gera o notebook de demonstração do trabalho final (versão SBCAS 2027).

O notebook não duplica o código da análise: importa as funções de sobrevivencia.py e experimento.py (a mesma fonte
usada na execução oficial) e lê os resultados oficiais de resultados_sbcas/. Uso: python construir_notebook.py
A primeira versão (classificação em 5 anos, outubro de 2026) está no ramo entrega-disciplina-out2026."""
import nbformat as nbf

md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell
C = []

C.append(md("""# O aprendizado de máquina supera o modelo clínico? Um estudo de caso em colangite biliar primária

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/claytonchagas/ml4health/blob/main/ml4health_cbp_mayo.ipynb)

**Trabalho final da disciplina TCC00367, Introdução ao Aprendizado de Máquina para Saúde (PGC/UFF).** Clayton Escouper das Chagas e Flávio Seixas. Documentação completa no [README](https://github.com/claytonchagas/ml4health#readme) e artigo em `sbcas/artigo/main.pdf`.

**Pergunta.** Um serviço que estima o risco de pacientes com colangite biliar primária com as cinco variáveis do modelo de Mayo (idade, bilirrubina, albumina, tempo de protrombina e edema) ganharia algo ao trocar o modelo de Cox por um modelo de aprendizado de máquina? Comparamos, nos mesmos pacientes e nas mesmas partições, quatro modelos de sobrevivência num desenho 2 × 2:

| | 5 variáveis de Mayo | 17 variáveis |
|---|---|---|
| **Cox** | Cox de Mayo reestimado (**referência**) | Cox penalizado (*elastic net*) |
| **Aprendizado de máquina** | Random survival forest (RSF) | Random survival forest (RSF) |

O desfecho é óbito ou transplante em até cinco anos, a métrica principal é o C de Uno em cinco anos e a leitura segue um plano registrado antes da análise (margem de +0,02 no C de Uno).

**Como usar.** Execute as células em ordem. O modo de execução é escolhido na seção 2.4:

- `"apresentacao"` (padrão, 2 a 4 minutos): carrega os dados, mostra as curvas de iteração, treina os quatro modelos ao vivo em uma partição e lê os resultados oficiais para as tabelas e os gráficos;
- `"rapido"` (15 a 25 minutos): refaz a validação cruzada com 1 repetição e um *bootstrap* menor, sem gravar por cima dos resultados oficiais;
- `"completo"` (várias horas no Colab gratuito): executa os scripts da análise e regrava `resultados_sbcas/`."""))

# ------------------------------------------------------------------------------------------------ 1
C.append(md("""## 1. Dependências do ambiente de execução

A célula abaixo prepara o ambiente: no Colab, clona o repositório (código, dados e resultados oficiais) e instala o que faltar. Os pacotes principais são `scikit-survival` (modelos e métricas de sobrevivência), `scikit-learn`, `pandas`, `numpy` e `matplotlib`; `xgboost` só é usado na análise de classificação da primeira versão. As versões exatas da execução oficial estão em `requirements.txt` (Python 3.13, scikit-learn 1.9.1, scikit-survival 0.28.0); no Colab, os números de uma reexecução podem diferir na terceira casa decimal."""))
C.append(code("""import importlib.util, os, subprocess, sys

REPO = "https://github.com/claytonchagas/ml4health"
if not os.path.exists("sobrevivencia.py"):            # no Colab (ou fora do repositório): clona e entra na pasta
    if not os.path.exists("ml4health"):
        subprocess.run(["git", "clone", "--depth", "1", REPO], check=True)
    os.chdir("ml4health")

pacotes = {"sksurv": "scikit-survival", "xgboost": "xgboost", "matplotlib": "matplotlib"}
faltando = [pip for mod, pip in pacotes.items() if importlib.util.find_spec(mod) is None]
if faltando:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", *faltando])

import numpy, pandas, sklearn, sksurv, matplotlib
print("Pasta de trabalho:", os.getcwd())
print("Python", sys.version.split()[0])
for m in (numpy, pandas, sklearn, sksurv, matplotlib):
    print(f"{m.__name__:12s} {m.__version__}")"""))

# ------------------------------------------------------------------------------------------------ 2
C.append(md("""## 2. Etapas de execução

### 2.1 Bibliotecas utilizadas

Além das bibliotecas gerais, o notebook importa os módulos do próprio projeto: `experimento.py` (carga e codificação dos dados) e `sobrevivencia.py` (modelos, métricas, validação cruzada e valor incremental). São os mesmos arquivos usados na execução oficial que gerou o artigo."""))
C.append(code("""import time, warnings
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown

from sklearn.base import clone
from sklearn.model_selection import RepeatedStratifiedKFold
from sksurv.linear_model import CoxPHSurvivalAnalysis, CoxnetSurvivalAnalysis
from sksurv.ensemble import RandomSurvivalForest
from sksurv.metrics import concordance_index_ipcw
from sksurv.nonparametric import kaplan_meier_estimator

import experimento as exp
import sobrevivencia as sv
from sobrevivencia import HORIZONTE, MARGEM, N_BOOT, N_CONFIG_RSF, REFERENCIA, SEMENTE

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False})
pd.set_option("display.precision", 3)
R = "resultados_sbcas/"
ALT = ["Cox penalizado, 17 var.", "RSF, 5 var.", "RSF, 17 var."]
ORDEM = [REFERENCIA] + ALT
CORES = dict(zip(ORDEM, ["#1f4e79", "#7fa7d0", "#c0504d", "#e6a19e"]))
pd.set_option("display.float_format", lambda v: f"{v:.3f}")
pd.set_option("display.max_colwidth", 80)
NOMES = {"Age": "Idade", "Sex_M": "Sexo masculino", "Drug_Dpen": "Tratamento (D-penicilamina)", "Ascites": "Ascite",
         "Hepatomegaly": "Hepatomegalia", "Spiders": "Aranhas vasculares", "Edema": "Edema", "Bilirubin": "Bilirrubina",
         "Cholesterol": "Colesterol", "Albumin": "Albumina", "Copper": "Cobre urinário", "Alk_Phos": "Fosfatase alcalina",
         "SGOT": "AST", "Tryglicerides": "Triglicerídeos", "Platelets": "Plaquetas", "Prothrombin": "Tempo de protrombina",
         "Stage": "Estágio histológico"}"""))

C.append(md("""### 2.2 Funções de apoio

As funções que definem a análise estão em `sobrevivencia.py`. As três mais importantes são mostradas abaixo:

- `modelos()`: os quatro *pipelines* (pré-processamento + modelo) e os espaços de busca de hiperparâmetros fixados no plano. Toda etapa que aprende com os dados (logaritmo, imputação, padronização, escolha de hiperparâmetros) fica dentro do `Pipeline` e é refeita no treino de cada partição;
- `metricas()`: C de Uno, AUC e Brier em cinco anos e Brier integrado no conjunto de teste, com a distribuição de censura estimada no treino;
- `valor_incremental()`: diferença de C de Uno contra a referência nas predições fora do treino, com *bootstrap* pareado de pacientes e intervalo de Bonferroni.

Outras funções usadas: `preparar()` (carga e rótulo de sobrevivência), `ajustar()` (busca aninhada pelo C de Uno em cinco anos), `predizer()` (risco em cinco anos, $1 - S(5\\ \\text{anos} \\mid \\mathbf{x})$), `validacao_cruzada()` e `calibracao_5anos()`."""))
C.append(code("""import inspect
for fn in (sv.modelos, sv.metricas):
    print(inspect.getsource(fn))"""))
C.append(md("Funções auxiliares do notebook (leitura dos resultados e gráficos):"))
C.append(code("""def ler(nome):
    \"\"\"Lê um CSV de resultados_sbcas/.\"\"\"
    return pd.read_csv(R + nome)


def particao(df_part, rep, k):
    \"\"\"Índices de treino e teste da partição k da repetição rep, tal como gravados na execução oficial.\"\"\"
    col = df_part[f"Repetição {rep}"].to_numpy()
    return np.where(col != k)[0], np.where(col == k)[0]


def hiperparametros_da_particao(nome, fold):
    \"\"\"Hiperparâmetros escolhidos pela busca aninhada na execução oficial, no formato do Pipeline.\"\"\"
    h = ler("hiperparametros.csv")
    h = h[(h.Modelo == nome) & (h.Fold == fold)].iloc[0]
    if nome.startswith("Cox penalizado"):
        return {"m__l1_ratio": float(h["l1_ratio"]), "m__alphas": [float(h["alphas"])]}
    if nome.startswith("RSF"):
        mf = h["max_features"]
        mf = mf if mf == "sqrt" else float(mf)
        md = None if pd.isna(h["max_depth"]) else int(h["max_depth"])
        return {"m__min_samples_split": int(h["min_samples_split"]), "m__min_samples_leaf": int(h["min_samples_leaf"]),
                "m__max_features": mf, "m__max_depth": md}
    return {}


def grafico_delta(vi, tc, titulo):
    \"\"\"ΔC contra a referência com os dois intervalos de Bonferroni e a margem de +0,02.\"\"\"
    fig, ax = plt.subplots(figsize=(7.5, 3))
    for i, mod in enumerate(ALT):
        v, t = vi.loc[mod], tc.loc[mod]
        ax.errorbar(v["Diferença"], i + 0.12, xerr=[[v["Diferença"] - v["ICBonf_inf"]], [v["ICBonf_sup"] - v["Diferença"]]],
                    fmt="o", color=CORES[mod], capsize=3, label="bootstrap (plano)" if i == 0 else None)
        m = t["Diferença média por partição"]
        ax.errorbar(m, i - 0.12, xerr=[[m - t["IC Bonferroni inf"]], [t["IC Bonferroni sup"] - m]],
                    fmt="s", color=CORES[mod], mfc="white", capsize=3, label="teste t corrigido" if i == 0 else None)
    ax.axvline(0, color="grey", lw=1); ax.axvline(MARGEM, color="black", ls="--", lw=1)
    ax.set_yticks(range(len(ALT)), ALT); ax.set_ylim(len(ALT) - 0.5, -0.9)
    ax.text(MARGEM, -0.75, " margem +0,02", fontsize=8)
    ax.set_xlabel("ΔC de Uno em 5 anos (modelo menos referência), IC de Bonferroni 98,3%")
    ax.set_title(titulo, fontsize=10); ax.legend(fontsize=8, loc="upper left", frameon=False, ncol=2)
    plt.tight_layout(); plt.show()"""))

C.append(md("""### 2.3 Carregamento e pré-processamento do dataset

**Dados.** Coorte de 418 pacientes da Mayo Clinic (1974 a 1984), a mesma do UCI 878 ([doi.org/10.24432/C5R02G](https://doi.org/10.24432/C5R02G)). A execução usa a cópia versionada `data/pbc_rdatasets.csv` (o `survival::pbc` do R), verificada por SHA-256 a cada carga. Desses pacientes, 312 participaram de dois ensaios randomizados e 106 recusaram a randomização e têm só as medidas de rotina.

**Rótulo de sobrevivência.** Cada paciente vira o par (tempo, evento): o evento principal é óbito ou transplante, e quem saiu do acompanhamento sem evento é censurado no último contato. Ninguém é excluído por ter saído antes de cinco anos. `N_Days` (tempo de seguimento) define o rótulo e **nunca** entra como preditor."""))
C.append(code("""df, X, y, origem = sv.preparar("transplante_livre")
print("Origem:", origem)
print(f"Pacientes: {len(y)} | eventos (óbito ou transplante): {int(y['event'].sum())} "
      f"| eventos até 5 anos: {int((y['event'] & (y['time'] <= HORIZONTE)).sum())}")
print("Situação final:", df["Status"].map({"C": "censura", "CL": "transplante", "D": "óbito"}).value_counts().to_dict())
print("Randomizados:", int(df["Drug"].notna().sum()), "| não randomizados:", int(df["Drug"].isna().sum()))
print("Pacientes com as 17 variáveis completas:", int(X[exp.TODAS17].notna().all(axis=1).sum()),
      "| com as 5 de Mayo completas:", int(X[exp.MAYO5].notna().all(axis=1).sum()))
X.head()"""))
C.append(code("""fig, ax = plt.subplots(1, 2, figsize=(11, 3.4))
for rotulo, mask in [("todos (418)", np.ones(len(y), bool)), ("randomizados (312)", df["Drug"].notna().to_numpy()),
                     ("não randomizados (106)", df["Drug"].isna().to_numpy())]:
    t, s = kaplan_meier_estimator(y[mask]["event"], y[mask]["time"])
    ax[0].step(t / 365.25, s, where="post", label=rotulo)
ax[0].axvline(5, color="grey", ls=":"); ax[0].set_xlabel("Anos"); ax[0].set_ylabel("Sobrevida livre de transplante")
ax[0].set_title("Kaplan-Meier", fontsize=10); ax[0].legend(fontsize=8, frameon=False)
aus = X[exp.TODAS17].isna().sum().sort_values()
ax[1].barh([NOMES[c] for c in aus.index], aus.values, color=["#1f4e79" if c in exp.MAYO5 else "#bbbbbb" for c in aus.index])
ax[1].set_xlabel("Pacientes com valor ausente"); ax[1].set_title("Ausentes por variável (azul: variáveis de Mayo)", fontsize=10)
plt.tight_layout(); plt.show()"""))
C.append(md("""**Pré-processamento.** Nos modelos de Cox: logaritmo das variáveis laboratoriais assimétricas, imputação (mediana com 5 variáveis; imputação iterativa multivariada com 17) e padronização. Nas florestas: só imputação, na escala original. Abaixo, o *pipeline* do Cox de Mayo ajustado no treino da primeira partição e aplicado ao seu teste: o teste é transformado com a mediana, as médias e os desvios do treino."""))
C.append(code("""part = pd.read_csv(R + "particoes.csv", index_col=0)
tr, te = particao(part, 0, 0)
nome, cols, est, grade, n_config = sv.modelos()[0]
pre = clone(est)[:-1].fit(X.iloc[tr][cols])
print(f"Partição 0 da repetição 0: {len(tr)} pacientes de treino, {len(te)} de teste")
pd.DataFrame(pre.transform(X.iloc[te][cols]), columns=cols, index=X.index[te]).head()"""))

C.append(md("""### 2.4 Hiperparâmetros utilizados

Escolha aqui o **modo de execução**. Os hiperparâmetros abaixo foram fixados no plano de análise; os valores de cada modelo são escolhidos por busca aninhada (3 partições internas, critério C de Uno em cinco anos) dentro do treino de cada partição externa."""))
C.append(code("""MODO = "apresentacao"     # "apresentacao" (padrão), "rapido" ou "completo"

print(f"Horizonte: {HORIZONTE} dias (5 anos) | semente: {SEMENTE} | validação cruzada: 5 repetições x 5 partições")
print(f"Configurações sorteadas por floresta: {N_CONFIG_RSF} | reamostragens bootstrap: {N_BOOT} | margem: +{MARGEM}")
for nome, cols, est, grade, n_config in sv.modelos():
    m = est.named_steps["m"]
    fixos = {k: v for k, v in m.get_params().items() if k in ("n_estimators", "ties", "alpha", "fit_baseline_model")}
    print(f"\\n{nome}: {len(cols)} variáveis | fixos: {fixos}")
    if grade:
        print(f"  busca: {n_config} configurações em", {k.replace('m__', ''): (v if k != 'm__alphas' else
              [round(a[0], 4) for a in v]) for k, v in grade.items()})"""))
C.append(md("Hiperparâmetros escolhidos nas 25 partições da execução oficial (frequência de cada valor):"))
C.append(code("""h = ler("hiperparametros.csv")
for nome, colunas in [("Cox penalizado, 17 var.", ["l1_ratio", "alphas", "coeficientes não nulos"]),
                      ("RSF, 5 var.", ["min_samples_leaf", "min_samples_split", "max_features", "max_depth"]),
                      ("RSF, 17 var.", ["min_samples_leaf", "min_samples_split", "max_features", "max_depth"])]:
    sub = h[h.Modelo == nome]
    print(nome + ":")
    for c in colunas:
        cont = sub[c].fillna("livre").astype(str).value_counts().to_dict()
        print(f"  {c}: {cont}")"""))

# ------------------------------------------------------------------------------------------------ 3
C.append(md("""## 3. Execução

### 3.1 Valores e gráficos de iteração

Modelos de sobrevivência não são treinados por épocas como uma rede neural, mas cada um tem um eixo de iteração que mostra como o ajuste evolui. Os três gráficos usam o treino e o teste da primeira partição:

- **Cox de Mayo:** a verossimilhança parcial negativa a cada iteração de Newton-Raphson (a "perda" do Cox), que converge em poucas iterações;
- **Cox penalizado:** o caminho de regularização, isto é, o C de Uno no teste e o número de coeficientes não nulos ao longo das intensidades de penalização, para cada proporção L1;
- **RSF de 17 variáveis:** o C de Uno no teste e o C fora da amostra *bootstrap* (*out-of-bag*) conforme o número de árvores cresce, com os hiperparâmetros escolhidos nessa partição."""))
C.append(code("""def nll_parcial(beta, Z, tempo, evento):
    \"\"\"Verossimilhança parcial negativa de Cox (empates de Breslow), dividida pelo número de pacientes.\"\"\"
    eta = Z @ beta
    ordem = np.argsort(-tempo)
    eta_o, ev_o, t_o = eta[ordem], evento[ordem], tempo[ordem]
    log_risco = np.logaddexp.accumulate(eta_o)                # log da soma de exp(eta) no conjunto de risco
    # empates: o conjunto de risco inclui todos com o mesmo tempo (o maior acumulado entre os empatados)
    df_t = pd.DataFrame({"t": t_o, "lr": log_risco})
    lr = df_t.groupby("t")["lr"].transform("max").to_numpy()
    return -np.sum(ev_o * (eta_o - lr)) / len(tempo)

nome, cols, est, grade, _ = sv.modelos()[0]
pre = clone(est)[:-1].fit(X.iloc[tr][cols]); Ztr = pre.transform(X.iloc[tr][cols]); Zte = pre.transform(X.iloc[te][cols])
perdas = []
warnings.filterwarnings("ignore", category=UserWarning)   # avisos esperados: penalização que zera tudo; poucas árvores no OOB
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for k in range(0, 9):
        beta = np.zeros(len(cols)) if k == 0 else CoxPHSurvivalAnalysis(alpha=0.0, ties="breslow", n_iter=k).fit(Ztr, y[tr]).coef_
        perdas.append(nll_parcial(beta, Ztr, y[tr]["time"], y[tr]["event"]))

nome, cols, est, grade, _ = sv.modelos()[1]
pre = clone(est)[:-1].fit(X.iloc[tr][cols]); Ztr17 = pre.transform(X.iloc[tr][cols]); Zte17 = pre.transform(X.iloc[te][cols])
alphas = np.logspace(0, -3, 40)
caminho = {}
for l1 in [0.1, 0.5, 0.9, 1.0]:
    cn = CoxnetSurvivalAnalysis(l1_ratio=l1, alphas=alphas, fit_baseline_model=False).fit(Ztr17, y[tr])
    cs = [concordance_index_ipcw(y[tr], y[te], Zte17 @ cn.coef_[:, j], tau=HORIZONTE)[0] for j in range(len(cn.alphas_))]
    caminho[l1] = (cn.alphas_, cs, (np.abs(cn.coef_) > 1e-10).sum(axis=0))

nome, cols, est, grade, _ = sv.modelos()[3]
hp = hiperparametros_da_particao(nome, 0)
imp = clone(est)[:-1].fit(X.iloc[tr][cols]); Wtr = imp.transform(X.iloc[tr][cols]); Wte = imp.transform(X.iloc[te][cols])
rsf = RandomSurvivalForest(n_estimators=10, warm_start=True, oob_score=True, random_state=SEMENTE, n_jobs=-1,
                           **{k.replace("m__", ""): v for k, v in hp.items()})
n_arvores, c_teste, c_oob = [], [], []
for n in [10, 25, 50, 75, 100, 150, 200, 250, 300]:
    rsf.set_params(n_estimators=n).fit(Wtr, y[tr])
    r5 = 1 - np.array([f(HORIZONTE) for f in rsf.predict_survival_function(Wte)])
    n_arvores.append(n); c_teste.append(concordance_index_ipcw(y[tr], y[te], r5, tau=HORIZONTE)[0]); c_oob.append(rsf.oob_score_)

fig, ax = plt.subplots(1, 3, figsize=(14, 3.5))
ax[0].plot(range(len(perdas)), perdas, "o-", color=CORES[REFERENCIA])
ax[0].set_xlabel("Iteração de Newton-Raphson"); ax[0].set_ylabel("Verossimilhança parcial negativa / n")
ax[0].set_title("Cox de Mayo: perda por iteração", fontsize=10)
for l1, (a, cs, nz) in caminho.items():
    ax[1].plot(a, cs, label=f"proporção L1 = {l1}")
ax[1].set_xscale("log"); ax[1].invert_xaxis(); ax[1].set_xlabel("Intensidade da penalização (α), decrescente")
ax[1].set_ylabel("C de Uno no teste"); ax[1].set_title("Cox penalizado: caminho de regularização", fontsize=10)
ax[1].legend(fontsize=7, frameon=False)
ax[2].plot(n_arvores, c_teste, "o-", color=CORES["RSF, 17 var."], label="C de Uno no teste")
ax[2].plot(n_arvores, c_oob, "s--", color="grey", label="C fora da amostra bootstrap (OOB)")
ax[2].set_xlabel("Número de árvores"); ax[2].set_title("RSF de 17 variáveis: desempenho por número de árvores", fontsize=10)
ax[2].legend(fontsize=7, frameon=False)
plt.tight_layout(); plt.show()
print("Perda do Cox por iteração:", np.round(perdas, 4))
a, cs, nz = caminho[0.5]
print("Cox penalizado (L1 = 0,5): coeficientes não nulos de", nz.min(), "a", nz.max(), "ao longo do caminho")"""))

C.append(md("""### 3.2 Os quatro modelos treinados ao vivo em uma partição

Antes de olhar as 25 partições, uma partição treinada aqui mesmo: a primeira da primeira repetição, com os hiperparâmetros que a busca aninhada escolheu nela na execução oficial. Como as partições, as sementes e os hiperparâmetros são os mesmos, as métricas devem coincidir com as gravadas em `resultados_sbcas/folds.csv` (última coluna), a menos de diferenças de versão das bibliotecas."""))
C.append(code("""folds_oficiais = ler("folds.csv")
linhas, riscos = [], {}
t0 = time.time()
for nome, cols, est, grade, n_config in sv.modelos():
    m = clone(est).set_params(**hiperparametros_da_particao(nome, 0)).fit(X.iloc[tr][cols], y[tr])
    esc, r5, fs = sv.predizer(m, X.iloc[te][cols])
    riscos[nome] = r5
    met = sv.metricas(y[tr], y[te], r5, fs)
    oficial = folds_oficiais[(folds_oficiais.Modelo == nome) & (folds_oficiais.Fold == 0)]["C de Uno (5 anos)"].iloc[0]
    linhas.append({"Modelo": nome, **{k: v for k, v in met.items() if k != "Suporte 1 a 5 anos"},
                   "C de Uno oficial (folds.csv)": oficial})
print(f"Tempo: {time.time() - t0:.0f} s")
pd.DataFrame(linhas).set_index("Modelo").drop(columns=["C de Harrell (risco em 5 anos)"])"""))

C.append(md("""### 3.3 Validação cruzada 5 × 5 aninhada

Conforme o `MODO`:

- `"apresentacao"`: lê os resultados oficiais (25 partições, 2.000 reamostragens);
- `"rapido"`: refaz a validação cruzada com 1 repetição (5 partições) e 200 reamostragens, só na memória;
- `"completo"`: executa os scripts da análise, que regravam `resultados_sbcas/` (várias horas no Colab gratuito)."""))
C.append(code("""if MODO == "completo":
    for cmd in (["sobrevivencia.py"], ["sobrevivencia.py", "--desfecho", "obito"], ["ic_desempenho.py"],
                ["calibracao_figura.py"], ["curva_decisao.py"], ["importancia_permutacao.py"],
                ["comparador_graf.py"], ["mayo1989.py"], ["sbcas/artigo/gerar_tabelas.py"]):
        print(">>", " ".join(cmd)); subprocess.run([sys.executable, *cmd], check=True)

if MODO == "rapido":
    t0 = time.time()
    folds, oof, hiper, _, _ = sv.validacao_cruzada(X, y, n_rep=1)
    vi_todos = sv.valor_incremental(y, oof, folds, ALT, n_boot=200)
    print(f"Tempo: {time.time() - t0:.0f} s (1 repetição; resultados só na memória)")
else:
    folds, vi_todos = ler("folds.csv"), ler("valor_incremental.csv")
    oof = pd.read_csv(R + "oof_risco5.csv", index_col=0)
print("Partições avaliadas por modelo:", folds.groupby("Modelo").size().to_dict())"""))

C.append(md("""### 3.4 Medidas de desempenho

**Discriminação e erro de predição** (média e desvio entre partições). C de Uno e AUC: maior é melhor (0,5 é o acaso). Brier: menor é melhor."""))
C.append(code("""met = ["C de Uno (5 anos)", "AUC (5 anos)", "Brier (5 anos)", "Brier integrado (1 a 5 anos)"]
resumo = folds.groupby("Modelo", sort=False)[met].agg(["mean", "std"]).loc[ORDEM]
display(resumo.round(3))

fig, ax = plt.subplots(figsize=(7, 3))
dados = [folds[folds.Modelo == m]["C de Uno (5 anos)"] for m in ORDEM]
bp = ax.boxplot(dados, vert=False, patch_artist=True, widths=0.5)
for caixa, m in zip(bp["boxes"], ORDEM):
    caixa.set_facecolor(CORES[m]); caixa.set_alpha(0.7)
ax.set_yticks(range(1, 5), ORDEM); ax.invert_yaxis()
ax.set_xlabel("C de Uno em 5 anos no teste de cada partição"); ax.set_title("Variação entre partições", fontsize=10)
plt.tight_layout(); plt.show()"""))

C.append(md("""**Valor incremental: a pergunta principal.** $\\Delta C$ é a diferença de C de Uno entre o modelo e a referência nos mesmos pacientes. Regra de leitura do plano: se o intervalo exclui zero, a diferença está **demonstrada**; se o limite superior fica abaixo da margem de +0,02, um ganho dessa ordem está **descartado**; se o intervalo inclui zero e passa da margem, a coorte **não decide**. Desde a regra combinada (análise posterior), um ganho só é dado como descartado quando o *bootstrap* (círculos) e o teste t corrigido (quadrados) o descartam."""))
C.append(code("""vi = vi_todos[vi_todos["Métrica"] == "C de Uno (5 anos)"].set_index("Modelo")
if MODO == "rapido":       # teste t corrigido refeito sobre as 5 partições desta execução
    from scipy import stats
    fo = folds.pivot(index="Fold", columns="Modelo", values="C de Uno (5 anos)")
    q = stats.t.ppf(1 - 0.05 / 3 / 2, len(fo) - 1)
    tc = pd.DataFrame([{"Modelo": m, "Diferença média por partição": (fo[m] - fo[REFERENCIA]).mean(),
                        "IC Bonferroni inf": (fo[m] - fo[REFERENCIA]).mean() - q * np.sqrt(1 / len(fo) + 1 / 4) * (fo[m] - fo[REFERENCIA]).std(),
                        "IC Bonferroni sup": (fo[m] - fo[REFERENCIA]).mean() + q * np.sqrt(1 / len(fo) + 1 / 4) * (fo[m] - fo[REFERENCIA]).std()}
                       for m in ALT]).set_index("Modelo")
else:
    tc = ler("valor_incremental_t_corrigido.csv").set_index("Modelo").loc[ALT]
if MODO == "rapido":
    display(Markdown("*Modo rápido: 1 repetição e 200 reamostragens. Os números diferem dos oficiais (5 repetições, 2.000 reamostragens) e servem só para demonstrar a execução.*"))

def leitura(v, t):
    boot = v["ICBonf_inf"] > 0 or v["ICBonf_sup"] < 0
    teste = t["IC Bonferroni inf"] > 0 or t["IC Bonferroni sup"] < 0
    lado = "a favor do modelo" if v["Diferença"] > 0 else "a favor da referência"
    if boot and teste:
        return f"diferença demonstrada ({lado})"
    if boot:
        return f"indício de diferença {lado} (só no bootstrap)"
    if v["ICBonf_sup"] < MARGEM and t["IC Bonferroni sup"] < MARGEM:
        return "sem ganho demonstrado; ganho de 0,02 descartado"
    if v["ICBonf_sup"] < MARGEM:
        return "sem ganho demonstrado; ganho de 0,02 descartado só no plano"
    return "sem ganho demonstrado; a coorte não decide"

tab = pd.DataFrame({m: {"ΔC": vi.loc[m, "Diferença"],
                        "IC bootstrap": f"{vi.loc[m, 'ICBonf_inf']:.4f} a {vi.loc[m, 'ICBonf_sup']:.4f}",
                        "IC teste t corrigido": f"{tc.loc[m, 'IC Bonferroni inf']:.3f} a {tc.loc[m, 'IC Bonferroni sup']:.3f}",
                        "Leitura": leitura(vi.loc[m], tc.loc[m])} for m in ALT}).T
display(tab)
grafico_delta(vi, tc, "Óbito ou transplante em 5 anos, contra o Cox de Mayo reestimado")"""))

C.append(md("""**Sensibilidade: só óbito** (transplante tratado como censura), resultados oficiais."""))
C.append(code("""vio = ler("valor_incremental_obito.csv")
vio = vio[vio["Métrica"] == "C de Uno (5 anos)"].set_index("Modelo")
tco = ler("valor_incremental_t_corrigido.csv").set_index("Modelo")
tco = tco.loc[[m + " (óbito)" for m in ALT]].rename(index=lambda s: s.replace(" (óbito)", ""))
display(pd.DataFrame({m: {"ΔC": vio.loc[m, "Diferença"], "Leitura": leitura(vio.loc[m], tco.loc[m])} for m in ALT}).T)
grafico_delta(vio, tco, "Só óbito em 5 anos, contra o Cox reestimado")"""))

C.append(md("""**Calibração em cinco anos.** Por quintis de risco previsto, o risco previsto contra o observado por Kaplan-Meier (barras: IC 95%); a diagonal é a calibração perfeita. A razão O/E resume a coorte inteira (ideal 1). Resultados oficiais, nas predições agregadas."""))
C.append(code("""cal = ler("calibracao_quintis_ic.csv")
fig, ax = plt.subplots(1, 4, figsize=(15, 3.6), sharey=True)
for a, m in zip(ax, ORDEM):
    c = cal[cal.Modelo == m]
    a.errorbar(c["Previsto (média)"], c["Observado (KM)"],
               yerr=[c["Observado (KM)"] - c["Observado IC95_inf"], c["Observado IC95_sup"] - c["Observado (KM)"]],
               fmt="o", color=CORES[m], capsize=3)
    a.plot([0, 1], [0, 1], color="grey", ls=":"); a.set_xlim(0, 1); a.set_ylim(0, 1)
    oe = c.iloc[0]
    a.set_title(f"{m}\\nO/E = {oe['O/E (5 anos)']:.2f} ({oe['O/E IC95_inf']:.2f} a {oe['O/E IC95_sup']:.2f})", fontsize=9)
    a.set_xlabel("Risco previsto em 5 anos")
ax[0].set_ylabel("Risco observado (Kaplan-Meier)")
plt.tight_layout(); plt.show()"""))

C.append(md("""**Utilidade clínica: curva de decisão.** Para a decisão hipotética de intensificar o acompanhamento de quem tem risco acima de um limiar, o benefício líquido conta os pacientes com evento corretamente sinalizados e desconta os sinalizados sem evento; 0,01 equivale a um acerto líquido a mais por 100 pacientes."""))
C.append(code("""dc = ler("curva_decisao.csv")
fig, ax = plt.subplots(figsize=(7, 3.8))
ax.plot(dc["Limiar"], dc["Tratar todos"], color="lightgrey", label="tratar todos")
ax.plot(dc["Limiar"], dc["Tratar nenhum"], color="black", lw=0.8, label="tratar nenhum")
for m in ORDEM:
    ax.plot(dc["Limiar"], dc[m], color=CORES[m], label=m)
ax.set_ylim(-0.05, 0.35); ax.set_xlabel("Limiar de risco em 5 anos"); ax.set_ylabel("Benefício líquido")
ax.legend(fontsize=7, frameon=False); plt.tight_layout(); plt.show()
dif = (dc["RSF, 17 var."] - dc[REFERENCIA])
i = dif.abs().idxmax()
print(f"Maior distância entre RSF de 17 variáveis e referência: {abs(dif[i]) * 100:.1f} acertos líquidos por 100 pacientes "
      f"no limiar de {dc.loc[i, 'Limiar']:.0%} (a favor da {'RSF' if dif[i] > 0 else 'referência'})")"""))

C.append(md("""**Subgrupo fora do treino.** Treino nos 312 randomizados e teste nos 106 não randomizados, que nenhum modelo viu. Com 17 variáveis é um teste de transporte, porque nove delas são imputadas nos 106."""))
C.append(code("""sg = ler("subgrupo_independente.csv").set_index("Modelo").loc[ORDEM]
display(sg[["C de Uno (5 anos)", "C de Uno IC95_inf", "C de Uno IC95_sup", "AUC (5 anos)", "Brier (5 anos)", "O/E (5 anos)"]].round(3))"""))

C.append(md("""**Contra a fórmula de Mayo de 1989** (análise posterior ao plano): os coeficientes publicados, sem reajuste, avaliados nos pacientes em que foram estimados."""))
C.append(code("""mf = ler("mayo1989_coorte.csv").set_index("Comparação")
display(mf[["C de Uno agregado", "Diferença", "IC bootstrap inf", "IC bootstrap sup", "IC teste corrigido inf", "IC teste corrigido sup"]].round(4))"""))

C.append(md("""**De onde vêm os ganhos aparentes.** Escolhas de avaliação que produzem ganho sem que o modelo melhore: avaliar o modelo nos próprios pacientes de treino (nos 312 randomizados) e usar o tempo de seguimento como entrada, um vazamento do desfecho (XGBoost de 17 variáveis na tarefa de três classes do Kaggle, versão de outubro)."""))
C.append(code("""da = ler("graf312_dentro_amostra.csv").set_index("Modelo")
display(da[["C de Uno dentro da amostra", "C de Uno fora da partição (agregado)", "Otimismo (Uno)"]].round(3))
vz = pd.read_csv("resultados/vazamento.csv").groupby("Entrada")[["Log loss", "AUROC macro (OvR)", "Acuracia"]].mean()
display(vz.round(3))
print(f"Ganho aparente da RSF de 17 variáveis avaliada no treino: +{da.loc['RSF, 17 var.', 'Otimismo (Uno)']:.3f} no C de Uno")
print(f"Ganho aparente do vazamento por N_Days: +{vz.loc['com N_Days', 'AUROC macro (OvR)'] - vz.loc['sem N_Days', 'AUROC macro (OvR)']:.3f} na AUROC macro")
print(f"Maior |ΔC| entre modelos (Tabela de valor incremental): {vi['Diferença'].abs().max():.3f}")"""))

C.append(md("""**O que a floresta usa.** Importância por permutação na RSF de 17 variáveis: quanto o C de Uno cai no teste ao embaralhar cada variável (média nas 5 partições da primeira repetição; barras: desvio entre partições)."""))
C.append(code("""ip = ler("importancia_permutacao_rsf17.csv").head(8).iloc[::-1]
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.barh(ip["Variável"].map(NOMES), ip["Queda média"], xerr=ip["Desvio entre partições"],
        color=["#1f4e79" if v in exp.MAYO5 else "#bbbbbb" for v in ip["Variável"]])
ax.set_xlabel("Queda no C de Uno ao permutar"); ax.set_title("Oito maiores (azul: variáveis de Mayo)", fontsize=10)
plt.tight_layout(); plt.show()"""))

# ------------------------------------------------------------------------------------------------ 4
C.append(md("""## 4. Leitura dos resultados

1. **Nenhum modelo teve ganho demonstrado** sobre o Cox com as cinco variáveis de Mayo: nenhum intervalo de $\\Delta C$ exclui zero, nos dois métodos de inferência.
2. **A resposta muda de modelo para modelo** quanto a descartar um ganho de 0,02: descartado para a RSF de 5 variáveis; para o Cox penalizado, a coorte não decide; para a RSF de 17 variáveis, o resultado depende do método e da semente do *bootstrap* (inconclusivo). Com cerca de 130 eventos até cinco anos, a meia-largura dos intervalos é da ordem da própria margem.
3. **Calibração e curva de decisão** não sugeriram vantagem do aprendizado de máquina; o Cox penalizado, o de maior C, teve o desvio de calibração mais nítido.
4. **Ganho aparente:** avaliar a floresta nos próprios pacientes de treino eleva o C mais do que qualquer diferença entre modelos, e usar o tempo de seguimento como entrada infla a AUROC na tarefa de classificação. A lição é de método: julgar o ganho do AM contra o modelo clínico pertinente, fora da amostra de treino, com a incerteza explícita e sem variáveis que vazem o desfecho.

Os números exatos, as limitações e a discussão estão no README e no artigo (`sbcas/artigo/main.pdf`)."""))

nb = nbf.v4.new_notebook()
nb["cells"] = C
nb["metadata"] = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                  "language_info": {"name": "python"}, "colab": {"provenance": []}}
nbf.write(nb, "ml4health_cbp_mayo.ipynb")
print("Notebook gerado com", len(C), "células")

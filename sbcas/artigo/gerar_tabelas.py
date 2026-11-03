"""Gera as tabelas LaTeX do artigo SBCAS direto dos CSV em resultados_sbcas/ (nenhum número é digitado à mão).

Uso (na raiz do repositório): python sbcas/artigo/gerar_tabelas.py
Saída: sbcas/artigo/tabelas/*.tex e sbcas/artigo/tabelas/numeros.tex (macros com os números citados no texto)."""
import re
from pathlib import Path

import numpy as np
import pandas as pd

R = Path("resultados_sbcas")
T = Path("sbcas/artigo/tabelas")
T.mkdir(parents=True, exist_ok=True)

ROTULO = {"Cox, 5 var. (referência)": "Cox, 5 var. (referência)", "Cox penalizado, 17 var.": "Cox penalizado, 17 var.",
          "RSF, 5 var.": "RSF, 5 var.", "RSF, 17 var.": "RSF, 17 var."}
ORDEM = list(ROTULO)
REF_COX = "Cox, 5 var. (referência)"


def f(x, d=3):
    """Número com vírgula decimal e sinal de menos tipográfico."""
    if pd.isna(x):
        return "--"
    if round(x, d) == 0:
        x = 0.0  # evita "-0,000"
    s = f"{x:.{d}f}".replace(".", "{,}")
    return f"${s}$"


def ic(a, b, d=3):
    return f"{f(a, d)} a {f(b, d)}"


def fe(x, d=3):
    """Mesmo que f, com ponto decimal (abstract em inglês)."""
    if pd.isna(x):
        return "--"
    if round(x, d) == 0:
        x = 0.0
    return f"${x:.{d}f}$"


def tabela_desempenho(suf=""):
    res = pd.read_csv(R / f"resumo_cv{suf}.csv", header=[0, 1], index_col=0)
    vi = pd.read_csv(R / f"valor_incremental{suf}.csv")
    cal = pd.read_csv(R / f"calibracao_quintis_ic{suf}.csv").groupby("Modelo").first()
    linhas = []
    for m in ORDEM:
        r = res.loc[m]
        c = cal.loc[m]
        # Fable: uma linha por modelo, "média (desvio)"; O/E com IC 95% (compacta a tabela)
        lin = [ROTULO[m]]
        for met in ["C de Uno (5 anos)", "AUC (5 anos)", "Brier (5 anos)", "Brier integrado (1 a 5 anos)"]:
            lin.append(f"{f(r[(met, 'mean')])} ({f(r[(met, 'std')])})")
        lin.append(f"{f(c['O/E (5 anos)'], 2)} ({ic(c['O/E IC95_inf'], c['O/E IC95_sup'], 2)})")
        linhas.append(" & ".join(lin) + r" \\")
    return "\n".join(linhas)


def tabela_leitura(desfechos=(("", "Óbito ou transplante, contra o Cox de Mayo reestimado (referência do plano)"),
                              ("_obito", "Só óbito, contra o Cox reestimado (sensibilidade)")), formula=True):
    """Leitura do valor incremental no C de Uno: bootstrap do plano e teste t corrigido (D11), regra combinada.
    Junção: a Tabela 3 volta a ter os três blocos (principal, só óbito, fórmula de 1989), como na versão A,
    porque os quatro pareceres comparativos pediram a sensibilidade só óbito na tabela principal."""
    tc = pd.read_csv(R / "valor_incremental_t_corrigido.csv").set_index("Modelo")
    linhas = []
    for suf, rotulo in desfechos:
        vi = pd.read_csv(R / f"valor_incremental{suf}.csv")
        vi = vi[vi["Métrica"] == "C de Uno (5 anos)"].set_index("Modelo")
        linhas.append(f"\\multicolumn{{5}}{{@{{}}l}}{{\\textit{{{rotulo}}}}} \\\\")
        for m in ORDEM[1:]:
            chave = m if suf == "" else m + " (óbito)"
            b_sup, t_sup = vi.loc[m, "ICBonf_sup"], tc.loc[chave, "IC Bonferroni sup"]
            leitura = "sim" if (b_sup < 0.02 and t_sup < 0.02) else ("não (só no plano)" if b_sup < 0.02 else "não")
            linhas.append(f"\\quad {m} & {f(vi.loc[m, 'Diferença'])} & {ic(vi.loc[m, 'ICBonf_inf'], b_sup, 4)} & "
                          f"{ic(tc.loc[chave, 'IC Bonferroni inf'], t_sup)} & {leitura} \\\\")
    if not formula:
        return "\n".join(linhas)
    # G1 (D14): mesma leitura contra a fórmula de Mayo publicada em 1989 (final, sem reajuste), nos dois desfechos.
    # Junção: o bloco só óbito (mayo1989_coorte_obito.csv, complemento H1 de D14) sai do texto e entra na tabela,
    # porque o Opus apontou que a frase com cinco intervalos era ilegível para o público do evento.
    for suf, rotulo in [("", "Óbito ou transplante, contra a fórmula de 1989 sem reajuste (análise posterior)"),
                        ("_obito", "Só óbito, contra a fórmula de 1989 sem reajuste (análise posterior)")]:
        mf = pd.read_csv(R / f"mayo1989_coorte{suf}.csv")
        linhas.append(f"\\multicolumn{{5}}{{@{{}}l}}{{\\textit{{{rotulo}}}}} \\\\")
        for m in ORDEM:
            r = mf[mf["Comparação"] == f"{m} menos fórmula"].iloc[0]
            b_sup, t_sup = r["IC bootstrap sup"], r["IC teste corrigido sup"]
            leitura = "sim" if (b_sup < 0.02 and t_sup < 0.02) else ("não (só no plano)" if b_sup < 0.02 else "não")
            rot = "Cox, 5 var. (reestimado)$^{*}$" if m == ORDEM[0] else m
            linhas.append(f"\\quad {rot} & {f(r['Diferença'])} & {ic(r['IC bootstrap inf'], b_sup, 4)} & "
                          f"{ic(r['IC teste corrigido inf'], t_sup)} & {leitura} \\\\")
    return "\n".join(linhas)


def tabela_enquadramentos():
    t = pd.read_csv(R / "tabela_enquadramentos.csv")
    curto = {"(a)": "(a) Classificação de óbito em 5 anos, sem os censurados antes de 5 anos",
             "(b)": "(b) Sobrevivência, óbito ou transplante (principal)",
             "(c)": "(c) Sobrevivência, só óbito",
             "(d)": r"(d) Classificação C/CL/D, \texttt{N\_Days} na entrada"}
    linhas = []
    for _, r in t.iterrows():
        k = r["Enquadramento"][:3]
        met = {"AUROC": "AUROC", "C de Uno (5 anos)": "C de Uno", "AUROC macro (OvR)": "AUROC macro"}[r["Métrica"]]
        comp = r"XGBoost, 17 var., com e sem \texttt{N\_Days}" if k == "(d)" else r["Comparação"]
        if pd.isna(r["IC_inf"]):
            icx = r"sem IC; ganho em 96\% das partições" if "96%" in r["Tipo de IC"] else r["Tipo de IC"]
        else:
            icx = ic(r["IC_inf"], r["IC_sup"])
        ev = f"{int(r['Eventos'])} óbitos" if k == "(d)" else str(int(r['Eventos']))  # (d): três classes; 161 são só os óbitos
        linhas.append(f"{curto[k]} & {int(r['n'])} / {ev} & {met} & {comp} & {f(r['Δ'])} & {icx}" + r" \\")
    return "\n".join(linhas)


def tabela_fontes():
    """G2: fontes de ganho aparente medidas nestes dados (cada linha muda uma só escolha de avaliação)."""
    da = pd.read_csv(R / "graf312_dentro_amostra.csv").set_index("Modelo")
    dv = pd.read_csv(R / "graf312_derivacao.csv").set_index("Fórmula").loc["inicial, n = 312"]
    gc = pd.read_csv(R / "graf312_comparacoes.csv")
    gc = gc[(gc["Métrica"] == "C de Uno (5 anos)") & gc["Comparação"].str.startswith("Cox, 7 var.")].iloc[0]
    en = pd.read_csv(R / "tabela_enquadramentos.csv")
    vz = en[en["Enquadramento"].str.startswith("(d)")].iloc[0]
    se = pd.read_csv(R / "sensibilidade_semente_bootstrap.csv")
    alt = se[se.Semente != 2026]
    mais = lambda x, d=3: ("+" if round(x, d) > 0 else "") + f(x, d)
    pct = int(re.search(r"(\d+)%", vz["Tipo de IC"]).group(1))  # "96% das 25 partições com ganho"
    n_ganho = round(pct * 25 / 100)
    # Fable (H2, parecer 1 item 6.5; parecer 4 item 2.3): três blocos, para que a legenda não prometa
    # "uma só escolha" nem "IC pareado" para linhas que não têm isso. A linha da fórmula muda também o
    # modelo (contraste não isolado); a do sorteio é sensibilidade da inferência, não ganho.
    bloco = lambda t: r"\multicolumn{4}{@{}l}{\textit{" + t + r"}} \\"
    L = [
        bloco("Fontes de ganho aparente (sem intervalo pareado)"),
        ("Avaliar no próprio treino", "RSF, 17 var.: no próprio treino contra fora da partição (312)", "C de Uno",
         mais(da.loc["RSF, 17 var.", "Otimismo (Uno)"])),
        ("", "Cox de Mayo: idem (312)", "C de Uno", mais(da.loc[REF_COX, "Otimismo (Uno)"])),
        ("Vazamento do desfecho", r"XGBoost, 17 var., com e sem o tempo de seguimento (418; classificação)",
         "AUROC macro", mais(vz["Δ"]) + f" ({n_ganho} de 25 partições)"),
        bloco("Escolhas que pouco mudaram o resultado (IC 95\\% pareado)"),
        ("Fórmula avaliada onde foi estimada",
         "Fórmula de 1989 (estimada nos 312) contra Cox de Mayo ajustado só nos 312, fora da partição",
         "C de Uno", f"{mais(-dv['Diferença (Cox menos fórmula)'])} ({ic(-dv['IC95 sup'], -dv['IC95 inf'])})"),
        ("Outras variáveis no comparador", "Cox com as 7 variáveis de Graf et al. contra Cox de Mayo (312)",
         "C de Uno", f"{mais(gc['Diferença'])} ({ic(gc['IC95 inf'], gc['IC95 sup'])})"),
        bloco("Sensibilidade da inferência (não é ganho)"),
        (r"Sorteio do \textit{bootstrap}", "Limite superior do IC da RSF, 17 var., em 25 sementes (418)",
         "C de Uno", f"{f(alt.ICBonf_sup.min(), 4)} a {f(alt.ICBonf_sup.max(), 4)}; acima de 0,02 em {int((~alt['Exclui a margem']).sum())}"),
    ]
    return "\n".join(l if isinstance(l, str) else " & ".join(l) + r" \\" for l in L)


def tabela_cox():
    hr = pd.read_csv(R / "cox5_razoes_risco.csv")
    ph = pd.read_csv(R / "cox5_riscos_proporcionais.csv")
    ph = ph[ph["Transformação do tempo"] == "km"]
    linhas = []
    for _, r in hr.iterrows():
        p_todo = ph[(ph["Janela"] == "todo o seguimento") & (ph["Variável"] == r["Variável"])]["p (Bonferroni, 5 testes)"].iloc[0]
        p_5 = ph[(ph["Janela"] == "até 5 anos") & (ph["Variável"] == r["Variável"])]["p (Bonferroni, 5 testes)"].iloc[0]
        pf = lambda p: "$>0{,}99$" if p >= 0.995 else f(p, 3)
        linhas.append(f"{r['Variável']} & {f(r['Razão de risco'], 2)} ({ic(r['IC95_inf'], r['IC95_sup'], 2)}) & {pf(p_todo)} & {pf(p_5)}" + r" \\")
    return "\n".join(linhas)


def macros():
    """Números citados no texto, como macros, para que texto e CSV não divirjam."""
    m = {}
    sub = pd.read_csv(R / "subgrupo_independente.csv").set_index("Modelo")
    for k, nome in zip("ABCD", ORDEM):
        m[f"subUno{k}"] = f(sub.loc[nome, "C de Uno (5 anos)"])
        m[f"subUnoInf{k}"] = f(sub.loc[nome, "C de Uno IC95_inf"])
        m[f"subUnoSup{k}"] = f(sub.loc[nome, "C de Uno IC95_sup"])
        m[f"subOE{k}"] = f(sub.loc[nome, "O/E (5 anos)"], 2)
    imp = pd.read_csv(R / "importancia_permutacao_rsf17.csv").set_index("Variável")["Queda média"]
    for v in ["Bilirubin", "Copper", "Albumin"]:
        m[f"imp{v}"] = f(imp[v])
    dc = pd.read_csv(R / "curva_decisao.csv")
    dif = dc["RSF, 17 var."] - dc["Cox, 5 var. (referência)"]
    m["dcMaxDif"] = f(dif.abs().max())
    # C6: sentido da maior diferença e em quantos limiares a RSF ficou à frente
    m["dcMaxLimiar"] = f"{round(100 * dc.loc[dif.abs().idxmax(), 'Limiar'])}\\%"
    m["dcMaxFavorece"] = "a referência" if dif[dif.abs().idxmax()] < 0 else "a RSF"
    m["dcRSFmaior"], m["dcLimiares"] = str(int((dif > 0).sum())), str(len(dif))
    dco = pd.read_csv(R / "curva_decisao_obito.csv")
    m["dcMaxDifObito"] = f((dco["RSF, 17 var."] - dco["Cox, 5 var. (referência)"]).abs().max())
    h = pd.read_csv(R / "hiperparametros.csv")
    nz = h[h.Modelo == "Cox penalizado, 17 var."]["coeficientes não nulos"]
    m["coxnetMin"], m["coxnetMax"] = str(int(nz.min())), str(int(nz.max()))
    # B3-01: desvio da diferença entre partições (C de Uno) e maior diferença entre C de Uno nativo e por risco5
    vi = pd.read_csv(R / "valor_incremental.csv")
    dp = vi[vi["Métrica"] == "C de Uno (5 anos)"]["Δ por partição (desvio)"]
    m["dispDifMin"], m["dispDifMax"] = f(dp.min()), f(dp.max())
    res = pd.read_csv(R / "resumo_cv.csv", header=[0, 1], index_col=0)
    nat = (res[("C de Uno, escore nativo (5 anos)", "mean")] - res[("C de Uno (5 anos)", "mean")]).abs().max()
    m["nativoMax"] = f(nat, 4)
    # D11: teste t corrigido para validação cruzada repetida (Nadeau e Bengio, 2003), nível de Bonferroni (3 comparações)
    from scipy import stats
    fo = pd.read_csv(R / "folds.csv").pivot(index="Fold", columns="Modelo", values="C de Uno (5 anos)")
    n_part, razao = len(fo), 1 / 4  # 25 partições; teste/treino = 1/4 na validação 5 x 5
    tcrit = stats.t.ppf(1 - 0.05 / 3 / 2, n_part - 1)
    linhas_nb = []
    for k, nome in zip("ABC", ORDEM[1:]):
        d = fo[nome] - fo[ORDEM[0]]
        ep = np.sqrt(1 / n_part + razao) * d.std(ddof=1)
        inf, sup = d.mean() - tcrit * ep, d.mean() + tcrit * ep
        m[f"nbSup{k}"] = f(sup, 3)
        linhas_nb.append({"Modelo": nome, "Diferença média por partição": d.mean(), "EP corrigido": ep,
                          "IC Bonferroni inf": inf, "IC Bonferroni sup": sup})
    # E3: mesmo teste para a AUC em 5 anos da RSF de 5 variáveis (única diferença demonstrada pelo bootstrap)
    fa = pd.read_csv(R / "folds.csv").pivot(index="Fold", columns="Modelo", values="AUC (5 anos)")
    d = fa["RSF, 5 var."] - fa[ORDEM[0]]
    ep = np.sqrt(1 / len(fa) + razao) * d.std(ddof=1)
    m["nbAucInfB"], m["nbAucSupB"] = f(d.mean() - tcrit * ep, 3), f(d.mean() + tcrit * ep, 3)
    linhas_nb.append({"Modelo": "RSF, 5 var. (AUC 5 anos)", "Diferença média por partição": d.mean(), "EP corrigido": ep,
                      "IC Bonferroni inf": d.mean() - tcrit * ep, "IC Bonferroni sup": d.mean() + tcrit * ep})
    # Mesmo teste na sensibilidade com óbito como evento (achado E1 da segunda revisão tripla)
    foo = pd.read_csv(R / "folds_obito.csv").pivot(index="Fold", columns="Modelo", values="C de Uno (5 anos)")
    for k, nome in zip("ABC", ORDEM[1:]):
        d = foo[nome] - foo[ORDEM[0]]
        ep = np.sqrt(1 / len(foo) + razao) * d.std(ddof=1)
        inf, sup = d.mean() - tcrit * ep, d.mean() + tcrit * ep
        m[f"nbSupObito{k}"] = f(sup, 3)
        linhas_nb.append({"Modelo": nome + " (óbito)", "Diferença média por partição": d.mean(), "EP corrigido": ep,
                          "IC Bonferroni inf": inf, "IC Bonferroni sup": sup})
    pd.DataFrame(linhas_nb).to_csv(R / "valor_incremental_t_corrigido.csv", index=False)
    # E2: estabilidade do limite de Bonferroni da RSF de 17 variáveis em 25 sementes alternativas do bootstrap
    sem = pd.read_csv(R / "sensibilidade_semente_bootstrap.csv")
    alt = sem[sem.Semente != 2026]
    mf = pd.read_csv(R / "mayo1989_coorte.csv").set_index("Comparação")
    m["formulaC"] = f(mf.loc["Fórmula de 1989 (final, n = 418)", "C de Uno agregado"])
    m["refMenosFormula"] = f(mf.loc[f"{ORDEM[0]} menos fórmula", "Diferença"])
    da = pd.read_csv(R / "graf312_dentro_amostra.csv").set_index("Modelo")
    m["otimRSF"], m["otimCox"] = f(da.loc["RSF, 17 var.", "Otimismo (Uno)"]), f(da.loc[REF_COX, "Otimismo (Uno)"])
    # G4: subgrupo contra a fórmula inicial (D15) e C de Harrell nos 312 (D16)
    sg = pd.read_csv(R / "mayo1989_subgrupo.csv").set_index("Modelo")
    m["subDifFormMax"] = f(sg.loc[["Cox penalizado, 17 var.", "RSF, 17 var."], "Dif. contra fórmula inicial (312)"].max())
    m["subEventos"] = str(int(sg["Eventos (106)"].iloc[0]))
    m["subFormulaIni"] = f(sg.loc["fórmula inicial (312)", "C de Uno (106)"])
    gc = pd.read_csv(R / "graf312_comparacoes.csv")
    gh = gc[gc["Métrica"] == "C de Harrell"]
    m["harrellGraf"] = f(gh[gh["Comparação"].str.startswith("Cox, 7 var.")]["C de a"].iloc[0])
    m["harrellMayo"] = f(gh[gh["Comparação"].str.startswith("Cox, 7 var.")]["C de b"].iloc[0])
    m["harrellRSF"] = f(gh[gh["Comparação"].str.startswith("RSF, 17 var. menos Cox, 5")]["C de a"].iloc[0])
    m["semAlt"], m["semNaoExclui"] = str(len(alt)), str(int((~alt["Exclui a margem"]).sum()))
    m["semMin"], m["semMax"] = f(alt.ICBonf_sup.min(), 4), f(alt.ICBonf_sup.max(), 4)
    # F2: C de Uno da referência nas predições agregadas (base das diferenças), nos dois desfechos
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from sobrevivencia import REFERENCIA, _cuno, preparar
    for suf, desf, nome in [("", "transplante_livre", "refAgr"), ("_obito", "obito", "refAgrObito")]:
        _, _, y, _ = preparar(desf)
        oof = pd.read_csv(R / f"oof_risco5{suf}.csv", index_col=0)
        m[nome] = f(_cuno(y, oof[REFERENCIA].to_numpy()))
        m[nome + "EN"] = fe(_cuno(y, oof[REFERENCIA].to_numpy()))
    # ---- Fable (revisão SBCAS 2027): números que o texto ainda trazia digitados à mão ----
    viC = vi[vi["Métrica"] == "C de Uno (5 anos)"].set_index("Modelo")
    m["difMin"], m["difMax"] = f(viC["Diferença"].min()), f(viC["Diferença"].max())
    m["difMinEN"], m["difMaxEN"] = fe(viC["Diferença"].min()), fe(viC["Diferença"].max())
    m["refMedio"] = f(res.loc[ORDEM[0], ("C de Uno (5 anos)", "mean")])
    m["coxpenDif"] = f(viC.loc["Cox penalizado, 17 var.", "Diferença"])
    m["coxpenSupPlano"] = f(viC.loc["Cox penalizado, 17 var.", "ICBonf_sup"])
    m["rsfDezLimitePlano"] = f(viC.loc["RSF, 17 var.", "ICBonf_sup"], 4)
    viA = vi[vi["Métrica"] == "AUC (5 anos)"].set_index("Modelo")
    m["aucRSFcinco"] = f(viA.loc["RSF, 5 var.", "Diferença"])
    m["aucRSFcincoInf"], m["aucRSFcincoSup"] = f(viA.loc["RSF, 5 var.", "ICBonf_inf"]), f(viA.loc["RSF, 5 var.", "ICBonf_sup"])
    # H9 (parecer 1, item 3): precisão alcançada, como meia-largura dos IC pareados do desfecho principal
    ml = (viC["ICBonf_sup"] - viC["ICBonf_inf"]) / 2
    m["meiaLargPlanoMin"], m["meiaLargPlanoMax"] = f(ml.min()), f(ml.max())
    tc = pd.read_csv(R / "valor_incremental_t_corrigido.csv").set_index("Modelo").loc[ORDEM[1:]]
    mlt = (tc["IC Bonferroni sup"] - tc["IC Bonferroni inf"]) / 2
    m["meiaLargTcMin"], m["meiaLargTcMax"] = f(mlt.min()), f(mlt.max())
    # Calibração: faixa do O/E e quintil mais alto da RSF de 17 variáveis
    cal = pd.read_csv(R / "calibracao_quintis_ic.csv")
    oe = cal.groupby("Modelo").first()["O/E (5 anos)"]
    m["oeMin"], m["oeMax"] = f(oe.min(), 2), f(oe.max(), 2)
    q5 = cal[(cal.Modelo == "RSF, 17 var.") & (cal.Quintil == 5)].iloc[0]
    m["rsfDezQuintilPrev"], m["rsfDezQuintilObs"] = f(q5["Previsto (média)"]), f(q5["Observado (KM)"])
    # Curva de decisão: maior diferença por 100 pacientes
    m["dcMaxDifPorCem"] = f(100 * dif.abs().max(), 1)
    # Vazamento (linha d) e classificação com exclusão (linha a), com o nível do IC (parecer 3, item 3.i)
    en = pd.read_csv(R / "tabela_enquadramentos.csv")
    vz = en[en["Enquadramento"].str.startswith("(d)")].iloc[0]
    m["vazamentoAUROC"] = f(vz["Δ"])
    ca = en[en["Enquadramento"].str.startswith("(a)")].iloc[0]
    m["classifDif"], m["classifInf"], m["classifSup"] = f(ca["Δ"]), f(ca["IC_inf"]), f(ca["IC_sup"])
    m["classifComparacoes"] = re.search(r"m=(\d+)", ca["Tipo de IC"]).group(1)
    # H1: fórmula de 1989 no desfecho só óbito (mayo1989_coorte_obito.csv), relatada no texto
    mfo = pd.read_csv(R / "mayo1989_coorte_obito.csv").set_index("Comparação")
    m["formulaCObito"] = f(mfo.loc["Fórmula de 1989 (final, n = 418)", "C de Uno agregado"])
    for pref, comp in [("refMenosFormulaObito", f"{ORDEM[0]} menos fórmula"), ("rsfCincoMenosFormulaObito", "RSF, 5 var. menos fórmula")]:
        r = mfo.loc[comp]
        m[pref] = f(r["Diferença"])
        m[pref + "Inf"], m[pref + "Sup"] = f(r["IC bootstrap inf"]), f(r["IC bootstrap sup"])
        m[pref + "TcInf"], m[pref + "TcSup"] = f(r["IC teste corrigido inf"]), f(r["IC teste corrigido sup"])
    outros = mfo.loc[["Cox penalizado, 17 var. menos fórmula", "RSF, 17 var. menos fórmula"]]
    m["outrosFormulaObitoCruzamZero"] = "sim" if ((outros["IC bootstrap inf"] < 0) & (outros["IC bootstrap sup"] > 0)).all() else "não"
    # H4: subgrupo, maior diferença dos modelos de 17 variáveis contra o Cox reestimado (não contra a fórmula)
    m["subDifRefMax"] = f(sg.loc[["Cox penalizado, 17 var.", "RSF, 17 var."], "Dif. contra Cox, 5 var. (referência)"].max())
    # H6: otimismo também em C de Harrell, a métrica prevista no plano complementar
    m["otimRSFHarrell"] = f(da.loc["RSF, 17 var.", "Otimismo (Harrell)"])
    m["otimRSFEN"] = fe(da.loc["RSF, 17 var.", "Otimismo (Uno)"])
    # Sensibilidade só óbito, resumida no texto: limites superiores pelo plano e pelo teste corrigido
    vio = pd.read_csv(R / "valor_incremental_obito.csv")
    vio = vio[vio["Métrica"] == "C de Uno (5 anos)"].set_index("Modelo")
    for k, nome in zip("ABC", ORDEM[1:]):
        m[f"obitoDif{k}"] = f(vio.loc[nome, "Diferença"])
        m[f"obitoSupPlano{k}"] = f(vio.loc[nome, "ICBonf_sup"])
    m["otimRSFdentro"], m["otimRSFfora"] = f(da.loc["RSF, 17 var.", "C de Uno dentro da amostra"]), f(da.loc["RSF, 17 var.", "C de Uno fora da partição (agregado)"])
    with open(T / "numeros.tex", "w") as fh:
        fh.write("% Gerado por gerar_tabelas.py a partir de resultados_sbcas/. Não editar.\n")
        for k, v in m.items():
            fh.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")


def main():
    macros()  # grava valor_incremental_t_corrigido.csv, usado pela tabela de leitura
    (T / "desempenho.tex").write_text(tabela_desempenho("") + "\n")
    (T / "desempenho_obito.tex").write_text(tabela_desempenho("_obito") + "\n")
    (T / "enquadramentos.tex").write_text(tabela_enquadramentos() + "\n")
    (T / "leitura.tex").write_text(tabela_leitura() + "\n")
    (T / "leitura_obito.tex").unlink(missing_ok=True)  # o bloco só óbito voltou à Tabela 3 do artigo
    (T / "fontes.tex").write_text(tabela_fontes() + "\n")
    (T / "cox.tex").write_text(tabela_cox() + "\n")
    macros()
    for p in sorted(T.glob("*.tex")):
        print(f"== {p}\n{p.read_text()}")


if __name__ == "__main__":
    main()

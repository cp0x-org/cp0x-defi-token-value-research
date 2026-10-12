"""Decomposition, variance shares and pre-registered regressions (METHOD_R4.md). Writes data/results.json."""
import json, sys, numpy as np, pandas as pd, statsmodels.formula.api as smf
P = pd.read_csv("data/panel.csv")
P["dH"] = P.H_end - P.H_start
CONT = ["y", "g", "s", "m", "ln_M_start", "ln_mc_start", "beta", "drawdown_start", "H_start", "dH"]

def winsor(d):
    d = d.copy()
    for c in CONT:
        lo = d.groupby("window")[c].transform(lambda x: x.quantile(0.025))
        hi = d.groupby("window")[c].transform(lambda x: x.quantile(0.975))
        d[c] = d[c].clip(lo, hi)
    return d

def shares(d):
    x = d[["y", "g", "m", "s"]].copy()
    x = x - d.groupby("window")[["y", "g", "m", "s"]].transform("mean")
    v = x.y.var()
    return {"business_growth_g": x.g.cov(x.y) / v, "rerating_m": x.m.cov(x.y) / v, "dilution_minus_s": (-x.s).cov(x.y) / v, "n": len(x)}

def cats(d):
    vc = d.category.value_counts()
    keep = set(vc[vc >= 10].index)
    return d.category.where(d.category.isin(keep), "other")

def fit(formula, d):
    d = d.copy(); d["cat"] = cats(d)
    m = smf.ols(formula, d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.group)[0]})
    return m

def coef(m, k):
    ci = m.conf_int().loc[k]
    return {"coef": round(float(m.params[k]), 4), "p": round(float(m.pvalues[k]), 4), "ci95": [round(float(ci[0]), 4), round(float(ci[1]), 4)]}

CTRL = "ln_M_start + ln_mc_start + beta + drawdown_start + C(cat) + C(window)"
R1 = f"y ~ g + s + {CTRL}"
R1H = f"y ~ g + s + H_start + dH + {CTRL}"
R2 = f"y ~ s + H_start + dH + {CTRL}"

def run(base, label, wins=True):
    dec = base.dropna(subset=["g", "m", "s"])  # C12a: all decomposable observations
    d = base.dropna(subset=["g", "m", "s", "beta", "drawdown_start"])
    out = {"label": label, "shares_pooled": shares(dec), "shares_by_window": {w: shares(x) for w, x in dec.groupby("window")},
           "shares_pooled_regression_sample": shares(d)}
    dw = winsor(d) if wins else d
    m1 = fit(R1, dw)
    out["R1"] = {"n": int(m1.nobs), "r2": round(m1.rsquared, 4), "g": coef(m1, "g"), "s": coef(m1, "s"), "ln_M_start": coef(m1, "ln_M_start")}
    dh = dw.dropna(subset=["H_start", "dH"])
    m1s, m1h = fit(R1, dh), fit(R1H, dh)
    out["R1h"] = {"n": int(m1h.nobs), "r2_R1_same_sample": round(m1s.rsquared, 4), "r2_R1h": round(m1h.rsquared, 4),
                  "delta_r2": round(m1h.rsquared - m1s.rsquared, 4), "H_start": coef(m1h, "H_start"), "dH": coef(m1h, "dH")}
    m2 = fit(R2, dh)
    out["R2"] = {"n": int(m2.nobs), "r2": round(m2.rsquared, 4), "s": coef(m2, "s"), "H_start": coef(m2, "H_start"),
                 "dH": coef(m2, "dH"), "ln_M_start": coef(m2, "ln_M_start"), "drawdown_start": coef(m2, "drawdown_start"), "beta": coef(m2, "beta")}
    sh = out["shares_pooled"]
    out["verdicts"] = {
        "H1_g_largest_share": sh["business_growth_g"] > max(sh["rerating_m"], sh["dilution_minus_s"]),
        "H2_s_negative_p05": out["R1"]["s"]["coef"] < 0 and out["R1"]["s"]["p"] < 0.05,
        "H3_holder_share_dR2_below_0.02": out["R1h"]["delta_r2"] < 0.02,
        "H4_lnM_negative_p05": out["R1"]["ln_M_start"]["coef"] < 0 and out["R1"]["ln_M_start"]["p"] < 0.05}
    return out

C2 = {"savings-xdai","usdx-money-usdx","crypto-com-chain","near","arbitrum","baby-doge-coin","flock-2","livepeer"}
frozen = P[~P.supply_artefact]
main = frozen[~frozen.gecko_id.isin(C2)]
P = P[~P.gecko_id.isin(C2)]
res = {"main": run(main, "main")}
rob = {"frozen_universe": run(frozen, "frozen universe without C2 exclusions")}
rob["no_winsor"] = run(main, "no winsorization", wins=False)
rob["with_artefacts"] = run(P, "including |s|>ln5")
z = main.copy(); z["H_start"] = z.H_start.fillna(0); z["H_end"] = z.H_end.fillna(0); z["dH"] = z.H_end - z.H_start
rob["H_missing_0"] = run(z, "H missing = 0")
for w in ["W1", "W2", "W3"]:
    rob[f"drop_{w}"] = run(main[main.window != w], f"drop {w}")
big = main.category.value_counts().index[0]
rob["drop_largest_cat"] = run(main[main.category != big], f"drop {big}")
sec = main.copy()
_n = sec.groupby(["window", "category"]).category.transform("size")
sec["cat2"] = sec.category.where(_n >= 5, "other")  # C12b: frozen rule, < 5 in the window pooled
lr = np.log(sec.p_end / sec.p_start)
sec["y"] = lr - lr.groupby([sec.window, sec.cat2]).transform("median")
rob["secondary_outcome"] = run(sec.drop(columns="cat2"), "token minus category median")
res["robustness"] = rob
json.dump(res, open("data/results.json", "w"), indent=1, default=float)
m = res["main"]
print(json.dumps({k: m[k] for k in ["shares_pooled", "R1", "R1h", "R2", "verdicts"]}, indent=1, default=float))
for k, v in rob.items(): print(k, v["verdicts"], "n", v["R1"]["n"])

rows = []
for k, v in [("main", res["main"])] + list(rob.items()):
    rows.append(dict(run=k, n=v["R1"]["n"], n_decomp=v["shares_pooled"]["n"], share_g=round(v["shares_pooled"]["business_growth_g"], 2), share_m=round(v["shares_pooled"]["rerating_m"], 2),
        share_minus_s=round(v["shares_pooled"]["dilution_minus_s"], 2), R1_g=v["R1"]["g"]["coef"], R1_s=v["R1"]["s"]["coef"], R1_s_p=v["R1"]["s"]["p"],
        R1_lnM=v["R1"]["ln_M_start"]["coef"], R1_lnM_p=v["R1"]["ln_M_start"]["p"], dR2_H=v["R1h"]["delta_r2"], H_start=v["R1h"]["H_start"]["coef"],
        H_start_p=v["R1h"]["H_start"]["p"], R2_beta=v["R2"]["beta"]["coef"], R2_beta_p=v["R2"]["beta"]["p"],
        H1=bool(v["verdicts"]["H1_g_largest_share"]), H2=bool(v["verdicts"]["H2_s_negative_p05"]), H3=bool(v["verdicts"]["H3_holder_share_dR2_below_0.02"]), H4=bool(v["verdicts"]["H4_lnM_negative_p05"])))
pd.DataFrame(rows).to_csv("data/runs_summary.csv", index=False)

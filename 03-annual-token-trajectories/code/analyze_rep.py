"""Part A of METHOD_R4_REPLICATION.md -> data/results_rep.json"""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
P = pd.read_csv("data/panel_rep.csv")
P["dH"] = P.H_end - P.H_start
C2 = {"savings-xdai", "usdx-money-usdx", "crypto-com-chain", "near", "arbitrum", "baby-doge-coin", "flock-2", "livepeer"}
main = P[~P.supply_artefact & ~P.gecko_id.isin(C2)]
CONT = ["y", "g", "s", "m", "ln_M_start", "ln_mc_start", "beta", "drawdown_start", "H_start", "dH"]
def winsor(d):
    d = d.copy()
    for c in CONT:
        lo = d.groupby("window")[c].transform(lambda x: x.quantile(0.025)); hi = d.groupby("window")[c].transform(lambda x: x.quantile(0.975))
        d[c] = d[c].clip(lo, hi)
    return d
def fit(f, d):
    d = d.copy(); vc = d.category.value_counts(); d["cat"] = d.category.where(d.category.isin(set(vc[vc >= 10].index)), "other")
    if d.window.nunique() < 2: f = f.replace(" + C(window)", "")
    return smf.ols(f, d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.group)[0]})
def cf(m, k):
    ci = m.conf_int().loc[k]; return {"coef": round(float(m.params[k]), 4), "p": round(float(m.pvalues[k]), 4), "ci95": [round(float(ci[0]), 4), round(float(ci[1]), 4)]}
CTRL = "ln_M_start + ln_mc_start + beta + drawdown_start + C(cat) + C(window)"
R1 = f"y ~ g + s + {CTRL}"; R1H = f"y ~ g + s + H_start + dH + {CTRL}"; R2 = f"y ~ s + H_start + dH + {CTRL}"
def run(d, wins=True):
    d = d.dropna(subset=["g", "m", "s", "beta", "drawdown_start", "H_start", "dH"])
    dw = winsor(d) if wins else d
    m1, mh, m2 = fit(R1, dw), fit(R1H, dw), fit(R2, dw)
    return {"n": int(mh.nobs), "n_by_window": dw.window.value_counts().sort_index().to_dict(), "H_start": cf(mh, "H_start"), "dH": cf(mh, "dH"),
            "delta_r2": round(mh.rsquared - m1.rsquared, 4), "R2_H_start": cf(m2, "H_start")}
res = {"pooled": run(main), "A1_A2": run(main[main.window.isin(["A1", "A2"])])}
res["verdicts"] = {"HR1": res["pooled"]["H_start"]["coef"] > 0 and res["pooled"]["H_start"]["p"] < 0.05,
                   "HR2": res["A1_A2"]["H_start"]["coef"] > 0 and res["A1_A2"]["H_start"]["p"] < 0.10}
res["reported"] = {"no_winsor": run(main, wins=False), **{w: run(main[main.window == w]) for w in ["A1", "A2", "A3"]}}
res["sample"] = {"obs_entered": int(len(P[~P.gecko_id.isin(C2)])), "obs_main_decomposable": int(main.g.notna().sum()), "protocols": int(main.group.nunique())}
json.dump(res, open("data/results_rep.json", "w"), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))

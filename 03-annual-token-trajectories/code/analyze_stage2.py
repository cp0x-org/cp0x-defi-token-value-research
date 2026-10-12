"""Stage 2 regressions per METHOD_R4_STAGE2.md -> data/results_stage2.json, data/runs_summary_stage2.csv"""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
P = pd.read_csv("data/panel_stage2.csv")
P["dH"] = P.H_end - P.H_start
C2 = {"savings-xdai", "usdx-money-usdx", "crypto-com-chain", "near", "arbitrum", "baby-doge-coin", "flock-2", "livepeer"}
P["lnp"] = np.log1p(P.new_products); P["lnc"] = np.log1p(P.new_chains)
P["lnlp"] = np.log1p(P.lost_products); P["lnlc"] = np.log1p(P.lost_chains)
CONT = ["y", "g", "s", "ln_M_start", "ln_mc_start", "beta", "drawdown_start", "H_start", "dH", "lnp", "lnc", "lnlp", "lnlc", "treasury_change"]
def winsor(d):
    d = d.copy()
    for c in CONT:
        lo = d.groupby("window")[c].transform(lambda x: x.quantile(0.025)); hi = d.groupby("window")[c].transform(lambda x: x.quantile(0.975))
        d[c] = d[c].clip(lo, hi)
    return d
def fit(f, d):
    d = d.copy(); vc = d.category.value_counts(); d["cat"] = d.category.where(d.category.isin(set(vc[vc >= 10].index)), "other")
    return smf.ols(f, d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.group)[0]})
def cf(m, k):
    return {"coef": round(float(m.params[k]), 4), "p": round(float(m.pvalues[k]), 4)}
BASE = "s + H_start + dH + ln_M_start + ln_mc_start + beta + drawdown_start + hack + C(cat) + C(window)"
def run(d, wins=True, P_VAR="lnp", C_VAR="lnc", extra=""):
    d = d.dropna(subset=["g", "m", "s", "beta", "drawdown_start", "H_start", "dH", P_VAR, C_VAR])
    dw = winsor(d) if wins else d
    f2 = f"y ~ {P_VAR} + {C_VAR} + {BASE}{extra}"
    m2 = fit(f2, dw); m1 = fit(f2 + " + g", dw)
    dt = dw.dropna(subset=["treasury_change"]); mt = fit(f2 + " + treasury_change", dt)
    o = {"n_R2s": int(m2.nobs), "R2s_products": cf(m2, P_VAR), "R2s_chains": cf(m2, C_VAR),
         "R1s_products": cf(m1, P_VAR), "R1s_chains": cf(m1, C_VAR), "R1s_g": cf(m1, "g"),
         "n_R2t": int(mt.nobs), "R2t_treasury": cf(mt, "treasury_change"), "R2s_hack": cf(m2, "hack")}
    H5 = o["R2s_products"]["coef"] > 0 and o["R2s_products"]["p"] < 0.05
    H6 = o["R2s_chains"]["coef"] > 0 and o["R2s_chains"]["p"] < 0.05
    o["verdicts"] = {"H5": H5, "H6": H6,
        "H7_products": (abs(o["R1s_products"]["coef"]) <= 0.5 * abs(o["R2s_products"]["coef"])) if H5 else None,
        "H7_chains": (abs(o["R1s_chains"]["coef"]) <= 0.5 * abs(o["R2s_chains"]["coef"])) if H6 else None,
        "H8": o["R2t_treasury"]["coef"] > 0 and o["R2t_treasury"]["p"] < 0.05}
    return o
frozen = P[~P.supply_artefact]; main = frozen[~frozen.gecko_id.isin(C2)]
res = {"main": run(main)}
rb = {"no_winsor": run(main, wins=False)}
z = main.copy(); z["H_start"] = z.H_start.fillna(0); z["H_end"] = z.H_end.fillna(0); z["dH"] = z.H_end - z.H_start
rb["H_missing_0"] = run(z)
rb["with_lost"] = run(main, extra=" + lnlp + lnlc")
for w in ["W1", "W2", "W3"]: rb[f"drop_{w}"] = run(main[main.window != w])
rb["frozen_universe"] = run(frozen)
cap = main.copy(); cap["cp"] = cap.new_products.clip(upper=10); cap["cc"] = cap.new_chains.clip(upper=10); CONT += ["cp", "cc"]
rb["raw_counts_cap10"] = run(cap, P_VAR="cp", C_VAR="cc")
res["robustness"] = rb
json.dump(res, open("data/results_stage2.json", "w"), indent=1, default=float)
rows = []
for k, v in [("main", res["main"])] + list(rb.items()):
    rows.append({"run": k, "n_R2s": v["n_R2s"], "products_R2s": v["R2s_products"]["coef"], "p_products": v["R2s_products"]["p"],
        "products_R1s": v["R1s_products"]["coef"], "chains_R2s": v["R2s_chains"]["coef"], "p_chains": v["R2s_chains"]["p"], "chains_R1s": v["R1s_chains"]["coef"],
        "n_R2t": v["n_R2t"], "treasury": v["R2t_treasury"]["coef"], "p_treasury": v["R2t_treasury"]["p"], "hack": v["R2s_hack"]["coef"], "p_hack": v["R2s_hack"]["p"],
        **{k2: v["verdicts"][k2] for k2 in v["verdicts"]}})
t = pd.DataFrame(rows); t.to_csv("data/runs_summary_stage2.csv", index=False); print(t.to_string())

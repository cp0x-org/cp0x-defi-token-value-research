"""Stage 4 (METHOD_R4_STAGE4.md, CHANGES C8-C9).
Usage: python3 analyze_stage4.py audit_list   -> writes data/stage4_audit_candidates.csv (no outcome columns)
       python3 analyze_stage4.py run          -> needs data/stage4_audit.csv, writes results"""
import sys, json, numpy as np, pandas as pd, statsmodels.formula.api as smf
P = pd.read_csv("data/panel.csv")
C2 = {"savings-xdai", "usdx-money-usdx", "crypto-com-chain", "near", "arbitrum", "baby-doge-coin", "flock-2", "livepeer"}
main = P[~P.supply_artefact & ~P.gecko_id.isin(C2)].copy()
E = pd.read_csv("data/onchain_supply.csv"); E["chain"] = "ethereum"
O = pd.read_csv("data/onchain_supply_evm.csv")
S = pd.concat([E, O], ignore_index=True)
S = S[~S.gecko_id.isin(["axelar", "dydx-chain", "geodnet"])]  # C6, C13
W = {"W1": ("2023-10-01", "2024-10-01"), "W2": ("2024-10-01", "2025-10-01"), "W3": ("2025-10-01", "2026-10-01")}
def si(r):
    x = S[S.gecko_id == r.gecko_id]
    if x.empty: return np.nan, ""
    a, b = W[r.window]; t0, t1 = x[f"NET_{a}"].iloc[0], x[f"NET_{b}"].iloc[0]
    return (np.log(t1 / t0) if pd.notna(t0) and pd.notna(t1) and t0 > 0 and t1 > 0 else np.nan), x.chain.iloc[0]
vals = [si(r) for _, r in main.iterrows()]
main["s_issue"] = [v[0] for v in vals]; main["supply_chain"] = [v[1] for v in vals]
main["u"] = main.s - main.s_issue
base = main.dropna(subset=["g", "m", "s", "beta", "drawdown_start", "s_issue"])
if sys.argv[1] == "audit_list":
    a = base.reindex(base.u.abs().sort_values(ascending=False).index).head(20)
    a[["window", "start", "end", "name", "gecko_id", "supply_chain", "s", "s_issue", "u"]].assign(
        cg_supply_change_pct=lambda d: ((np.exp(d.s) - 1) * 100).round(1), onchain_change_pct=lambda d: ((np.exp(d.s_issue) - 1) * 100).round(1)
    ).drop(columns=["s", "s_issue", "u"]).to_csv("data/stage4_audit_candidates.csv", index=False)
    print(open("data/stage4_audit_candidates.csv").read()); sys.exit()

AUD = pd.read_csv("data/stage4_audit.csv")
main = main.merge(AUD[["window", "gecko_id", "class"]], on=["window", "gecko_id"], how="left")
main["u_aud"] = np.where(main["class"] == "recount", 0.0, main.u)
main.to_csv("data/panel_stage4.csv", index=False)
base = main.dropna(subset=["g", "m", "s", "beta", "drawdown_start", "s_issue"])
CONT = ["y", "g", "s", "s_issue", "u", "u_aud", "ln_M_start", "ln_mc_start", "beta", "drawdown_start"]
def winsor(d):
    d = d.copy()
    for c in CONT:
        lo = d.groupby("window")[c].transform(lambda x: x.quantile(0.025)); hi = d.groupby("window")[c].transform(lambda x: x.quantile(0.975))
        d[c] = d[c].clip(lo, hi)
    return d
def fit(f, d):
    d = d.copy(); vc = d.category.value_counts(); d["cat"] = d.category.where(d.category.isin(set(vc[vc >= 10].index)), "other")
    return smf.ols(f, d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.group)[0]})
def cf(m, k): return {"coef": round(float(m.params[k]), 4), "p": round(float(m.pvalues[k]), 4)}
CTRL = "ln_M_start + ln_mc_start + beta + drawdown_start + C(cat) + C(window)"
def run(d, wins=True, uvar="u"):
    e = winsor(d) if wins else d
    m9 = fit(f"y ~ g + s_issue + {uvar} + {CTRL}", e); m2 = fit(f"y ~ g + s_issue + {CTRL}", e)
    o = {"n": int(m9.nobs), "u": cf(m9, uvar), "s_issue_with_u": cf(m9, "s_issue"), "s_issue_alone": cf(m2, "s_issue")}
    o["H9"] = o["u"]["coef"] < 0 and o["u"]["p"] < 0.05
    o["H2a_wide"] = o["s_issue_alone"]["coef"] < 0 and o["s_issue_alone"]["p"] < 0.05
    return o
res = {"main": run(base)}
R = {"no_winsor": run(base, wins=False)}
for w in W: R[f"drop_{w}"] = run(base[base.window != w])
R["ethereum_only"] = run(base[base.supply_chain == "ethereum"])
R["audited"] = run(base, uvar="u_aud")
R["drop_recount_cases"] = run(base[base["class"] != "recount"])
res["robustness"] = R
res["descriptive"] = {"obs": int(len(base)), "tokens": int(base.gecko_id.nunique()), "non_eth_obs": int((base.supply_chain != "ethereum").sum()),
    "median_u_pct": round(float((np.exp(base.u.median()) - 1) * 100), 2), "audit_classes": AUD["class"].value_counts().to_dict()}
json.dump(res, open("data/results_stage4.json", "w"), indent=1, default=float)
rows = [{"run": k, "n": v["n"], "u": v["u"]["coef"], "p_u": v["u"]["p"], "s_issue_with_u": v["s_issue_with_u"]["coef"], "p_s_issue_with_u": v["s_issue_with_u"]["p"],
         "s_issue_alone": v["s_issue_alone"]["coef"], "p_s_issue_alone": v["s_issue_alone"]["p"], "H9": v["H9"], "H2a_wide": v["H2a_wide"]} for k, v in [("main", res["main"])] + list(R.items())]
t = pd.DataFrame(rows); t.to_csv("data/runs_summary_stage4.csv", index=False)
print(json.dumps(res["descriptive"])); print(t.to_string())

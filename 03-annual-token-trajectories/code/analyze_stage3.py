"""Stage 3: recount flag and dilution re-test (METHOD_R4_STAGE3.md) -> data/results_stage3.json, data/runs_summary_stage3.csv"""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
from common import load_cg
P = pd.read_csv("data/panel.csv")
C2 = {"savings-xdai", "usdx-money-usdx", "crypto-com-chain", "near", "arbitrum", "baby-doge-coin", "flock-2", "livepeer"}
main = P[~P.supply_artefact & ~P.gecko_id.isin(C2)].copy()

def max_jump(gid, s0, s1, thr):
    """CHANGES C7: level shift between 7-day medians of implied supply before and after a day,
    on a day when the 7-day median price moved by less than 15%."""
    d = load_cg(gid).loc[pd.Timestamp(s0) - pd.Timedelta(days=7): pd.Timestamp(s1) + pd.Timedelta(days=7)]
    S = np.log(d.mc / d.p); pr = np.log(d.p)
    before_S = S.rolling(7).median(); after_S = S[::-1].rolling(7).median()[::-1].shift(-1)
    before_p = pr.rolling(7).median(); after_p = pr[::-1].rolling(7).median()[::-1].shift(-1)
    jump = (after_S - before_S).abs(); pj = (after_p - before_p).abs()
    inside = (jump.index >= pd.Timestamp(s0)) & (jump.index <= pd.Timestamp(s1))
    return bool(((jump > np.log(1 + thr)) & (pj < np.log(1 + 0.15)) & inside).any())
for thr in (0.10, 0.15, 0.25):
    main[f"recount_{int(thr*100)}"] = [max_jump(r.gecko_id, r.start, r["end"], thr) for _, r in main.iterrows()]

sup = pd.read_csv("data/onchain_supply.csv")
# per-window availability: s_issue is NaN when TS is missing at either date
W = {"W1": ("2023-10-01", "2024-10-01"), "W2": ("2024-10-01", "2025-10-01"), "W3": ("2025-10-01", "2026-10-01")}
def s_issue(r):
    x = sup[sup.gecko_id == r.gecko_id]
    if x.empty: return np.nan
    a, b = W[r.window]
    t0, t1 = float(x[f"NET_{a}"].iloc[0]), float(x[f"NET_{b}"].iloc[0])  # CHANGES C9: net of dead/zero balances
    return np.log(t1 / t0) if t0 > 0 and t1 > 0 else np.nan
main["s_issue"] = [s_issue(r) for _, r in main.iterrows()]
main.loc[main.gecko_id.isin(["axelar", "dydx-chain"]), "s_issue"] = np.nan  # CHANGES C6
main.to_csv("data/panel_stage3.csv", index=False)

CONT = ["y", "g", "s", "s_issue", "ln_M_start", "ln_mc_start", "beta", "drawdown_start"]
def winsor(d):
    d = d.copy()
    for c in CONT:
        if d[c].notna().sum() == 0: continue
        lo = d.groupby("window")[c].transform(lambda x: x.quantile(0.025)); hi = d.groupby("window")[c].transform(lambda x: x.quantile(0.975))
        d[c] = d[c].clip(lo, hi)
    return d
def fit(f, d):
    d = d.copy(); vc = d.category.value_counts(); d["cat"] = d.category.where(d.category.isin(set(vc[vc >= 10].index)), "other")
    return smf.ols(f, d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d.group)[0]})
def cf(m, k): return {"coef": round(float(m.params[k]), 4), "p": round(float(m.pvalues[k]), 4)}
CTRL = "ln_M_start + ln_mc_start + beta + drawdown_start + C(cat) + C(window)"
base = main.dropna(subset=["g", "m", "s", "beta", "drawdown_start"])

def h2a(d, wins=True, both=False):
    e = d.dropna(subset=["s_issue"]); e = winsor(e) if wins else e
    m = fit(f"y ~ g + s_issue {'+ s ' if both else ''}+ {CTRL}", e)
    mc = fit(f"y ~ g + s + {CTRL}", e)
    o = {"n": int(m.nobs), "s_issue": cf(m, "s_issue"), "s_cg_same_sample": cf(mc, "s"), "corr_s_s_issue": round(float(e.s.corr(e.s_issue)), 3)}
    if both: o["s_with_both"] = cf(m, "s")
    o["H2a"] = o["s_issue"]["coef"] < 0 and o["s_issue"]["p"] < 0.05
    return o
def h2b(d, thr=15, wins=True):
    e = d[~d[f"recount_{thr}"]]; e = winsor(e) if wins else e
    m = fit(f"y ~ g + s + {CTRL}", e)
    o = {"n": int(m.nobs), "s": cf(m, "s"), "flag_share": round(float(d[f"recount_{thr}"].mean()), 3)}
    o["H2b"] = o["s"]["coef"] < 0 and o["s"]["p"] < 0.05
    return o
res = {"main": {"H2a": h2a(base), "H2b": h2b(base)}, "robustness": {}}
R = res["robustness"]
R["no_winsor"] = {"H2a": h2a(base, wins=False), "H2b": h2b(base, wins=False)}
for w in W: R[f"drop_{w}"] = {"H2a": h2a(base[base.window != w]), "H2b": h2b(base[base.window != w])}
R["recount_10"] = {"H2b": h2b(base, thr=10)}; R["recount_25"] = {"H2b": h2b(base, thr=25)}
R["both_measures"] = {"H2a": h2a(base, both=True)}
d = base.dropna(subset=["s_issue"])
res["descriptive"] = {"eth_tokens": int(d.gecko_id.nunique()), "eth_obs": int(len(d)),
    "median_s_issue_pct": round(float((np.exp(d.s_issue.median()) - 1) * 100), 2), "share_s_issue_zero": round(float((d.s_issue.abs() < 1e-6).mean()), 3),
    "median_s_cg_pct_same_obs": round(float((np.exp(d.s.median()) - 1) * 100), 2),
    "recount_flag_share_main": round(float(base.recount_15.mean()), 3)}
json.dump(res, open("data/results_stage3.json", "w"), indent=1, default=float)
rows = []
for k, v in [("main", res["main"])] + list(R.items()):
    a, b = v.get("H2a", {}), v.get("H2b", {})
    rows.append({"run": k, "n_H2a": a.get("n"), "s_issue": a.get("s_issue", {}).get("coef"), "p_s_issue": a.get("s_issue", {}).get("p"),
        "s_cg_same_sample": a.get("s_cg_same_sample", {}).get("coef"), "p_s_cg_same": a.get("s_cg_same_sample", {}).get("p"), "corr": a.get("corr_s_s_issue"),
        "H2a": a.get("H2a"), "n_H2b": b.get("n"), "s_no_recounts": b.get("s", {}).get("coef"), "p_s_no_recounts": b.get("s", {}).get("p"), "flag_share": b.get("flag_share"), "H2b": b.get("H2b")})
t = pd.DataFrame(rows); t.to_csv("data/runs_summary_stage3.csv", index=False)
print(json.dumps(res["descriptive"])); print(t.to_string())

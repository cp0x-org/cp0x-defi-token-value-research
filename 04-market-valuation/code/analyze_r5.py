"""Research 5 analysis per METHOD_R5.md -> data/results_r5.json, data/runs_r5.csv"""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy import stats
X = pd.read_csv("data/panel_r5.csv")
X["ptype"] = np.where(X.window.str.startswith("W"), "main", "rep")
VAL_EXCL = {"parent#aerodrome", "parent#velodrome", "parent#thena", "id#4989", "parent#tokenlon", "id#7571", "parent#lista-dao", "parent#apex-protocol"}  # CHANGES_R5 R2: explicit group ids
X["val_excl"] = X.group.isin(VAL_EXCL)
X["is_curve"] = X.name.str.contains("Curve", case=False)
X["catwin"] = X.key + "_" + X.window
X["cat"] = X.key

def winsor(d, cols):
    d = d.copy()
    for c in cols:
        lo = d.groupby("window")[c].transform(lambda x: x.quantile(0.025)); hi = d.groupby("window")[c].transform(lambda x: x.quantile(0.975))
        d[c] = d[c].clip(lo, hi)
    return d
def ols(f, d): return smf.ols(f, d).fit()
def cluster_cov(m, d, col):
    return m.get_robustcov_results(cov_type="cluster", groups=pd.factorize(d[col])[0]).cov_params()
def twoway(m, d, c1, c2):
    """Cameron-Gelbach-Miller two-way clustered covariance."""
    v1 = m.get_robustcov_results(cov_type="cluster", groups=pd.factorize(d[c1])[0]).cov_params()
    v2 = m.get_robustcov_results(cov_type="cluster", groups=pd.factorize(d[c2])[0]).cov_params()
    v12 = m.get_robustcov_results(cov_type="cluster", groups=pd.factorize(d[c1].astype(str) + "|" + d[c2].astype(str))[0]).cov_params()
    V = v1 + v2 - v12
    # guard against non-PSD
    w, U = np.linalg.eigh(V); V = (U * np.clip(w, 0, None)) @ U.T
    return V

def h1(d, wins=True, cov="twoway"):
    d = d[~d.conflict_stage1]
    d = d.dropna(subset=["y", "d_C_eth", "d_share", "ln_mc_start", "beta", "drawdown_start"]).copy()
    if wins: d = winsor(d, ["y", "d_C_eth", "d_share", "ln_mc_start", "beta", "drawdown_start"])
    f = "y ~ d_C_eth + d_share + ln_mc_start + beta + drawdown_start" + (" + C(window)" if d.window.nunique() > 1 else "")
    m = ols(f, d); names = list(m.params.index)
    V = twoway(m, d, "group", "catwin") if cov == "twoway" else cluster_cov(m, d, "group")
    i, j = names.index("d_share"), names.index("d_C_eth")
    diff = m.params["d_share"] - m.params["d_C_eth"]; se = np.sqrt(V[i, i] + V[j, j] - 2 * V[i, j])
    p_one = 1 - stats.norm.cdf(diff / se) if se > 0 else np.nan
    p_two = 2 * (1 - stats.norm.cdf(abs(diff / se))) if se > 0 else np.nan
    return {"n": int(m.nobs), "b_share": round(float(m.params["d_share"]), 4), "b_cat": round(float(m.params["d_C_eth"]), 4),
            "diff": round(float(diff), 4), "se_diff": round(float(se), 4), "p_one_sided": round(float(p_one), 5), "p_two_sided": round(float(p_two), 5)}

def model_v_sample(d):
    return d[d.rev_start_ok & ~d.val_excl & ~d.conflict_start].dropna(subset=["ln_mc_start", "ln_F0", "ln_take0", "prior_share_growth"]).copy()
FV = "ln_mc_start ~ ln_F0 + ln_take0 + prior_share_growth + C(cat) + C(window)"
def h2(d, wins=True, cov="protocol"):
    v = model_v_sample(d)
    if wins: v = winsor(v, ["ln_mc_start", "ln_F0", "ln_take0", "prior_share_growth"])
    m = ols(FV, v); names = list(m.params.index)
    V = cluster_cov(m, v, "group") if cov == "protocol" else twoway(m, v, "group", "catwin")
    k = names.index("ln_take0"); se = np.sqrt(V[k, k]); b = m.params["ln_take0"]
    return {"n": int(m.nobs), "b_take": round(float(b), 4), "se": round(float(se), 4), "p_one_sided": round(float(1 - stats.norm.cdf(b / se)), 5),
            "p_two_sided": round(float(2 * (1 - stats.norm.cdf(abs(b / se)))), 5), "a_lnF": round(float(m.params["ln_F0"]), 4), "r2": round(float(m.rsquared), 3)}, m, v

def h3(d, wins=True, cov="protocol"):
    _, m, v = h2(d, wins=wins)
    v = v.copy(); v["resid"] = v.ln_mc_start - m.fittedvalues
    v = v.dropna(subset=["y", "beta", "drawdown_start"])
    if wins: v = winsor(v, ["y", "resid", "beta", "drawdown_start"])
    m3 = ols("y ~ resid + beta + drawdown_start + C(cat) + C(window)", v); names = list(m3.params.index)
    V = cluster_cov(m3, v, "group") if cov == "protocol" else twoway(m3, v, "group", "catwin")
    k = names.index("resid"); se = np.sqrt(V[k, k]); b = m3.params["resid"]
    return {"n": int(m3.nobs), "b_resid": round(float(b), 4), "se": round(float(se), 4), "p_one_sided": round(float(stats.norm.cdf(b / se)), 5),
            "p_two_sided": round(float(2 * (1 - stats.norm.cdf(abs(b / se)))), 5)}

def holm(ps):
    order = np.argsort(ps); adj = [None] * len(ps); running = 0
    for rank, i in enumerate(order):
        running = max(running, min(1, (len(ps) - rank) * ps[i])); adj[i] = running
    return adj

res = {}
main, rep = X[X.ptype == "main"], X[X.ptype == "rep"]
res["H1"] = {"main": h1(main), "rep": h1(rep)}
res["H2"] = {"main": h2(main)[0], "rep": h2(rep)[0]}
res["H3"] = {"main": h3(main), "rep": h3(rep)}
ps = [res["H1"]["main"]["p_one_sided"], res["H2"]["main"]["p_one_sided"], res["H3"]["main"]["p_one_sided"]]
adj = holm(ps)
signs = {"H1": res["H1"]["rep"]["diff"] > 0, "H2": res["H2"]["rep"]["b_take"] > 0, "H3": res["H3"]["rep"]["b_resid"] < 0}
rep_p = {"H1": res["H1"]["rep"]["p_one_sided"], "H2": res["H2"]["rep"]["p_one_sided"], "H3": res["H3"]["rep"]["p_one_sided"]}
res["verdicts"] = {h: {"p_main_one_sided": ps[i], "p_holm": round(adj[i], 5), "main_holds": adj[i] < 0.05,
                       "replication_same_sign_p10": bool(signs[h] and rep_p[h] < 0.10), "recognised": bool(adj[i] < 0.05 and signs[h] and rep_p[h] < 0.10)}
                   for i, h in enumerate(["H1", "H2", "H3"])}
# robustness (main periods)
R = {}
R["no_winsor"] = {"H1": h1(main, wins=False), "H2": h2(main, wins=False)[0], "H3": h3(main, wins=False)}
for w in ["W1", "W2", "W3"]:
    sub = main[main.window != w]; R[f"drop_{w}"] = {"H1": h1(sub), "H2": h2(sub)[0], "H3": h3(sub)}
big = main.key.value_counts().index[0]; sub = main[main.key != big]
R["drop_largest_category"] = {"category": big, "H1": h1(sub), "H2": h2(sub)[0], "H3": h3(sub)}
R["alt_clustering"] = {"H1_protocol_only": h1(main, cov="protocol"), "H2_twoway": h2(main, cov="twoway")[0], "H3_twoway": h3(main, cov="twoway")}
sub = main[~main.is_curve]; R["no_curve"] = {"H2": h2(sub)[0], "H3": h3(sub)}
ns = main.copy(); ns["d_C_eth"] = ns.d_C_ns_eth; ns["d_share"] = ns.d_share_ns; ns["key"] = ns.key_nosplit; ns["cat"] = ns.key_nosplit; ns["catwin"] = ns.key_nosplit + "_" + ns.window
ns["prior_share_growth"] = [np.log((a / b) / (c / d)) if min(a, b, c, d) > 0 else np.nan for a, b, c, d in zip(ns.Fmain_ns0, ns.C_ns0, ns.Fmain_nsp, ns.C_nsp)]
R["no_base_asset_split"] = {"H1": h1(ns), "H2": h2(ns)[0], "H3": h3(ns)}
nk = main.groupby("key").group.transform("nunique")
sub = main[~main.key.str.endswith("|other") & (nk > 1)]
R["posthoc_drop_other_and_single_categories"] = {"H1": h1(sub), "H2": h2(sub)[0], "H3": h3(sub)}
res["robustness"] = R
# descriptive variance shares (fee and revenue variants, main periods, demeaned by window)
def shares(d, comps):
    x = d.dropna(subset=["y"] + comps)[["window", "y"] + comps].copy()
    for c in ["y"] + comps: x[c] = x[c] - x.groupby("window")[c].transform("mean")
    v = x.y.var(); out = {c: round(float(x[c].cov(x.y) / v), 3) for c in comps}; out["n"] = len(x); return out
fm = main.copy(); fm["minus_s"] = -fm.s_cg
fm = fm[~fm.conflict_stage1]
res["shares_fee_variant"] = shares(fm, ["d_C_eth", "d_share", "d_D", "d_MF", "minus_s"])
res["shares_rev_variant"] = shares(fm[fm.rev_variant], ["d_C_eth", "d_share", "d_D", "d_take", "d_MR", "minus_s"])
res["sample"] = {"conflict_start_main": int(main.conflict_start.sum()), "conflict_stage1_main": int(main.conflict_stage1.sum()), "conflict_start_rep": int(rep.conflict_start.sum()), "conflict_stage1_rep": int(rep.conflict_stage1.sum()), "main_obs": int(len(main)), "rep_obs": int(len(rep)), "valuation_excluded_obs_main": int(main.val_excl.sum()), "rev_variant_main": int(main.rev_variant.sum())}
json.dump(res, open("data/results_r5.json", "w"), indent=1, default=float)
print(json.dumps({k: res[k] for k in ["H1", "H2", "H3", "verdicts", "shares_fee_variant", "shares_rev_variant", "sample"]}, indent=1, default=float))

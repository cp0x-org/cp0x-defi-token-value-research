"""METHOD_W0 T2 and T3 (Research 5 model V and residual test) on the W0 window, Research 5 code with the window FE removed."""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy import stats
X = pd.read_csv("/home/claude/r22/data/panel_r5_w0.csv")
VAL_EXCL = {"parent#aerodrome", "parent#velodrome", "parent#thena", "id#4989", "parent#tokenlon", "id#7571", "parent#lista-dao", "parent#apex-protocol"}
X["cat"] = X.key
def winsor(d, cols):
    d = d.copy()
    for c in cols: d[c] = d[c].clip(d[c].quantile(0.025), d[c].quantile(0.975))
    return d
v = X[X.rev_start_ok & ~X.group.isin(VAL_EXCL) & ~X.conflict_start].dropna(subset=["ln_mc_start", "ln_F0", "ln_take0", "prior_share_growth"]).copy()
out = {"model_V_sample": int(len(v)), "dropped_no_prior_share": int((X.rev_start_ok & X.prior_share_growth.isna()).sum())}
if len(v) >= 15:
    vw = winsor(v, ["ln_mc_start", "ln_F0", "ln_take0", "prior_share_growth"])
    m = smf.ols("ln_mc_start ~ ln_F0 + ln_take0 + prior_share_growth + C(cat)", vw).fit(cov_type="HC1")
    b, se = m.params["ln_take0"], m.bse["ln_take0"]
    out["T2"] = {"n": int(m.nobs), "b_take": round(float(b), 4), "se": round(float(se), 4), "p_one_sided_positive": round(float(1 - stats.norm.cdf(b / se)), 4),
                 "ci95": [round(float(b - 1.96 * se), 3), round(float(b + 1.96 * se), 3)], "a_lnF": round(float(m.params["ln_F0"]), 3),
                 "consistent_no_premium": bool(1 - stats.norm.cdf(b / se) >= 0.05), "ci_excludes_1": bool(b + 1.96 * se < 1), "n_categories": int(vw.cat.nunique())}
    vw["resid"] = vw.ln_mc_start - m.fittedvalues
    t = vw.dropna(subset=["y", "beta", "drawdown_start"])
    t = winsor(t, ["y", "resid", "beta", "drawdown_start"])
    if len(t) >= 15:
        m3 = smf.ols("y ~ resid + beta + drawdown_start + C(cat)", t).fit(cov_type="HC1")
        b3, se3 = m3.params["resid"], m3.bse["resid"]
        out["T3"] = {"n": int(m3.nobs), "b_resid": round(float(b3), 4), "se": round(float(se3), 4), "p_one_sided_negative": round(float(stats.norm.cdf(b3 / se3)), 4),
                     "p_two_sided": round(float(2 * (1 - stats.norm.cdf(abs(b3 / se3)))), 4), "consistent_no_prediction": bool(stats.norm.cdf(b3 / se3) >= 0.05)}
    else: out["T3"] = "not evaluable (n < 15)"
else:
    out["T2"] = out["T3"] = "not evaluable (n < 15)"
s1 = X[~X.conflict_stage1].dropna(subset=["d_share"])
out["descriptive_share"] = {"n": int(len(s1)), "median_d_share": round(float(s1.d_share.median()), 3), "median_pct": round(float(np.expm1(s1.d_share.median()) * 100), 1),
                            "share_losing": round(float((s1.d_share < 0).mean()), 3), "median_category_growth_vs_eth": round(float(s1.d_C_eth.median()), 3)}
json.dump(out, open("/home/claude/r22/data/results_w0_r5.json", "w"), indent=1)
print(json.dumps(out, indent=1))

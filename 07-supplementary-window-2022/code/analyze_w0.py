"""METHOD_W0 T1 and descriptive statistics for the Research 4 part."""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy import stats
P = pd.read_csv("/home/claude/r22/data/panel_w0.csv")
C2 = {"savings-xdai", "usdx-money-usdx", "crypto-com-chain", "near", "arbitrum", "baby-doge-coin", "flock-2", "livepeer"}
d = P[~P.supply_artefact & ~P.gecko_id.isin(C2)].dropna(subset=["g", "m", "s", "beta", "drawdown_start"]).copy()
CONT = ["y", "g", "s", "m", "ln_M_start", "ln_mc_start", "beta", "drawdown_start"]
for c in CONT: d[c] = d[c].clip(d[c].quantile(0.025), d[c].quantile(0.975))
vc = d.category.value_counts(); d["cat"] = d.category.where(d.category.isin(set(vc[vc >= 10].index)), "other")
m = smf.ols("y ~ g + s + ln_M_start + ln_mc_start + beta + drawdown_start + C(cat)", d).fit(cov_type="HC1")
b, se = m.params["g"], m.bse["g"]; p_one = 1 - stats.norm.cdf(b / se)
raw = P[~P.gecko_id.isin(C2)]
x = raw.dropna(subset=["y", "g", "m", "s"]); x = x.assign(ms=-x.s)
v = x.y.var(); shares = {k: round(float(x[k].cov(x.y) / v), 3) for k in ["g", "m", "ms"]}
res = {"T1": {"n": int(m.nobs), "b_g": round(float(b), 4), "se": round(float(se), 4), "p_one_sided": round(float(p_one), 4),
              "ci95": [round(float(b - 1.96 * se), 3), round(float(b + 1.96 * se), 3)], "r2": round(float(m.rsquared), 3),
              "consistent": bool(b > 0 and p_one < 0.10), "categories": d.cat.value_counts().to_dict()},
       "descriptive": {"n": int(len(raw)), "share_beat_eth": round(float((raw.y > 0).mean()), 3), "median_y": round(float(raw.y.median()), 3),
                       "median_pct_vs_eth": round(float(np.expm1(raw.y.median()) * 100), 1), "variance_shares_g_m_minus_s": shares,
                       "corr_y_g": round(float(raw[["y", "g"]].corr().iloc[0, 1]), 3)}}
json.dump(res, open("/home/claude/r22/data/results_w0_r4.json", "w"), indent=1)
print(json.dumps(res, indent=1)); print(m.summary().tables[1])

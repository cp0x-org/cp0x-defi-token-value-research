"""Post-hoc diagnostics for T2/T3 on W0 (CHANGES_W0 W1): residual degrees of freedom and specifications without category FE. Not used for verdicts."""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
exec(open('/home/claude/r22/analyze_r5_w0.py').read().split('out = {')[0])
vw = winsor(v, ["ln_mc_start", "ln_F0", "ln_take0", "prior_share_growth"])
res = {}
for name, f in [("V_with_catFE", "ln_mc_start ~ ln_F0 + ln_take0 + prior_share_growth + C(cat)"), ("V_no_catFE", "ln_mc_start ~ ln_F0 + ln_take0 + prior_share_growth")]:
    m = smf.ols(f, vw).fit(cov_type="HC1"); mt = smf.ols(f, vw).fit()
    res[name] = {"n": int(m.nobs), "resid_df": int(mt.df_resid), "b_take": round(float(m.params["ln_take0"]), 3), "p_HC1_two": round(float(m.pvalues["ln_take0"]), 4), "p_classic_t_two": round(float(mt.pvalues["ln_take0"]), 4)}
    t = vw.copy(); t["resid"] = t.ln_mc_start - m.fittedvalues; t = winsor(t.dropna(subset=["y","beta","drawdown_start"]), ["y","resid","beta","drawdown_start"])
    f3 = "y ~ resid + beta + drawdown_start" + (" + C(cat)" if "with" in name else "")
    m3 = smf.ols(f3, t).fit(cov_type="HC1"); m3t = smf.ols(f3, t).fit()
    res[name.replace("V_", "H3_")] = {"n": int(m3.nobs), "resid_df": int(m3t.df_resid), "b_resid": round(float(m3.params["resid"]), 3), "p_HC1_two": round(float(m3.pvalues["resid"]), 4), "p_classic_t_two": round(float(m3t.pvalues["resid"]), 4)}
json.dump(res, open('/home/claude/r22/data/posthoc_w0.json','w'), indent=1); print(json.dumps(res, indent=1))

"""Post-hoc checks (not in any frozen method; labelled post hoc in the write-up). -> data/posthoc.json"""
import json, subprocess, sys, numpy as np, pandas as pd
out = {}
# 1. Stage 1: drop observations with < 80 days of fee data in the end window
src = open("analyze.py").read(); src = src[:src.index('res = {"main"')]
exec(src)
m = main[main.fee_days_end >= 80]
r = run(m, "posthoc end-window fee coverage >= 80 days")
out["stage1_end_fee_coverage_80"] = {"n_dropped": int(len(main) - len(m)), "dropped": main[main.fee_days_end < 80][["window", "name", "fee_days_end"]].values.tolist(),
    "verdicts": {k: bool(v) for k, v in r["verdicts"].items()}, "R1_lnM": r["R1"]["ln_M_start"], "dR2_H": r["R1h"]["delta_r2"], "H_start": r["R1h"]["H_start"]}
# 2. Stage 3 and 4 without tokens with shrinking supply
g = {}
exec(open("analyze_stage3.py").read().split('res = {"main"')[0], g)
out["stage3_drop_nxm"] = g["h2a"](g["base"][g["base"].gecko_id != "nxm"])
out["stage3_drop_nxm_bancor_olympus"] = g["h2a"](g["base"][~g["base"].gecko_id.isin(["nxm", "bancor", "olympus"])])
h = {}
sys.argv = ["x", "run"]
exec(open("analyze_stage4.py").read().split('res = {"main"')[0], h)
out["stage4_drop_nxm"] = h["run"](h["base"][h["base"].gecko_id != "nxm"])
out["stage4_drop_nxm_bancor_olympus"] = h["run"](h["base"][~h["base"].gecko_id.isin(["nxm", "bancor", "olympus"])])
json.dump(out, open("data/posthoc.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))

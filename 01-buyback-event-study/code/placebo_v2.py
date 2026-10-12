"""Placebo test for research 2, version 2 (METHOD_R2_V2.md, rule 9).
Uses the exact functions of matching_v2.py for twin selection and outcomes, so the observed value
and the random-date distribution come from one implementation.
Cell: demand class, flow start, four events; horizon 30 days; both layers:
  basket = token minus median of control basket (COMP, CRV, ENS) over the same window,
  twins  = token minus median of up to three nearest twins with distance <= 0.25.
Random dates per token: at least 100 observations of history, at least 45 days from own events,
window inside the data. 1000 sets. Output: data/placebo_v2_results.json"""
import json, pathlib, sys
import numpy as np
import pandas as pd
import matching_v2 as M
from analyze import load_ratios, CFG

HERE = pathlib.Path(__file__).parent
H = 30
N_ITER = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
FLOW = [("coingecko:aave", "2025-04-09"), ("coingecko:dydx-chain", "2025-03-24"),
        ("coingecko:ether-fi", "2025-05-08"), ("coingecko:gmx", "2024-10-30")]
rng = np.random.default_rng(42)

def main():
    ratios = load_ratios()
    _, own = M.event_dates_by_token()
    hist = {pr.get("history_token") for pr in CFG["programs"] if pr.get("history_token")}
    universe = [c for c in ratios.columns if c != CFG["benchmark"] and c not in hist and c not in M.STAGE3_ADDED]
    basket = [c for c in CFG["control_tokens"] if c in ratios.columns]

    def outcomes(tok, t0):
        a = M.fwd(ratios[tok], t0, H)
        if a is None:
            return None, None
        b = [M.fwd(ratios[c], t0, H) for c in basket if c != tok]
        b = [x for x in b if x is not None]
        vb = a - float(np.median(b)) if b else None
        pm, cands = M.select_twins(ratios, universe, own, tok, t0)
        if pm is None:
            return vb, None
        good = [(d, c) for d, c in cands if d <= M.THRESH][:M.K]
        tw = [M.fwd(ratios[c], t0, H) for _, c in good]
        tw = [x for x in tw if x is not None]
        vt = a - float(np.median(tw)) if tw else None
        return vb, vt

    obs = []
    for tok, ds in FLOW:
        vb, vt = outcomes(tok, pd.Timestamp(ds))
        obs.append({"token": tok.split(":")[1], "date": ds, "vs_basket": vb, "vs_twins": vt})
    ob = [o["vs_basket"] for o in obs if o["vs_basket"] is not None]
    ot = [o["vs_twins"] for o in obs if o["vs_twins"] is not None]
    observed = {"basket": float(np.median(ob)) if len(ob) == 4 else None,
                "twins": float(np.median(ot)) if len(ot) == 4 else None}

    meds = {"basket": [], "twins": []}
    tries = 0
    while min(len(meds["basket"]), len(meds["twins"])) < N_ITER and tries < N_ITER * 40:
        tries += 1
        vbs, vts = [], []
        for tok, _ in FLOW:
            s = ratios[tok].dropna()
            if len(s) < 101: break
            lo, hi = s.index[100], s.index[-1] - pd.Timedelta(days=H + 3)
            for _ in range(40):
                d = lo + pd.Timedelta(days=int(rng.integers(0, (hi - lo).days + 1)))
                if any(abs((d - e).days) < 45 for e in own.get(tok, [])): continue
                vb, vt = outcomes(tok, d)
                if vb is not None and vt is not None:
                    vbs.append(vb); vts.append(vt); break
        if len(vbs) == 4:
            if len(meds["basket"]) < N_ITER: meds["basket"].append(float(np.median(vbs)))
            if len(meds["twins"]) < N_ITER: meds["twins"].append(float(np.median(vts)))
    res = {"method": "METHOD_R2_V2.md rule 9", "horizon_days": H, "observed_events": obs, "observed_median": observed}
    for k in ("basket", "twins"):
        m = np.array(meds[k])
        res[k] = {"iterations": int(len(m)), "q05": float(np.quantile(m, .05)), "q50": float(np.quantile(m, .5)),
                  "q95": float(np.quantile(m, .95)),
                  "p_one_sided": float((m >= observed[k]).mean()) if observed[k] is not None else None}
    (HERE / "data" / "placebo_v2_results.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps({"observed": observed, "basket": res["basket"], "twins": res["twins"]}, indent=1, ensure_ascii=False))

if __name__ == "__main__":
    main()

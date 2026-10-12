"""Diagnostic only (METHOD_R6V): a manually cleaned transfer proxy, to see whether the gap is fixable by hand.
Rules decided after seeing P1 results, therefore they cannot change the verdict:
- Aave: outflows from the Collector and Aave Grants DAO to EOAs/multisigs, ignoring the same-transaction-inflow rule
  (stream withdrawals and payload executions often also move tokens into the Collector); Ecosystem Reserve and
  Incentives Controller excluded as Safety Module / liquidity-mining rewards.
- Sky: outflows from the Pause Proxy to EOAs/multisigs ignoring the same-transaction-inflow rule (payments are minted
  via Vat.suck into the Pause Proxy and forwarded in the same transaction).
- Lido, Uniswap: P1 unchanged (no rule-based fix exists for committee pre-funding or for lumpy DAO-to-foundation grants).
"""
import pandas as pd, numpy as np, sys
sys.argv = [sys.argv[0]]
from build_P import classify
bench = pd.read_csv("data/reported_spending.csv"); rows = []
for p in ["lido", "aave", "sky", "uniswap"]:
    O = pd.read_csv(f"data/P_outflows_{p}.csv.gz")
    if p in ("aave", "sky"):
        src = {"aave": {"0x464c71f6c2f760dda6093dcb91c24c39e5d6e18c", "0x89c51828427f70d77875c6747759fb17ba10ceb0"},
               "sky": {"0xbe8e3e3618f7474f8cb1d074a26affef007e98fb"}}[p]
        need = sorted(set(O[O.frm.isin(src) & (O.usd > 0)].to)); C = classify(need)
        O["rc2"] = O.to.map(C)
        O["m"] = O.frm.isin(src) & O.rc2.isin(["eoa", "multisig"])
    else:
        O["m"] = O.p1
    for _, r in bench[bench.protocol == p].iterrows():
        w = O[(O.day >= r.period_start) & (O.day <= r.period_end)]
        rows.append(dict(protocol=p, period_start=r.period_start, reported=r.amount_usd, P_manual=float(w.usd.fillna(0)[w.m].sum()),
                         P_manual_noown=float(w.usd.fillna(0)[w.m & ~w.own].sum())))
M = pd.DataFrame(rows); M["r"] = M.P_manual / M.reported; M["r_noown"] = M.P_manual_noown / M.reported
M.to_csv("data/proxy_P_manual.csv", index=False)
l = np.abs(np.log(M.r)); print(M.round(2).to_string()); print("median |ln r|", round(float(l.median()), 3), "protocol median r", M.groupby("protocol").r.median().round(2).to_dict())

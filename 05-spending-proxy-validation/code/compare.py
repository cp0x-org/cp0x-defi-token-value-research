"""Apply the frozen criteria of METHOD_R6V to families P (P1) and B (B1); diagnostics for other variants."""
import json, numpy as np, pandas as pd
from scipy.stats import spearmanr
bench = pd.read_csv("data/reported_spending.csv")
P = pd.read_csv("data/proxy_P.csv"); B = pd.read_csv("data/proxy_B.csv")
M = bench.merge(P, on=["protocol", "period_start", "period_end"], how="left").merge(B, on=["protocol", "period_start", "period_end"], how="left")
M.to_csv("data/comparison.csv", index=False)

def evaluate(col):
    d = M[M[col].notna()].copy()  # a zero proxy counts as an infinite error, not as missing
    d["r"] = d[col] / d.amount_usd; d["abs_ln_r"] = np.abs(np.log(d.r.astype(float)))
    n_units, n_prot = len(d), d.protocol.nunique()
    coverage = n_units >= 10 and n_prot >= 4
    c1_val = float(d.abs_ln_r.median()); c1 = c1_val <= np.log(1.4)
    pm = d.groupby("protocol").r.median(); inside = int(((pm >= 0.5) & (pm <= 2)).sum())
    need = int(np.ceil(0.8 * n_prot)); c2 = inside >= need
    pairs = []
    for p, g in d.sort_values("period_start").groupby("protocol"):
        for (_, a), (_, b) in zip(g.iloc[:-1].iterrows(), g.iloc[1:].iterrows()):
            pairs.append(np.sign(b[col] - a[col]) == np.sign(b.amount_usd - a.amount_usd))
    c3 = (np.mean(pairs) >= 2 / 3) if len(pairs) >= 3 else None
    rho = spearmanr(d[col], d.amount_usd).correlation if n_units >= 3 else np.nan
    passed = bool(coverage and c1 and c2 and (c3 is None or c3))
    return dict(variant=col, units=n_units, protocols=n_prot, coverage_ok=coverage, median_abs_ln_r=round(c1_val, 3), median_ratio_error_x=round(float(np.exp(c1_val)), 2),
                C1=bool(c1), protocol_median_r={k: round(float(v), 2) for k, v in pm.items()}, C2=bool(c2), C2_inside=f"{inside}/{n_prot} (need {need})",
                C3=None if c3 is None else bool(c3), C3_pairs=f"{int(np.sum(pairs))}/{len(pairs)}", spearman=round(float(rho), 2), PASS=passed)

out = {"primary": [evaluate("P1"), evaluate("B1")], "diagnostic": [evaluate(c) for c in ["P0", "P1c", "B0", "B1_noown"]]}
json.dump(out, open("data/verdict.json", "w"), indent=1, default=str)
pd.set_option("display.width", 250)
cols = ["protocol", "period_start", "period_end", "amount_usd", "P0", "P1", "P1c", "B1", "B0"]
X = M[cols].copy()
for c in cols[3:]: X[c] = (X[c] / 1e6).round(1)
print(X.to_string()); print(json.dumps(out, indent=1, default=str))

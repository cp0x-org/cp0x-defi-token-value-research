"""Part B of METHOD_R4_REPLICATION.md: start-of-window variables for window F (2026-10-01 to 2027-10-01), saved before the outcome exists."""
import numpy as np, pandas as pd
from common import load_cg, at, load_fees, sum90
C2 = {"savings-xdai", "usdx-money-usdx", "crypto-com-chain", "near", "arbitrum", "baby-doge-coin", "flock-2", "livepeer"}
c = pd.read_csv("data/candidates.csv", dtype=str, keep_default_na=False); c = c[(c.excluded == "") & ~c.gecko_id.isin(C2)]
eth = load_cg("ethereum"); s0 = "2026-10-01"; d0 = pd.Timestamp(s0); rows = []
for _, r in c.iterrows():
    cg = load_cg(r.gecko_id)
    if cg is None: continue
    mc0, p0 = at(cg, s0, "mc"), at(cg, s0, "p")
    if not mc0 or not p0 or mc0 < 50e6: continue
    fees = load_fees(r.slug, "dailyFees")
    if fees is None: continue
    f0, n0 = sum90(fees, s0)
    if n0 < 80 or f0 <= 0: continue
    hr = load_fees(r.slug, "dailyHoldersRevenue"); h0 = np.nan
    if hr is not None:
        a0, k0 = sum90(hr, s0); h0 = min(max(a0 / f0, 0), 1) if k0 > 0 else np.nan
    hist = cg.loc[d0 - pd.Timedelta(days=365): d0, "p"]
    j = pd.concat([np.log(hist).diff(), np.log(eth.loc[d0 - pd.Timedelta(days=365): d0, "p"]).diff()], axis=1, keys=["t", "e"], sort=True).dropna()
    rows.append(dict(window="F", start=s0, end="2027-10-01", group=r.group, slug=r.slug, name=r["name"], gecko_id=r.gecko_id, category=r.category,
        mc_start=mc0, p_start=p0, eth_start=at(eth, s0, "p"), fees90_start=f0, fee_days_start=n0, H_start=h0, S_start=mc0 / p0,
        ln_M_start=np.log(mc0 / (f0 * 365 / 90)), ln_mc_start=np.log(mc0), beta=float(np.polyfit(j.e, j.t, 1)[0]) if len(j) >= 250 else np.nan,
        drawdown_start=float(np.log(p0 / hist.max()))))
D = pd.DataFrame(rows).sort_values("mc_start", ascending=False); D.to_csv("data/forward_start_2026-10-01.csv", index=False)
print(len(D), "protocols;", int(D.H_start.notna().sum()), "with holder share;", int((D.H_start > 0).sum()), "with H > 0")

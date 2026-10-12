"""Build the protocol x window panel exactly as in METHOD_R4.md."""
import numpy as np, pandas as pd
from common import load_cg, at, last_date, load_fees, sum90, WINDOWS
c = pd.read_csv("data/candidates.csv", dtype=str, keep_default_na=False)
c = c[c.excluded == ""]
eth = load_cg("ethereum")
rows = []
for wi, (s0, s1) in enumerate(WINDOWS, 1):
    e0, e1 = at(eth, s0, "p"), at(eth, s1, "p")
    for _, r in c.iterrows():
        cg = load_cg(r.gecko_id)
        if cg is None: continue
        mc0, p0 = at(cg, s0, "mc"), at(cg, s0, "p")
        if not mc0 or not p0 or mc0 < 50e6: continue
        fees = load_fees(r.slug, "dailyFees")
        if fees is None: continue
        f0, n0 = sum90(fees, s0)
        if n0 < 80 or f0 <= 0: continue
        # end point, with delisting rule
        end = pd.Timestamp(s1); delisted = False
        ld = last_date(cg)
        if ld is None or ld < end:
            delisted = True; end = ld
        p1, mc1 = at(cg, end, "p"), at(cg, end, "mc")
        e_end = at(eth, end, "p")
        f1, n1 = sum90(fees, s1)
        hr = load_fees(r.slug, "dailyHoldersRevenue")
        h0 = h1 = np.nan
        if hr is not None:
            a0, k0 = sum90(hr, s0); a1, k1 = sum90(hr, s1)
            h0 = min(max(a0 / f0, 0), 1) if k0 > 0 else np.nan  # C11
            h1 = min(max(a1 / f1, 0), 1) if (f1 > 0 and k1 > 0) else np.nan
        # beta and drawdown over the 365 days before start
        d0 = pd.Timestamp(s0)
        hist = cg.loc[d0 - pd.Timedelta(days=365): d0, "p"]
        lr = np.log(hist).diff()
        le = np.log(eth.loc[d0 - pd.Timedelta(days=365): d0, "p"]).diff()
        j = pd.concat([lr, le], axis=1, keys=["t", "e"]).dropna()
        beta = float(np.polyfit(j.e, j.t, 1)[0]) if len(j) >= 250 else np.nan
        dd = float(np.log(p0 / hist.max())) if hist.notna().any() else np.nan
        y = np.log(p1 / p0) - np.log(e_end / e0) if p1 else np.nan
        S0, S1 = mc0 / p0, (mc1 / p1 if (mc1 and p1) else np.nan)
        ok = f1 > 0 and not np.isnan(S1)
        g = np.log(f1 / f0) - np.log(e_end / e0) if f1 > 0 else np.nan
        m = np.log((mc1 / f1) / (mc0 / f0)) if ok else np.nan
        s = np.log(S1 / S0) if ok else np.nan
        rows.append(dict(window=f"W{wi}", start=s0, end=str(end.date()), group=r.group, slug=r.slug, name=r["name"],
            gecko_id=r.gecko_id, category=r.category, delisted=delisted, mc_start=mc0, mc_end=mc1, p_start=p0, p_end=p1,
            fees90_start=f0, fees90_end=f1, fee_days_start=n0, fee_days_end=n1, H_start=h0, H_end=h1,
            y=y, g=g, m=m, s=s, ln_M_start=np.log(mc0 / (f0 * 365 / 90)), ln_mc_start=np.log(mc0),
            beta=beta, drawdown_start=dd, eth_ret=np.log(e_end / e0)))
df = pd.DataFrame(rows)
df["identity_err"] = df.y - (df.g + df.m - df.s)
df["supply_artefact"] = df.s.abs() > np.log(5)
df.to_csv("data/panel.csv", index=False)
print(df.groupby("window").size().to_dict(), "obs; decomposable:", df.g.notna().sum(),
      "| max identity error:", float(df.identity_err.abs().max()), "| artefacts:", int(df.supply_artefact.sum()),
      "| delisted:", int(df.delisted.sum()))

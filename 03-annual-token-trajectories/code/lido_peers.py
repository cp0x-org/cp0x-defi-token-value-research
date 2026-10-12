"""Descriptive comparison of Lido with staking peers (not pre-registered). -> data/lido_peers.csv, data/eth_lst_share.csv"""
import json, os, numpy as np, pandas as pd
from common import load_cg, at, sum90, WINDOWS
def series(path):
    try: d = json.load(open(path))
    except Exception: return None
    ch = d.get("totalDataChart") or []
    if not ch: return None
    return pd.Series({pd.Timestamp(t, unit="s").normalize(): float(v) for t, v in ch}).groupby(level=0).sum().sort_index()
def summed(paths):
    ss = [s for s in (series(p) for p in paths) if s is not None]
    return pd.concat(ss, axis=1).sum(axis=1, min_count=1) if ss else None
CHILD = {"ether-fi": ["ether.fi-stake", "ether.fi-liquid", "etherfi-borrowing-market", "etherfi-cash-liquid"],
         "marinade-finance": ["marinade-liquid-staking", "marinade-native", "marinade-select"],
         "origin-defi": ["origin-dollar", "origin-ether", "origin-arm", "origin-sonic"]}
def rev(slug):
    if slug in CHILD: return summed([f"raw/peers/child__{c}__dailyRevenue.json" for c in CHILD[slug]])
    return series(f"raw/peers/{slug}__dailyRevenue.json")
P = pd.read_csv("data/panel.csv")
S3 = pd.read_csv("data/panel_stage3.csv")[["window", "group", "s_issue"]]
P = P.merge(S3, on=["window", "group"], how="left")
PEERS = ["lido-dao", "rocket-pool", "ether-fi", "frax-share", "ssv-network", "eigenlayer", "ankr", "jito-governance-token", "marinade", "sanctum-2", "benqi", "lista", "stride", "origin-protocol", "solayer"]
X = P[P.gecko_id.isin(PEERS)].copy()
eth = load_cg("ethereum")
recs = []
for _, r in X.iterrows():
    R = rev(r.slug)
    r0 = sum90(R, r.start)[0] if R is not None else np.nan
    r1 = sum90(R, r["end"])[0] if R is not None else np.nan
    er = np.log(at(eth, r["end"], "p") / at(eth, r.start, "p"))
    recs.append(dict(window=r.window, name=r["name"], gecko_id=r.gecko_id, y=r.y, g=r.g, m=r.m, s=r.s, s_issue=r.s_issue,
        rev90_start=r0, rev90_end=r1,
        rev_growth_eth=(np.log(r1 / r0) - er) if (r0 > 0 and r1 > 0) else np.nan,
        take_start=r0 / r.fees90_start if r.fees90_start > 0 else np.nan, take_end=r1 / r.fees90_end if r.fees90_end > 0 else np.nan,
        mc_to_rev_start=r.mc_start / (r0 * 365 / 90) if r0 > 0 else np.nan, mc_to_rev_end=r.mc_end / (r1 * 365 / 90) if r1 > 0 else np.nan,
        H_start=r.H_start, mc_start=r.mc_start))
D = pd.DataFrame(recs).sort_values(["window", "y"], ascending=[True, False])
D.to_csv("data/lido_peers.csv", index=False)
# ETH liquid staking: Lido share of fees among ETH LST products
ETH_LST = {"lido": "raw/peers/lido__dailyFees.json", "rocket-pool": "raw/peers/rocket-pool__dailyFees.json",
    "ether.fi-stake": "raw/peers/child__ether.fi-stake__dailyFees.json", "frax-ether": "raw/peers/child__frax-ether__dailyFees.json",
    "origin-ether": "raw/peers/child__origin-ether__dailyFees.json", "kelp": "raw/peers/child__kelp__dailyFees.json"}
for s in ["binance-staked-eth", "meth-protocol", "coinbase-wrapped-staked-eth", "renzo", "liquid-collective", "stakewise", "puffer-finance", "swell", "stader"]:
    ETH_LST[s] = f"raw/peers/{s}__dailyFees.json"
rows = []
for d in ["2023-10-01", "2024-10-01", "2025-10-01", "2026-10-01"]:
    v = {k: (sum90(series(p), d)[0] if series(p) is not None else 0.0) for k, p in ETH_LST.items()}
    tot = sum(v.values())
    rows.append({"date": d, "lido_share": v["lido"] / tot, **{f"share_{k}": v[k] / tot for k in v}})
Sh = pd.DataFrame(rows); Sh.to_csv("data/eth_lst_share.csv", index=False)
pd.set_option("display.width", 250)
pc = lambda x: (np.exp(x) - 1) * 100
show = D.copy()
for c in ["y", "g", "m", "s", "s_issue", "rev_growth_eth"]: show[c] = pc(show[c]).round(0)
for c in ["take_start", "take_end", "H_start"]: show[c] = (show[c] * 100).round(1)
show["mc_to_rev_start"] = show.mc_to_rev_start.round(1); show["mc_to_rev_end"] = show.mc_to_rev_end.round(1)
print(show[["window", "name", "y", "g", "m", "s", "s_issue", "rev_growth_eth", "take_start", "take_end", "mc_to_rev_start", "mc_to_rev_end", "H_start"]].to_string(index=False))
print(Sh.set_index("date").round(3)[["lido_share", "share_ether.fi-stake", "share_rocket-pool", "share_binance-staked-eth", "share_coinbase-wrapped-staked-eth", "share_meth-protocol"]].to_string())

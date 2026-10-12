"""Stage 2 variables per METHOD_R4_STAGE2.md, merged onto data/panel.csv -> data/panel_stage2.csv"""
import os, json, glob, collections, numpy as np, pandas as pd
P = pd.read_csv("data/panel.csv")

def breakdown(slug):
    """dict date -> {(chain, product): fees}"""
    files = [f"raw/bd/{slug}.json"]
    try: ok = bool(json.load(open(files[0])).get("totalDataChartBreakdown"))
    except Exception: ok = False
    if not ok: files = glob.glob(f"raw/bd/child__{slug}__*.json")
    rows = collections.defaultdict(float)
    for f in files:
        try: d = json.load(open(f))
        except Exception: continue
        for ts, ch in d.get("totalDataChartBreakdown") or []:
            day = pd.Timestamp(ts, unit="s").normalize()
            for chain, prods in ch.items():
                if isinstance(prods, dict):
                    for prod, v in prods.items(): rows[(day, chain, prod)] += float(v or 0)
                else: rows[(day, chain, "_")] += float(prods or 0)
    if not rows: return None
    s = pd.Series(rows); s.index.names = ["date", "chain", "product"]
    return s

def active(bd, date, level):
    d = pd.Timestamp(date)
    w = bd[(bd.index.get_level_values("date") > d - pd.Timedelta(days=90)) & (bd.index.get_level_values("date") <= d)]
    t = w.groupby(level=level).sum()
    return set(t[t > 0].index)

def treasury(slug):
    f = f"raw/treasury/{slug}.json"
    try: d = json.load(open(f))
    except Exception: return None
    ct = d.get("chainTvls") or {}
    ser = []
    for k, v in ct.items():
        if k == "OwnTokens" or "-" in k: continue
        s = pd.Series({pd.Timestamp(x["date"], unit="s").normalize(): x["totalLiquidityUSD"] for x in v.get("tvl", [])})
        if len(s): ser.append(s.groupby(level=0).last())
    if not ser: return None
    return pd.concat(ser, axis=1).sort_index().ffill(limit=7).sum(axis=1, min_count=1)

def tval(t, date):
    d = pd.Timestamp(date); w = t.loc[d - pd.Timedelta(days=7): d].dropna()
    return float(w.iloc[-1]) if len(w) else np.nan

hacks = json.load(open("raw/hacks.json"))
hk = collections.defaultdict(list)
for h in hacks:
    for key in (h.get("parentProtocolId"), f"id#{h.get('defillamaId')}" if h.get("defillamaId") else None):
        if key: hk[key].append(pd.Timestamp(h["date"], unit="s"))

cache_bd, cache_tr, out = {}, {}, []
for _, r in P.iterrows():
    if r.slug not in cache_bd: cache_bd[r.slug] = breakdown(r.slug)
    if r.slug not in cache_tr: cache_tr[r.slug] = treasury(r.slug)
    bd, tr = cache_bd[r.slug], cache_tr[r.slug]
    rec = {"window": r.window, "group": r.group}
    if bd is not None:
        p0, p1 = active(bd, r.start, "product"), active(bd, r["end"], "product")
        c0, c1 = active(bd, r.start, "chain"), active(bd, r["end"], "chain")
        rec.update(new_products=len(p1 - p0), lost_products=len(p0 - p1), new_chains=len(c1 - c0), lost_chains=len(c0 - c1),
                   n_products_start=len(p0), n_chains_start=len(c0))
    if tr is not None:
        t0, t1 = tval(tr, r.start), tval(tr, r["end"])
        rec.update(T_start=t0, T_end=t1, treasury_change=(t1 - t0) / r.mc_start if (t0 >= 1e6 and not np.isnan(t1)) else np.nan)
    s0, s1 = pd.Timestamp(r.start), pd.Timestamp(r["end"])
    rec["hack"] = int(any(s0 < d <= s1 for d in hk.get(r.group, [])))
    out.append(rec)
S = pd.DataFrame(out)
M = P.merge(S, on=["window", "group"], how="left")
M.to_csv("data/panel_stage2.csv", index=False)
print("rows", len(M), "| breakdown coverage", int(M.new_products.notna().sum()), "| treasury_change coverage", int(M.treasury_change.notna().sum()), "| hacks", int(M.hack.sum()))

"""Rebuilds the frozen stage-3 universe from the raw DefiLlama dump.
Criterion: categories Dexs and Derivatives, all-time holders revenue > 0, versions grouped by parentProtocol.
Source dump: data/holders_rev_raw.json (api.llama.fi/overview/fees?dataType=dailyHoldersRevenue).
Run: python3 build_universe.py  -> prints whether the result matches data/stage3_universe_frozen.csv"""
import json, pathlib
import pandas as pd
HERE = pathlib.Path(__file__).parent
ps = json.load(open(HERE / "data" / "holders_rev_raw.json"))
rows = []
for p in ps:
    if p.get("category") not in ("Dexs", "Derivatives"): continue
    tot = p.get("totalAllTime") or 0
    if not tot or tot <= 0: continue
    parent = p.get("parentProtocol") or p.get("defillamaId") or p.get("name")
    rows.append({"name": p.get("name"), "parent": str(parent), "category": p.get("category"), "holders_rev_all_time_usd": round(float(tot))})
df = pd.DataFrame(rows)
u = (df.sort_values("holders_rev_all_time_usd", ascending=False)
       .groupby("parent").agg(name=("name", "first"), category=("category", "first"),
            holders_rev_all_time_usd=("holders_rev_all_time_usd", "sum"), versions=("name", lambda x: "; ".join(x)))
       .reset_index().sort_values("holders_rev_all_time_usd", ascending=False))
frozen = pd.read_csv(HERE / "data" / "stage3_universe_frozen.csv").drop(columns=["frozen_at_utc"])
same = u.reset_index(drop=True).astype(str).equals(frozen.reset_index(drop=True).astype(str))
print(f"протоколов: {len(u)} | совпадает с замороженным перечнем: {same}")

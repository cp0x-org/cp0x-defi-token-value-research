"""Research 6: mechanical join of outcomes to the frozen decision tables (METHOD_R6, CHANGES D4)."""
import json, os, sys, numpy as np, pandas as pd
os.chdir("/home/claude/r4rep"); sys.path.insert(0, "/home/claude/r4rep")
from common import load_cg, at, load_fees, sum90
R5 = "/home/claude/r5"; R6 = "/home/claude/r6"
SLUG = {"lido": "lido", "aave": "aave", "sky": "maker", "uniswap": "uniswap"}
GROUP = {"lido": "id#182", "aave": "parent#aave", "sky": "parent#maker", "uniswap": "parent#uniswap"}
GECKO = {"lido": "lido-dao", "aave": "aave", "sky": "sky", "uniswap": "uniswap"}
PRIMARY = {"usage_market": "category_fee_share", "monetization": "take_rate", "capital": "tvl", "token_price": "token_vs_eth"}

# category fee share (R5 breakdown, same main-category rule)
meta = pd.read_csv(f"{R5}/data/category_map.csv")
bd = json.load(open(f"{R5}/raw/overview_fees_breakdown.json"))
rec = {}
for ts, row in bd["totalDataChartBreakdown"]:
    day = pd.Timestamp(ts, unit="s").normalize()
    for name, v in row.items(): rec[(day, name)] = float(v or 0)
FE = pd.Series(rec).unstack(fill_value=np.nan).sort_index()
def s90(cols, date):
    d1 = pd.Timestamp(date); w = FE.loc[d1 - pd.Timedelta(days=89): d1, [c for c in cols if c in FE.columns]]
    return float(w.sum().sum()) if w.shape[1] else np.nan
def share(p, date):
    g = GROUP[p]; mk = meta[meta.group == g].main_key.iloc[0]
    own = meta[(meta.group == g) & (meta.key == mk)].name.tolist(); cat = meta[meta.key == mk].name.tolist()
    a, b = s90(own, date), s90(cat, date)
    return a / b if b and b > 0 else np.nan

def rev_series(slug):
    d = json.load(open(f"{R5}/raw/rev/{slug}.json")); ch = d.get("totalDataChart") or []
    return pd.Series({pd.Timestamp(t, unit="s").normalize(): float(v) for t, v in ch}).groupby(level=0).sum().sort_index()
def tvl_series(p):
    fn = f"{R6}/raw/tvl_{SLUG[p] if p != 'sky' else 'sky'}.json"
    if not os.path.exists(fn): return None
    d = json.load(open(fn)); return pd.Series({pd.Timestamp(x["date"], unit="s").normalize(): x["totalLiquidityUSD"] for x in d["tvl"]}).sort_index()

ETH = load_cg("ethereum")
F = {p: load_fees(SLUG[p], "dailyFees") for p in SLUG}; R = {p: rev_series(SLUG[p]) for p in SLUG}; T = {p: tvl_series(p) for p in SLUG}
cutoff = min([F[p].index.max() for p in SLUG] + [ETH.p.dropna().index.max()] + [load_cg(GECKO[p]).p.dropna().index.max() for p in SLUG])

def value(p, metric, date):
    if metric == "fees": return sum90(F[p], date)[0]
    if metric == "revenue": return sum90(R[p], date)[0]
    if metric == "take_rate":
        f, r = sum90(F[p], date)[0], sum90(R[p], date)[0]; return r / f if f > 0 else np.nan
    if metric == "category_fee_share": return share(p, date)
    if metric == "tvl":
        s = T[p]; return float(s.loc[:pd.Timestamp(date)].iloc[-1]) if s is not None and len(s.loc[:pd.Timestamp(date)]) else np.nan
    if metric == "token_vs_eth":
        cg = load_cg(GECKO[p]); a, e = at(cg, date, "p"), at(ETH, date, "p")
        return a / e if a and e else np.nan
    return np.nan

import re
def parse_date(x):
    """The first date expression in the text, YYYY-MM-DD or YYYY-MM (then the first day of that month) (CHANGES D5)."""
    m = re.search(r"\d{4}-\d{2}(-\d{2})?", str(x))
    if not m: return pd.NaT
    return pd.Timestamp(m.group(0) if m.group(1) else m.group(0) + "-01")

G = pd.read_csv(f"{R6}/decisions/goal_map.csv")
D = pd.concat([pd.read_csv(f"{R6}/decisions/{p}_decisions.csv").assign(protocol=p) for p in SLUG])
X = D.merge(G, on=["protocol", "id"], how="left")
rows = []
for _, r in X.iterrows():
    out = dict(t0=str(parse_date(r.executed_start).date()) if pd.notna(parse_date(r.executed_start)) else "", protocol=r.protocol, id=r.id, title=r.title, cls=r["class"], line_item=r.line_item, executed_start=r.executed_start,
               goal_category=r.goal_category, primary_metric=PRIMARY.get(r.goal_category, ""))
    evaluable = r.goal_category in PRIMARY
    t0 = parse_date(r.executed_start)
    mets = [m for m in str(r.metrics).split(";") if m and m != "nan"] if evaluable else []
    # token vs ETH is reported descriptively for every decision (METHOD_R6; CHANGES D6)
    mets = list(dict.fromkeys(([PRIMARY[r.goal_category]] if evaluable else []) + mets + ["token_vs_eth"]))
    for m in mets:
        if m == "category_tvl_share": continue  # not computable (CHANGES D4)
        v0 = value(r.protocol, m, t0) if pd.notna(t0) else np.nan
        for w in (6, 12, 24):
            t1 = t0 + pd.DateOffset(months=w) if pd.notna(t0) else pd.NaT
            if pd.isna(t1) or t1 > cutoff: out[f"{m}_{w}m"] = "not yet observable"; continue
            v1 = value(r.protocol, m, t1)
            out[f"{m}_{w}m"] = round(float(np.log(v1 / v0)), 4) if (v0 and v1 and v0 > 0 and v1 > 0) else np.nan
    if evaluable:
        pm = out.get(f"{PRIMARY[r.goal_category]}_12m")
        out["primary_12m_sign"] = ("+" if pm > 0 else "-") if isinstance(pm, float) and not np.isnan(pm) else ("not yet observable" if pm == "not yet observable" else "")
    rows.append(out)
O = pd.DataFrame(rows)
O.to_csv(f"{R6}/data_outcomes.csv", index=False)
json.dump({"cutoff": str(cutoff.date())}, open(f"{R6}/outcomes_cutoff.json", "w"))
print("cutoff", cutoff.date())
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 50)
E = O[O.goal_category.isin(PRIMARY)]
print(E[["protocol", "id", "executed_start", "goal_category", "primary_metric"] + [c for c in E.columns if c.endswith("_12m") or c.endswith("_6m")] + ["primary_12m_sign"]].to_string())

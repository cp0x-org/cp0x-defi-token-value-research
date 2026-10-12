"""Feasibility and survivorship check for adding 2022 windows to Research 4/5.
Universe A: Research 4 kept candidates (protocols currently in the DefiLlama fee dashboard, with a gecko id).
Universe B: DefiLlama protocols marked dead (deadFrom) with a gecko id, not already in A.
For window starts 2022-04-01 and 2022-10-01: market cap (7-day median, CoinGecko), fee coverage (>= 80 of 90 days,
positive), and the one-year return against ETH, to see whether tokens that would be missing differ from those kept."""
import os, sys, json, time, subprocess, numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/r4rep"); os.chdir("/home/claude/r4rep")
from common import load_cg, at, load_fees, sum90
R = "/home/claude/r22"
STARTS = ["2022-04-01", "2022-10-01"]
def year_later(s): return str((pd.Timestamp(s) + pd.DateOffset(years=1)).date())

def get_cg(g):
    out = f"raw/cg/{g}.csv"
    if os.path.exists(out): return
    for attempt in range(6):
        r = subprocess.run(["curl", "-s", "-m", "30", "-o", out, "-w", "%{http_code}", f"https://www.coingecko.com/price_charts/export/{g}/usd.csv"], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200": break
        if code == "404": open(out, "w").close(); break
        time.sleep(20 * (attempt + 1))
    time.sleep(2)

def get_fees(slug):
    out = f"raw/fees/{slug}__dailyFees.json"
    if os.path.exists(out) and os.path.getsize(out) > 0: return
    for attempt in range(4):
        p = subprocess.run(["curl", "-s", "-m", "90", "-o", out, "-w", "%{http_code}", f"https://api.llama.fi/summary/fees/{slug}?dataType=dailyFees&excludeTotalDataChartBreakdown=true"], capture_output=True, text=True)
        if p.stdout.strip() in ("200", "404", "400"): break
        time.sleep(10 * (attempt + 1))
    time.sleep(0.5)

c = pd.read_csv("data/candidates.csv", dtype=str, keep_default_na=False)
A = c[c.excluded == ""][["slug", "name", "category", "gecko_id"]].assign(universe="A_current")
P = json.load(open(f"{R}/raw/protocols.json"))
EXCL = {"Chain", "CEX", "Gaming", "Luck Games", "Physical TCG", "Gamified Mining", "SoFi", "AI Agents", "DePIN", "Domains", "Wallets",
        "Developer Tools", "Services", "Payments", "Privacy", "Block Builders", "DAO Service Provider", "Telegram Bot", "Token Locker"}
B = pd.DataFrame([dict(slug=p.get("slug"), name=p.get("name"), category=p.get("category"), gecko_id=p.get("gecko_id"), deadFrom=p.get("deadFrom"))
                  for p in P if p.get("deadFrom") and p.get("gecko_id")])
B = B[~B.gecko_id.isin(A.gecko_id) & ~B.category.isin(EXCL)].drop_duplicates("gecko_id").assign(universe="B_dead")
U = pd.concat([A, B], ignore_index=True)
for g in sorted(set(U.gecko_id) | {"ethereum"}): get_cg(g)
ETH = load_cg("ethereum")
rows = []
for _, r in U.iterrows():
    cg = load_cg(r.gecko_id)
    for s in STARTS:
        mc = at(cg, s, "mc") if cg is not None else None
        if not mc or mc < 50e6: continue
        get_fees(r.slug)
        f = load_fees(r.slug, "dailyFees")
        tot, ndays = sum90(f, s) if f is not None else (0.0, 0)
        e = year_later(s)
        p0, p1 = at(cg, s, "p"), at(cg, e, "p")
        e0, e1 = at(ETH, s, "p"), at(ETH, e, "p")
        y = float(np.log(p1 / p0) - np.log(e1 / e0)) if (p0 and p1) else np.nan
        rows.append(dict(start=s, universe=r.universe, slug=r.slug, name=r["name"], category=r.category, gecko_id=r.gecko_id,
                         deadFrom=r.get("deadFrom"), mc_start=mc, fee_days=ndays, fees90=tot, fee_ok=bool(ndays >= 80 and tot > 0), y_vs_eth=y,
                         price_end_missing=p1 is None))
X = pd.DataFrame(rows); X.to_csv(f"{R}/check_2022.csv", index=False)
for s in STARTS:
    d = X[X.start == s]
    d = d.assign(group=np.where(d.fee_ok, "enters (fee data ok)", np.where(d.universe == "B_dead", "dead, no fee data", "alive, no fee data")))
    print("\n== window start", s, "| tokens >= $50M:", len(d))
    print(d.groupby("group").agg(n=("slug", "size"), median_y_vs_eth=("y_vs_eth", "median"), share_beat_eth=("y_vs_eth", lambda x: float((x > 0).mean())),
                                 price_end_missing=("price_end_missing", "sum"), mc_median_musd=("mc_start", lambda x: float(np.median(x) / 1e6))).round(3).to_string())

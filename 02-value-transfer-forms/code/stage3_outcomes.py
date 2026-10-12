"""Stage 3 outcome recomputation with strictly calendar windows.
Replaces the earlier ad-hoc code that shifted by rows on gappy series.
Rules (as stated in the report):
- all prices relative to ETH;
- value at date d = last observation on or before d, stale by at most MAX_STALE days;
- token, twin and basket use the same calendar start and end dates;
- twin distance = |drawdown from 365-day max diff| + 0.5 * |90-day pre-run diff|, threshold 0.25;
- twin requires 365 days of history; candidates with own day-precision events in [d-45, d+90] excluded;
- basket = median of COMP, CRV, ENS (those with valid data at the dates), fixed in advance;
- twins never come from tokens studied in this stage or LDO, nor from tokens with documented disqualifying events near the window;
- vs_twin and vs_basket are arithmetic differences of simple returns, not compounded ratios.
Run: python3 stage3_outcomes.py  -> data/stage3_outcomes_recomputed.csv"""
import json, pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
MAX_STALE = 7
THRESH = 0.25
ETH = "coingecko:ethereum"
BASKET = ["coingecko:compound-governance-token", "coingecko:curve-dao-token", "coingecko:ethereum-name-service"]
# (a) tokens of protocols studied in this stage (registry) plus LDO, the object of application: never twins
SUBJECTS = {"coingecko:" + t for t in ["sushi", "gains-network", "gmx", "jito-governance-token", "ether-fi", "aave",
    "curve-dao-token", "uniswap", "pendle", "rocket-pool", "looksrare", "frax-share", "joe", "balancer", "dydx-chain",
    "yearn-finance", "vertex-protocol", "lido-dao", "havven"]}
# (b) documented disqualifying events (delisting, migration, shutdown) with the window they poison
DISQUALIFY = {"coingecko:vertex-protocol": [("2025-07-01", "2025-08-31", "закрытие Vertex при переезде на Ink")]}

EVENTS = [  # (label, token, date, transition)
    ("Balancer veBAL, первый поток", "coingecko:balancer", "2022-04-21", "введение прямого дохода с нуля"),
    ("Jito TipRouter, первый поток", "coingecko:jito-governance-token", "2025-01-30", "введение прямого дохода с нуля"),
    ("Sushi xSUSHI, восстановление", "coingecko:sushi", "2024-01-23", "введение выкупа с распределением с нуля"),
    ("ether.fi, старт выкупа с раздачей", "coingecko:ether-fi", "2025-05-08", "введение выкупа с распределением с нуля"),
    ("Trader Joe sJOE, деплой", "coingecko:joe", "2022-02-24", "замена выкупа прямыми выплатами"),
    ("Gains, переход на BB&D", "coingecko:gains-network", "2024-07-12", "замена прямых выплат выкупом с распределением"),
    ("GMX, первая раздача купленного", "coingecko:gmx", "2024-10-30", "замена прямых выплат выкупом с распределением"),
    ("Yearn YIP-56, прямые выплаты в казну", "coingecko:yearn-finance", "2021-01-19", "лестница: прямой доход в выкуп в казначейство"),
    ("Yearn YIP-65, решение", "coingecko:yearn-finance", "2021-12-28", "лестница: решение о раздаче выкупленного"),
    ("Yearn YIP-65, старт раздачи", "coingecko:yearn-finance", "2023-10-19", "лестница: выкуп в казначейство в выкуп с распределением"),
]

def load():
    p = pd.read_csv(HERE / "data" / "prices.csv", dtype={"date": str, "coin": str})
    p["date"] = pd.to_datetime(p["date"])
    piv = p.pivot_table(index="date", columns="coin", values="price", aggfunc="last").sort_index()
    eth = piv[ETH]
    rel = piv.div(eth, axis=0).drop(columns=[ETH])
    return rel

def asof(series, d):
    s = series.dropna()
    s = s[s.index <= d]
    if s.empty or (d - s.index[-1]).days > MAX_STALE:
        return np.nan
    return s.iloc[-1]

def metrics(series, d):
    s = series.dropna()
    if s.empty: return None
    hist_days = (d - s.index[0]).days
    v0 = asof(series, d)
    vpre = asof(series, d - pd.Timedelta(days=90))
    win = s[(s.index > d - pd.Timedelta(days=365)) & (s.index <= d)]
    dd = v0 / win.max() - 1 if (not np.isnan(v0) and len(win)) else np.nan
    pre = v0 / vpre - 1 if not np.isnan(vpre) else np.nan
    return {"v0": v0, "dd": dd, "pre90": pre, "hist_days": hist_days}

def fwd(series, d, h):
    v0 = asof(series, d); v1 = asof(series, d + pd.Timedelta(days=h))
    if np.isnan(v0) or np.isnan(v1): return np.nan
    return v1 / v0 - 1

def main():
    rel = load()
    ev = pd.read_csv(HERE / "events.csv", dtype=str, keep_default_na=False)
    ev = ev[ev.date_precision == "day"]
    ev_dates = {}
    for _, r in ev.iterrows():
        ev_dates.setdefault(r.token_coingecko, []).append(pd.Timestamp(r.date))
    cfg = json.load(open(HERE / "config.json"))
    hist_tokens = {p.get("history_token") for p in cfg.get("programs", []) if p.get("history_token")}
    out = []
    for label, tok, ds, trans in EVENTS:
        d = pd.Timestamp(ds)
        m = metrics(rel[tok], d)
        row = {"event": label, "transition": trans, "token": tok, "date": ds,
               "hist_days": m["hist_days"], "pre90": m["pre90"], "dd365": m["dd"]}
        for h in (30, 90):
            row[f"tok_{h}"] = fwd(rel[tok], d, h)
            b = [fwd(rel[c], d, h) for c in BASKET if c in rel.columns]
            b = [x for x in b if not np.isnan(x)]
            row[f"basket_n_{h}"] = len(b)
            row[f"vs_basket_{h}_pp"] = (row[f"tok_{h}"] - np.median(b)) * 100 if b and not np.isnan(row[f"tok_{h}"]) else np.nan
        best = (np.inf, None)
        if m["hist_days"] >= 365 and not np.isnan(m["dd"]) and not np.isnan(m["pre90"]):
            for c in rel.columns:
                if c == tok or c in hist_tokens or c in SUBJECTS: continue
                if any(pd.Timestamp(a) <= d + pd.Timedelta(days=90) and pd.Timestamp(b) >= d - pd.Timedelta(days=90) for a, b, _ in DISQUALIFY.get(c, [])): continue
                if any(-45 < (e - d).days <= 90 for e in ev_dates.get(c, [])): continue  # own event anywhere in [d-45, d+90]
                cm = metrics(rel[c], d)
                if cm is None or cm["hist_days"] < 365 or np.isnan(cm["dd"]) or np.isnan(cm["pre90"]): continue
                if np.isnan(fwd(rel[c], d, 90)): continue
                dist = abs(cm["dd"] - m["dd"]) + 0.5 * abs(cm["pre90"] - m["pre90"])
                if dist < best[0]: best = (dist, c)
        row["twin"] = best[1].split(":")[1] if best[1] else ""
        row["twin_dist"] = best[0] if best[1] else np.nan
        ok = best[1] is not None and best[0] <= THRESH
        row["twin_ok"] = ok
        for h in (30, 90):
            if ok:
                tw = fwd(rel[best[1]], d, h)
                row[f"twin_{h}"] = tw
                row[f"vs_twin_{h}_pp"] = (row[f"tok_{h}"] - tw) * 100 if not np.isnan(tw) else np.nan
            else:
                row[f"twin_{h}"] = np.nan; row[f"vs_twin_{h}_pp"] = np.nan
        row["twin_own_90"] = row.get("twin_90", np.nan)
        vt, vb = row["vs_twin_90_pp"], row["vs_basket_90_pp"]
        row["robust_sign_90"] = (bool(np.sign(vt) == np.sign(vb)) if not (np.isnan(vt) or np.isnan(vb)) else "")
        out.append(row)
    df = pd.DataFrame(out)
    df.to_csv(HERE / "data" / "stage3_outcomes_recomputed.csv", index=False)
    pd.set_option("display.width", 250)
    show = df[["event", "date", "twin", "twin_dist", "tok_90", "twin_own_90", "vs_twin_30_pp", "vs_twin_90_pp", "vs_basket_90_pp", "robust_sign_90"]].copy()
    for c in ["tok_90", "twin_own_90"]: show[c] = (show[c] * 100).round(1)
    for c in ["twin_dist"]: show[c] = show[c].round(3)
    for c in ["vs_twin_30_pp", "vs_twin_90_pp", "vs_basket_90_pp"]: show[c] = show[c].round(1)
    print(show.to_string(index=False))

if __name__ == "__main__":
    main()

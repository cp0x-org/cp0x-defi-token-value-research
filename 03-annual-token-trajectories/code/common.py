import os, json, functools
import numpy as np, pandas as pd
WINDOWS = [("2023-10-01", "2024-10-01"), ("2024-10-01", "2025-10-01"), ("2025-10-01", "2026-10-01")]

@functools.lru_cache(maxsize=None)
def load_cg(gid):
    p = f"raw/cg/{gid}.csv"
    if not os.path.exists(p) or os.path.getsize(p) == 0: return None
    d = pd.read_csv(p)
    if d.empty: return None
    d["date"] = pd.to_datetime(d.event_date.str[:10])
    d = d.rename(columns={"close_price_usd": "p", "market_cap_usd": "mc"})
    d["p"] = pd.to_numeric(d.p, errors="coerce"); d["mc"] = pd.to_numeric(d.mc, errors="coerce")
    d.loc[d.p <= 0, "p"] = np.nan; d.loc[d.mc <= 0, "mc"] = np.nan
    return d.set_index("date")[["p", "mc"]].sort_index()

def at(df, date, col):
    """Median of the 7 daily values ending at date (METHOD: Measurement)."""
    d = pd.Timestamp(date)
    s = df.loc[d - pd.Timedelta(days=6): d, col].dropna()
    return float(s.median()) if len(s) else None

def last_date(df, col="p"):
    s = df[col].dropna()
    return s.index.max() if len(s) else None

@functools.lru_cache(maxsize=None)
def load_fees(slug, kind):
    p = f"raw/fees/{slug}__{kind}.json"
    if not os.path.exists(p) or os.path.getsize(p) == 0: return None
    try: d = json.load(open(p))
    except Exception: return None
    ch = d.get("totalDataChart") or []
    if not ch: return None
    s = pd.Series({pd.Timestamp(t, unit="s").normalize(): float(v) for t, v in ch}).sort_index()
    return s

def sum90(s, date):
    """Sum over 90 days ending at date and number of days with data."""
    d = pd.Timestamp(date)
    w = s.loc[d - pd.Timedelta(days=89): d]
    return float(w.sum()), int(w.notna().sum())

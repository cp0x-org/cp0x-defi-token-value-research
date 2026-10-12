"""Correction of 2026-10-08. class_cut.py measured the pre-event run-up (pre90) over the last 90 price observations
(pre.iloc[-90]) instead of 90 calendar days. Price series have gaps, so 90 rows can span more than 90 days. This script
recomputes pre90 on calendar days with the same rule matching_v2.py already uses for the twin match (last observation
on or before t0 - 90 days, at most 7 days earlier), and recomputes the run-up correlations and stage medians.
Inputs: data/class_cut_events_v2.csv, events.csv, the token/ETH ratio series from analyze.load_ratios (needs prices.csv,
not redistributed). Outputs: data/class_cut_events_v2_pre90_calendar.csv, data/class_cut_v2_pre90_calendar.csv."""
import pathlib, pandas as pd, numpy as np
from analyze import load_ratios
HERE = pathlib.Path(__file__).parent
DATA = HERE.parent / "data" if (HERE.parent / "data").exists() else HERE / "data"
R = load_ratios()
d = pd.read_csv(DATA / "class_cut_events_v2.csv")
ev = pd.read_csv(DATA / "events.csv", parse_dates=["date"])
tok = {(r.protocol, str(r.date.date())): r.token_coingecko for r in ev.itertuples()}
def pre90_calendar(t, day):
    s = R[t].dropna(); t0 = pd.Timestamp(day); now = s.loc[:t0]
    past = s[s.index <= t0 - pd.Timedelta(days=90)]
    if not len(now) or not len(past) or (t0 - pd.Timedelta(days=90) - past.index[-1]).days > 7: return np.nan
    return now.iloc[-1] / past.iloc[-1] - 1
d["pre90_calendar"] = [pre90_calendar(tok[(p, x)], x) for p, x in zip(d.protocol, d.date)]
d = d.rename(columns={"pre90": "pre90_rows_superseded"})
d.to_csv(DATA / "class_cut_events_v2_pre90_calendar.csv", index=False)
d.groupby(["class", "stage"]).pre90_calendar.median().round(3).rename("med_pre90_calendar").to_csv(DATA / "class_cut_v2_pre90_calendar.csv")
for name, sub in [("all events", d), ("decisions and activations", d[d.stage.isin(["decision", "activation"])])]:
    for col in ["pre90_rows_superseded", "pre90_calendar"]:
        b = sub.dropna(subset=[col, "vs_basket_30d"]); m = sub.dropna(subset=[col, "vs_match_30d"])
        print(f"{name:26s} {col:22s} basket {b[col].corr(b.vs_basket_30d):+.3f} (n={len(b)})  twins {m[col].corr(m.vs_match_30d):+.3f} (n={len(m)})")

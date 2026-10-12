"""RESEARCH 2, VERSION 2 (METHOD_R2_V2.md). Based on the calendar version of matching_control.py: identical except pre-event metrics use calendar windows
(drawdown vs max over the preceding 365 calendar days, pre-run vs value 90 calendar days earlier, stale <= 7 days)
and the candidate pool excludes tokens added to the price base in stage 3. Output: data/matched_controls_calendar.csv

Original docstring: Matched-control layer: for each day-precision event, pick the token from the price
universe with the most similar pre-event profile (drawdown from trailing 365d high and
90d pre-return, both on token/ETH ratios), excluding the event's own token and any
candidate that has its own program event within +/-45 days. Outcome = event token's
forward relative return minus the matched twin's, at 30/90/180d.
Output: data/matched_controls.csv. Limitations: thin candidate pool (~20 tokens),
twins may carry their own confounders; treat as a robustness check, not ground truth."""
import json, os, pathlib
import numpy as np
import pandas as pd
from analyze import load_ratios, CFG

HERE = pathlib.Path(__file__).parent
WINDOWS = [30, 90, 180]

def event_dates_by_token():
    ev = pd.read_csv(HERE / "events.csv", parse_dates=["date"])
    ev = ev[ev["date_precision"] == "day"]
    d = {}
    for _, r in ev.iterrows():
        d.setdefault(r["token_coingecko"], []).append(r["date"])
    return ev, d

STAGE3_ADDED = {"coingecko:joe", "coingecko:balancer", "coingecko:yearn-finance", "coingecko:vertex-protocol"}

def pre_metrics(series, t0):
    s = series.loc[:t0].dropna()
    if len(s) < 100:
        return None
    if (t0 - s.index[-1]).days > 7:
        return None
    win = s[s.index > t0 - pd.Timedelta(days=365)]
    dd = s.iloc[-1] / win.max() - 1
    past = s[s.index <= t0 - pd.Timedelta(days=90)]
    r90 = s.iloc[-1] / past.iloc[-1] - 1 if len(past) and (t0 - pd.Timedelta(days=90) - past.index[-1]).days <= 7 else None
    return dd, r90

def fwd(series, t0, w):
    base = series.loc[:t0].dropna()
    if base.empty:
        return None
    b = base.iloc[-1]
    sub = series.loc[:t0 + pd.Timedelta(days=w)].dropna()
    if len(sub) and (sub.index[-1] - (t0 + pd.Timedelta(days=w))).days > -3:
        return sub.iloc[-1] / b - 1
    return None

K = 3
THRESH = 0.25

def select_twins(ratios, universe, own_events, tok, t0):
    pm = pre_metrics(ratios[tok], t0)
    if pm is None or pm[1] is None:
        return None, []
    cands = []
    for c in universe:
        if c == tok:
            continue
        if any(-45 < (d - t0).days <= 90 for d in own_events.get(c, [])):
            continue
        cm = pre_metrics(ratios[c], t0)
        if cm is None or cm[1] is None:
            continue
        cands.append((abs(cm[0] - pm[0]) + 0.5 * abs(cm[1] - pm[1]), c))
    cands.sort()
    return pm, cands

def main():
    ratios = load_ratios()
    ev, own_events = event_dates_by_token()
    hist = {pr.get("history_token") for pr in CFG["programs"] if pr.get("history_token")}
    universe = [c for c in ratios.columns if c != CFG["benchmark"] and c not in hist]
    universe = [c for c in universe if c not in STAGE3_ADDED]
    out_name = "matched_controls_v2.csv"
    if os.environ.get("EXCLUDE_SUBJECTS") == "1":  # sensitivity only, not the pre-registered rule
        subj = set(ev["token_coingecko"].dropna()) | {"coingecko:lido-dao"}
        universe = [c for c in universe if c not in subj]
        out_name = "matched_controls_v2_nosubjects.csv"
    rows = []
    for _, e in ev.iterrows():
        tok, t0 = e["token_coingecko"], e["date"]
        if tok not in ratios.columns:
            continue
        pm, cands = select_twins(ratios, universe, own_events, tok, t0)
        if pm is None or not cands:
            continue
        good = [(d, c) for d, c in cands if d <= THRESH][:K]
        used = good if good else [cands[0]]
        row = {"program": e["protocol"], "event": e["event_type"], "date": str(t0.date()),
               "token_dd": round(pm[0], 3), "token_pre90": round(pm[1], 3),
               "match": "|".join(c.split(":")[1] for _, c in used),
               "match_dist": round(max(d for d, _ in used), 3), "n_twins": len(good)}
        for w in WINDOWS:
            a = fwd(ratios[tok], t0, w)
            tw = [fwd(ratios[c], t0, w) for _, c in good]
            tw = [x for x in tw if x is not None]
            row[f"diff_vs_match_{w}d"] = round(a - float(np.median(tw)), 4) if (a is not None and tw) else None
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(HERE / "data" / out_name, index=False)
    print(f"событий: {len(df)}, с тремя двойниками: {(df.n_twins == 3).sum()}, с одним-двумя: {df.n_twins.between(1, 2).sum()}, без пригодного: {(df.n_twins == 0).sum()}")

if __name__ == "__main__":
    main()

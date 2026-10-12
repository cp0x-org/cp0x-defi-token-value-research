"""Lido LDO accumulation mandate case, recomputed with the verified stage-3 calendar engine.
Replaces the earlier ad-hoc computation that shifted series by rows.
Same rules as stage3_outcomes.py: calendar windows, value as-of with <= 7 days staleness, twin distance
|drawdown diff| + 0.5*|90-day pre-run diff| <= 0.25, twin needs 365 days of history, no twins from studied
tokens or tokens with documented disqualifying events, no candidates with own events in [d-45, d+90].
Both controls reported. Output: data/lido_mandate_events_calendar.csv"""
import json, pathlib
import numpy as np
import pandas as pd
import stage3_outcomes as E

HERE = pathlib.Path(__file__).parent
TOK = "coingecko:lido-dao"
EVENTS = [
    ("Параметры транша 1", "2026-04-14", "окно накрывает взлом моста Kelp 18.04.2026"),
    ("Первый филл мандата", "2026-04-21", "окно накрывает взлом моста Kelp 18.04.2026"),
    ("Параметры транша 2", "2026-06-12", ""),
    ("Параметры транша 3", "2026-07-10", ""),
    ("Параметры фазы 2, потолок повышен", "2026-08-25", "активация NEST 10.08.2026 в 90-дневной предыстории"),
    ("Параметры транша 4", "2026-09-25", ""),
]

def main():
    rel = E.load()
    ev = pd.read_csv(HERE / "events.csv", dtype=str, keep_default_na=False)
    ev = ev[ev.date_precision == "day"]
    own = {}
    for _, r in ev.iterrows():
        own.setdefault(r.token_coingecko, []).append(pd.Timestamp(r.date))
    cfg = json.load(open(HERE / "config.json"))
    hist = {p.get("history_token") for p in cfg.get("programs", []) if p.get("history_token")}
    last = rel.index.max()
    out = []
    for label, ds, note in EVENTS:
        d = pd.Timestamp(ds)
        m = E.metrics(rel[TOK], d)
        row = {"event": label, "date": ds, "note": note, "pre90": m["pre90"], "dd365": m["dd"],
               "window_closed_30": bool(d + pd.Timedelta(days=30) <= last)}
        row["tok_30"] = E.fwd(rel[TOK], d, 30)
        b = [E.fwd(rel[c], d, 30) for c in E.BASKET if c in rel.columns]
        b = [x for x in b if not np.isnan(x)]
        row["vs_basket_30_pp"] = (row["tok_30"] - np.median(b)) * 100 if b and not np.isnan(row["tok_30"]) else np.nan
        best = (np.inf, None)
        for c in rel.columns:
            if c == TOK or c in hist or c in E.SUBJECTS: continue
            if any(-45 < (e - d).days <= 90 for e in own.get(c, [])): continue
            if any(pd.Timestamp(a) <= d + pd.Timedelta(days=90) and pd.Timestamp(z) >= d - pd.Timedelta(days=90) for a, z, _ in E.DISQUALIFY.get(c, [])): continue
            cm = E.metrics(rel[c], d)
            if cm is None or cm["hist_days"] < 365 or np.isnan(cm["dd"]) or np.isnan(cm["pre90"]): continue
            if np.isnan(E.fwd(rel[c], d, 30)): continue
            dist = abs(cm["dd"] - m["dd"]) + 0.5 * abs(cm["pre90"] - m["pre90"])
            if dist < best[0]: best = (dist, c)
        ok = best[1] is not None and best[0] <= E.THRESH
        row["twin"] = best[1].split(":")[1] if best[1] else ""
        row["twin_dist"] = best[0] if best[1] else np.nan
        row["twin_ok"] = ok
        tw = E.fwd(rel[best[1]], d, 30) if ok else np.nan
        row["twin_30"] = tw
        row["vs_twin_30_pp"] = (row["tok_30"] - tw) * 100 if ok and not np.isnan(tw) else np.nan
        vt, vb = row["vs_twin_30_pp"], row["vs_basket_30_pp"]
        row["robust_sign_30"] = bool(np.sign(vt) == np.sign(vb)) if not (np.isnan(vt) or np.isnan(vb)) else ""
        out.append(row)
    df = pd.DataFrame(out)
    df.to_csv(HERE / "data" / "lido_mandate_events_calendar.csv", index=False)
    show = df[["event", "date", "window_closed_30", "pre90", "tok_30", "twin", "twin_dist", "vs_twin_30_pp", "vs_basket_30_pp", "robust_sign_30"]].copy()
    for c in ["pre90", "tok_30"]: show[c] = (show[c] * 100).round(1)
    show["twin_dist"] = show["twin_dist"].round(3)
    for c in ["vs_twin_30_pp", "vs_basket_30_pp"]: show[c] = show[c].round(1)
    pd.set_option("display.width", 250)
    print(show.to_string(index=False))
    print("последняя дата цен:", last.date())

if __name__ == "__main__":
    main()

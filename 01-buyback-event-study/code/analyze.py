"""Event study on token/ETH relative performance around each program event, plus flow overlay
where on-chain data exists. Everything is measured AGAINST ETH so market beta cancels out.
Outputs: data/event_summary.csv, charts/<program>_<event>.png, charts/flows_<program>.png"""
import json, pathlib, datetime as dt
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).parent
CFG = json.loads((HERE / "config.json").read_text())
WINDOWS = CFG.get("event_windows_days", [7, 30, 90, 180])
PRE_DAYS = 30

def load_ratios():
    px = pd.read_csv(HERE / "data" / "prices.csv", parse_dates=["date"])
    wide = px.pivot_table(index="date", columns="coin", values="price").sort_index()
    bench = CFG["benchmark"]
    for prog in CFG["programs"]:
        h = prog.get("history_token")
        if h and h in wide.columns and prog["token"] in wide.columns:
            hist = wide[h] / prog.get("splice_ratio", 1)
            cur = wide[prog["token"]]
            cutover = cur.dropna().index.min()
            wide[prog["token"]] = pd.concat([hist.loc[:cutover - pd.Timedelta(days=1)], cur.loc[cutover:]])
    ratios = wide.div(wide[bench], axis=0)
    return ratios

def event_study(ratios):
    rows, charts = [], []
    (HERE / "charts").mkdir(exist_ok=True)
    for prog in CFG["programs"]:
        coin = prog["token"]
        if coin not in ratios.columns:
            continue
        series = ratios[coin].dropna()
        for ev in prog.get("events", []):
            d0 = pd.Timestamp(ev["date"])
            if d0 not in series.index:
                near = series.index[series.index.get_indexer([d0], method="nearest")]
                if len(near) == 0:
                    continue
                d0 = near[0]
            base = series.loc[d0]
            ctrl = [c for c in CFG.get("control_tokens", []) if c in ratios.columns and c != coin]
            others = ctrl or [p2["token"] for p2 in CFG["programs"] if p2["token"] != coin and p2["token"] in ratios.columns]
            basket = ratios[others].div(ratios[others].loc[:d0].ffill().loc[d0]).median(axis=1).dropna()
            row = {"program": prog["id"], "event": ev["label"], "date": str(d0.date()), "verified": ev.get("verified", False)}
            for w in WINDOWS:
                target = d0 + pd.Timedelta(days=w)
                sub = series.loc[:target]
                if len(sub) and (sub.index[-1] - target).days > -3:
                    tok_n = sub.iloc[-1] / base
                    row[f"ret_vs_eth_{w}d"] = round(tok_n - 1, 4)
                    bsub = basket.loc[:target]
                    row[f"ret_vs_basket_{w}d"] = round(tok_n / bsub.iloc[-1] - 1, 4) if len(bsub) else None
                else:
                    row[f"ret_vs_eth_{w}d"] = None
                    row[f"ret_vs_basket_{w}d"] = None
            rows.append(row)
            lo, hi = d0 - pd.Timedelta(days=PRE_DAYS), d0 + pd.Timedelta(days=max(WINDOWS))
            win = series.loc[lo:hi] / base
            if len(win) > 5:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(win.index, win.values)
                ax.axvline(d0, linestyle="--")
                ax.axhline(1.0, linewidth=0.5)
                ax.set_title(f"{prog['id']} vs ETH, indexed=1 at {d0.date()}\n{ev['label']}")
                fig.autofmt_xdate(); fig.tight_layout()
                p = HERE / "charts" / f"{prog['id']}_{d0.date()}.png"
                fig.savefig(p, dpi=110); plt.close(fig)
                charts.append(p)
    summary = pd.DataFrame(rows)
    summary.to_csv(HERE / "data" / "event_summary.csv", index=False)
    return summary, charts

def flow_overlay(ratios):
    out = []
    for prog in CFG["programs"]:
        f = HERE / "data" / f"flows_{prog['id']}.csv"
        if not f.exists():
            continue
        flows = pd.read_csv(f, parse_dates=["date"])
        if flows.empty:
            continue
        daily = flows.groupby("date")["amount"].sum()
        series = ratios[prog["token"]].dropna()
        fig, ax = plt.subplots(figsize=(9, 4.5))
        lo = daily.index.min() - pd.Timedelta(days=20)
        win = series.loc[lo:]
        ax.plot(win.index, win.values, label="token/ETH")
        ax2 = ax.twinx()
        ax2.bar(daily.index, daily.values, width=2.5, alpha=0.4, label="buyback inflow")
        ax.set_title(f"{prog['id']}: token/ETH vs on-chain buyback settlements")
        fig.autofmt_xdate(); fig.tight_layout()
        p = HERE / "charts" / f"flows_{prog['id']}.png"
        fig.savefig(p, dpi=110); plt.close(fig)
        out.append(p)
    return out

if __name__ == "__main__":
    ratios = load_ratios()
    summary, charts = event_study(ratios)
    flow_charts = flow_overlay(ratios)
    pd.set_option("display.width", 160)
    print(summary.to_string(index=False))
    print("charts:", [c.name for c in charts + flow_charts])

def intensity_metrics():
    """For each day-precision event in events.csv with an annualized program size:
    intensity = daily program rate / median daily token volume (30d before event);
    revenue_coverage = program size / annualized protocol revenue (trailing 90d x4)."""
    ev = pd.read_csv(HERE / "events.csv", parse_dates=["date"])
    ev = ev[(ev["date_precision"] == "day") & ev["size_usd_annualized"].notna()]
    vols = pd.read_csv(HERE / "data" / "volumes.csv", parse_dates=["date"])
    rev = pd.read_csv(HERE / "data" / "revenue.csv", parse_dates=["date"])
    slug_by_token = {p["token"]: p.get("llama_slug") for p in CFG["programs"]}
    rows = []
    for _, e in ev.iterrows():
        tok = e["token_coingecko"]
        d0 = e["date"]
        v = vols[(vols["token"] == tok) & (vols["date"] >= d0 - pd.Timedelta(days=30)) & (vols["date"] < d0)]
        med_vol = v["volume_usd"].median() if len(v) else None
        slug = slug_by_token.get(tok)
        r = rev[(rev["protocol"] == slug) & (rev["date"] >= d0 - pd.Timedelta(days=90)) & (rev["date"] < d0)]
        ann_rev = r["revenue_usd"].sum() * 4 if len(r) > 30 else None
        daily_rate = e["size_usd_annualized"] / 365.0
        rows.append({
            "protocol": e["protocol"], "event": e["event_type"], "date": str(d0.date()),
            "program_daily_usd": round(daily_rate),
            "median_daily_volume_usd": round(med_vol) if med_vol else None,
            "intensity_pct_of_volume": round(100 * daily_rate / med_vol, 2) if med_vol else None,
            "annualized_revenue_usd": round(ann_rev) if ann_rev else None,
            "program_pct_of_revenue": round(100 * e["size_usd_annualized"] / ann_rev, 1) if ann_rev else None,
        })
    df = pd.DataFrame(rows)
    df.to_csv(HERE / "data" / "intensity.csv", index=False)
    return df

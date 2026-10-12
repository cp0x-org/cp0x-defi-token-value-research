"""Fundamentals layer: daily protocol revenue via DefiLlama free API and daily token
trading volume via OKX (quote USD, Coinbase fallback). No keys.
Outputs: data/revenue.csv (date, protocol, revenue_usd) and
data/volumes.csv (date, token, volume_usd, source).
Volume is single-venue and thus a LOWER BOUND of global volume; use it consistently
(same source across time) and prefer within-token comparisons."""
import json, time, pathlib, datetime as dt
import requests
import pandas as pd

HERE = pathlib.Path(__file__).parent
CFG = json.loads((HERE / "config.json").read_text())

def revenue_series(slug: str) -> pd.DataFrame:
    url = f"https://api.llama.fi/summary/fees/{slug}"
    r = requests.get(url, params={"dataType": "dailyRevenue"}, timeout=40)
    r.raise_for_status()
    chart = r.json().get("totalDataChart", [])
    return pd.DataFrame(
        [{"date": dt.datetime.utcfromtimestamp(ts).date(), "protocol": slug, "revenue_usd": v} for ts, v in chart]
    )

def okx_volumes(inst: str, start: dt.date) -> pd.DataFrame:
    rows, after = [], ""
    url = "https://www.okx.com/api/v5/market/history-candles"
    while True:
        params = {"instId": inst, "bar": "1D", "limit": "100"}
        if after:
            params["after"] = after
        r = requests.get(url, params=params, timeout=40).json()
        data = r.get("data", [])
        if not data:
            break
        for c in data:
            ts = int(c[0]) // 1000
            d = dt.datetime.utcfromtimestamp(ts).date()
            rows.append({"date": d, "volume_usd": float(c[7]) if float(c[7]) else float(c[6]), "close": float(c[4])})
        after = data[-1][0]
        if dt.datetime.utcfromtimestamp(int(data[-1][0]) // 1000).date() < start:
            break
        time.sleep(0.25)
    df = pd.DataFrame(rows)
    return df[df["date"] >= start] if not df.empty else df

def coinbase_volumes(product: str, start: dt.date) -> pd.DataFrame:
    rows = []
    end = dt.date.today()
    cur = start
    while cur < end:
        hi = min(cur + dt.timedelta(days=290), end)
        r = requests.get(
            f"https://api.exchange.coinbase.com/products/{product}/candles",
            params={"granularity": 86400, "start": f"{cur}T00:00:00Z", "end": f"{hi}T00:00:00Z"},
            headers={"User-Agent": "research"}, timeout=40,
        )
        if r.status_code == 200:
            for ts, low, high, open_, close, vol in r.json():
                rows.append({"date": dt.datetime.utcfromtimestamp(ts).date(), "volume_usd": vol * close, "close": close})
        cur = hi
        time.sleep(0.35)
    return pd.DataFrame(rows)

def main():
    start = dt.datetime.strptime(CFG["price_start"], "%Y-%m-%d").date()
    (HERE / "data").mkdir(exist_ok=True)
    rev, vol = [], []
    for prog in CFG["programs"]:
        slug = prog.get("llama_slug")
        if slug:
            try:
                df = revenue_series(slug)
                print(f"revenue {slug}: {len(df)} days")
                rev.append(df)
            except Exception as e:
                print(f"revenue {slug} FAILED: {str(e)[:80]}")
        sym = prog.get("okx_inst")
        if sym:
            df = okx_volumes(sym, start)
            src = "okx"
            hist_sym = prog.get("okx_inst_history")
            if hist_sym is not None and not df.empty:
                hist = okx_volumes(hist_sym, start)
                if hist.empty and prog.get("coinbase_history_product"):
                    hist = coinbase_volumes(prog["coinbase_history_product"], start)
                if not hist.empty:
                    cutover = df["date"].min()
                    df = pd.concat([hist[hist["date"] < cutover], df], ignore_index=True)
                    src = "okx_spliced"
            if df.empty and prog.get("coinbase_product"):
                df = coinbase_volumes(prog["coinbase_product"], start)
                src = "coinbase"
            elif not df.empty and prog.get("coinbase_product") and (df["date"].min() - start).days > 45:
                gap = coinbase_volumes(prog["coinbase_product"], start)
                gap = gap[gap["date"] < df["date"].min()] if not gap.empty else gap
                if not gap.empty:
                    df = pd.concat([gap, df], ignore_index=True)
                    src = "okx+coinbase"
            if not df.empty:
                df = df.groupby("date", as_index=False)["volume_usd"].sum()
                df["token"] = prog["token"]
                df["source"] = src
                print(f"volume {sym}: {len(df)} days ({src})")
                vol.append(df)
            else:
                print(f"volume {sym}: none")
    if rev:
        pd.concat(rev, ignore_index=True).drop_duplicates(["date", "protocol"]).to_csv(HERE / "data" / "revenue.csv", index=False)
    if vol:
        pd.concat(vol, ignore_index=True).drop_duplicates(["date", "token"]).to_csv(HERE / "data" / "volumes.csv", index=False)
    print("saved revenue.csv and volumes.csv")

if __name__ == "__main__":
    main()

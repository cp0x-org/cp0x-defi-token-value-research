"""Collect daily prices for all tokens in config via DefiLlama coins API (free, no key).
Output: data/prices.csv with columns date, coin, price.
The chart endpoint caps points per call, so we page in ~180-day windows."""
import json, time, datetime as dt, pathlib
import requests
import pandas as pd

BASE = "https://coins.llama.fi/chart/{coins}"
HERE = pathlib.Path(__file__).parent
CFG = json.loads((HERE / "config.json").read_text())

def fetch_coin(coin: str, start_ts: int, end_ts: int) -> pd.DataFrame:
    rows = []
    step = 180 * 86400
    t = start_ts
    while t < end_ts:
        span = min(180, (end_ts - t) // 86400 + 1)
        url = BASE.format(coins=coin)
        for attempt in range(4):
            try:
                r = requests.get(url, params={"start": t, "span": span, "period": "1d"}, timeout=40)
                r.raise_for_status()
                data = r.json()["coins"].get(coin, {}).get("prices", [])
                break
            except Exception as e:
                if attempt == 3:
                    raise
                time.sleep(2 * (attempt + 1))
        for p in data:
            rows.append({"date": dt.datetime.utcfromtimestamp(p["timestamp"]).date(), "coin": coin, "price": p["price"]})
        t += step
        time.sleep(0.4)
    df = pd.DataFrame(rows)
    return df.drop_duplicates(subset=["date", "coin"], keep="last") if not df.empty else df

def main():
    start_ts = int(dt.datetime.strptime(CFG["price_start"], "%Y-%m-%d").timestamp())
    end_ts = int(time.time())
    coins = sorted({p["token"] for p in CFG["programs"]} | {p["history_token"] for p in CFG["programs"] if p.get("history_token")} | set(CFG.get("control_tokens", [])) | {CFG["benchmark"]})
    out = []
    for c in coins:
        df = fetch_coin(c, start_ts, end_ts)
        print(f"{c}: {len(df)} daily points")
        out.append(df)
    res = pd.concat(out, ignore_index=True)
    (HERE / "data").mkdir(exist_ok=True)
    res.to_csv(HERE / "data" / "prices.csv", index=False)
    print("saved", HERE / "data" / "prices.csv")

if __name__ == "__main__":
    main()

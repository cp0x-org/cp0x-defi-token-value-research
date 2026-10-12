"""Download the daily price series used by stage3_outcomes.py (study 2, internal name Research 3).

Added for the public repository. The frozen package contained data/prices.csv, which is not
redistributed here because the prices originate from CoinGecko, whose terms restrict
redistribution. This script rebuilds the file with the same columns (date, coin, price) from the
DefiLlama coins API, using fetch_coin() from collect_prices.py (the collector of the same
research package, copied unchanged).

The coin list and first dates below are the coverage of the frozen prices.csv
(30 series, 2020-06-01 to 2026-10-03). Providers revise history, so a fresh download may differ
slightly from the frozen file. The frozen file's sha256 is recorded in
method/MANIFEST_frozen_archive_20261006.sha256 (./package/data/prices.csv, 1d9383c3...).

Run from the working directory that holds stage3_outcomes.py:
    python3 fetch_prices_stage3.py      -> data/prices.csv
"""
import datetime as dt
import hashlib
import pathlib

import pandas as pd

from collect_prices import fetch_coin

HERE = pathlib.Path(__file__).parent
FROZEN_SHA256 = "1d9383c398eb80f7973e03b7d845b5fbcb38138ac351fc8cba80f13067036744"
END = "2026-10-03"

# coin id -> first date present in the frozen prices.csv
COINS = {
    "coingecko:aave": "2021-06-01",
    "coingecko:aerodrome-finance": "2023-09-15",
    "coingecko:balancer": "2020-06-24",
    "coingecko:compound-governance-token": "2020-06-16",
    "coingecko:curve-dao-token": "2020-08-14",
    "coingecko:dydx-chain": "2023-11-27",
    "coingecko:ethena": "2024-04-03",
    "coingecko:ether-fi": "2024-03-18",
    "coingecko:ethereum": "2020-06-01",
    "coingecko:ethereum-name-service": "2021-11-09",
    "coingecko:frax-share": "2021-06-01",
    "coingecko:gains-network": "2021-11-02",
    "coingecko:gmx": "2021-09-14",
    "coingecko:havven": "2021-06-01",
    "coingecko:hyperliquid": "2024-11-29",
    "coingecko:jito-governance-token": "2023-12-08",
    "coingecko:joe": "2021-08-10",
    "coingecko:jupiter-exchange-solana": "2024-02-01",
    "coingecko:lido-dao": "2021-05-31",
    "coingecko:looksrare": "2022-01-10",
    "coingecko:maker": "2021-06-01",
    "coingecko:pendle": "2023-01-01",
    "coingecko:pump-fun": "2025-07-14",
    "coingecko:raydium": "2021-06-01",
    "coingecko:rocket-pool": "2022-12-31",
    "coingecko:sky": "2024-09-24",
    "coingecko:sushi": "2021-06-01",
    "coingecko:uniswap": "2021-05-31",
    "coingecko:vertex-protocol": "2023-11-22",
    "coingecko:yearn-finance": "2020-07-20",
}


def ts(day: str) -> int:
    return int(dt.datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc).timestamp())


def main():
    end_ts = ts(END) + 86399
    frames = []
    for coin, start in COINS.items():
        df = fetch_coin(coin, ts(start), end_ts)
        print(f"{coin}: {len(df)} daily points")
        frames.append(df)
    res = pd.concat(frames, ignore_index=True)
    res = res[pd.to_datetime(res["date"]) <= pd.Timestamp(END)]
    out = HERE / "data" / "prices.csv"
    out.parent.mkdir(exist_ok=True)
    res.to_csv(out, index=False)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print("saved", out)
    print("sha256", digest, "| identical to frozen file:", digest == FROZEN_SHA256)


if __name__ == "__main__":
    main()

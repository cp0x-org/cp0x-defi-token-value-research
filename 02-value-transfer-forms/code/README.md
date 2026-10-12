# Code for study 2 (02-value-transfer-forms)

The scripts expect one working directory that holds the scripts, `config.json`, `events.csv` and a `data/` subfolder. Set it up from the repository folder like this.

```
mkdir work && cp code/*.py code/config.json data/events.csv work/
mkdir work/data && cp data/*.csv data/holders_rev_raw.json work/data/
cd work
```

Run order

1. `python3 fetch_prices_stage3.py` downloads the 30 daily price series from the DefiLlama coins API into `data/prices.csv`. The frozen file is not redistributed because the prices originate from CoinGecko. The script prints whether the new file matches the frozen sha256 (1d9383c3...). Providers revise history, so small differences are possible.
2. `python3 stage3_outcomes.py` rewrites `data/stage3_outcomes_recomputed.csv`. With the frozen prices it reproduces the published file byte for byte (verified before the freeze on 2026-10-06).
3. `python3 build_universe.py` rebuilds the 164-protocol universe from `data/holders_rev_raw.json` and prints whether it matches the frozen list. Then check the hash with `cd data && sha256sum -c ../../method/stage3_universe_frozen.sha256` (adjust the path to where the method folder is).
4. Optional. `DA_DIR=<clone of DefiLlama/dimension-adapters at commit 1029ba611a85d425d3a022d5f274fd3b9c6a29a0> python3 c_screening.py --start 0 --end 164 --out data/rerun.csv` reruns the screening. The cache of source responses is not published, so this run queries Snapshot, DefiLlama and Bing again and can differ from the frozen result.

Requirements are Python 3 with pandas, numpy and requests. No API keys are needed.

`collect_prices.py` is the collector of the research package, copied as is, and `fetch_prices_stage3.py` imports its `fetch_coin` function. All other scripts are copied unchanged from the frozen package.

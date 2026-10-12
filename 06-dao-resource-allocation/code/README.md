# Code for study 6 (Research 6)

Scripts are copied as they were run. They use absolute paths from the original workspace (`/home/claude/r4rep`, `/home/claude/r5`, `/home/claude/r6`, `/home/claude/r6v`). To rerun, recreate those paths or edit the path constants at the top of each script.

## Run order

1. `join_outcomes.py` joins outcomes to the frozen decision tables and goal map. It writes `data_outcomes.csv` and `outcomes_cutoff.json` (cutoff 2026-10-05). `join.log` is the printed output of the run.
2. `sensitivity.py` checks the pattern rule under 20 readings (change log entry D7). It writes `data_pattern_sensitivity.csv` and `data_usage_decisions.csv`.
3. `make_scale.py` builds the spending scale table. It writes `data_scale.csv`. It reuses the loaders at the top of `join_outcomes.py`.

## Inputs from other studies in this series

| Input | Original path | Produced by |
|---|---|---|
| Shared loaders (`load_cg`, `at`, `load_fees`, `sum90`) | `r4rep/common.py` | Study 3, copied here as `common.py` |
| DefiLlama daily fees | `r4rep/raw/fees/*__dailyFees.json` | Study 3 |
| CoinGecko daily prices | `r4rep/raw/cg/*.csv` | Study 3. Not redistributed because of CoinGecko terms. Download with `fetch_prices.py` (copied from study 3) for `ethereum`, `lido-dao`, `aave`, `sky`, `uniswap` |
| DefiLlama revenue | `r5/raw/rev/*.json` | Study 4 |
| DefiLlama fee breakdown by product (28 MB) | `r5/raw/overview_fees_breakdown.json` | Study 4 |
| Category map | `r5/data/category_map.csv` | Study 4 |
| DefiLlama treasury | `r6v/raw/treasury_*.json` | Study 5 (validation) |
| DefiLlama protocol TVL | `r6/raw/tvl_*.json` | Included here in `data/raw/`, downloaded 2026-10-07 from `https://api.llama.fi/protocol/{lido,aave,sky,uniswap}` |

## Dependencies

Python 3 with pandas and numpy.

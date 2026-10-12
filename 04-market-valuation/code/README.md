# Code for study 4 (Research 5)

Scripts are copied as they were run, so paths inside them point to the original working directories (`/home/claude/r5`, `/home/claude/r4rep`). Adjust those paths before running. Python 3 with numpy, pandas, scipy and statsmodels.

| File | Role |
|---|---|
| `fetch_raw_r5.py` | Downloads the DefiLlama fee breakdown and per-group revenue series. Written at publication to document the requests. It was not part of the original run. |
| `common.py` | Helper module from the Research 4 replication package (`load_fees`, `sum90`). `build_r5.py` imports it. |
| `build_r5.py` | Builds `data/category_map.csv` and `data/panel_r5.csv`. |
| `analyze_r5.py` | Runs H1 to H3, the Holm correction, the replication rule and all robustness checks. Writes `data/results_r5.json`. |

## Run order

1. Put the inputs in a working directory. `raw/overview_fees_breakdown.json` comes from `fetch_raw_r5.py` (check its sha256 against `data/raw/RAW_HASHES.sha256`). `raw/rev/` and `raw/fees/` are copies of `data/raw/rev/` and `data/raw/fees/`. The Research 4 panels `panel.csv` and `panel_rep.csv` come from the Research 4 folder (`03-annual-token-trajectories`).
2. `python build_r5.py`
3. `python analyze_r5.py`

With the stored inputs, the independent reviewer reproduced `category_map.csv`, `panel_r5.csv` and `results_r5.json` byte for byte (method/REVIEW_R5.md, second pass).

Notes. Some revenue files are `child__` aggregates made by the C1 child-summing rule of Research 4. `fetch_raw_r5.py` fetches parent series only, so use the stored `data/raw/rev/` for exact reproduction. `data/raw/fees/` also contains a few series added later for the 2022–2023 supplementary window. They are not read for the Research 5 panel, and no existing file was changed. CoinGecko prices and market caps enter only through the Research 4 panels. Raw CoinGecko exports are not redistributed.

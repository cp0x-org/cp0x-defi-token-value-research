# Code for the supplementary window 2022–2023 (W0)

Python 3 scripts, copied as is from the working copy. They need pandas, numpy, scipy and statsmodels, plus `curl` for the downloads in `check_2022.py`.

These scripts must run from the study 3 and study 4 working directories and depend on folders `03-annual-token-trajectories` and `04-market-valuation`. They import `common.py` (study 3 helpers, in `03-annual-token-trajectories/code/`) and read the study 3 candidate list and raw series. The original paths are hard-coded. `/home/claude/r4rep` is the study 3 replication working copy, `/home/claude/r5` is the study 4 working copy, and `/home/claude/r22` is this folder (outputs go to `/home/claude/r22/data/`). Adjust these paths before running.

## Set up

1. Build a study 3 working directory as described in `03-annual-token-trajectories/code/README.md` (with `data/candidates.csv`, `raw/fees/`, `raw/fees_children/` and `raw/cg/` from `fetch_prices.py`, since CoinGecko exports are not redistributed). Every W0 entrant's fee series is in `03-annual-token-trajectories/data/raw/fees/`.
2. Build a study 4 working directory as described in `04-market-valuation/code/README.md` (with `raw/overview_fees_breakdown.json` from `fetch_raw_r5.py`, and `raw/rev/` and `raw/fees/` from `04-market-valuation/data/raw/`).
3. Point `/home/claude/r22` (or the edited path) at a copy of this folder, with `raw/protocols.json` taken from `data/raw/protocols.json`.

## Run order

| Step | Script | Run from | Writes | Method reference |
|---|---|---|---|---|
| 1 | `check_2022.py` | study 3 working directory (the script changes into it) | `check_2022.csv`; also downloads missing CoinGecko and fee series into raw/ | Feasibility and survivorship, before the freeze |
| 2 | `build_panel_w0.py` | study 3 working directory, on PYTHONPATH | data/panel_w0.csv | Window and sample |
| 3 | `analyze_w0.py` | any | data/results_w0_r4.json | T1, descriptive |
| 4 | `build_r5_w0.py` | study 4 working directory | data/category_map_w0.csv, data/panel_r5_w0.csv | Window and sample (study 4 variables) |
| 5 | `analyze_r5_w0.py` | any | data/results_w0_r5.json | T2, T3 |
| 6 | `posthoc_w0.py` | any | data/posthoc_w0.json | CHANGES W1, diagnostics only |

The `kind` column of `check_2022.csv` was added after the script ran and is not produced by `check_2022.py`. Before step 2, the W0 build also reran `fetch_fees_children.py` from folder 03 in the study 3 working directory, which aggregated one new parent (beethoven-x), as logged in CHANGES W2. The hashes in `method/SHA256SUMS_W0.txt` refer to the scripts at the top level of the original folder.

# Code for study 3 (Research 4)

Python 3 scripts, copied as is from the study's working copy. They need pandas, numpy and statsmodels, plus `curl` for the download scripts and openpyxl for `make_workbook.py`. All scripts use paths relative to one working directory that contains `data/` and `raw/`.

## Set up a working directory

```
cd 03-annual-token-trajectories
mkdir work && cd work
cp ../code/*.py .
cp -r ../data data
ln -s data/raw raw          # fees/, fees_children/, peers/, overview_fees.json, hacks.json, LDO Agent files
```

Missing raw inputs must be downloaded again. CoinGecko CSV exports are not redistributed (`python3 fetch_prices.py` writes `raw/cg/`). DefiLlama fee breakdowns and treasury series are not included for size reasons (`python3 fetch_stage2.py` writes `raw/bd/` and `raw/treasury/`). `raw/protocols.json` and `raw/lite.json` were saved by hand from https://api.llama.fi/protocols and https://api.llama.fi/lite/protocols2. The sha256 of every original file is in `data/raw/RAW_NOT_INCLUDED.sha256`. Live sources change, so re-downloaded files will not match those hashes exactly and results can differ slightly.

## Run order

| Step | Script | Writes | Method reference |
|---|---|---|---|
| 1 | `build_candidates.py` | data/candidates.csv | METHOD_R4.md, Universe 1-3 |
| 2 | `fetch_prices.py` | raw/cg/ | Measurement |
| 3 | `fetch_fees.py`, then `fetch_fees_children.py` | raw/fees/, raw/fees_children/ | Measurement, CHANGES C1 |
| 4 | `build_panel.py` | data/panel.csv | Universe 4-5, Measurement, C11 |
| 5 | `analyze.py` | data/results.json, data/runs_summary.csv | Stage 1, C12 |
| 6 | `fetch_stage2.py`, `build_stage2.py`, `analyze_stage2.py` | raw/bd/, raw/treasury/, data/panel_stage2.csv, data/results_stage2.json, data/runs_summary_stage2.csv | Stage 2, C3, C4 |
| 7 | `fetch_supply.py`, `fetch_supply_evm.py`, `fetch_dead.py` | data/onchain_supply*.csv, data/supply_blocks*.json | Stages 3 and 4, C5, C8, C9 |
| 8 | `analyze_stage3.py` | data/panel_stage3.csv, data/results_stage3.json, data/runs_summary_stage3.csv | Stage 3, C6, C7 |
| 9 | `analyze_stage4.py audit_list`, manual audit into data/stage4_audit.csv, then `analyze_stage4.py run` | data/stage4_audit_candidates.csv, data/panel_stage4.csv, data/results_stage4.json, data/runs_summary_stage4.csv | Stage 4, C13 |
| 10 | `lido_peers.py` | data/lido_peers.csv, data/eth_lst_share.csv | descriptive, not pre-registered |
| 11 | `posthoc.py` | data/posthoc.json | post hoc checks (CHANGES, last section) |
| 12 | `price_check.py`, `survivorship_check.py` | data/price_check.csv, data/missing_cg_fdv.csv | data quality, C10 |
| 13 | `fetch_fees_rep.py`, `fetch_fees_children.py`, `build_panel_rep.py`, `analyze_rep.py` | data/panel_rep.csv, data/results_rep.json | METHOD_R4_REPLICATION.md, Part A |
| 14 | `forward_start.py` | data/forward_start_2026-10-01.csv | METHOD_R4_REPLICATION.md, Part B |
| 15 | `make_workbook.py <out.xlsx>` | Excel workbook of the outputs | optional |

`common.py` holds shared helpers (7-day median at a date, 90-day fee sums, window dates). `data/results_stage3_gross.json` and `data/runs_summary_stage3_gross.csv` are the stage 3 result on the frozen gross totalSupply definition, produced before CHANGES C9.

Files without a producing script were prepared during the study and are included as data. These are `data/token_addresses.csv` (token contract per group, from DefiLlama), `data/missing_cg.csv` and `data/missing_cg_meta.csv` (candidates without a CoinGecko CSV), `data/stage4_audit.csv` (manual audit with sources) and `data/stage4_bridging_check.md`. The staking peer series in `raw/peers/` were downloaded from the same DefiLlama summary endpoints.

`logs/` holds the console logs of the download runs.

The independent reviewer re-ran steps 4 to 12 twice and obtained byte-identical outputs (method/REVIEW_R4.md).

License: MIT.

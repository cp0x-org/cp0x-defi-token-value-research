# Code for study 5 (Research 6 validation)

The scripts are copied as they were run. They use relative paths, so run them from the study folder (`05-spending-proxy-validation/`), not from `code/`. They expect a working layout with `data/` and `raw/` next to each other.

Requirements are Python 3.11 or newer, pandas, numpy and scipy. No API key is needed. The routescan API, the DefiLlama coins API and three public Ethereum RPC endpoints are called without credentials.

## Run order

| Step | Script | Reads | Writes |
|---|---|---|---|
| 0 | (prepare) | `data/raw/*.gz`, `data/raw/prices_defillama.tar.gz` | `raw/treasury_<slug>.json`, `raw/prices/*.json` |
| 1 | `fetch_transfers.py` | `data/treasury_sets.json` | `raw/tx/<address>_{tokentx,txlist,txlistinternal}.json` (about 331 MB, not in the repo) |
| 2 | `build_P.py` | `raw/tx/`, `raw/prices/`, `data/reported_spending.csv`, `data/recipient_class.json` | `data/P_outflows_<protocol>.csv.gz`, `data/proxy_P.csv`, `data/P_diagnostics.csv` |
| 3 | `build_B.py` | `raw/treasury_<slug>.json`, `data/reported_spending.csv` | `data/B_steps_<protocol>.csv.gz`, `data/proxy_B.csv`, `data/B_largest_outflow_days.csv` |
| 4 | `compare.py` | `data/reported_spending.csv`, `data/proxy_P.csv`, `data/proxy_B.csv` | `data/comparison.csv`, `data/verdict.json` |
| 5 | `manual_variant.py` (diagnostic only) | `data/P_outflows_*.csv.gz`, `data/reported_spending.csv` | `data/proxy_P_manual.csv` |

Step 0 in a shell, from the study folder.

```
mkdir -p raw && for f in data/raw/treasury_*.json.gz; do gunzip -c "$f" > "raw/$(basename "$f" .gz)"; done
tar -xzf data/raw/prices_defillama.tar.gz -C raw
```

`raw/prices/native.json` (the ETH price) is not shipped. `build_P.py` downloads any missing price file from coins.llama.fi on first run.

## Notes

- `compare.py` and `manual_variant.py` can be run directly on the shipped CSV files, without steps 1 to 3.
- Step 1 queries live APIs. A fresh download should match the recorded hashes in `data/raw/raw_files.sha256` only if the API returns the same rows. Compare row counts if hashes differ.
- `build_P.py` reuses `data/recipient_class.json` and only classifies addresses that are missing from it. Classification uses the `latest` block state (see REVIEW_R6V.md, section 1).
- The DefiLlama treasury JSON files in `data/raw/` were downloaded on 2026-10-07. The script that fetched them is not part of the study files. DefiLlama serves the current version of a treasury series, so a new download can differ from the stored one. Use the stored files to reproduce family B.
- `manual_variant.py` rewrites `data/recipient_class.json` after `proxy_P.csv` is produced (REVIEW_R6V.md, Note 8). Its docstring still states the Sky mechanism that the review refuted. The corrected explanation is in CHANGES_R6V.md, entry V12.

# 05. Can treasury outflows measure DAO spending? A pre-registered validation

Study 5 of the cp0x DeFi token value research series (internal name Research 6 validation). Publisher cp0x (https://cp0x.com), published 2026-10-08, version 1.0.

Report page: https://cp0x.com/blog/can-treasury-outflows-measure-dao-spending

## Abstract

This cp0x study tested whether treasury outflows computed automatically from public data can stand in for the spending that DAOs (decentralised autonomous organisations) report. The benchmark is 12 protocol-years of reported spending for Lido, Aave, Sky and Uniswap in 2023 to 2025, frozen with a sha256 hash before any outflow was computed. The primary transfer-based proxy (P1, Ethereum mainnet) misses the reported figure by a median factor of 2.21, against a pre-registered limit of 1.4, and only Lido has a median ratio inside the allowed band of 0.5 to 2. The primary balance-based proxy (B1, DefiLlama daily balances on all chains) covers only 9 protocol-years, below the required 10, with a median error factor of 2.12. Neither family passes, so by the frozen decision rule Research 6 continues as case studies. The gaps have structural causes that differ by protocol and that no scalable rule removes.

## Key findings

- In the cp0x Research 6 validation (Lido, Aave, Sky and Uniswap, 12 protocol-years, 2023 to 2025), the transfer-based treasury outflow proxy P1 differed from reported DAO spending by a median factor of 2.21 (median absolute log ratio 0.792 against a limit of 0.336).
- In the same study, the median ratio of P1 to reported spending was 6.36 for Uniswap, 2.52 for Aave, 1.55 for Lido and 0.15 for Sky, so only 1 of 4 protocols fell inside the allowed band of 0.5 to 2.
- In the same study, P1 matched the direction of change in reported spending in only 5 of 8 year pairs, with a Spearman rank correlation of −0.15.
- The balance-based proxy B1, built from DefiLlama daily treasury balances, covered only 9 of the 12 protocol-years because the balance series start in February 2023 (Sky in October 2023), and its median error factor was 2.12.
- In 2023 to 2025 the mismatch had structural causes, for example Uniswap DAO funding the Uniswap Foundation in tranches ($42.7M in 2023, about $138M of UNI in 2025) and Sky minting payments directly to recipients outside the treasury.
- A manually cleaned diagnostic version of the transfer proxy still had a median error of about 2.0 times (0.714 log points), so accurate on-chain spending figures would need address-by-address labelling of each protocol.

## Study at a glance

| Item | Value |
|---|---|
| Question | Does an automatic treasury outflow track reported DAO spending well enough to use at scale? |
| Sample | 12 protocol-years in 4 protocols (3 each for Lido, Aave, Sky, Uniswap); 9 covered in family B; Olympus screened out |
| Period | 2023-01-01 to 2025-12-31 (Lido first unit May to December 2023) |
| Unit of returns | Not applicable; the unit of comparison is r = proxy outflow (USD) / reported spending (USD) |
| Benchmark or control | Realised spending from protocol or commissioned financial reports |
| Data sources | Routescan, DefiLlama treasury and coins APIs, DefiLlama-Adapters, protocol reports |
| Method | Two proxy families (transfers P, balances B) tested on accuracy, bias, direction of change and coverage |
| Pre-registration | Method frozen 2026-10-07T09:18:12Z, sha256 4dfa38a8…0815; benchmark frozen 2026-10-07T09:31:26Z, sha256 16882766…e9f6 |
| Independent review | Yes, 2026-10-07; one bug fixed and several explanations corrected, verdict unchanged |
| Main verdict | Both families fail; Research 6 becomes case studies and no new proxy is designed |

## Files

| Path | Description |
|---|---|
| `README.md` | This file |
| `MANIFEST.sha256` | sha256 of every file in this folder, relative paths |
| `data/reported_spending.csv` | Frozen benchmark of reported spending (12 rows) |
| `data/benchmark.sha256` | Hash and freeze time recorded for the benchmark (see note below) |
| `data/treasury_sets.json` | Ethereum treasury addresses and own-token list per protocol, taken from the DefiLlama adapter |
| `data/proxy_P.csv` | Family P totals per unit (P0, P1, P1c and exclusion breakdown) |
| `data/proxy_B.csv` | Family B totals per unit (B1, B0, B1 without own token) |
| `data/comparison.csv` | Benchmark joined with every proxy variant |
| `data/verdict.json` | Criteria results for P1, B1 and diagnostic variants |
| `data/proxy_P_manual.csv` | Manually cleaned diagnostic variant (post hoc, cannot change the verdict) |
| `data/P_diagnostics.csv` | Outflow counts and unpriced transfers per protocol |
| `data/B_largest_outflow_days.csv` | Five largest net balance outflow days per protocol |
| `data/P_outflows_{aave,lido,sky,uniswap}.csv.gz` | Every treasury outflow 2023 to 2025 with USD value and classification |
| `data/B_steps_{aave,lido,olympus,sky,uniswap}.csv.gz` | Daily token value changes from DefiLlama balances |
| `data/recipient_class.json` | Recipient address class (eoa, multisig, contract) from `eth_getCode` and `getThreshold()` at the latest block |
| `data/raw/treasury_<slug>.json.gz` | DefiLlama treasury API downloads of 2026-10-07 (gzip of the original JSON) |
| `data/raw/prices_defillama.tar.gz` | DefiLlama coins API daily price files used by `build_P.py`, without `native.json` |
| `data/raw/treasury.js`, `data/raw/olympus_index.js`, `data/raw/adapters_commit.txt` | DefiLlama-Adapters treasury registry and Olympus adapter at commit 07a9a4704869135e59815475058d22b544471a86 |
| `data/raw/raw_files.sha256` | sha256 of every original raw download, including the 33 transaction files in `raw/tx/` (about 331 MB, not shipped) and the 9 superseded pre-fix files in `raw/tx_dedup_old/` |
| `method/METHOD_R6V.md`, `.sha256`, `.frozen_at` | Frozen method, its hash and freeze time |
| `method/CHANGES_R6V.md` | Change log V1 to V13 |
| `method/REVIEW_R6V.md` | Independent review |
| `method/REPORT_R6V_ru.md` | Final report in Russian (source of the English page) |
| `method/benchmark_notes/*.md` | Benchmark collection notes with quotes and source URLs for Aave, Lido, Olympus, Sky and Uniswap |
| `code/*.py`, `code/README.md` | Scripts as run, and run order |

## Data dictionary

Monetary values are USD, not rounded. Dates are ISO (YYYY-MM-DD, UTC). A unit is one protocol and one reported period.

### `data/reported_spending.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | lido, aave, sky or uniswap |
| period_start | date | | First day of the reported period |
| period_end | date | | Last day of the reported period (inclusive) |
| amount_usd | number | USD | Reported realised spending |
| includes | string | | Components of the figure as reported |
| excluded_or_gap | string | | Items excluded and known gaps |
| source | string | URL | Report the figure comes from |

### `data/proxy_P.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol, period_start, period_end | string, date, date | | Unit key, as in the benchmark |
| P0 | number | USD | Gross external outflow from the treasury set |
| P1 | number | USD | Primary rule-based net external outflow (P0 minus same-transaction-inflow outflows, non-multisig contracts and burns) |
| P1c | number | USD | P1 without the protocol's own token |
| excl_swap | number | USD | Outflows removed because the treasury received value in the same transaction |
| excl_contract | number | USD | Outflows removed because the recipient is a non-multisig contract |
| excl_burn | number | USD | Outflows to 0x0 or 0x…dead |
| n_out | integer | count | Outflow rows in the unit |
| n_unpriced | integer | count | Outflow rows without a price (mostly spam tokens, see REVIEW section 2) |

### `data/proxy_B.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol, period_start, period_end | string, date, date | | Unit key |
| series_start | date | | First day of the earliest DefiLlama chain key |
| B1 | number | USD | Primary net daily balance outflow, sum over days of max(0, −net value change) |
| B0 | number | USD | Gross balance outflow, sum of negative token value changes |
| B1_noown | number | USD | B1 computed without own-token keys (diagnostic) |
| covered | boolean | | True if the series covers the whole unit; B values are empty when False |

### `data/comparison.csv`

All columns of `reported_spending.csv`, `proxy_P.csv` and `proxy_B.csv`, joined on protocol, period_start and period_end. Definitions are as above.

### `data/proxy_P_manual.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol, period_start | string, date | | Unit key |
| reported | number | USD | Benchmark amount |
| P_manual | number | USD | Manually cleaned P1 (rules in `code/manual_variant.py`, set after seeing P1) |
| P_manual_noown | number | USD | P_manual without own token |
| r, r_noown | number | ratio | P_manual / reported and P_manual_noown / reported |

The Sky values in this file are treasury moves, not payments (CHANGES V10). Do not read them as spending.

### `data/P_diagnostics.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | Protocol |
| outflows | integer | count | Outflow rows 2023 to 2025 |
| unpriced | integer | count | Rows without a DefiLlama price |
| unpriced_tokens | string | | Symbols of unpriced tokens (truncated to 300 characters) |

### `data/B_largest_outflow_days.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | Protocol (includes olympus) |
| day | date | | Day of the balance step |
| net_dv | number | USD | Net value change over all tokens that day (negative is outflow) |

The series runs past 2025, so some listed days fall outside the study window.

### `data/P_outflows_<protocol>.csv.gz`

| Column | Type | Unit | Definition |
|---|---|---|---|
| hash | string | | Transaction hash |
| ts | integer | Unix seconds | Block timestamp |
| frm, to | string | address | Sender (in the treasury set) and recipient (outside it) |
| token | string | address | Token contract, or `native` for ETH |
| sym | string | | Token symbol as given by the API (may be empty or spam text) |
| amt | number | token units | Amount after decimals |
| kind | string | | erc20, txlist or txlistinternal |
| li | string | | Log index or trace id where available (`None` for ERC-20 rows, the API gives none) |
| out, inn | boolean | | Row is an outflow from, or inflow to, the treasury set |
| day | date | | UTC day of the transfer |
| swap_tx | boolean | | Treasury also received value in the same transaction |
| own | boolean | | Token is the protocol's own token |
| usd | number | USD | Value at the nearest DefiLlama daily price within 3 days, empty if unpriced |
| rclass | string | | Recipient class: eoa, multisig, contract, burn, or not_needed (classification not required) |
| p1 | boolean | | Row counts toward P1 |

### `data/B_steps_<protocol>.csv.gz`

| Column | Type | Unit | Definition |
|---|---|---|---|
| day | date | | Day d of the step from d−1 to d |
| chain | string | | DefiLlama chain key (for example Ethereum or Ethereum-OwnTokens) |
| own | boolean | | Chain key is an own-token key |
| token | string | | Token symbol as given by DefiLlama |
| dv | number | USD | (units_d − units_d−1) × price on day d (d−1 if units_d is 0) |

### JSON files

`verdict.json` holds, for each variant, units, protocols, coverage_ok, median_abs_ln_r (log points), median_ratio_error_x (exp of the former), C1, protocol_median_r, C2, C2_inside, C3, C3_pairs, spearman and PASS. `treasury_sets.json` maps the DefiLlama treasury key (maker is Sky) to its Ethereum owner addresses and own-token expression. `recipient_class.json` maps lower-case addresses to eoa, multisig or contract.

## Reproduction

1. Check the frozen files. From `method/`, run `sha256sum -c METHOD_R6V.sha256`. The benchmark hash in `data/benchmark.sha256` (16882766…e9f6) matches `data/reported_spending.csv`.
2. To recompute the verdict from the shipped totals, run `python code/compare.py` from this folder.
3. To rebuild everything, follow `code/README.md`. Step 1 downloads about 331 MB of transactions from the routescan API, and their original hashes are in `data/raw/raw_files.sha256`.

Note on `data/benchmark.sha256`. It also records a hash of `CHANGES_R6V.md` (494b6b6a…7c09) at benchmark freeze time, when the log held entries V1 to V4. Entries V5 to V13 were appended after the review, so the current log has a different hash (4381bced…bc5b). This is expected and does not affect the benchmark hash.

## License

Data and text are licensed CC BY 4.0. Code is licensed MIT. Reported spending figures come from the cited protocol reports. Raw CoinGecko price exports are not included. The ETH price file (`native.json`) is not shipped and is re-downloaded by `build_P.py`. Addresses in the data are public blockchain addresses.

## How to cite

cp0x (2026). Can treasury outflows measure DAO spending? A pre-registered validation. cp0x DeFi token value research, study 5, version 1.0. https://cp0x.com/blog/can-treasury-outflows-measure-dao-spending

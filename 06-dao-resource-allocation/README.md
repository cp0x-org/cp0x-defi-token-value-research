# How DAOs allocate resources: Lido, Aave, Sky and Uniswap, 2023–2025

This cp0x case study (Research 6) examines how four of the most transparent DAOs, Lido, Aave, Sky and Uniswap, allocated resources in 2023–2025 and what happened to protocol metrics after their decisions. It covers 112 decisions selected by pre-set materiality thresholds, including 58 spending and incentive decisions. Of the 58 spending and incentive decisions, 54 state a goal, but only 14 state it in terms of metrics published for all protocols. The pre-set rule for a cross-DAO pattern was met in only 2 of 20 readings, with opposite signs, so the study finds no robust pattern. Spending was 1.07 and 1.19 times DAO revenue at Lido in 2024 and 2025, fell from 0.92 to 0.44 of revenue at Aave between 2023 and 2025, and was about 0.5 at Sky, while the Uniswap DAO had almost no revenue. All results are descriptive associations on a small, non-random sample, with outcomes measured to 2026-10-05.

## Key findings

- In cp0x Research 6, 54 of 58 major spending and incentive decisions taken by Lido, Aave, Sky and Uniswap in 2023–2025 stated a goal, but only 14 stated it in terms of public metrics such as fees, revenue, category share, total value locked or token price, and 40 named goals that no public source measures systematically.
- In cp0x Research 6, the pre-set rule for a cross-DAO pattern in 2023–2025 decisions at Lido, Aave, Sky and Uniswap was met in 2 of 20 readings, one negative (7 of 10 class A decisions) and one positive (3 of 4 DAOs for incentives with fixed category coverage), so no robust pattern was found.
- In cp0x Research 6, user incentives aimed at growth were the most common measurable decision type (5 decisions in 4 DAOs), and 12 months later the protocol's share of category fees had risen after Lido's Liquidity Observation Lab and Aave's Merit and fallen after Sky Token Rewards and two Uniswap incentive waves.
- In cp0x Research 6, Lido's spending was 1.07 times DAO revenue in 2024 and 1.19 times in 2025, or 0.88 and 1.04 excluding Token Reward Plan compensation paid in LDO, with revenue as defined by DefiLlama.
- In cp0x Research 6, Aave's spending fell from 0.92 to 0.54 to 0.44 of revenue in 2023, 2024 and 2025 as revenue grew, Sky spent about 0.5 of revenue, and the Uniswap DAO had almost no revenue until its fee switch at the end of December 2025.

## Study at a glance

| Item | Value |
|---|---|
| Question | How do DAOs allocate economic resources, and what happened to the protocol business and token after decisions of different types? |
| Sample | 112 decisions in 4 DAOs (Lido 14, Aave 23, Sky 45, Uniswap 30) |
| Period | Decisions executed 2023-01-01 to 2025-12-31. Spending scale 2022–2025. Outcomes to 2026-10-05 |
| Unit of returns | Log change (natural log of end value over start value) over 6, 12 and 24 months. Main window 12 months |
| Benchmark or control | The protocol's category (share of category fees). Token returns against ETH |
| Data sources | DAO and foundation spending reports, governance records, DefiLlama, CoinGecko |
| Method | Case studies. Materiality thresholds, goal-to-metric map by a separate executor, freeze, then a mechanical outcome join |
| Pre-registration | Partial. Method frozen 2026-10-07T13:55:26Z, sha256 b1143c78…b551a. Decision tables and goal map frozen 2026-10-07T15:06:47Z before the join. The pattern rule's "decision type" and counting unit were undefined, so it was checked under 20 readings after results |
| Independent review | Yes, 2026-10-07. Two must-fix and several should-fix items, all addressed |
| Main verdict | Goals are almost always stated but rarely checkable (14 of 58). Checkable outcomes are mixed, with no robust pattern |


Full report page: https://cp0x.com/blog/how-daos-allocate-resources-lido-aave-sky-and-uniswap-20232025

Publisher cp0x (https://cp0x.com). Published 2026-10-08. Version 1.0. Internal name Research 6. The final report in Russian is `method/REPORT_R6.md`.

## Files

| Path | Description |
|---|---|
| `README.md` | This file |
| `MANIFEST.sha256` | sha256 of every file in this folder |
| `data/decisions/{lido,aave,sky,uniswap}_decisions.csv` | Frozen decision tables (112 rows in total) |
| `data/decisions/goal_map.csv` | Frozen map from stated goal to goal category and metric |
| `data/decisions/{lido,aave,sky,uniswap}_card_inputs.md` | Frozen case-card inputs (blinding log, denominators, line items by year, selected, class C and rejected decisions, gaps) |
| `data/decisions/all_frozen.sha256` | Hashes written when the decision tables, card inputs and goal map were frozen (2026-10-07T15:06:47Z) |
| `data/decisions/lido_frozen.sha256` | Earlier freeze of the Lido table (2026-10-07T14:17:04Z) |
| `data/data_outcomes.csv` | Outcomes joined to every decision (final run, after change D6) |
| `data/data_outcomes_first_run.csv` | Join output before change D6, kept for the record |
| `data/data_pattern_sensitivity.csv` | Pattern rule under 20 readings (change D7) |
| `data/data_usage_decisions.csv` | The 10 usage-goal decisions with an observed 12-month window, frozen and fixed-coverage share |
| `data/data_scale.csv` | Spending against fees, revenue and liquid treasury, 2022–2025 |
| `data/outcomes_cutoff.json` | Outcome data cutoff (2026-10-05) |
| `data/raw/tvl_{lido,aave,sky,uniswap}.json` | DefiLlama protocol TVL downloads, 2026-10-07 |
| `method/METHOD_R6.md`, `.sha256`, `.frozen_at` | Frozen method (Russian), its hash and freeze time |
| `method/METHOD_R6_DRAFT.md` | Draft method before freezing |
| `method/CHANGES_R6.md` | Change log D1 to D8 (Russian) |
| `method/CHANGES_R6_as_frozen_with_decisions.md` | Change log as frozen with the decision tables (D1 to D3) |
| `method/REVIEW_R6.md` | Independent review (English) |
| `method/REPORT_R6.md` | Final report after review (Russian) |
| `code/` | Scripts, run log and `code/README.md` |

### Verifying the freeze

From `data/`, run `sha256sum -c decisions/lido_frozen.sha256` and `sha256sum -c decisions/all_frozen.sha256`. The decision tables, card inputs and goal map match. The `CHANGES_R6.md` line in `all_frozen.sha256` (f47f30f3…) matches `method/CHANGES_R6_as_frozen_with_decisions.md`. The `CHANGES_R6.md` line in `lido_frozen.sha256` (14699e66…) refers to an earlier version of the change log that was not kept. The last line of each freeze file is the freeze time, which sha256sum reports as an improperly formatted line. From `method/`, `sha256sum -c METHOD_R6.sha256` checks the frozen method.

## Data dictionary

Log change means the natural log of the value at the end of the window divided by the value at t0. It is unitless. Converting to percent uses e^x − 1.

### `data/decisions/*_decisions.csv`

Frozen tables, published byte for byte as frozen, so several numeric columns also contain explanatory text.

| Column | Type | Unit | Definition |
|---|---|---|---|
| id | string | | Decision id, DAO, year, then A, B or LI and a number. LI marks a line-item change |
| title | string | | Short description of the decision |
| approved | string | ISO date or text | Approval date and vote |
| executed_start | string | ISO date or text | Start of execution. The first date in the text is used as t0 (change D5) |
| executed_end | string | ISO date or text | End of execution where known |
| amount_usd | number or text | USD | Amount as stated in the source. Text when not stated in USD |
| token_amount | string | tokens | Amount in tokens where stated |
| class | string | | A (investment in the protocol) or B (value distribution) |
| line_item | string | | Class A line item or class B type |
| denominator_year | number | year | Year of the materiality denominator |
| denominator_usd | number | USD | Materiality denominator |
| materiality | number or text | ratio | amount_usd / denominator_usd |
| selection_rule | string | | Which selection rule applied, with flags |
| stated_goal | string | | Goal as quoted from the source |
| expected_metric | string | | Metric named by the DAO, if any |
| sources | string | | Links to forum posts, votes and reports |

### `data/decisions/goal_map.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | lido, aave, sky or uniswap |
| id | string | | Decision id |
| goal_category | string | | usage_market, monetization, capital, token_price, no_metric_in_data or not_named |
| metrics | string | | Semicolon-separated metrics from the data that match the goal |
| justification | string | | The mapper's reason |

### `data/data_outcomes.csv` and `data/data_outcomes_first_run.csv`

The first-run file has the same columns except that token_vs_eth columns were filled only for the 17 evaluable decisions.

| Column | Type | Unit | Definition |
|---|---|---|---|
| t0 | date | ISO date | Window start parsed from executed_start. Empty if no date |
| protocol | string | | lido, aave, sky or uniswap |
| id | string | | Decision id |
| title | string | | Decision title |
| cls | string | | Class A or B |
| line_item | string | | Line item |
| executed_start | string | | As in the decision table |
| goal_category | string | | From goal_map.csv |
| primary_metric | string | | category_fee_share, take_rate, tvl or token_vs_eth. Empty if the goal has no metric |
| token_vs_eth_{6,12,24}m | number or text | log change | Change in token price divided by ETH price (7-day medians). "not yet observable" if the window ends after the cutoff |
| category_fee_share_{6,12,24}m | number or text | log change | Change in the protocol's share of its category's fees (90-day sums, DefiLlama breakdown) |
| fees_{6,12,24}m | number or text | log change | Change in 90-day protocol fees |
| take_rate_{6,12,24}m | number or text | log change | Change in revenue divided by fees (90-day sums) |
| revenue_{6,12,24}m | number or text | log change | Change in 90-day protocol revenue |
| tvl_{6,12,24}m | number or text | log change | Change in DefiLlama TVL on the date |
| primary_12m_sign | string | | + or − for the primary metric over 12 months, "not yet observable", or empty |

### `data/data_pattern_sensitivity.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| type | string | | Decision type (line item group or class A) |
| counting | string | | decision (each decision counts) or dao (majority sign per DAO) |
| measure | string | | base_12m (frozen category) or fixedcov_12m (fixed-coverage category) |
| daos | integer | count | DAOs with at least one observed decision of this type |
| n | integer | count | Observed cases |
| negative | integer | count | Cases with a negative sign |
| positive | integer | count | Cases with a positive sign |
| meets_rule | boolean | | At least 3 DAOs, at least 3 cases and at least 2/3 of cases with one sign |

### `data/data_usage_decisions.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | DAO |
| id | string | | Decision id |
| t0 | date | ISO date | Window start |
| type_line_item | string | | Line item group |
| type_class | string | | Class |
| base_12m | number | log change | 12-month change in category fee share, frozen definition |
| fixedcov_12m | number | log change | Same with the category limited to products that had fees at least 90 days before t0 |

### `data/data_scale.csv`

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | DAO |
| year | integer | year | Calendar year |
| spend | number | USD millions | Level 1 plus level 2 spending from the case cards. Empty if not determinable |
| fees | number | USD millions | DefiLlama calendar-year fees |
| revenue | number | USD millions | DefiLlama calendar-year revenue |
| liquid_treasury_end | number | USD millions | DefiLlama treasury excluding own token at year end |
| spend_to_rev | number | ratio | spend / revenue |
| spend_to_fees | number | ratio | spend / fees |
| runway_years | number | years | liquid_treasury_end / spend |

## Reproduction

See `code/README.md`. Run `join_outcomes.py`, then `sensitivity.py` and `make_scale.py`. The scripts need inputs from studies 3, 4 and 5 of this series, listed in `code/README.md`. CoinGecko price exports are not included because CoinGecko terms restrict redistribution, and `code/fetch_prices.py` downloads them.

## License

Data and text are licensed under CC BY 4.0. Code is licensed under MIT. Cite as cp0x (2026), How DAOs allocate resources: Lido, Aave, Sky and Uniswap, 2023–2025, cp0x DeFi token value research, study 6, version 1.0.

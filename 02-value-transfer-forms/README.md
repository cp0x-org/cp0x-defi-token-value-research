# 02-value-transfer-forms. Buybacks vs direct distributions: does the form of value transfer matter?

Study 2 of the cp0x DeFi token value research series (internal name Research 3). Full page: https://cp0x.com/blog/buybacks-vs-direct-distributions-does-the-form-of-value-transfer-matter


## Abstract

Study 2 of the cp0x DeFi token value research series asks whether the form in which a DeFi protocol passes value to its governance token is linked to the token's later price against ETH. It compares direct distributions of fees, buybacks with distribution of the purchased tokens (buy-and-distribute) and buybacks into the treasury, using seven dated transitions in seven protocols between February 2022 and May 2025 plus a two-step case at Yearn. Each token was measured over 90 calendar days after the first actual flow to holders, against a matched "twin" token where one qualified and otherwise against a basket of COMP, CRV and ENS. Six of the seven cases came in below the main control, one of them practically at zero (Sushi, -0.3 percentage points), and the only positive case was ether.fi at +9.8 points against the basket. Seven cases are far too few to show that the forms are equivalent, but the study found no historical support for the view that the market rewards a more direct flow.

## Key findings

- In study 2 of the cp0x series (seven DeFi value-transfer transitions, 2022 to 2025), no form of value transfer showed a consistent 90-day price advantage against ETH-relative controls, and six of the seven cases were below the main control.
- Both introductions of direct distributions from zero in study 2 underperformed their control over 90 days, Balancer (April 2022) by 11.2 percentage points against its twin COMP and Jito (January 2025) by 2.3 points.
- The only clean switch from buy-and-distribute to direct distributions found by study 2, Trader Joe in February 2022, trailed the control basket by 36.3 percentage points over 90 days while JOE lost 51.6% against ETH.
- Both switches from direct distributions to buy-and-distribute in study 2 were negative over 90 days, Gains Network (July 2024) at -31.8 percentage points against its twin and the basket and GMX (October 2024) at -81.9 points against the basket.
- In study 2 an early signal in favour of direct distributions disappeared after checking what holders actually received, which moved Sushi and ether.fi to buy-and-distribute, and after an external review replaced row-count windows with calendar windows.
- Only three of the seven study 2 cases had a qualifying twin token, all three twins were COMP, and in all three the 90-day sign against the twin matched the sign against the basket.
- A frozen search of 164 DEX and derivatives protocols in study 2 found no new switches from direct distributions to buy-and-distribute, but 144 of the 164 had sources too thin to classify even as negative cases, so this does not show that such switches are rare.

## Study at a glance

| Item | Detail |
|---|---|
| Question | Is the form of value transfer to a governance token systematically linked to the token's later relative price? |
| Sample | 7 transitions in 7 protocols (Balancer, Jito, Sushi, ether.fi, Trader Joe, Gains Network, GMX); 3 Yearn rows shown separately |
| Period | Events 2021-01-19 to 2025-05-08; main seven 2022-02-24 to 2025-05-08 |
| Unit of returns | Token price in ETH; outcome is token minus control simple 90-day return, in percentage points (pp) |
| Benchmark or control | Twin token matched on drawdown and pre-event run (distance at most 0.25), else median of COMP, CRV and ENS (basket); both reported |
| Data sources | Protocol docs, votes and on-chain deployments for dates; DefiLlama coins API daily prices keyed by CoinGecko ids; DefiLlama, Snapshot and web search for the protocol search |
| Method | Dated event study, one row per transition, no pooled test |
| Pre-registration | Partial. Analysis rules frozen mid-study after early numbers; universe and search procedure frozen 2026-10-03 before screening, universe sha256 d4556a803bd1e7f1 |
| Independent review | Yes, three external reproduction rounds; final package reproduces all outcomes byte for byte |
| Main verdict | Historical data do not allow a reliable ranking of direct distributions, buy-and-distribute and treasury buybacks by effect on token price |

## Files

| Path | Description |
|---|---|
| README.md | This file |
| MANIFEST.sha256 | sha256 of every file in this folder |
| data/cases.csv | Curated English case table (built for publication from the engine output, the registry and events.csv; no new statistics) |
| data/stage3_outcomes_recomputed.csv | Output of code/stage3_outcomes.py, source of every result number (copied as is) |
| data/stage3_registry.csv | Registry of all 28 transitions considered, forms, dates, control layer, confounders, exclusion reasons (Russian free text) |
| data/events.csv | 55 day-dated events with source URLs; engine input used for twin exclusions |
| data/stage3_events_v19_input.csv | Historical input file the stage started from; its numbers are superseded |
| data/stage3_universe_frozen.csv | Frozen universe of 164 DEX and derivatives protocols |
| data/stage3_search_log.csv | Log of every search template, calibration attempt and result, including negatives (Russian free text) |
| data/stage3_c_auto_screening.csv | Automated screening status per protocol with manual QA notes |
| data/stage3_c_auto_screening_evidence.csv | All evidence snippets collected by the screening |
| data/stage3_c_manual_queue.csv | Manual verdicts for the 13-protocol queue (Russian) |
| data/c_manual_queue_en.csv | English translation of the manual queue, added for publication |
| data/holders_rev_raw.json | Raw DefiLlama dump (api.llama.fi/overview/fees?dataType=dailyHoldersRevenue), source of the universe |
| method/C_PROCEDURE_FROZEN.md and .sha256 | Frozen search procedure (frozen 2026-10-03T18:05:11Z) and its hash from the frozen archive |
| method/stage3_universe_frozen.sha256 | Freeze-time hash of the universe file |
| method/FREEZE_NOTE.txt | Freeze note of the final archive, 2026-10-06 |
| method/MANIFEST_frozen_archive_20261006.sha256 | Full manifest of the frozen archive, including hashes of withheld files (prices.csv, screen_cache) |
| method/STAGE3_SUMMARY_final_report.md | Final corrected report (Russian), identical in text to Research3_report.docx |
| method/STAGE3_working_log.md | Working log with the rationale for each date and classification (Russian); sections with invalid numbers carry a banner, valid results are in sections 43 and 44 |
| method/Corrections_note.md | Corrections note of 2026-10-04 for studies 1 and 2 (internal names Research 2 and 3), converted from docx with pandoc; it records the three external review rounds |
| method/package_README_frozen.md | README of the frozen package (Russian) |
| code/stage3_outcomes.py | Outcome engine (calendar windows, twin matching, basket, sign check) |
| code/build_universe.py | Rebuilds the 164-protocol universe from the raw dump |
| code/c_screening.py | Automated screening with the frozen query |
| code/config.json | Engine configuration (programs, basket, benchmark) |
| code/collect_prices.py | Price collector of the research package (DefiLlama coins API), copied as is |
| code/fetch_prices_stage3.py | Added for publication; rebuilds data/prices.csv for the exact 30 series |
| code/README.md | Run order |

Withheld files. The frozen package contained `data/prices.csv` (daily prices keyed by CoinGecko ids, sha256 1d9383c398eb80f7...) and `data/screen_cache/` (924 cached responses, 22 MB). Prices are not redistributed because CoinGecko terms restrict redistribution; use the download script. The screening cache contains third-party texts with personal contact details, so it is withheld; its per-file hashes are in the archive manifest, and c_screening.py rebuilds it from the network (results may differ because sources change).

## Data dictionary

Types are string, date (ISO YYYY-MM-DD), integer, float, boolean. Empty cells mean not applicable or not established.

### data/cases.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| case_id | string | | Case identifier |
| in_main_seven | boolean | | True for the seven main transitions, false for Yearn ladder rows |
| protocol | string | | Protocol name |
| category | string | | A direct from zero, B buyback-and-distribute to direct, C direct to buyback-and-distribute, D buyback-and-distribute from zero, ladder outside ABCD |
| transition_en | string | | Plain description of the change |
| form_before, form_after | string | | Taxonomy code of the form (no_distribution, fee_share_direct, buyback_distribute, buyback_treasury) |
| decision_or_announcement_date | date | | Decision, proposal or announcement date where known |
| activation_date | date | | First actual flow to holders (empty for the YIP-65 decision row) |
| date_basis | string | | How the event date was established |
| primary_sources | string | | URLs or on-chain references, separated by " ; " |
| confounder_strength | string | | none, moderate or strong |
| confounders_en | string | | Concurrent events recorded |
| event_date_used | date | | Date used by the engine |
| token_id | string | | Price series id (DefiLlama coins API, CoinGecko id) |
| history_days | integer | days | Days of price history before the event |
| pre90_vs_eth_return | float | fraction | Token return against ETH over the 90 days before the event |
| drawdown_365d_vs_eth | float | fraction | Drawdown from the 365-day maximum of the ETH-relative price |
| token_vs_eth_30d_return, token_vs_eth_90d_return | float | fraction | Token return against ETH after the event |
| basket_n | integer | tokens | Basket tokens with valid data at 90 days |
| vs_basket_30d_pp, vs_basket_90d_pp | float | percentage points | Token return minus basket median return |
| nearest_twin | string | | Nearest eligible candidate (a twin only if twin_ok is true) |
| nearest_twin_distance | float | index | Matching distance, threshold 0.25 |
| twin_ok | boolean | | Twin qualifies |
| twin_vs_eth_90d_return | float | fraction | Twin's own return against ETH over 90 days |
| vs_twin_30d_pp, vs_twin_90d_pp | float | percentage points | Token return minus twin return |
| sign_agrees_twin_basket_90d | boolean | | 90-day signs against twin and basket agree |
| main_control | string | | twin if twin_ok, else basket |
| vs_main_control_90d_pp | float | percentage points | 90-day outcome against the main control |

### data/stage3_outcomes_recomputed.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| event | string | | Event label (Russian) |
| transition | string | | Transition type (Russian) |
| token | string | | Price series id |
| date | date | | Event date |
| hist_days | integer | days | Price history before the event |
| pre90 | float | fraction | 90-day pre-event return against ETH |
| dd365 | float | fraction | Drawdown from 365-day maximum, ETH-relative |
| tok_30, tok_90 | float | fraction | Token return against ETH, 30 and 90 days |
| basket_n_30, basket_n_90 | integer | tokens | Basket tokens with data |
| vs_basket_30_pp, vs_basket_90_pp | float | percentage points | Token minus basket median |
| twin | string | | Nearest candidate id |
| twin_dist | float | index | Matching distance |
| twin_ok | boolean | | Distance at most 0.25 |
| twin_30, twin_90 | float | fraction | Twin return against ETH |
| vs_twin_30_pp, vs_twin_90_pp | float | percentage points | Token minus twin |
| twin_own_90 | float | fraction | Same as twin_90 |
| robust_sign_90 | boolean | | Signs agree at 90 days |

### data/stage3_registry.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | Protocol |
| event | string | | Description (Russian) |
| decision_date | date | | Decision date |
| activation_date | date | | First actual flow to holders |
| launch_date | date | | Launch of the construction, not a flow date |
| intermediate_stage_date | date | | Intermediate decision between vote and flow |
| mechanism_from, mechanism_to | string | | Form before and after |
| mechanistic_eligible | boolean | | Activation date confirmed and event fits by meaning |
| transition_type | string | | Category code (A, B, C, D with suffix) |
| control_layer | string | | matched, basket or none |
| exclusion_reason | string | | Reason for exclusion (Russian) |
| confounder_strength | string | | none, moderate, strong |
| confounders | string | | Concurrent events and dating notes (Russian) |

### data/events.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | Protocol |
| token_coingecko | string | | Price series id |
| mechanism_type | string | | Mechanism code |
| event_type | string | | forum_proposal, vote_passed, first_execution, mechanism_upgrade, param_change and similar |
| date | date | | Event date |
| date_precision | string | | day or coarser; only day events are used by the engine |
| params | string | | Parameters as described by sources |
| size_usd_annualized | float | USD per year | Programme size where known |
| funding_source | string | | Source of funds |
| discretion | string | | Who executes |
| source_url | string | | Source |
| confounders | string | | Concurrent events |
| verified | boolean | | Date checked |
| notes | string | | Notes |

### data/stage3_events_v19_input.csv

Historical input (Russian headers). Columns are token, date, change type, description, three earlier twins, nearest distance, and medians against three twins at 90, 180 and 365 days in percentage points. These numbers come from the earlier method and are superseded.

### data/stage3_universe_frozen.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| frozen_at_utc | string | ISO timestamp | Freeze time, 2026-10-03T17:58:23Z |
| parent | string | | DefiLlama parent protocol id |
| name | string | | Largest version name |
| category | string | | Dexs or Derivatives |
| holders_rev_all_time_usd | integer | USD | All-time holders revenue, summed over versions |
| versions | string | | Versions merged under the parent |

### data/stage3_search_log.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| pass | string | | Search pass (1_targeted to 7_impermax_case) |
| template_id | string | | Template or calibration id |
| template_text | string | | Query text |
| protocol | string | | Protocol found or checked |
| finding | string | | What was found (Russian) |
| form_before, form_after | string | | Forms found |
| classification | string | | Classification of the finding |
| note | string | | Note |
| template_validated | string | | Whether the template passed its positive control |
| positive_control | string | | Control case used |
| positive_control_found | string | | Whether the control was recovered |

### data/stage3_c_auto_screening.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol, brand | string | | Universe name and search brand |
| source_url, source_type, date, snippet | string | | Best evidence item |
| old_mechanism_candidate, new_mechanism_candidate | string | | Forms detected |
| current_form_defillama | string | | Current form per DefiLlama methodology |
| screening_status | string | | yes, unclear, no_supported, no_low_recall |
| confidence | string | | Script confidence |
| reason | string | | Script reason (Russian) |
| n_evidence, n_historical | integer | items | Evidence items, of which historical |
| qa_note | string | | Manual QA note |

### data/stage3_c_auto_screening_evidence.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | Universe name |
| source_type | string | | defillama_methodology, defillama_adapter, snapshot, frozen_c_query, discovery, fetched_page |
| source_url | string | | Source |
| date | date | | Source date where known |
| snippet | string | | Text excerpt |
| tags | string | | Detected mechanism tags |

### data/stage3_c_manual_queue.csv and data/c_manual_queue_en.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | Universe name |
| queue_status | string | | control, closed_false_positive, closed_noise, closed |
| reason / reason_en | string | | Reason for the verdict |
| C_answer / c_answer | string | | Verdict on a direct-to-buyback-and-distribute switch |

## Reproduction

See `code/README.md`. In short, copy `code/*`, `data/events.csv` and the `data/` folder into a working directory, run `fetch_prices_stage3.py`, then `stage3_outcomes.py` and `build_universe.py`, and check the universe hash with `sha256sum -c`. A fresh price download may differ slightly from the frozen prices, so the frozen outcomes file is the reference.

## License

Data and text are licensed CC BY 4.0. Code is licensed MIT. Publisher cp0x (https://cp0x.com), version 1.0, published 2026-10-08. Page: https://cp0x.com/blog/buybacks-vs-direct-distributions-does-the-form-of-value-transfer-matter

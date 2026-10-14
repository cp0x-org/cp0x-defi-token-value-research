# Do token buybacks move prices? An event study of 43 DeFi decisions

The cp0x buyback event study measured how DeFi tokens moved against ETH after 43 dated DAO decisions to return value to holders in 16 protocols between 2022 and 2026. Each event was compared with two controls, a fixed basket of three DeFi tokens and the median of up to three tokens in a similar state before the event, and a claim was accepted only when both controls gave the same sign. Among buybacks, only the first public announcement of a programme was followed by a positive 30-day result on both controls, a median of +4.2 percentage points against the basket and +12.0 points against matched tokens, on seven events with a spread of about 40 points. Governance votes showed no positive reaction (-0.8 and -1.8 points), and late changes of known mechanisms showed a small negative (-4.3 and -3.6 points). Programme size did not order outcomes, no premium for burning was visible, and all results are associations in a small sample, not causal effects.

## Key findings

- In the cp0x buyback event study (16 DeFi protocols, 2022 to 2026), the first public announcement of a buyback programme was followed by a median 30-day return against ETH of +4.2 percentage points versus a control basket (n=7, IQR 40.6) and +12.0 points versus matched tokens (n=6), the only buyback stage positive on both controls.
- In the same study, governance votes approving buybacks showed no positive reaction, with median 30-day results of -0.8 percentage points against the basket and -1.8 points against matched tokens (n=7 on each).
- Late activations, parameter changes, cuts and pauses of known buyback mechanisms were followed by a small negative 30-day median of -4.3 percentage points against the basket (IQR 3.9, the narrowest of any stage) and -3.6 points against matched tokens (n=7).
- For the first actual buyback purchases the controls disagreed (-3.8 percentage points against the basket, +17.6 against matched tokens), and a placebo test on 1,000 random date sets gave one-sided p=0.64 and p=0.04, so the study does not establish a special reaction to first purchases.
- Across five buyback launches with flows from about 5,500 to 142,000 USD per day, none of three size measures (USD per day, share of revenue, share of trading volume) ordered 30-day outcomes, and the smallest programme, ether.fi, had the best result.
- Buyback events that burned the bought tokens showed no premium, with a 30-day median of -13.3 percentage points against the basket and -5.3 points against matched tokens (n=5), and all four burn votes and activations were negative on both controls.
- The study found no evidence that a token's 90-day run-up before an event predicts its result after it, since the correlation had opposite signs on the two controls (+0.10 on 39 events, -0.08 on 35 events).

## Study at a glance

| Item | Value |
|---|---|
| Question | Do DAO decisions to buy back tokens, pay out revenue or cut supply coincide with better token performance against ETH, and at which stage? |
| Sample | Database of 20 protocols and 55 events; computed sample of 43 day-precision events in 16 protocols |
| Period | Events from 2022-02-09 to 2026-09-02; prices to 2026-10-03 |
| Unit of returns | 30-day return of the token/ETH ratio minus the control's return, in percentage points (pp); 90 days secondary |
| Benchmark or control | ETH as numeraire; basket of COMP, CRV and ENS; median of up to three matched tokens ("twins") |
| Data sources | Governance primary sources; DefiLlama prices and revenue; single-venue exchange volumes |
| Method | Event study by class and decision stage, two control layers, sign-agreement rule, placebo test |
| Pre-registration | Partial. Version 2 method frozen 2026-10-04 14:12 UTC before any version 2 result (sha256 6d4457ffb272...); original design not pre-registered |
| Independent review | External reproduction check of version 2, 2026-10-04, no critical findings |
| Main verdict | Only first buyback announcements (positive) and late changes (small negative) hold on both controls |


Full report page: https://cp0x.com/blog/do-token-buybacks-move-prices-an-event-study-of-43-defi-decisions

Study 1 of the cp0x DeFi token value research series (internal name Research 2, version 2). Publisher cp0x (https://cp0x.com). Published 2026-10-08, version 1.0.

## Files

| Path | Description |
|---|---|
| `data/events.csv` | Event database, 55 events in 18 protocols with date, date precision, mechanism, stage, size, funding source, execution, primary source URL, confounders. The computed sample is the 43 day-precision events that are not context rows |
| `data/class_cut_events_v2.csv` | Per-event outcomes for the 43 computed events against the basket and against the median of three twins (main results file) |
| `data/matched_controls_v2.csv` | Twins selected for each of 40 matchable events, distance and twin-layer outcomes at 30, 90 and 180 days |
| `data/cells_v2_both_layers.csv` | Class by stage medians, n and IQR on both layers, in percentage points (tables of the report) |
| `data/class_cut_v2.csv` | Class by stage cells as written by `class_cut.py` on the version 2 matches, as fractions |
| `data/size_measures_flow_v2.csv` | Three size measures and 30-day outcomes of five buyback launches |
| `data/intensity.csv` | Programme flow against single-venue volume and revenue for events with a known programme size |
| `data/fundamentals_slice_v2.csv` | Revenue momentum before and revenue change after buyback launches |
| `data/placebo_v2_results.json` | Placebo test for the flow-start cell on both layers, 1,000 random date sets, seed 42 |
| `data/lido_mandate_events_calendar.csv` | Lido LDO purchase mandate case of 2026, recomputed with the calendar engine |
| `data/revenue.csv` | Raw DefiLlama daily protocol revenue used for size and revenue measures |
| `data/sensitivity_no_subjects/` | Sensitivity variant with studied tokens and LDO removed from the twin pool (`EXCLUDE_SUBJECTS=1`) |
| `data/superseded_v1/` | Results of the frozen 2026-10-02 version (`matched_controls.csv`, `class_cut*.csv`) and of the audit recalculation with calendar metrics and a single twin (`*_calendar.csv`). Kept only to document the version history. Not valid for conclusions |
| `method/METHOD_R2_V2.md`, `method/METHOD_R2_V2.sha256` | Version 2 method, frozen 2026-10-04 14:12 UTC before computation, and its checksum (sha256 6d4457ffb27295791b67dd6fd6887dc1b939524fc1d39f6b4c8fd4f80e9b6117) |
| `method/R2_V2_RESULTS.md` | Results under the frozen rules, claim by claim, and the external reproduction check |
| `method/AUDIT_STAGE12.md` | Audit of the frozen version that found row-count matching metrics |
| `method/CORRECTIONS_NOTE.md` | Corrections note for this study and study 2, converted from docx |
| `method/PREDICTIONS.md` | Registry of predictions for future events, frozen 2026-10-02, with an addendum of 2026-10-04 |
| `method/TAXONOMY.md` | Rules for coding events by class, stage and direction |
| `method/reviews/review_1_frozen_draft.md` | Last surviving review of the frozen draft, converted from docx |
| `method/source_reports_ru/` | Source reports in Russian, the corrected report `DRAFT_REPORT_V2.md`, the extension `EXTENSION.md` (sections marked invalid are superseded) and the frozen report of 2026-10-02 (historical) |
| `code/` | Scripts and `config.json`; see `code/README.md` |
| `MANIFEST.sha256` | sha256 of every file in this folder |

Method, review and source report files are mostly in Russian. The English report page is the public summary.

Not included. Raw daily prices (`prices.csv`) come from the DefiLlama coins API keyed by CoinGecko IDs and are not redistributed because CoinGecko terms restrict redistribution; `code/collect_prices.py` downloads them again. Raw single-venue exchange volumes (`volumes.csv`, OKX, Coinbase and Gate candles) are also not redistributed; `code/collect_fundamentals.py` downloads them, and derived measures are in `intensity.csv` and `size_measures_flow_v2.csv`. Charts, per-event scratch files and the frozen review archive of 2026-10-02 are not included.

## Data dictionary

Conventions. Dates are ISO (YYYY-MM-DD). Returns are simple returns of the token/ETH price ratio. Columns ending in `_30d`, `_90d`, `_180d` or without `_pp` are fractions (0.042 means +4.2 percentage points); columns named `_pp`, `med*`, `iqr*` in `cells_v2_both_layers.csv`, and `B`, `T`, `outcome_30d_pp` are percentage points. Empty cells mean no value (no suitable twin, window not closed, or no data).

Controlled vocabularies. `class` is `demand` (buybacks), `payout` (direct payouts) or `supply` (supply reduction). `stage` is `proposal` (first public announcement), `decision` (vote with recorded result), `flow_start` (first actual flow) or `activation` (late activations, parameter changes, upgrades, cuts and pauses). `direction` is `expands_return` or `reduces_return`.

### data/events.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | Protocol identifier |
| token_coingecko | string | | Token identifier in the price base (`coingecko:<id>`) |
| mechanism_type | string | | `buyback_distribute`, `buyback_treasury`, `buyback_treasury_gated`, `buyback_revenue_gated`, `buyback_burn`, `buyback_immutable`, `fee_share` or `emission_cut` |
| event_type | string | | `forum_proposal`, `vote_passed`, `first_execution`, `param_change`, `mechanism_upgrade` or `schedule_effective`; mapped to stage by `class_cut.py` |
| date | date | | Event date from the primary source |
| date_precision | string | | `day` or `month`; only `day` events are computed |
| params | string | | Programme parameters as stated in the source |
| size_usd_annualized | number | USD per year | Annualised programme size where known |
| funding_source | string | | `all_revenue`, `revenue_surplus` or `treasury` |
| discretion | string | | `committee` (discretionary execution) or `immutable` (automatic rule) |
| source_url | string | | Primary source for the date |
| confounders | string | | Other events in the outcome window; rows containing "context row" are excluded |
| verified | boolean | | Date checked against the primary source |
| notes | string | | Free-text notes |

### data/class_cut_events_v2.csv (also sensitivity_no_subjects and superseded_v1 variants)

| Column | Type | Unit | Definition |
|---|---|---|---|
| class | string | | Mechanism class |
| direction | string | | Expands or reduces value return |
| stage | string | | Decision stage |
| protocol | string | | Protocol identifier |
| date | date | | Event date |
| pre90 | number | fraction | Superseded. Change of the token/ETH ratio over the last 90 observations before the event, as computed by `class_cut.py`; replaced by `pre90_calendar` in `class_cut_events_v2_pre90_calendar.csv` (see `method/CORRECTION_2026-10-08_pre90.md`) |
| vs_basket_30d, vs_basket_90d | number | fraction | Token return minus median return of COMP, CRV and ENS over 30 or 90 days |
| vs_match_30d, vs_match_90d | number | fraction | Token return minus median return of the twins over 30 or 90 days |
| match_dist | number | distance | Largest distance among the twins used; above 0.25 means no suitable twin |

### data/matched_controls_v2.csv (also sensitivity and superseded variants)

| Column | Type | Unit | Definition |
|---|---|---|---|
| program | string | | Protocol identifier |
| event | string | | Event type |
| date | date | | Event date |
| token_dd | number | fraction | Drawdown of the token/ETH ratio from its high over the preceding 365 calendar days |
| token_pre90 | number | fraction | Change of the token/ETH ratio over the preceding 90 calendar days |
| match | string | | Twin token IDs separated by a vertical bar (nearest unsuitable candidate if none qualified) |
| match_dist | number | distance | Largest distance among the twins listed |
| n_twins | integer | count | Number of suitable twins (distance 0.25 or less, at most 3) |
| diff_vs_match_30d, _90d, _180d | number | fraction | Token return minus median twin return |
| match_dd, match_pre90 | number | fraction | Superseded files only. Twin's drawdown and pre-run, counted in rows in `matched_controls.csv` |

### data/cells_v2_both_layers.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| class, stage | string | | Cell |
| nB, medB, iqrB | integer, number, number | count, pp, pp | Basket layer events, median and IQR (75th minus 25th percentile) |
| nT, medT, iqrT | integer, number, number | count, pp, pp | Twin layer events with a suitable twin, median and IQR |

### data/class_cut_v2.csv (also sensitivity and superseded variants)

| Column | Type | Unit | Definition |
|---|---|---|---|
| class, stage | string | | Cell |
| n | integer | count | Events in the cell; the demand decision cell counts 8 because it includes Ethena 2026-09-02 with an unclosed window, effective n is 7 |
| med_basket_30, med_basket_90 | number | fraction | Median basket-layer outcome |
| med_match_30 | number | fraction | Median twin-layer outcome, suitable twins only |
| n_match | integer | count | Events with a suitable twin |
| iqr_match_30 | number | fraction | IQR of twin-layer outcomes |
| med_pre90 | number | fraction | Median pre-event run-up |

### data/size_measures_flow_v2.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol | string | | Protocol at its buyback launch |
| daily_usd | number | USD per day | Programme flow; derived from programme share times revenue for ether.fi and GMX |
| pct_volume | number | percent | Daily flow as a share of median daily token volume on one venue |
| pct_revenue | number | percent | Share of protocol revenue directed to the programme |
| outcome_30d_pp | number | pp | Superseded single-twin outcome of the frozen version, kept for comparison |
| B | number | pp | Version 2 outcome against the basket, 30 days |
| T | number | pp | Version 2 outcome against the median of three twins, 30 days |

### data/intensity.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol, event, date | string, string, date | | Event |
| program_daily_usd | number | USD per day | Annualised programme size divided by 365 |
| median_daily_volume_usd | number | USD | Median daily single-venue volume over the 30 days before the event |
| intensity_pct_of_volume | number | percent | Daily programme flow over median daily volume |
| annualized_revenue_usd | number | USD per year | Revenue over the 90 days before the event times 4 |
| program_pct_of_revenue | number | percent | Programme size over annualised revenue |

### data/fundamentals_slice_v2.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| protocol, anchor | string, date | | Protocol and launch date |
| rev_momentum_before | number | fraction | Revenue over 90 days before launch versus the previous 90 days, minus 1 |
| rev_change_after | number | fraction | Revenue over 90 days after launch versus 90 days before, minus 1 |
| fwd_unlock_90d_pct_supply, fwd_unlock_90d_vs_flow | string | | Placeholder; value "нет источника" means no data source |
| outcome_vs_match_30d, outcome_vs_match_90d | number | fraction | Superseded single-twin outcomes; version 2 outcomes are in `class_cut_events_v2.csv` |

### data/lido_mandate_events_calendar.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| event | string | | Event label in Russian. "Параметры транша N" means tranche N parameters published, "Первый филл мандата" first mandate fill, "Параметры фазы 2, потолок повышен" phase 2 parameters with raised cap |
| date | date | | Event date |
| note | string | | Confounder note in Russian (Kelp bridge hack of 2026-04-18 in window; NEST activation of 2026-08-10 in the 90-day pre-period) |
| pre90, dd365 | number | fraction | LDO/ETH change over 90 days and drawdown from 365-day high |
| window_closed_30 | boolean | | Whether the 30-day window had closed |
| tok_30 | number | fraction | LDO/ETH return over 30 days |
| vs_basket_30_pp | number | pp | Outcome against the basket |
| twin, twin_dist, twin_ok | string, number, boolean | | Twin, its distance and whether it qualifies |
| twin_30 | number | fraction | Twin return over 30 days |
| vs_twin_30_pp | number | pp | Outcome against the twin |
| robust_sign_30 | boolean | | Whether both controls give the same sign |

### data/revenue.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| date | date | | Day |
| protocol | string | | DefiLlama protocol slug |
| revenue_usd | number | USD | DefiLlama `dailyRevenue` |

### data/placebo_v2_results.json

Keys `observed_events` (the four events with basket and twin outcomes as fractions), `observed_median`, and per layer (`basket`, `twins`) `iterations`, `q05`, `q50`, `q95` (fractions) and `p_one_sided`.

## Reproduction

See `code/README.md`. In short, place the scripts, `config.json` and `data/events.csv` in one working folder, download prices with `collect_prices.py`, then run `matching_v2.py`, `class_cut.py` on the version 2 matches and `placebo_v2.py`. Prices downloaded later may differ slightly from the study's data run, which ended 2026-10-03, so tail windows of the latest events can move.

## License

Data and text are licensed under CC BY 4.0. Code is licensed under MIT. Raw prices are not included; their terms are set by their providers. Cite as shown on the report page.

## Correction of 2026-10-08

The pre-event run-up was originally measured over the last 90 price observations instead of 90 calendar days. It has been recomputed on calendar days (`code/fix_pre90_calendar.py`). Corrected correlations with the 30-day outcome are +0.04 (basket, 39 events) and -0.21 (twins, 35 events) for all events, and +0.22 (22) and -0.19 (21) for decisions and activations, against +0.10, -0.08, +0.23 and -0.12 before. The signs stay opposite on the two layers, so the conclusion (no evidence that the run-up predicts the result) is unchanged. Details in `method/CORRECTION_2026-10-08_pre90.md`.

| File | Description | Rows | Key columns |
|---|---|---|---|
| data/class_cut_events_v2_pre90_calendar.csv | Per-event outcomes with the superseded and the corrected run-up | 43 | class, stage, protocol, date, pre90_rows_superseded, pre90_calendar, vs_basket_30d, vs_match_30d |
| data/class_cut_v2_pre90_calendar.csv | Median corrected run-up by class and stage | 11 | class, stage, med_pre90_calendar |

Columns new in these files: `pre90_rows_superseded` (number, fraction) is the original value; `pre90_calendar` (number, fraction) is the change of the token/ETH ratio from the last observation on or before the event date minus 90 days (at most 7 days earlier) to the last observation on or before the event date; `med_pre90_calendar` (number, fraction) is its median within a class and stage.

# 04-market-valuation. What does the market pay for in DeFi tokens? Category growth, market share, monetisation and valuation

Study 4 of the cp0x DeFi token value research series (internal name Research 5). Full report at https://cp0x.com/blog/what-does-the-market-pay-for-in-defi-tokens-category-growth-market-share-monetisation-and-valuation

Study 4 of the cp0x DeFi token value research series (internal name Research 5) asks what one-year returns of decentralised finance (DeFi) tokens against ETH were made of, what the market paid for at the start of each year, and whether tokens that looked cheap relative to their business later did better. The sample is 200 observations of protocols with a market cap of at least 50 million USD in three October-to-October periods from 2023 to 2026, replicated on 169 observations in April-to-April periods. None of the three pre-registered hypotheses held. At equal fees, protocols that kept a larger share of fees (a higher take rate) were not valued higher, with a coefficient of −0.03 and a 95% confidence interval (CI) from −0.40 to 0.34 on 120 observations, and cheap tokens did not later outperform expensive ones. These are associations, not causes. The main estimates come from 2023–2026, and the supplementary 2022–2023 window is small and pointed the other way on valuation, on about 10 informative observations.

## Key findings

- In cp0x study 4 (October 2023 to October 2026), share growth and category growth had similar, weak associations with token returns against ETH, with coefficients of 0.20 and 0.16 and a difference of 0.04 (standard error 0.08, one-sided p 0.32, n = 168), so no difference was detected.
- In cp0x study 4, the median DeFi protocol with a token lost 47%, 43% and 30% of its category fee share in the three years from October 2023 to October 2026, while median category fees grew against ETH by 49%, 72% and 7%.
- In cp0x study 4, at equal fees, a higher take rate was not associated with a higher market cap at the starts of October 2023, 2024 and 2025, with a coefficient of −0.03 (95% CI −0.40 to 0.34, n = 120), which rules out valuation in proportion to revenue.
- In cp0x study 4, market cap rose much less than proportionally with fees, with a coefficient of 0.37 on log fees, so a protocol with twice the fees was worth about 30% more on average.
- In cp0x study 4, tokens that were cheap relative to their business did not later beat expensive ones, with a coefficient of 0.13 in October periods (95% CI −0.09 to 0.35) and 0.29 in April periods (two-sided p 0.004), the opposite of the hypothesised sign.
- In cp0x study 4, Lido's share of ETH liquid staking fees was 89%, 84%, 64% and 70% in October 2023 to 2026, and in the last year its share and take rate rose while the ETH staking market and Lido's revenue multiple fell.
- In a supplementary October 2022 to October 2023 window, cp0x study 4's valuation results reversed sign (take rate coefficient 0.83), but on only about 10 informative observations.

## Study at a glance

| Item | Detail |
|---|---|
| Question | What returns against ETH were made of, what the market paid for, and whether cheapness predicted the next year |
| Sample | 200 main and 169 replication observations, market cap at least 50 million USD at start, positive DefiLlama fees on at least 80 of the prior 90 days |
| Period | Main October 2023 to October 2026 (W1 to W3). Replication April 2023 to April 2026 (A1 to A3). Supplementary October 2022 to October 2023 |
| Unit of returns | Token log return against ETH, y = ln(P_end/P_start) − ln(ETH_end/ETH_start), in log points |
| Benchmark or control | ETH. Controls are log market cap, beta to ETH, drawdown, period fixed effects (FE) and, in stages 2 and 3, category FE |
| Data sources | DefiLlama fees, revenue and categories. CoinGecko prices, market caps and supply via the study 3 panels |
| Method | Exact decomposition, three clustered regressions, Holm correction, replication rule |
| Pre-registration | Frozen 2026-10-07T03:56:53Z, METHOD_R5.md sha256 5d5a0ca9 |
| Independent review | Two passes on 2026-10-07, no verdict changed |
| Main verdict | H1, H2 and H3 not recognised. No take rate premium at equal fees, and cheapness did not predict outperformance |

## Files

| Path | Content |
|---|---|
| `data/panel_r5.csv` | Final analysis panel, one row per protocol group and period (369 rows, 200 main and 169 replication) |
| `data/panel_r5_frozen_run.csv` | Panel of the first run of the frozen method, before corrections R1 to R3 (369 rows) |
| `data/category_map.csv` | Every DefiLlama product with its category key and its group's main key (2,843 rows) |
| `data/revenue_methodology.csv` | DefiLlama methodology text for fees and revenue of products in the sample (264 rows), used in the revenue-quality check |
| `data/take_rate_check.csv` | Take rate at the start of each main period for the revenue-quality check (202 rows) |
| `data/results_r5.json` | All results of the corrected run (H1 to H3, verdicts, robustness, variance shares, sample counts) |
| `data/results_r5_frozen_run.json` | Results of the first run of the frozen method |
| `data/raw/rev/` | DefiLlama daily revenue per group (165 JSON files, some are DefiLlama "not found" responses, kept as downloaded) |
| `data/raw/fees/` | DefiLlama daily fee and holders-revenue summary series per group, from the study 3 download (377 JSON files) |
| `data/raw/RAW_HASHES.sha256` | sha256, size and time of the DefiLlama files not included, including the 28 MB product breakdown |
| `method/METHOD_R5.md`, `method/METHOD_R5.sha256` | Frozen method and its sha256 with the freeze time 2026-10-07T03:56:53Z |
| `method/METHOD_R5_DRAFT.md` | Method draft before the freeze, including the revenue-quality check of 2026-10-07 (Russian) |
| `method/CHANGES_R5.md` | All changes after the freeze (R1 to R5, clarifications, text fix of 2026-10-08 in Russian) |
| `method/REVIEW_R5.md` | Independent review, two passes |
| `method/INTERIM_R5.md` | Final results note (Russian), identical in content to the published results document |
| `code/` | Scripts and run order, see `code/README.md` |
| `MANIFEST.sha256` | sha256 of every file in this folder |

The supplementary October 2022 to October 2023 window has its own folder, `07-supplementary-window-2022`.

Not included. The DefiLlama product breakdown `overview_fees_breakdown.json` (28,403,582 bytes) is above the 20 MB file limit. Its sha256 is `560015c6ba501a0a5ac8f8fa1fffcd9f0d1dcefcf5a724af7a644be5f35e7bf7` and `code/fetch_raw_r5.py` downloads a current version. Raw CoinGecko price exports are not redistributed because of CoinGecko's terms. Prices and market caps enter through the study 3 panels, whose download script is in the study 3 folder.

## Data dictionary

### data/panel_r5.csv

Suffix convention. `0` is the period start, `1` the period end, `p` 365 days before the start. Fee and revenue amounts are 90-day sums ending at that date, in USD. Log changes are natural logs.

| Column | Type | Unit | Definition |
|---|---|---|---|
| window | string | none | Period. W1 to W3 are October to October 2023–24, 2024–25, 2025–26. A1 to A3 are April to April over the same years |
| group | string | none | DefiLlama protocol group id (`parent#...` or `id#...`) |
| slug | string | none | DefiLlama slug used for the summary series |
| name | string | none | Protocol name |
| gecko_id | string | none | CoinGecko id of the token |
| key | string | none | Main category key of the group (DefiLlama category, liquid staking categories split by base asset) |
| key_nosplit | string | none | Main category without the base-asset split |
| start, end | date | ISO date | Period start and end |
| y | float | log points | Token log return against ETH, ln(P_end/P_start) − ln(ETH_end/ETH_start) |
| eth_ret | float | log points | ETH log return in USD over the period |
| mc_start, mc_end | float | USD | Market cap at start and end (median of 7 daily CoinGecko values) |
| s_cg | float | log points | Δln circulating supply (CoinGecko, MC / P) |
| beta | float | none | Slope of daily token log returns on ETH log returns over the 365 days before start |
| drawdown_start | float | log points | ln(P_start / maximum price over the prior 365 days) |
| ln_mc_start | float | ln USD | ln of mc_start |
| F0, F1, Fp | float | USD | Group fees from the DefiLlama group summary series (CHANGES R1) |
| Fbreak0, Fbreak1, Fbreakp | float | USD | Group fees summed from the product breakdown |
| Fmain0, Fmain1, Fmainp | float | USD | Group fees from products in its main category key |
| C0, C1, Cp | float | USD | Total fees of all products in the main category key |
| Fmain_ns0, Fmain_ns1, Fmain_nsp | float | USD | As Fmain, without the base-asset split |
| C_ns0, C_ns1, C_nsp | float | USD | As C, without the base-asset split |
| R0, R1, Rp | float | USD | Group revenue (DefiLlama dailyRevenue). Empty where no series exists |
| share0, share1, sharep | float | ratio | Fmain / C |
| take0, take1 | float | ratio | Take rate R / F |
| d_C | float | log points | Δln C |
| d_C_eth | float | log points | Δln C − eth_ret, category growth against ETH |
| d_share | float | log points | Δln share |
| d_D | float | log points | Δln(F / Fmain), diversification term |
| d_take | float | log points | Δln take |
| d_MF | float | log points | Δln(MC / F) |
| d_MR | float | log points | Δln(MC / R) |
| rev_variant | bool | none | Revenue variant defined (R at least 1% of F at both ends) |
| err_fee, err_rev | float | log points | Identity error of the fee and revenue decompositions |
| ln_F0 | float | ln USD | ln F0 |
| ln_take0 | float | ln ratio | ln take0 |
| prior_share_growth | float | log points | ln(share0 / sharep) |
| rev_start_ok | bool | none | R0 at least 1% of F0 (stages 2 and 3) |
| d_share_ns | float | log points | Δln share without the base-asset split |
| d_C_ns_eth | float | log points | Category growth against ETH without the base-asset split |
| conflict_start | bool | none | F0 and Fbreak0 both positive and differ more than twofold (excluded from stages 2 and 3) |
| conflict_stage1 | bool | none | Same test at start or end (excluded from stage 1) |

### data/panel_r5_frozen_run.csv

Same columns as `panel_r5.csv` without `Fbreak*`, `conflict_start` and `conflict_stage1`. In this run F is the breakdown sum.

### data/category_map.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| name | string | none | DefiLlama product name |
| group | string | none | Protocol group id |
| category | string | none | DefiLlama category on 2026-10-07 |
| chain0 | string | none | First listed chain |
| key | string | none | Category key with base-asset split |
| key_nosplit | string | none | Category key without split |
| fees_all_time | float | USD | All-time fees of the product |
| main_key | string | none | Key of the group's product with the largest all-time fees |
| main_key_nosplit | string | none | Same without split |

### data/revenue_methodology.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| group | string | none | Protocol group id |
| child | string | none | Product name |
| category | string | none | DefiLlama category |
| fees_all | float | USD | All-time fees |
| Fees, Revenue, ProtocolRevenue, HoldersRevenue, SupplySide | string | none | DefiLlama methodology text for each quantity |

### data/take_rate_check.csv

| Column | Type | Unit | Definition |
|---|---|---|---|
| window | string | none | Main period |
| name | string | none | Protocol name |
| category | string | none | DefiLlama category |
| tk | float | ratio | Take rate R / F at period start |
| tk_pct | float | percent | tk × 100, rounded |

## Reproduction

See `code/README.md`. In short, download the breakdown with `code/fetch_raw_r5.py` and compare its sha256 with `data/raw/RAW_HASHES.sha256`, then run `code/build_r5.py` and `code/analyze_r5.py`. With the original inputs the independent reviewer reproduced `category_map.csv`, `panel_r5.csv` and `results_r5.json` byte for byte. A new DefiLlama download will differ, because DefiLlama revises its data.

## License

Data and text are licensed CC BY 4.0. Code is licensed MIT. Publisher cp0x (https://cp0x.com), published 2026-10-08, version 1.0. Page https://cp0x.com/blog/what-does-the-market-pay-for-in-defi-tokens-category-growth-market-share-monetisation-and-valuation

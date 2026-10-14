# Supplementary window October 2022 to October 2023

Supplementary check for studies 3 and 4 of the cp0x DeFi token value research series (internal name Window 2022, window label W0). Repository folder `07-supplementary-window-2022` of https://github.com/cp0x-org/cp0x-defi-token-value-research. This window has no page of its own. Its results appear as a section inside the pages of study 3 (https://cp0x.com/blog/what-drives-defi-token-returns-against-eth-annual-trajectories-of-110-protocols) and study 4 (https://cp0x.com/blog/what-does-the-market-pay-for-in-defi-tokens-category-growth-market-share-monetisation-and-valuation).

Internal names used in the files map to the public numbering as follows. Research 4 is study 3 (folder `03-annual-token-trajectories`) and Research 5 is study 4 (folder `04-market-valuation`). The Russian report in `method/REPORT_W0_ru.md` calls them "исследования 4 и 5".

## Summary

The main weakness of studies 3 and 4 is that their data cover one market regime, 2023 to 2026. This supplementary check adds one annual window, 2022-10-01 to 2023-10-01, the end of the bear market after Terra and FTX and the start of the recovery, and re-tests three main findings on it with the same code and only the window changed. The window has 28 observations, only 2 of 28 tokens beat ETH, and the median token lost 48.4% against ETH. The study 3 fee growth result was weakly consistent (coefficient 0.21 against 0.26 in the main periods, one-sided p = 0.058), but fragile. The study 4 valuation results pointed the other way, with a take rate coefficient of 0.83 and cheap tokens later beating expensive ones, but on about 10 informative observations in three categories, so this is weak contrary evidence that cannot outweigh the main periods. The method was frozen before any regression was run, but the window is not fully blind, because descriptive returns were seen in the survivorship check before the window was chosen.

This summary is an English rendering of the Russian report `method/REPORT_W0_ru.md` (dated 8 October 2026, after independent review), with numbers taken from that report, the results JSON files, `method/CHANGES_W0.md` and `method/REVIEW_W0.md`. Percentages in brackets next to log values are the restatement exp(x) − 1 recorded in the results files.

## Key findings

- In the supplementary window 2022-10-01 to 2023-10-01 (28 observations of DeFi protocols with a market cap of at least 50 million USD), only 2 of 28 tokens beat ETH, one of them practically at zero (Liquity at +0.002 log points), and the median token returned −0.661 log points against ETH, which is −48.4%.
- In the 2022–2023 window, the study 3 fee growth coefficient was 0.2134 (standard error 0.1357, one-sided p = 0.0579, 95% interval −0.053 to 0.479, n = 28) against 0.256 in the main 2023–2026 periods, which passes the frozen rule of a positive coefficient with one-sided p < 0.10.
- The 2022–2023 fee growth result is fragile, because one-sided p is 0.066 with a t distribution, 0.113 with HC3 standard errors and 0.067 without winsorisation, and dropping LooksRare, Biswap or Osmosis alone pushes it above 0.10.
- In the 2022–2023 window, the study 4 valuation model gave a take rate coefficient of 0.826 (one-sided p = 0.0002, 95% interval 0.369 to 1.283, n = 16) against −0.03 in the main periods (n = 120), so by the frozen rule the study 4 finding of no monetisation premium is not confirmed in this window.
- In the 2022–2023 window, cheap tokens relative to their business later beat expensive ones (residual coefficient −1.79, one-sided p = 0.0057, n = 16), so by the frozen rule the study 4 finding that cheapness did not predict returns is not confirmed in this window either.
- The 2022–2023 valuation results rest on about 10 informative observations in three categories (Dexs 6, Lending 2, CDP 2) with 4 residual degrees of freedom, because six of nine category keys have a single observation, so they are weak contrary evidence that does not outweigh the main periods.
- In the 2022–2023 window 72% of protocols (18 of 25) lost share within their category, with a median change of −0.297 log points (−25.7%), but part of this is mechanical because DefiLlama's fee breakdown grew from 113 products on 2022-10-01 to 318 on 2023-10-01.

## At a glance

| Item | Value |
|---|---|
| Question | Do three main findings of studies 3 and 4 (fee growth, no monetisation premium, cheapness does not predict) hold in a different market regime? |
| Sample | 29 entrants in the panel, 28 observations in test T1 after the study 3 exclusion list (C2), 16 in the valuation model (T2, T3), 25 in the share descriptive |
| Period | 2022-10-01 to 2023-10-01, one annual window (W0) |
| Unit of returns | Token log return against ETH, ln(P_end/P_start) − ln(ETH_end/ETH_start), in log points |
| Benchmark or control | ETH; category fixed effects (FE) in the valuation model |
| Data sources | DefiLlama fees, revenue and protocol list; CoinGecko prices and market caps (not redistributed) |
| Method | Study 3 regression R1 and study 4 model V and residual test, same code as the main studies, one window, heteroskedasticity-robust (HC1) errors, which equal protocol clustering here |
| Pre-registration | `method/METHOD_W0.md` frozen 2026-10-07T19:35:53Z, sha256 0e0c8a5537b6a986581f39757b1b99fe0f2bb25e15b360a3cc669d473c3a6e44. Not fully blind, descriptive returns were seen before the window was chosen |
| Independent review | One review (`method/REVIEW_W0.md`); all archived outputs reproduced by hash; must-fix and should-fix items addressed in `method/CHANGES_W0.md` and the report |
| Main verdict | Fee growth weakly consistent with study 3; valuation results inconsistent with study 4 by the frozen rule, but on so few effective observations that they carry little weight next to the main periods |

## Survivorship check

Before computing, the check in `data/check_2022.csv` tested whether dead tokens dropping out would bias the window. On 2022-10-01, 55 tokens among protocols that DefiLlama knows today or marks as dead had a market cap of at least 50 million USD. Of these, 29 meet the fee-data entry rule, 24 are alive but DefiLlama's fee series starts later, and 2 are dead (Hyphen, RenVM).

| Start | Group | n | Median return against ETH (log points) | Share beating ETH |
|---|---|---|---|---|
| 2022-10-01 | Enters (fee data ok) | 29 | −0.662 | 0.069 |
| 2022-10-01 | Alive, no fee data | 24 | −0.711 | 0.042 |
| 2022-10-01 | Dead, no fee data | 2 | −0.922 | 0.000 |
| 2022-04-01 | Enters (fee data ok) | 25 | −0.467 | 0.080 |
| 2022-04-01 | Alive, no fee data | 39 | −0.809 | 0.128 |
| 2022-04-01 | Dead, no fee data | 10 | −2.252 | 0.000 |

Tokens that do not enter moved against ETH roughly like those that do in the October window, so October was accepted. The April 2022 window was rejected because Terra-ecosystem and other tokens that lost from 60% to almost 100% against ETH drop out, and the survivors would look much better than the market.

The check is a lower bound on missing tokens. It cannot see protocols deleted from DefiLlama, and it misses alive protocols outside the fee dashboard such as Serum (about 285 million USD at the start, −3.36 log points against ETH) and Multichain (about 76 million USD, −0.72), dead protocol families whose token sits only on the parent, and 16 dead tokens whose CoinGecko download failed. Adding Serum alone moves the October dead group to n = 3 with a median of about −1.09, which does not change the choice of October.

## Results

### T1, fee growth (study 3)

The table shows the study 3 regression R1 on the window, with category FE where categories with fewer than 10 observations are pooled (Dexs 12, other 16).

| Test | n | Coefficient on fee growth | Standard error | One-sided p | 95% interval | R² | Main periods |
|---|---|---|---|---|---|---|---|
| T1 | 28 | 0.2134 | 0.1357 | 0.0579 | −0.053 to 0.479 | 0.174 | 0.256 |

The sign and size match the main periods, so the result is consistent with study 3 by the frozen rule. The support is weak, because the significance depends on the error type and on single tokens. Variance shares of the return decomposition are 0.71 for fee growth, 0.194 for rerating and 0.096 for minus dilution, and fee growth is the largest, as in study 3.

### T2 and T3, valuation (study 4)

The table shows model V (ln market cap on ln fees, ln take rate and prior share growth with category FE) and the residual test on 16 observations, 7 having been dropped for lack of prior share data.

| Test | n | Coefficient | Standard error | One-sided p | 95% interval | Classical t, two-sided p (4 df) | Frozen verdict |
|---|---|---|---|---|---|---|---|
| T2, take rate | 16 | 0.826 | 0.2333 | 0.0002 | 0.369 to 1.283 | 0.0092 | Inconsistent with study 4 |
| T3, valuation residual | 16 | −1.7895 | 0.7065 | 0.0057 | not reported | 0.0637 (one-sided 0.032) | Inconsistent with study 4 |

The coefficient on ln fees in model V is 0.709, and the T2 interval includes 1. Dropping any one of the 10 informative observations keeps the take rate coefficient between 0.65 and 0.95. The reading that this result carries little weight was made after the results were seen.

A post hoc version without category FE gives a take rate coefficient of 0.236 (two-sided p = 0.37) and a residual coefficient of 0.023 (p = 0.94). This is a different model, reported only as a diagnostic, and it gives no support to study 4 either way.

### Category share (descriptive)

| n | Share losing category share | Median change in share (log points) | Median change in share (percent) | Median category fee growth against ETH (log points) |
|---|---|---|---|---|
| 25 | 0.72 | −0.297 | −25.7 | −0.405 |

The share loss is close to the main periods (72.5% losing share), but part of it is mechanical because DefiLlama nearly tripled the number of tracked products during the year. The −0.405 median category growth is the Dexs value, since 12 of the 25 observations are Dexs, and the median across distinct category keys is −0.14.

## What this changes

The link between token returns and fee growth gained additional, though weak, support in a different market regime. The study 4 findings that the market did not pay for monetisation and that cheapness predicted nothing should be explicitly limited to 2023–2026. In 2022–2023 the data point the other way, though with very little confidence, and the series synthesis mentions this as a caveat to the finding that the market did not value tokens as a claim on cash flow.

## Limitations

- One window and 28 observations.
- The survivorship estimate is too favourable, because the check cannot see protocols removed from DefiLlama.
- The valuation check rests on about ten protocols in three categories, with thin 2021–2022 fee coverage behind the prior share variable (53 products on 2021-10-01).
- The descriptive figures of the window were known before the method was frozen.
- All results are associations, not causal effects.

## Files

| Path | Size | Content |
|---|---|---|
| `README.md` | | This file |
| `MANIFEST.sha256` | | sha256 of every file in this folder |
| `data/panel_w0.csv` | 29 rows | Study 3 panel for W0, all entrants before the C2 exclusion |
| `data/panel_r5_w0.csv` | 28 rows | Study 4 panel for W0 |
| `data/category_map_w0.csv` | 2,843 rows | Product to category key map (byte-identical to `04-market-valuation/data/category_map.csv`) |
| `data/check_2022.csv` | 129 rows | Survivorship and feasibility check for starts 2022-04-01 and 2022-10-01 |
| `data/results_w0_r4.json` | | T1 and descriptive results |
| `data/results_w0_r5.json` | | T2, T3 and category share results |
| `data/posthoc_w0.json` | | Post hoc degrees-of-freedom and no-FE diagnostics (CHANGES W1), not used for verdicts |
| `data/raw/protocols.json` | 8,531 protocols, 9.1 MB | DefiLlama protocol list (https://api.llama.fi/protocols), used for dead protocols in the survivorship check; file time 2026-10-07 19:13 UTC; sha256 03c42c914c13732aeff1f43b7e6c839bb4e4b1607f2b64b2847a5080ce08212d |
| `method/METHOD_W0.md`, `METHOD_W0.sha256`, `METHOD_W0.frozen_at` | | Frozen method, its hash and freeze time |
| `method/CHANGES_W0.md` | | Notes W1 to W4 after the freeze |
| `method/REVIEW_W0.md` | | Independent review |
| `method/REPORT_W0_ru.md` | | Final report in Russian, after review |
| `method/SHA256SUMS_W0.txt` | | Hashes recorded at the time of the run (paths relative to the original working directory, where scripts sat at the top level) |
| `method/check.log` | | Console output of the survivorship check, written before the freeze |
| `code/` | | Scripts and `code/README.md` |

## Data dictionary

All dates are ISO (YYYY-MM-DD). Log changes are natural logs. USD values are nominal. Booleans are `True`/`False`. Empty cells are missing values.

### data/panel_w0.csv (29 rows)

Same columns as `panel.csv` in folder 03. Test T1 drops the row whose `gecko_id` is in the C2 exclusion list (here only crypto-com-chain, Defi Swap) and rows with `supply_artefact = True` (none).

| Column | Type | Unit | Definition |
|---|---|---|---|
| window | string | | W0 (2022-10-01 to 2023-10-01) |
| start, end | date | | Window start and end; end is the last price date if delisted |
| group | string | | DefiLlama group key (parent#slug or id#n) |
| slug, name | string | | DefiLlama slug and display name |
| gecko_id | string | | CoinGecko id of the token |
| category | string | | DefiLlama category of the child with the largest all-time fees |
| delisted | bool | | Price series ended inside the window |
| mc_start, mc_end | float | USD | Market cap, 7-day median ending on the date |
| p_start, p_end | float | USD | Token price, 7-day median |
| fees90_start, fees90_end | float | USD | Sum of DefiLlama daily fees over 90 days ending on the date |
| fee_days_start, fee_days_end | int | days | Days with fee data in those 90 days |
| H_start, H_end | float | share 0 to 1 | 90-day holders revenue over 90-day fees; missing if no holders revenue data in the 90 days |
| y | float | log points | ln(p_end/p_start) minus ln of the ETH price ratio |
| g | float | log points | ln(fees90_end/fees90_start) minus the ETH log return (fee growth in ETH terms) |
| m | float | log points | Log change of market cap over fees (rerating) |
| s | float | log points | Log change of circulating supply, market cap over price (dilution) |
| ln_M_start | float | log | ln(market cap / annualised fees) at start |
| ln_mc_start | float | log USD | ln(mc_start) |
| beta | float | ratio | Slope of daily token log returns on ETH log returns over 365 days before start, at least 250 pairs |
| drawdown_start | float | log points | ln(p_start / maximum daily price in the 365 days before start) |
| eth_ret | float | log points | ETH log return over the window |
| identity_err | float | log points | y − (g + m − s), numerical check |
| supply_artefact | bool | | abs(s) > ln(5) |

### data/panel_r5_w0.csv (28 rows)

Same columns as `panel_r5.csv` in folder 04. Suffix `0` is the window start (2022-10-01), `1` the end (2023-10-01), `p` 365 days before the start (2021-10-01). Fee and revenue amounts are 90-day sums ending at that date, in USD.

| Column | Type | Unit | Definition |
|---|---|---|---|
| window | string | none | Period, W0 (2022-10-01 to 2023-10-01) |
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

### data/category_map_w0.csv (2,843 rows)

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

### data/check_2022.csv (129 rows)

| Column | Type | Unit | Definition |
|---|---|---|---|
| start | date | | Window start tested, 2022-04-01 or 2022-10-01 |
| universe | string | | A_current (study 3 candidates in today's DefiLlama fee dashboard, with a CoinGecko id) or B_dead (DefiLlama protocols with `deadFrom` and a CoinGecko id, not in A) |
| slug, name, category | string | | DefiLlama slug, name and category |
| gecko_id | string | | CoinGecko id of the token |
| deadFrom | date | | DefiLlama date from which the protocol is marked dead (B_dead only) |
| mc_start | float | USD | Market cap, 7-day median ending on the start date |
| fee_days | int | days | Days with DefiLlama fee data in the 90 days before start |
| fees90 | float | USD | Sum of DefiLlama daily fees in those 90 days |
| fee_ok | bool | | fee_days at least 80 and fees90 positive (entry rule, without the C1 child summing) |
| y_vs_eth | float | log points | Token log return over one year from start minus the ETH log return; empty if no end price |
| price_end_missing | bool | | No token price one year after start |
| kind | string | | Group label, one of enters, fee series starts later, no fee adapter at all, dead. Not produced by the archived `check_2022.py` (review S5) |

`check_2022.csv` is not listed in `method/SHA256SUMS_W0.txt`. Its sha256 at publication is 0a43edec1eb3327b0fc9cea0a59e7b22cdded2230d647f02f845505657d32db2.

### JSON results

`results_w0_r4.json` holds `T1` (n, b_g, se, p_one_sided, ci95, r2, consistent, categories) and `descriptive` (n, share_beat_eth, median_y, median_pct_vs_eth, variance_shares_g_m_minus_s, corr_y_g). `results_w0_r5.json` holds model_V_sample, dropped_no_prior_share, `T2` (b_take, se, p_one_sided_positive, ci95, a_lnF, consistent_no_premium, ci_excludes_1, n_categories), `T3` (b_resid, se, p_one_sided_negative, p_two_sided, consistent_no_prediction) and `descriptive_share` (n, median_d_share, median_pct, share_losing, median_category_growth_vs_eth). `posthoc_w0.json` holds V and H3 fits with and without category FE (n, resid_df, coefficient, p_HC1_two, p_classic_t_two).

## Reproduction

The scripts reuse the working directories of studies 3 and 4, so this folder depends on folders `03-annual-token-trajectories` and `04-market-valuation`. See `code/README.md` for the run order. Raw CoinGecko exports are not redistributed, and they are fetched again with `fetch_prices.py` from folder 03. The independent reviewer rebuilt `panel_w0.csv`, `panel_r5_w0.csv` and `category_map_w0.csv` from the original inputs with matching hashes. A new download will differ, because DefiLlama and CoinGecko revise their data.

## Notes on sources

- `METHOD_W0.md` says "Frozen 2026-10-08", while `METHOD_W0.frozen_at` records 2026-10-07T19:35:53Z. These are the same moment, 02:35:53 on 8 October in the working time zone (UTC+7).
- `METHOD_W0.md` gives 37 uncovered tokens for April 2022. CHANGES W3 corrects this to 39 (37 with a later fee series plus 2 with no fee adapter at all), and this README uses 39.
- `METHOD_W0.md` says revenue was downloaded for the new groups. The review (N2) found that every W0 group already had a revenue file from study 4, so nothing was downloaded.
- The title of `METHOD_W0.md` says "Frozen before computing". Regressions were not computed before the freeze, but the descriptive returns in `check_2022.csv` were (review S2, CHANGES W3).

## License

Data and text are licensed under CC BY 4.0. Code is licensed under MIT. DefiLlama data are redistributed under DefiLlama's terms. Raw CoinGecko prices are not included. Publisher cp0x (https://cp0x.com), published 2026-10-08, version 1.0.

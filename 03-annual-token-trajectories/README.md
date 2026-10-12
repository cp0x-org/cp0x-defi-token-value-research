# What drives DeFi token returns against ETH? Annual trajectories of 110 protocols

Study 3 of the cp0x DeFi token value research series (internal name Research 4). Repository folder `03-annual-token-trajectories` of https://github.com/cp0x-org/cp0x-defi-token-value-research.

## Summary

# What drives DeFi token returns against ETH? Annual trajectories of 110 protocols

Research 4 by cp0x asks which protocol states and DAO decisions are associated with a DeFi token beating ETH over one year. The sample is 202 observations of 110 DeFi protocols with a market capitalisation of at least 50 million USD, in three October-to-October windows from 2023 to 2026. Only 18%, 9% and 24% of tokens beat ETH, and the median token fell 27%, 60% and 42% against ETH. Fee growth measured in ETH was the only pre-registered factor associated with returns in every check in the main 2023–2026 analysis, accounting for about 30% of the variation within a window. A link between the holder share of fees and returns did not replicate on windows shifted by six months, and new products, new chains and unlocks showed no significant association. The main estimates come from the 2023–2026 regime; the supplementary 2022–2023 window is small. All results are associations, not causal effects.

## Key findings

- In Research 4 (202 observations of 110 DeFi protocols, October 2023 to October 2026), only 18%, 9% and 24% of tokens beat ETH in the three annual windows, and the median token lost 27%, 60% and 42% against ETH.
- In Research 4, fee growth in ETH terms was the only pre-registered factor that held in all nine robustness runs, and 10% more fee growth than a peer went with about 2.5% more annual token return against ETH (coefficient 0.256, p < 0.001, n = 175).
- In Research 4, fee growth alone accounts for about 30% of the within-window variation in annual returns against ETH, and the top fifth of tokens beat ETH by a median 16% with fees up 24% while the bottom fifth lost 80% with fees down 68%.
- In Research 4, a larger holder share of fees went with better returns at equal fee growth in the main 2023–2026 windows (coefficient 0.56, p = 0.0001, n = 135), but a pre-registered replication on April-to-April windows failed (0.12, p = 0.56, n = 109).
- In Research 4, new product versions (coefficient 0.21, p = 0.06), new chains (0.08, p = 0.18) and unlocks of existing tokens (−0.34, p = 0.12) showed no significant association with annual token returns against ETH.
- In Research 4, tokens with shrinking on-chain supply looked better (issuance coefficient −1.27, p = 0.02, n = 105) and hacked protocols did about 30% worse against ETH (p = 0.02), but the first rests on a few burn tokens, the hack was only a control, and neither survives multiple-testing correction.
- In a supplementary October 2022 to October 2023 window (28 observations), the Research 4 fee growth coefficient was 0.21 against 0.26 in the main windows (one-sided p = 0.058), which is weak and fragile support.

## Study at a glance

| Item | Value |
|---|---|
| Question | Which protocol states and DAO decisions are associated with a DeFi token outperforming ETH over one year |
| Sample | 202 observations of 110 DeFi protocols (38, 69, 95 per window) at stages 1–2, after the non-protocol exclusions of change C2. The on-chain stages 3–4 drop two last-window supply artefacts (Fulcrom and Stargate, circulating supply changing more than fivefold), so `panel_stage3.csv` and `panel_stage4.csv` hold 200 rows (38, 69, 93); 197 are decomposable and 175 enter the main regression |
| Period | 2023-10-01 to 2026-10-01 in three annual windows |
| Unit of returns | Token log return ln(P_end/P_start) minus the same for ETH, in log points; percents are exp(x) − 1 |
| Benchmark or control | ETH; secondary outcome against the category median |
| Data sources | DefiLlama fees, holders revenue, treasury, hacks; CoinGecko CSV prices and market caps; on-chain totalSupply |
| Method | Exact return decomposition; ordinary least squares (OLS) with window fixed effects (FE) and protocol-clustered errors |
| Pre-registration | Four stages frozen with sha256 (afa0248a, 6a479d8d, 092488f3, 4eb716ad); replication and forward test (acdd2646); forward start data (1df6b764). Holder share, ETH beta and hack findings were not pre-registered hypotheses |
| Independent review | Two passes, byte-identical re-run, all must-fix items corrected |
| Main verdict | Fee growth is the only robust association; holder share not replicated; other factors not significant or fragile |

Full report page: https://cp0x.com/blog/what-drives-defi-token-returns-against-eth

## Supplementary window 2022–2023

A supplementary window from 2022-10-01 to 2023-10-01 re-tested the fee growth result (test T1) with 28 observations. The coefficient was 0.21 against 0.26 in the main windows, one-sided p = 0.058, which passes the frozen rule but is fragile (p about 0.11 with HC3 errors; dropping LooksRare, Biswap or Osmosis alone makes it insignificant). The window is not fully blind, because descriptive returns were seen in the survivorship check before it was chosen. Its data, method and review are in folder `07-supplementary-window-2022`; `data/supplementary_window_2022/README.md` points there.

## Files

| Path | Content |
|---|---|
| `README.md` | This file |
| `MANIFEST.sha256` | sha256 of every file in this folder |
| `data/panel.csv` | Main protocol x window panel (stage 1), all entered observations before the C2 exclusions |
| `data/panel_stage2.csv` | Panel plus stage 2 variables (products, chains, treasury, hack) |
| `data/panel_stage3.csv` | Stage 3 main sample with recount flags and Ethereum on-chain issuance |
| `data/panel_stage4.csv` | Stage 4 main sample with wider on-chain issuance, unlock residual and audit class |
| `data/panel_rep.csv` | Shifted-window panel (April to April) for the holder share replication |
| `data/forward_start_2026-10-01.csv` | Frozen start-of-window data for the forward test 2026-10-01 to 2027-10-01; sha256 1df6b7648387fe27de5da0da5247117c0e5df35cc8cd96e1331cbd50e7b0fe00, recorded in `method/METHOD_R4_REPLICATION.sha256` |
| `data/onchain_supply.csv`, `data/onchain_supply_gross.csv`, `data/onchain_supply_evm.csv` | On-chain totalSupply at window dates (Ethereum net of burn addresses, Ethereum gross, other EVM chains) |
| `data/supply_blocks.json`, `data/supply_blocks_evm.json` | Block numbers used for each date and chain |
| `data/token_addresses.csv` | Token contract per group, from DefiLlama |
| `data/stage4_audit_candidates.csv`, `data/stage4_audit.csv` | 20 largest unlock residuals and their manual classification with sources |
| `data/stage4_bridging_check.md` | Per-token check of multi-chain mint and burn (CHANGES C8) |
| `data/lido_peers.csv`, `data/eth_lst_share.csv` | Lido and staking peers (descriptive); Lido share of 90-day fees among the ETH liquid staking products listed in `data/eth_lst_share.csv` (differs from the study 4 series, which splits the DefiLlama Liquid Staking category by base asset and keeps ETH only) |
| `data/candidates.csv` | All DefiLlama fee groups with token mapping and exclusion reason |
| `data/missing_cg.csv`, `data/missing_cg_meta.csv`, `data/missing_cg_fdv.csv` | Survivorship check for candidates without CoinGecko data (CHANGES C10) |
| `data/price_check.csv` | CoinGecko 7-day median prices against DefiLlama point prices |
| `data/runs_summary*.csv` | One row per main or robustness run, per stage |
| `data/results.json`, `data/results_stage2.json`, `data/results_stage3.json`, `data/results_stage3_gross.json`, `data/results_stage4.json`, `data/results_rep.json`, `data/posthoc.json` | Full regression output, as produced by the scripts |
| `data/SOURCES.txt` | Download times and DefiLlama adapter commits |
| `data/raw/fees/`, `data/raw/fees_children/`, `data/raw/peers/` | DefiLlama daily fees and holders revenue JSONs (downloaded 2026-10-06) |
| `data/raw/overview_fees.json`, `data/raw/hacks.json` | DefiLlama fees overview (universe) and hacks list |
| `data/raw/ldo_agent_tx_1.json`, `data/raw/ldo_agent_balance_latest.json`, `data/raw/latest_block.json` | LDO transfers of the Lido Aragon Agent and the reference block (supply check) |
| `data/raw/RAW_NOT_INCLUDED.sha256` | sha256 of raw files not redistributed (CoinGecko CSVs, DefiLlama breakdowns and treasury, protocol lists) |
| `data/supplementary_window_2022/README.md` | Pointer to folder 07-supplementary-window-2022 |
| `method/METHOD_R4.md`, `METHOD_R4_STAGE2.md`, `METHOD_R4_STAGE3.md`, `METHOD_R4_STAGE4.md`, `METHOD_R4_REPLICATION.md` | Frozen methods; each `.sha256` file holds the hash and the UTC freeze time |
| `method/CHANGES_R4.md` | Change log C1 to C13 and post hoc checks |
| `method/REVIEW_R4.md` | Independent review, first and second pass |
| `method/results_notes/` | Internal results notes in Russian: before review, after review, and version 2 (final, identical in content to the final results document) |
| `code/` | Scripts, run order in `code/README.md`, download logs in `code/logs/` |

## Data dictionary

Conventions. Dates are ISO (YYYY-MM-DD). Log changes are natural logs. USD values are nominal. Booleans are `True`/`False`. Empty cells are missing values. Windows W1, W2, W3 are 2023-10-01 to 2024-10-01, 2024-10-01 to 2025-10-01 and 2025-10-01 to 2026-10-01; A1, A2, A3 start on 1 April 2023, 2024 and 2025; F is 2026-10-01 to 2027-10-01.

### data/panel.csv (214 rows) and data/panel_rep.csv (177 rows)

The main analysis drops 12 rows whose `gecko_id` is in the C2 exclusion list (savings-xdai, usdx-money-usdx, crypto-com-chain, near, arbitrum, baby-doge-coin, flock-2, livepeer) and rows with `supply_artefact = True`.

| Column | Type | Unit | Definition |
|---|---|---|---|
| window | string | | W1 to W3 (panel.csv) or A1 to A3 (panel_rep.csv) |
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

### data/panel_stage2.csv (214 rows)

All panel.csv columns plus the following.

| Column | Type | Unit | Definition |
|---|---|---|---|
| new_products, lost_products | int | count | Product versions with fees at the end and none at the start, and the reverse |
| new_chains, lost_chains | int | count | Same rule for chains |
| n_products_start, n_chains_start | int | count | Products and chains with fees at the start |
| T_start, T_end | float | USD | DefiLlama treasury excluding own token |
| treasury_change | float | share of mc_start | (T_end − T_start) / mc_start, only if T_start ≥ 1 million USD |
| hack | int | 0 or 1 | DefiLlama hack record dated inside the window |

### data/panel_stage3.csv (200 rows)

Main-sample rows of panel.csv plus the following.

| Column | Type | Unit | Definition |
|---|---|---|---|
| recount_10, recount_15, recount_25 | bool | | CoinGecko implied-supply level shift above 10%, 15% or 25% while price moved less than 15% (CHANGES C7) |
| s_issue | float | log points | Log change of Ethereum totalSupply minus balances of 0x...dEaD and 0x0 (C9); missing outside the Ethereum sample |

### data/panel_stage4.csv (200 rows)

Main-sample rows of panel.csv plus the following.

| Column | Type | Unit | Definition |
|---|---|---|---|
| s_issue | float | log points | Net on-chain issuance on Ethereum, BSC, Base, OP Mainnet or Polygon |
| supply_chain | string | | Chain used for s_issue |
| u | float | log points | Unlock residual s − s_issue |
| class | string | | Audit class for the 20 largest abs(u): real, recount or unclear |
| u_aud | float | log points | u set to 0 where class is recount |

### data/forward_start_2026-10-01.csv (74 rows)

| Column | Type | Unit | Definition |
|---|---|---|---|
| window, start, end | string, date | | F, 2026-10-01, 2027-10-01 |
| group, slug, name, gecko_id, category | string | | As in panel.csv |
| mc_start, p_start | float | USD | 7-day median market cap and price at 2026-10-01 |
| eth_start | float | USD | ETH 7-day median price at 2026-10-01 |
| fees90_start, fee_days_start | float, int | USD, days | As in panel.csv |
| H_start | float | share | As in panel.csv |
| S_start | float | tokens | mc_start / p_start |
| ln_M_start, ln_mc_start, beta, drawdown_start | float | | As in panel.csv |

### data/onchain_supply.csv and data/onchain_supply_gross.csv (56 rows each)

| Column | Type | Unit | Definition |
|---|---|---|---|
| gecko_id, address | string | | Token and Ethereum contract |
| complete | bool | | All four dates read |
| decimals | float | | ERC-20 decimals |
| TS_{date} | float | tokens | totalSupply at the last block before 00:00 UTC of the date |
| rpc_{date} | string | | RPC endpoint that answered |
| error | string | | Read error, if any |
| BURNED_{date}, NET_{date} | float | tokens | Balances of 0x...dEaD and 0x0, and totalSupply minus them (onchain_supply.csv only) |

### data/onchain_supply_evm.csv (7 rows)

Columns gecko_id, chain, address, and TS, BURNED and NET for each date, defined as above.

### data/lido_peers.csv (31 rows)

| Column | Type | Unit | Definition |
|---|---|---|---|
| window, name, gecko_id | string | | Staking token in a window |
| y, g, m, s, s_issue | float | log points | As in the panels |
| rev90_start, rev90_end | float | USD | 90-day DefiLlama protocol revenue |
| rev_growth_eth | float | log points | Revenue growth minus the ETH log return |
| take_start, take_end | float | share | Revenue over fees (take rate) |
| mc_to_rev_start, mc_to_rev_end | float | ratio | Market cap over annualised revenue |
| H_start | float | share | As in panel.csv |
| mc_start | float | USD | As in panel.csv |

### data/eth_lst_share.csv (4 rows)

| Column | Type | Unit | Definition |
|---|---|---|---|
| date | date | | 2023-10-01 to 2026-10-01 |
| lido_share | float | share | Lido share of 90-day fees among the ETH liquid staking products listed in this file |
| share_{product} | float | share | Share of each listed product |

### data/candidates.csv (2,314 rows)

| Column | Type | Unit | Definition |
|---|---|---|---|
| group, slug, name | string | | DefiLlama group |
| category | string | | Category of the child with the largest all-time fees |
| gecko_id | string | | Token id, empty if none |
| n_children | int | count | Child protocols in the group |
| fees_all_time | float | USD | All-time fees in the overview |
| excluded | string | | Empty if kept; otherwise no_gecko_id, excluded_category or several_gecko_ids |

### data/token_addresses.csv (95 rows)

Columns group, gecko_id, address and chain, the contract used for on-chain supply.

### data/stage4_audit_candidates.csv and data/stage4_audit.csv (20 rows each)

| Column | Type | Unit | Definition |
|---|---|---|---|
| window, start, end, name, gecko_id, supply_chain | string | | Observation (audit_candidates) |
| cg_supply_change_pct, onchain_change_pct | float | percent | CoinGecko and on-chain supply change in the window |
| class | string | | real, recount or unclear (audit) |
| note, sources | string | | Reason and public sources (audit) |

### data/missing_cg.csv (26 rows), data/missing_cg_meta.csv (25 rows), data/missing_cg_fdv.csv (25 rows)

| Column | Type | Unit | Definition |
|---|---|---|---|
| gecko_id, slug, name, category, address, chain | string | | Candidate without a CoinGecko CSV and its contract |
| supply_latest | float | tokens | Current on-chain totalSupply |
| p_{date} | float | USD | DefiLlama point price at a window start (2-day search width) |
| fdv_{date} | float | USD | p times supply_latest, an upper bound on market cap |

### data/price_check.csv (40 rows)

Columns window, name, date, coingecko_7d_median (USD), defillama_point (USD) and ratio (CoinGecko over DefiLlama).

### data/runs_summary*.csv

One row per run (`run` = main or a robustness name). Columns hold sample sizes (`n...`), coefficients in log points per unit of the regressor, p-values (`p_...` or `..._p`), variance shares (`share_...`), the R-squared gain from holder share (`dR2_H`) and the hypothesis verdicts as booleans. `runs_summary_stage3_gross.csv` uses the frozen gross totalSupply definition from before CHANGES C9.

## Reproduction

See `code/README.md`. In short, copy `code/*.py` and `data/` into one working directory, link `raw` to `data/raw`, re-download CoinGecko CSVs with `fetch_prices.py` and DefiLlama breakdowns and treasury with `fetch_stage2.py`, then run the scripts in the listed order. With only the files in this folder, `analyze.py`, `analyze_stage2.py`, `analyze_stage4.py run` and `analyze_rep.py` reproduce `results.json`, `results_stage2.json`, `results_stage4.json` and `results_rep.json` byte for byte. `analyze_stage3.py` and `posthoc.py` also need the CoinGecko CSVs.

## License

Data and text are licensed CC BY 4.0. Code is licensed MIT. CoinGecko raw exports are not redistributed because their terms restrict it. Publisher cp0x (https://cp0x.com), version 1.0, published 2026-10-08.

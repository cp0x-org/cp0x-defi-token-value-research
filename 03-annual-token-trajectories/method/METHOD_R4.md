# Research 4. Method (frozen before any outcome is computed)

Frozen 2026-10-06. Any change after this point is logged in CHANGES_R4.md with a reason, and the frozen result is reported alongside.

## Question
Which protocol states and DAO decisions are associated with a token outperforming ETH over a one-year horizon.

## Unit of observation
Protocol x window. Three non-overlapping windows:
- W1: 2023-10-01 to 2024-10-01
- W2: 2024-10-01 to 2025-10-01
- W3: 2025-10-01 to 2026-10-01

## Universe
1. Candidates: every entry of DefiLlama api.llama.fi/overview/fees, grouped by parentProtocol (entries without a parent form their own group).
2. Token: gecko_id of the parent (api.llama.fi/lite/protocols2 parentProtocols), else the unique gecko_id among the group's children (api.llama.fi/protocols). Groups with no gecko_id or several distinct gecko_ids are excluded.
3. Category: category of the child with the largest all-time fees. Excluded categories: Chain, CEX, Gaming, Luck Games, Physical TCG, Gamified Mining, SoFi, AI Agents, DePIN, Domains, Wallets, Developer Tools, Services, Payments, Privacy, Block Builders, DAO Service Provider, Telegram Bot, Token Locker. Everything else is DeFi for this study.
4. Per window, a group enters if (a) market cap at window start >= $50M, (b) fee data exist on at least 80 of the 90 days before window start and the 90-day fee sum is > 0.
5. Survivorship: entry depends only on the window start. If the price series ends inside the window, the last available price is used and the observation is flagged delisted. Such observations stay in the return analysis.

## Measurement
- Price P and market cap MC at a date: median of the 7 daily CoinGecko values ending at that date (CoinGecko public CSV export). ETH price the same way.
- Circulating supply S = MC / P.
- Fees F at a date: sum of DefiLlama daily fees over the 90 days ending at that date (dimension-adapters version as served on 2026-10-06; adapter commit recorded in data/SOURCES.txt).
- Holder share H at a date: 90-day holders revenue / 90-day fees, clipped to [0, 1]. If DefiLlama has no holders-revenue series for the protocol, H is missing.
- Multiple M = MC / F.

## Outcome
Primary: y = ln(P_end/P_start) - ln(ETH_end/ETH_start).
Secondary: token log return minus the median log return of its category in the same window (categories with fewer than 5 observations in the window pooled into "other").

## Decomposition (identity, computed for every observation with F_start > 0 and F_end > 0)
y = g + m - s, where
- g = ln(F_end/F_start) - ln(ETH_end/ETH_start)   (business growth in ETH terms)
- m = ln(M_end/M_start)                            (re-rating)
- s = ln(S_end/S_start)                            (dilution)
Variance shares: share_k = cov(k, y) / var(y) for k in {g, m, -s}, after demeaning by window. The three shares sum to 1. Reported pooled and per window.

## Hypotheses
- H1. Business growth g has the largest variance share of the three components.
- H2. In regression R1 the coefficient on dilution s is negative with p < 0.05.
- H3. The holder share adds little: adding H_start and the change in H to R1 raises R-squared by less than 0.02.
- H4. In regression R1 the coefficient on ln M_start is negative with p < 0.05.

## Regressions
OLS, window fixed effects, standard errors clustered by protocol.
- R1: y ~ g + s + ln M_start + ln MC_start + beta + drawdown_start + category dummies (categories with >= 10 observations overall, others pooled) + window FE. Sample: observations with defined g.
- R1h: R1 + H_start + (H_end - H_start). Sample: R1 sample with non-missing H. R1 is re-estimated on the same sample to compute the R-squared gain for H3.
- R2 (decisions only, no concurrent business growth): y ~ s + H_start + (H_end - H_start) + ln M_start + ln MC_start + beta + drawdown_start + category dummies + window FE.
- beta: OLS slope of daily token log returns on daily ETH log returns over the 365 days before window start, at least 250 paired days, else missing (observation dropped from regressions).
- drawdown_start: ln(P_start / max daily price over the 365 days before start).
- Continuous regressors and y are winsorized at the 2.5 and 97.5 percentiles within each window.

## Data-quality rule
Observations with |s| > ln(5) are presumed to be a circulating-supply artefact. They are excluded from the decomposition and regressions in the main run, listed in a separate table, and included in a robustness run.

## Robustness (reported, not used to accept or reject hypotheses)
No winsorization; including |s| > ln(5); H missing set to 0; dropping each window in turn; secondary outcome; excluding the largest category.

## Out of scope for this freeze
Treasury spending and new-product launches are collected later, as a stage-2 extension with its own freeze. Value-return mechanism type from Research 2 and 3 enters only through the holder share in this stage.

## Interpretation limits
Associations, not causal effects. g is concurrent with y, so R1 is descriptive. R2 uses only variables the DAO controls or that are known at the window start.

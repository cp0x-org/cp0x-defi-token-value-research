# Research 5. Market, competitive position, monetisation and valuation of DeFi tokens (frozen before computing)

Frozen 2026-10-07. Builds on Research 4 (frozen archive Research4_frozen_20261006) for the sample, prices, market caps and supply.

## Question and stages
Stage 1 (decomposition): what the past one-year return of a token against ETH was made of. Stage 2 (valuation): what the market paid for at the start of a period. Stage 3 (prediction): whether being cheap or expensive relative to fundamentals at the start predicted the next year's return. The stages answer different questions and are not mixed.

## Sample and periods
Main periods: October to October 2023-24, 2024-25, 2025-26 (W1-W3). Replication periods: April to April 2023-24, 2024-25, 2025-26 (A1-A3). Observations are those of the Research 4 panels (data/panel.csv and data/panel_rep.csv of the replication package): same entry rule ($50M market cap at period start, fee data on at least 80 of 90 days, positive fees), same token exclusions (CHANGES C2), supply-artefact rule, price, market cap and CoinGecko supply measurement, and C11. y is the log return of the token against ETH.

## Data
- All fee quantities come from one source, the DefiLlama daily fee breakdown by product (api.llama.fi/overview/fees with totalDataChartBreakdown), downloaded once and stored (raw/overview_fees_breakdown.json). Product metadata (category, chains, parent group) come from the same download's protocol list. A group's fees F are the sum of its products.
- Revenue R comes from DefiLlama dailyRevenue per group (raw/rev/), with children summed where the parent has no series (C1 rule).
- Sums are over 90 days ending at the date.

## Categories
- The main category of a group is the category of its product with the largest all-time fees (as in Research 4).
- Liquid Staking, Liquid Restaking and Restaking are split by base asset; every other category is used as DefiLlama defines it. The base asset of a product in those three categories is the native asset of its first listed chain: Ethereum and Ethereum L2s (Arbitrum, Base, OP Mainnet, Linea, Scroll, zkSync Era, Mantle, Blast, Unichain) map to ETH; Solana to SOL; BSC to BNB; Avalanche to AVAX; Sui to SUI; Aptos to APT; Polygon to POL; Cosmos-family chains to their own chain name; anything else to "other". The resulting mapping is saved before outcomes are computed (data/category_map.csv).
- Category snapshot is the DefiLlama classification as downloaded on 2026-10-07; historical categories are not published (limitation).

## Definitions
- C: total 90-day fees of all products in the category key (all DefiLlama products, with or without a token, including products that appear during the period).
- F_main: the group's fees from its products in its main category key. share = F_main / C. diversification factor D = F / F_main.
- take = R / F. Revenue variant is defined only when R >= 1% of F at both ends of the period.
- M_R = MC / (R x 365/90), M_F = MC / (F x 365/90). S = circulating supply (CoinGecko, MC / P).

## Stage 1. Exact decomposition
Revenue variant: y = dln(C/ETH) + dln(share) + dln(D) + dln(take) + dln(M_R) - dln(S).
Fee variant (all observations): y = dln(C/ETH) + dln(share) + dln(D) + dln(M_F) - dln(S).
Both are identities; the maximum identity error is reported. Variance shares cov(k, y)/var(y), demeaned by period, are reported descriptively only.

H1. The market rewards gains against competitors more than growth of the whole category. Regression on main periods, fee-variant sample: y ~ dln(C/ETH) + dln(share) + ln MC_start + beta + drawdown_start + period FE (category FE are not used because they would absorb most of dln(C/ETH)). H1 holds if the coefficient on dln(share) exceeds the coefficient on dln(C/ETH), one-sided test of the difference, p < 0.05. Standard errors two-way clustered by protocol and by category x period (Cameron, Gelbach and Miller).

## Stage 2. What the market paid for at the start
All variables are measured at the period start; nothing from the period end enters stages 2 and 3.
Sample: revenue-variant observations (R >= 1% of F at the start), minus the valuation exclusions below.
Model V: ln MC = a ln F + b ln take + c prior_share_growth + category FE + period FE, where prior_share_growth = dln(share) over the 365 days before the start (missing if share is not defined a year earlier; such observations are dropped from model V).
H2. At equal fee scale the market pays more for higher monetisation: b > 0, p < 0.05, standard errors clustered by protocol. (Equivalent to ln M_F on ln F and ln take with a free coefficient on ln F; ln MC is not a regressor, and the coefficient on ln F is not forced to 1, which avoids a shared-denominator bias.) b = 0 means the market ignores monetisation; b = 1 with a = 1 means market cap is proportional to revenue.

Valuation exclusions (revenue not comparable, decided from the revenue check of 2026-10-07): ve(3,3) exchanges and RFQ venues whose revenue equals voter or protocol take of all fees (groups aerodrome, velodrome, thena, velo-finance, tokenlon), World Liberty Financial, Lista DAO, ApeX. They stay in stage 1 fee variant.

## Stage 3. Did relative cheapness predict the next year
The valuation residual of each observation is ln MC minus the fitted value of model V estimated on all observations of the same period type (main or replication), using only start-of-period variables. Positive residual = expensive relative to fundamentals.
H3. Cheap tokens later outperform expensive ones: y ~ residual + beta + drawdown_start + category FE + period FE, coefficient on residual < 0, p < 0.05, standard errors clustered by protocol.

## Exploratory, not a hypothesis
Value of new on-chain issuance during the year before the start, divided by revenue, for tokens with on-chain supply (Research 4 stage 3/4 sample), added to model V and to the H3 regression. Reported as exploratory.

## Common rules
- Continuous variables winsorised at 2.5/97.5 within period.
- Holm correction across the three p-values of H1-H3 on main periods.
- A hypothesis is recognised only if it holds on main periods after Holm and the same coefficient (H1: the difference) has the same sign with p < 0.10 on replication periods.
- Robustness (reported, not used for verdicts): no winsorisation; dropping each period; dropping the largest category; clustering by protocol only (H1) and two-way (H2, H3); without Curve (stages 2-3); category key without base-asset split.
- Results are described as associations, not causal effects.

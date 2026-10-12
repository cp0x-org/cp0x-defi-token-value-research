# Additional window October 2022 to October 2023 (W0) for Research 4 and 5. Frozen before computing

Frozen 2026-10-08. Purpose: check whether three main findings of Research 4 and 5 hold in a different market regime (late 2022 bear market to 2023 recovery). This is a supplementary check. It cannot change the verdicts of Research 4 and 5; it adds to or qualifies them.

## Feasibility and survivorship (done before this method, check_2022.csv)
At 2022-10-01, 55 tokens in the DefiLlama universe (current plus dead protocols with a gecko id) had a market cap of at least $50M. 29 meet the fee-data entry rule, 24 are alive but DefiLlama's fee series starts later, 2 are dead (Hyphen, RenVM). Median return against ETH over the following year was −0.66 (log) for those entering, −0.71 for alive-but-uncovered and −0.92 for dead. The April 2022 window was rejected because 10 dead tokens (Terra ecosystem and others) and 37 uncovered tokens did much worse than entrants.

## Window and sample
W0 = 2022-10-01 to 2023-10-01. Entry rules, measurement and exclusions exactly as in Research 4 (METHOD_R4.md with CHANGES C1, C2, C9, C11, C12): Research 4 candidate groups, market cap at least $50M at start (7-day median, CoinGecko), fees on at least 80 of 90 days before start and positive, children summed where the parent has no series (C1), the C2 token exclusions, the supply-artefact rule. The code is build_panel_rep.py of the Research 4 replication with only the window changed. Research 5 variables (category key with base-asset split, category fees, take rate, prior share growth) are built with the Research 5 code (build_r5.py logic) on W0, with revenue from DefiLlama dailyRevenue downloaded for the new groups.

## Tests (one window, so no window fixed effects; one observation per protocol, so heteroskedasticity-robust errors equal protocol clustering)
T1 (Research 4, fee growth). Regression R1 of Research 4: y ~ g + s + ln_M_start + ln_mc_start + beta + drawdown_start + category FE (categories with fewer than 10 observations pooled, as in Research 4), winsorised 2.5/97.5. Consistent with Research 4 if the coefficient on g is positive with one-sided p < 0.10.

T2 (Research 5, no premium for monetisation). Model V of Research 5 on W0: ln MC = a ln F + b ln take + c prior_share_growth + category FE, Research 5 valuation exclusions. Consistent with Research 5 if b is not significantly positive (one-sided p >= 0.05). Whether the 95% interval excludes b = 1 is reported.

T3 (Research 5, cheapness does not predict). Residual of model V on W0, then y ~ residual + beta + drawdown_start + category FE. Consistent with Research 5 if the coefficient on the residual is not significantly negative (one-sided p >= 0.05).

If the sample for T2 or T3 falls below 15 observations, the test is reported as not evaluable.

## Descriptive
Share of tokens beating ETH and the median return against ETH; Research 4 variance shares of g, m and −s; Research 5 median change in category share and share of observations losing share.

## Reporting
Results are reported next to the main periods as a check in a different regime, with the small sample stated. No other specification is used for conclusions. Any deviation is logged in CHANGES_W0.md.

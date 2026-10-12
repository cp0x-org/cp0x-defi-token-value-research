# Research 5. Changes after the method freeze

All changes below were made after the first run of the frozen method and after the independent review (REVIEW_R5.md). The first run's outputs are kept as data/results_r5_frozen_run.json and data/panel_r5_frozen_run.csv. No change altered a verdict: H1, H2 and H3 are not recognised in either run.

Timing note: the raw fee breakdown was downloaded 12 seconds after the freeze and the build and analysis scripts were written 1-2 minutes after it.

## R1. Fees for take rate and multiples from the same source as revenue (revised after the second review pass)
The frozen method takes all fee quantities from the DefiLlama product breakdown. About 500 products with positive fees are absent from that breakdown, so for some groups F covered fewer products than revenue R (WOOFi take rate up to 2.38, Defi App with F = 0). Group fees F (used in take, M_F, M_R and the diversification factor D) now come from the group summary series, the same source family as R; F_main and the category totals C stay on the breakdown. The identity stays exact.
Where the two sources are both positive and disagree by more than a factor of 2, the observation is treated as a data conflict. For stages 2 and 3 only the start date is checked, so nothing from the period end decides the sample (3 main observations: WOOFi W2, ZORA W3, Orderly W3). For stage 1 both dates are checked (5 main observations: WOOFi W1-W3, ZORA W3, Orderly W3). An earlier version of this rule also dropped observations whose fees fell to zero by the end, which used end-of-period information and removed losers; the second review pass caught it and it was replaced before the write-up.
## R2. Valuation exclusions by explicit group id (2026-10-07T04:08:05Z)
The first run matched excluded groups partly by name substring, which wrongly excluded Ethena ("thena") and relied on the name match for three groups whose ids were mistyped. Exclusions now use exact group ids: parent#aerodrome, parent#velodrome, parent#thena, id#4989 (Velo Finance), parent#tokenlon, id#7571 (World Liberty Financial), parent#lista-dao, parent#apex-protocol.

## R3. Robustness completed (2026-10-07T04:08:05Z)
The frozen robustness "category key without base-asset split" was run only for H1; it now covers H2 and H3. A post-hoc robustness drops observations in "|other" base-asset keys and in categories with a single sampled protocol.

## R4. Missing revenue
25 observations have no revenue at the start because DefiLlama has no revenue series for the group (for example Aster, Orderly, Ribbon, Saros, whose child series are also absent) or the series starts later (Blur from March 2026). Under the frozen rule they fail the 1% revenue threshold and enter only the fee variant of stage 1. Recorded here because the frozen text did not mention missing revenue explicitly.

## R5. Exploratory issuance analysis not done
The frozen exploratory variable (value of new issuance in the year before the start, divided by revenue) needs on-chain supply one year before each start, back to October 2022, which was not collected. It is not reported.

## Clarifications
- Replication rule "same sign with p < 0.10" is applied with the one-sided p-value in the hypothesised direction, consistent with the main tests. H2 replication passes on this reading (one-sided p 0.054) and would fail on the two-sided one (0.107); H2 is not recognised either way because it fails on main periods.
- The main category of a group is chosen from all-time fees up to October 2026, which is a mild look-ahead for stages 2-3 (category controls and prior share growth). Recorded as a limitation.
- Liquid-staking products are mapped by first listed chain; for multi-chain products this is arbitrary (Ankr maps to Fantom, hence "Liquid Staking|other"; Stride to Osmosis). The post-hoc robustness in R3 drops such keys.


Текстовая правка 8 октября 2026 (после фактчека публичного текста). В разделе стадии 2 пересчёт коэффициента в проценты был неточен: коэффициент 0,37, а не около 0,4, и 2^0,37 даёт около +29%, а не +35%. Исправлено на «примерно на 30%». Расчёты не менялись.

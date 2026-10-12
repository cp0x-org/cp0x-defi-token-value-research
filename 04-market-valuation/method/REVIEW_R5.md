# Review of Research 5 (independent, 2026-10-07)

Scope: METHOD_R5.md, build_r5.py, analyze_r5.py, data/*, revenue notes. No existing file was modified. Checks ran in /tmp/r5review.

## Reproducibility and freeze
- The SHA-256 of METHOD_R5.md is 5d5a0ca9...f0b9. It matches METHOD_R5.sha256, which records the freeze at 2026-10-07T03:56:53Z.
- Timing. raw/overview_fees_breakdown.json was written 12 s after the freeze, and build_r5.py and analyze_r5.py were written 1 to 2 min after it. The results JSON was written at 10:59:46 local time. The order is acceptable, but the write-up should say that the download came after the freeze.
- I re-ran build_r5.py and analyze_r5.py in the copy. category_map.csv, panel_r5.csv and results_r5.json are byte-identical to the originals. The maximum identity error is 1.8e-15 for both variants.
- Sample counts reconcile with Research 4. The main panel has 214 rows, minus 12 removed by C2 and 2 supply artefacts, which gives 200. The replication panel has 177 rows, minus 8, which gives 169. Every Research 4 group is found in the category map.
- Product names match fully. All 2,320 breakdown names are in the protocol list and no name is duplicated. The 90-day windows match Research 4: the median ratio of F0 to fees90_start is exactly 1.

## MUST-FIX

1. **The valuation exclusion matches Ethena by mistake.** The substring "thena" occurs inside "ethena", so Ethena (parent#ethena) is excluded from stages 2 and 3 in W2, W3 and A3. Three group ids in VAL_EXCL are also wrong:
   - ApeX is parent#apex-protocol.
   - Velo Finance is id#4989.
   - WLF is id#7571.

   Those three are excluded today only because the name substring catches them. Use an explicit set of group ids and drop the substring matching.
   - Effect after the fix: on main periods, H2 b = 0.002 (n = 121) and H3 b = 0.118 (n = 118, p one-sided 0.858). Replication results do not change, and no verdict changes.
2. **The exploratory issuance analysis is missing.** The method requires new issuance value divided by revenue, added to model V and to the H3 regression. The code does not implement it. Either implement it or record its omission in a CHANGES note.
3. **A required robustness run is incomplete.** The method lists "category key without base-asset split" as a robustness check in general terms, but the code runs it only for H1. The split also changes the category FE and prior_share_growth in H2 and H3, so those runs are missing.
4. **Missing revenue is treated as failing the revenue threshold, and this is undocumented.** There are 25 observations where R0 is NaN, and they fall silently out of the revenue variant and stages 2 and 3. They come from two sources:
   - Fetch failures. The raw/rev files for astherus, orderly-network, saros, ribbon-finance, defi-swap and stables-labs-usdx are DefiLlama "not found" text, and so are their child__ files. This includes Aster W3 with F0 of $153M.
   - Series that start late or are missing. Blur's revenue series starts in 2026-03, and Bancor, ShibaSwap, Maverick and ApeX have no data before the window.

   The 1% rule is about low revenue, not missing data. Also, the C1 child-summing rule is not in build_r5.py. It depends on pre-aggregated raw files such as ether-fi.json, and the fallback failed for the groups listed above. At minimum, list these observations and the reason for each in the write-up.
5. **Fee and revenue sources do not cover the same products. Document this and decide how to handle it.** In this download, 503 listed products with positive all-time fees have no breakdown series. These are mostly products DefiLlama treats as double-counted (Interface and others). Products in the sample affected include WooFi Pro Perps, Defi App Perps, Hyperliquid HLP, pump.fun Mobile App, Sushi Perps/Launchpad, THENA PERPS and lisAster. Revenue comes from per-protocol endpoints that do include them. The consequences are:
   - Defi App W3 has F = 0 and drops out completely. Its only product, which is also its main key, has no series.
   - WOOFi's F is 49 to 75% of the Research 4 figure, and its take is above 1 in five observations (up to 2.38).
   - C is understated for Interface and Launchpad keys.

## Should-consider

**Data and keys**
- **Large gaps between F0 and the Research 4 fees90_start.** ZORA W3 is 5.67M against 2,949 (×1,921), because the breakdown includes ZORA Coins. Orderly W3 is 1.20M against 582 (×2,062). WOOFi is off by 0.40 to 0.88 in every window, and Sushi W3 at the end is 0.76. Defi App is 0. Research 4 made the entry decisions on its own fee figures, so say this.
- **Some category keys are meaningless.**
  - Ankr's first chain is Fantom, so it lands in "Liquid Staking|other", together with Kinetiq (HYPE), TON, Bifrost, Berachain and Sonic LSTs. C grows from 1.2M to 18M, and Ankr's share goes from 0.74 to 0.13 to 0.015 purely because unrelated chains entered.
  - Stride's first chain is Osmosis, giving the key "Liquid Staking|Osmosis" (Stride plus MilkyWay).
  - Singleton keys give share ≡ 1 at both ends in 13 observations: Benqi|AVAX, EigenCloud, Solayer, Nexus Mutual, Threshold and Layer3. For these, dln share = 0 mechanically.
  - Removing all of these leaves the conclusions unchanged: H1 main diff 0.060 (p = 0.24), and H3 is unchanged. Report it as a limitation.
- **The main key uses look-ahead.** It is chosen from all-time fees up to October 2026, and it drives the category FE and prior_share_growth in stages 2 and 3. This conflicts in spirit with "nothing from period end". KyberSwap in W1 and A1 and Origin in A1 have Fmain0 = 0 because their main fees at the start were in another key. Lombard's Fmain0/F0 is 0.04. A robustness run that sets the main key from fees in the 365 days before the start would answer this.
- **Stage 1 loses the worst outcomes.** Observations drop because ln(0) is undefined:
  - F1 = 0: Ribbon W2, NFPrompt W2, LooksRare A1, Biswap A1, Abracadabra A2.
  - Main product at 0 at the end, likely a product migration: Synthetix W3, Drift W3, Avalon A3.
  - Fmain0 = 0: KyberSwap W1 and A1, Origin A1.

  H1 additionally loses 23 main observations without beta (less than 250 days of history). Report the funnel: 200, then 193 fee-variant, then 172 in H1. For model V, 167 pass the revenue rule, minus exclusions, minus 47 without prior share, which gives 120.
- **Take = 100% by construction for many protocols that are not excluded.** These include Synthetix, dYdX, Stargate, Synapse, Metaplex, KyberSwap, Ondo, Olympus, deBridge, Hyperlane and Definitive. This is the same non-comparability the ve(3,3) rule targets. The frozen list stays as it is, but add this as a limitation or a robustness run.

**Tests and code**
- **The replication rule is ambiguous.** The code applies "p < 0.10" to the one-sided p. H2 replication has a one-sided p of 0.0501 and a two-sided p of 0.1001, so the flag is True under the one-sided reading and False under the two-sided one. It does not change the verdict, but fix the reading before the write-up.
- **Model V has singleton category cells.** Nine of 27 categories in the main periods (6 of 21 in replication) have one observation. Their residual is exactly 0, and they add n to H3 without adding information. The H3 standard errors also ignore that the residual is a generated regressor.
- **Minor issues.**
  - start−365 is off by one day across 29 February 2024.
  - The docstring says data/runs_r5.csv is written, but it is not.
  - The maximum identity error is printed but not saved to the results JSON.
  - rev_variant is True for Defi App even though F = 0. This is harmless.
  - p-values use the normal distribution rather than t(G−1). There are 68 protocol clusters in main.
  - The CGM two-way formula (V1 + V2 − V12 on the intersection, with eigenvalue clipping) is correct.
  - The Holm step-down and the direction of the one-sided tests are correct.

## Interpretation risks a referee will raise
- **H1 (null) has low power.** se(diff) is 0.083, so the minimum detectable effect at 80% power is about 0.21 (one-sided 5%), or about 0.25 at the Holm level. dln(C/ETH) varies only across category × period cells. Both coefficients are about 0.2, against 1 in the identity, which means multiples absorbed most fee changes. The variance shares (dln share 1.23, dln C 0.01) are descriptive and must not be read as a test of H1.
- **H2 (null) is informative rather than empty.** b = 0.00 with se 0.19, so the 95% CI is roughly −0.38 to 0.38. b = 1 is rejected (z = −5.1 on main, −4.0 on replication).

  The coefficient a on ln F is 0.37 (se 0.064), far below 1 (z = −9.9). Possible reasons:
  - Truncation of the dependent variable. Entry requires MC of at least $50M, and min ln MC is 17.76 against a cutoff of 17.73, so the slope is attenuated.
  - Noise in 90-day fees.
  - F includes supply-side fees that never reach the token.
  - The category FE remove scale differences between categories.

  Since ln R = ln F + ln take, a = 0.37 together with b ≈ 0 means the market priced gross fees with an elasticity of about 0.37 and assigned no premium to the share retained. Say this explicitly. Do not report a = 0.37 as "the value of fees" in a structural sense.
- **H3 (null on main, significant with the opposite sign on replication).** On replication b = +0.30 (two-sided p = 0.004). Tokens that were expensive relative to fundamentals outperformed. The effect is concentrated in A1: with model V refit for A1 alone, n = 19 and b = 1.07. A2 gives 0.28 and A3 gives 0.05. Main periods are also positive (0.12), and dropping W2 gives 0.34 (p = 0.03).

  The correct statement is that there is no evidence cheapness predicted outperformance, and if anything the reverse held. Likely explanations are momentum, or the residual capturing unmeasured growth or quality. Report two-sided p-values next to the one-sided ones. Do not describe this as "H3 not confirmed" alone.
- **The samples are small.** Model V uses 120 main and 101 replication observations, from 68 and 57 protocols, with W1 and A1 under 40 observations each. Single periods (drop_Wk) move H3 from 0.01 to 0.34. All results are associations within a $50M+, survivor-weighted universe that uses a 2026 category snapshot.

# Second pass (2026-10-07)

I worked in a fresh copy made with `cp -rL` (/tmp/r5review2). No existing file was edited. The hash of METHOD_R5.md is unchanged.

## Confirmations
- **Reproducibility.** build_r5.py and analyze_r5.py reproduce category_map.csv, panel_r5.csv and results_r5.json byte for byte. The maximum identity error is 1.8e-15.
- **R2 is correct.** Exclusions use exact group ids, Ethena is back in, and 13 main observations are excluded.
- **R3 is correct.**
  - The no-split run now covers H2 and H3, and its prior_share_growth is rebuilt from the no-split columns (Fmain_nsp, C_nsp).
  - The post-hoc run drops "|other" keys and categories with a single sampled protocol.
- **R1 is implemented as described.**
  - F comes from the summary series, while F_main and C stay on the breakdown.
  - The identity stays exact, and D ≥ 1 in every kept observation.
  - The 11 excluded observations are exactly those listed.
- **R4 and R5 match the code.** R4 documents the missing revenue, and R5 records that the issuance analysis was not done.
- **Numbers in INTERIM that check out against results_r5.json and panel_r5.csv:**
  - Sample sizes: 192, 166, 117, ~100–120.
  - H1: 0.20, 0.16, difference 0.04, standard error 0.08, p 0.32; negative on replication.
  - H2: −0.10, CI −0.46 to 0.26; replication 0.28 with p 0.047.
  - Coefficient on ln F about 0.4. Doubling fees gives 2^0.427 = +34.5%, so "about 35%" is right.
  - H3: 0.10 with CI −0.14 to 0.35; replication 0.28 with two-sided p 0.006.
  - Post-hoc H1: 0.18, two-sided p 0.10.
  - No pre-specified robustness run is significant in the predicted direction.
  - Table medians: +49/−47, +72/−43, +7/−30.
  - Lido: share 89/84/64/70%. W1: y −50%, C +0%, share −6%, M_R −42%. W2: C −7%, M_R −21%. W3: share +10%, take +27%, C −30%, M_R −38%.

## Problems
1. **R1's exclusion uses end-of-period data and is described wrongly (must-fix).** The rule removes an observation from all stages if either source has zero fees, or the two sources differ by more than ×2, at the start or at the end. Two consequences:
   - Five of the 11 (Ribbon W2, NFPrompt W2, LooksRare A1, Biswap A1, Abracadabra A2) are not source conflicts. Both sources agree that F1 = 0, meaning the protocol died.
   - All 11 have negative y (−0.13 to −1.87). Seven of them (WOOFi ×3, NFPrompt, LooksRare, Biswap, Abracadabra) would otherwise be in the H3 sample.

   Removing them from stages 2 and 3 on the basis of end-of-period fees breaks the frozen rule that "nothing from period end enters stages 2 and 3", and it drops losers. Fix:
   - Apply the conflict test only at the start date for stages 2 and 3.
   - Use start and end for stage 1 only, and only for genuine disagreement (both sources positive).
   - My check of the start-only version leaves four exclusions (WOOFi W2, ZORA W3, Orderly W3, Defi App W3) and gives:
     - H2 main −0.03 (n 120); replication 0.28 with one-sided p **0.054**, so the replication flag for H2 flips to False.
     - H3 main 0.128 (n 117); replication 0.294 with two-sided p 0.004.
   - No verdict changes, but update the CHANGES clarification that says "H2 replication passes (0.047)".

   The INTERIM limitation "11 observations where the two fee downloads differ by more than ×2" is inaccurate. So is the CHANGES R1 text "data conflicts".
2. **The INTERIM claim that all variables are measured at the start is false (must-fix).** "Все переменные взяты на дату начала, без данных из конца периода" (stage 2) cannot stand while problem 1 is unresolved. It should also point to the main-key look-ahead that is already listed under limitations.
3. **The INTERIM says the A1 period drives the H3 reversal, which is wrong (must-fix).** "держится в основном на первом апрельском периоде" is not supported. Dropping A1 gives b = 0.22 with two-sided p 0.04. Dropping A2 gives 0.21 (p 0.17), and dropping A3 gives 0.34 (p 0.09). The reversal is spread across periods, which is stronger evidence against H3, not weaker.
4. **The INTERIM's claim about category growth contradicts its own table.** "Комиссии категории росли быстрее ETH в двух периодах из трёх" does not match the table, where the per-observation medians are positive in all three periods (+49/+72/+7%). The claim holds only for medians over distinct categories (+5%, +95%, −18%). Pick one basis and state it.
5. **The share-loss column uses a different denominator from the medians.** It counts all rows (81/74/65%), while the medians use only observations where d_share is defined (83/74/67%). Use one denominator.
6. **Overclaiming that remains in INTERIM:**
   - "все они исправлены". Not true: R5 was not done, R4 is documented only, and R1 changes a frozen definition.
   - "разницы между ними нет" (H1). Say "не обнаружена": the smallest detectable difference is about 0.2.
   - "рост забирали новые участники". C also contains incumbents without tokens, and the study does not identify entrants.
   - "повышение take rate или включение fee switch ... не вознаграждалось". H2 is a cross-sectional association in levels at the start. It does not test a change in take within a protocol or a fee-switch event.
   - Lido W3 "take rate +27%". The take rate moves from 4.87% to 6.21% (A3: 4.93% to 6.20%). Check this is not a change in DefiLlama methodology before calling it an improvement. Also, "общая переоценка" is Lido's own M_R, not a market-wide repricing.

# Independent review of Research 6 (case studies of DAO resource allocation)

Reviewed 2026-10-07. No existing file was modified. Scratch recomputations are in /tmp/claude-0/review_r6/ (`recompute.py`, `scale.py`, `treas.py`, `cov.py`, `orca.py`).

## Bottom line

The decision tables, the freeze and the join are sound. I found no arithmetic error in 75 materiality figures and 21 line-item tests, the frozen hashes still match, and my independent recomputation reproduces every primary 12m number I tried to 4 decimals.

The weak point is the step from data to the report's second headline, "no pattern meets the rule". It depends on two choices that are written down nowhere before the join: what counts as "one type" of decision, and whether the rule counts decisions or DAOs. Under the narrowest reading (line item "incentives", per decision) the report is right: 3 negative of 5 is 60%, below 2/3. Under the equally literal reading "class A, same goal", 7 of 10 observable usage-growth decisions in 4 DAOs have a negative 12m sign, which does meet the rule. One borderline goal_map call (Sky Integration Boost) also flips the incentives subset to 4 of 6. In addition, a large part of the negative signs for Uniswap and Sky comes from DefiLlama adding DEX and CDP adapters during the windows, which the method itself lists as an alternative explanation. These points must be in the report before it is published. They do not support "incentives don't work" either. They mean the honest statement is "there is a fragile negative candidate, and it is largely explained by data coverage and by one protocol".

The "Lido spending is about equal to revenue" remark holds as an order of magnitude (1.07 in 2024, 1.19 in 2025), but the text should give the two ratios and the revenue definition, because in 2025 spending exceeded revenue by about a fifth.

## 0. Integrity and freezing order

- `sha256(METHOD_R6.md)` = b1143c78…b551a, which matches `METHOD_R6.sha256`. Frozen 2026-10-07T13:55:26Z (20:55:26 local). The draft is older (20:52).
- All nine hashes in `decisions/all_frozen.sha256` (written 15:06:47Z) still match the four decision tables, the four card inputs and `goal_map.csv`. The Lido hashes in `lido_frozen.sha256` (14:17:04Z) still match `lido_decisions.csv` and `lido_card_inputs.md`.
- Order by mtime (local, +07): lido tables 21:14–21:16, lido freeze 21:17, sky 21:39–21:42, uniswap 21:43–21:46, aave 21:59–22:02, goal_map 22:06:07, all_frozen 22:06:47, raw TVL downloads 22:07:08–22:07:33, `join_outcomes.py` and CHANGES 22:08:16, `data_outcomes.csv` 22:08:23, report 22:10:49. The join ran once (`join.log` has one cutoff line). Nothing indicates that a table changed after the join.
- **CHANGES_R6.md no longer matches either frozen hash** (now 3d80fa6b…, frozen f47f30f3… at 22:06 and 14699e66… at 21:17). D5 was added at 22:08:16, seven seconds before the join output. D5 is declared as technical and written "при присоединении", which is acceptable, but the frozen version of CHANGES was not kept, so I cannot verify that D1–D4 are unchanged since the freeze. *Should-fix:* save the frozen version (or state explicitly that only D5 was appended) and hash the new version.
- `data_scale.csv` is in `/home/claude/r4rep/`, not in `/home/claude/r6/`, it was created at 22:09:29 and no script produces it. *Should-fix:* move it into r6 and add the script (my recomputation in §6 reproduces it).
- Outcome series (R4/R5 fees, prices, category breakdown) existed on disk before the decision tables were built. The executors' blinding logs record no use of them, and the method concedes that results are known. The logs do record incidental exposure to outcome-type content (Aave ACI retrospective "TVL growth per dollar spent", Merit round-1 results, revenue rows in the Lido GOOSE report and the bench files). That is properly logged, but the report's sentence "их собирали исполнители без доступа к результатам" overstates it (§7).

## 1. Method fidelity of the decision tables

**Arithmetic.** I recomputed |amount| / denominator for all 75 rows with numeric amounts. All agree with the `materiality` column to within 0.0015, and none is below its rule threshold (10% for decisions, 5% for line-item rows). I rechecked the line-item tests from each §3 against the card figures, all with the right sign, size and % change. Examples: Aave 2024 SP 12.13→22.07 (+9.94, +82%), Aave 2025 other 4.76→2.16 (−2.60, −55%, 6.7%), Uniswap 2025 legal/ops 2.150→4.491 (+109%, 10.4%), Lido 2024→25 incentives 14.3→8.9 (−38%, 9.8%), Sky 2024→25 incentives 11→48.16 (+37.16, 46.5%). Counts: 112 rows = A 79 (13/19/19/28) + B 33 (1/4/26/2), as the report says.

**Denominators.** The previous full year is used where it exists (Lido 2022 and 2024, Aave all years, Sky all years, Uniswap 2023 and 2024). The current-year budget is used and flagged where it does not exist: Lido 2024 decisions (approved 2024 budget 65.1M, circular because st2024 v1/v2 make up 96% of it) and Uniswap 2023 decisions (25.46M, which includes the reviewer-visible author division of a $60M three-year grants budget). Both appear in D1/D2 and in the report's limitations. Note: the Uniswap 2023 actual (7.11M) is 3.6 times smaller than the proxy, and under it CLIP and UAGP would be selected. The card says so, the report does not.

**Levels.** DAO→foundation transfers are treated as funding: Uniswap 2023 spending is 7.11 (not the 46.2 tranche), Sky 2025 spending excludes the SFF and Fortification grants and Genesis Capital, and Lido 2025 uses what the BORG foundations spent. The funding decisions still appear as class A budget rows (UNI-2023-A1, UNI-2025-A1, SKY-2025-A3/A4, LIDO-2025-A3/A4), which is documented in D2 and consistent across DAOs. Two notes:
- SKY-2025-A3 moved essentially the whole Pause Proxy treasury to SFF (Capital Transparency values both entity grants at 202.8M USD, against the 50M used as the amount). It is as much a class C reallocation to a level-2 holder as a budget. That is why DefiLlama's Sky liquid treasury drops from 67.2M to 0.3M at end-2025 (§6). *Note.*
- SFF's own spending (5.83M through 2025) is level 2 but is not in the 121.9M used for Sky 2025. Levels 1+2 would be about 127.7M. *Note* (≈5%).

**Selection rules and rejected lists (spot-checked well beyond 8 rows per protocol).** I found no clear miss above threshold in any rejected list. The borderline or rule-sensitive items are all flagged by the executors:
- Aave: Certora 2023 ($1.5M) and Gauntlet 2023 ($1.6M) would be selectable (10.5%, 11.2% of D2023) if their v2 AIPs executed in January 2024. Execution dates were not retrieved. The Umbrella budget ($8.7M, 22% of D2024) is excluded by the Safety Module choice in §1, documented in D2. BGD Phase 5 (2.3M + 4,000 AAVE) stays below 10% at any plausible AAVE price.
- Sky: the six STR rebalances in 2025 (160M, 137.5M, 100.85M SKY per 182 days, and so on) have no USD value. The first two are near or above the 8.0M threshold at any SKY price around $0.06. The table includes token-only decisions *provisionally* when a reported aggregate cost exceeds the threshold (Lido TRP, Sky STR, Uniswap DEF, UNIfication budget), and otherwise excludes them. That asymmetry is defensible under the no-pricing rule of D2, but it should be named in the limitations as more than "часть решений могла не пройти порог". *Note.*
- Uniswap: "Unichain Partners - 2025" ($2.09M, 9.3%) would be selected under the low alternative denominator. "Unichain Partners - 2026 and Beyond" ($9.88M) is committed in-period but executed after it. UNI-2025-A5 is included although spending starts in 2026. All flagged.
- Lido: the Curated Module fee change is class B (value moved from operators to the treasury), but "CSM v2 fee structure (2025-05-28)" is rejected as a protocol parameter. If CSM v2 changed the treasury share, it is the same kind of decision. *Note:* check and record.

**Class assignments.** Consistent with the method. The arguable ones are all flagged: GHO discount and its removal as B (in-kind), Umbrella kept with the Safety Module, Sky hump-only changes as B rather than C, Genesis Capital and the SFF grant as possibly C.

## 2. goal_map

The mapper's calls are mostly defensible given only stated_goal and expected_metric. I would classify these differently, or flag them as inconsistent:

| id | Map | My reading | Effect |
|---|---|---|---|
| SKY-2024-A6 Integration Boost (incentives) | no_metric | usage_market. The goal is USDS adoption by integrators, which is the same "product usage" logic used for SKY-2024-A3 | 12m share −0.098. **Incentives×usage becomes 4 negative of 6 = 67%, which meets the rule (§5)** |
| AAVE-2025-A2 GHO CEX Earn (incentives) | no_metric | usage_market is arguable ("accelerate adoption and increase market presence"). The named metric (GHO supply) is not in the data, so no_metric is also defensible | 12m share −0.065 |
| SKY-2023-A3 Launch Project raise | usage_market | no_metric. "take advantage of all growth opportunities" is generic, and the same mapper put SKY-2024-A1 ("improves growth") under no_metric | removes one negative from the class-level set (6 of 9 still meets 2/3) |
| AAVE-2025-A3 Ahab extension | no_metric | usage_market ("Road to 80%" is a market-share north star) | not observable before 2026-10-31, no effect |
| LIDO-2024-A2/A4, LIDO-2025-A2 vs LIDO-2025-A5 (the same LOL programme) | no_metric vs usage_market | consistent with the rule, since only the 2025 LEF request names the stETH-share KPI, but worth one sentence | if mapped like A5, they would add −0.268, −0.228 and −0.022 |
| AAVE-2025-B3 buyback | token_price | The method says the price effect of class B decisions already covered by R2/R3 is not re-evaluated. If Aave's buyback was in R2, this should be descriptive only | not observable, no effect now |
| AAVE-2024-A3, AAVE-2025-A1 (Merit) | monetization → take rate | fine under D4, but the goal named is "DAO revenue". Revenue over 12m was +0.370 (+45%) and −0.129. The report gives only the take-rate falls | wording (§7) |

The goal_map is frozen and should not be changed. The report should, however, say that the incentives result turns on one borderline classification.

## 3. join_outcomes.py

I recomputed with my own loaders (no `common.py`) and got the same values to 4 decimals:

| id | metric | data_outcomes | mine |
|---|---|---|---|
| UNI-2024-A1 | category_fee_share 12m | −0.7165 | −0.7165 (0.4667→0.2279) |
| UNI-2023-A1 | category_fee_share 12m | −0.2852 | −0.2852 |
| AAVE-2024-A2 | category_fee_share 12m | 0.0599 | 0.0599 (0.4968→0.5275) |
| LIDO-2025-A4 | category_fee_share 12m | −0.0008 | −0.0008 (0.6719→0.6713) |
| SKY-2024-A3 | category_fee_share 12m | −0.042 | −0.0420 (0.8754→0.8394) |
| AAVE-2024-A3 | take_rate 12m | −0.0936 | −0.0936 (0.1533→0.1396) |
| AAVE-2025-A1 | take_rate 12m | −0.1367 | −0.1367 |
| UNI-2025-A2 | tvl 12m | −0.1775 | −0.1775 |
| UNI-2023-A1 | token_vs_eth 12m | 0.1198 | 0.1198 |
| LIDO-2025-A4 | token_vs_eth 12m | −1.1061 | −1.1061 |

Logic checked:
- 90-day sums end on the date and include it (89 days back plus the date).
- The category share uses the R5 main key, with own = the group's products in the main key only (Sky Money, a Risk Curator, is correctly left out of Sky's numerator).
- Take rate is revenue / fees from 90-day sums. TVL is the last DefiLlama value on or before the date. Price is the median of 7 daily closes.
- Log change is computed only when both values are positive.
- "Not yet observable" is assigned exactly when t0 + window > cutoff.
- The cutoff is 2026-10-05, the minimum over fee and price series. The revenue, breakdown and TVL series all extend to that date or beyond, so no window is truncated.
- D5 date parsing gives the right t0 for every text date. AAVE-2024-A3 is 2024-05-01 and AAVE-2025-B3 is 2025-11-01. SKY-2025-B14 ("2025-H2") gets no date, which is harmless because it has no goal.

Findings:
- **Deviation from the method, not in CHANGES (should-fix).** The method says "Токен к ETH отчитывается для всех решений описательно". The script computes token_vs_eth only for the 17 evaluable decisions (`+ (["token_vs_eth"] if evaluable else [])`). 12m token_vs_eth is filled for 15 of 112 rows. Either compute it for all rows or record the change in CHANGES.
- Sky token_vs_eth is NaN for every decision before about 2024-10-01, because the CoinGecko `sky` series starts on 2024-09-24 and no MKR series is loaded. Using MKR/24,000 before the migration would fill it. *Note* (descriptive only).
- The sign rule has no dead zone: −0.0008 (LIDO-2025-A4) counts as a negative. *Note*: mention it in the report.
- Several rows share one programme or one vote and therefore the same or overlapping windows: UNI-2024-A1/A2 (URGP), AAVE-2024-A2/A3 and AAVE-2025-A1 (Merit), and UNI-2025-A1/A2 (same t0 2025-03-21). Per-decision counts therefore treat them as independent. *Note* (§5).

## 4. Data coverage as an alternative explanation (should-fix)

The DefiLlama fees breakdown adds adapters without history. Orca DEX has its first non-zero day on 2024-11-12, although the DEX has existed since 2021. Meteora DLMM starts on 2025-01-20 and Aerodrome Slipstream on 2024-05-04. Over the UNI-2024-A1 window, Solana-chain DEXs go from 13.1% to 52.8% of the Dexs category, and Meteora DLMM plus Orca alone are 20.9 pp of the end window. That growth is partly real (memecoin trading on Raydium and Meteora) and partly coverage.

Holding the category to adapters that already had data 90 days before t0 (a crude lower bound that also drops genuine entrants), the 12m change in share becomes:

| id | base | fixed coverage |
|---|---|---|
| UNI-2023-A1 | −0.285 | −0.043 |
| UNI-2024-A1 | −0.717 | −0.334 |
| UNI-2024-A2 | −0.842 | −0.273 |
| UNI-2024-A5 | −0.280 | **+0.386** |
| UNI-2025-A1 | +0.064 | +0.730 |
| AAVE-2024-A2 | +0.060 | +0.401 |
| SKY-2024-A3 | −0.042 | **+0.075** |
| SKY-2023-A3 | −0.024 | −0.017 |
| LIDO-2025-A4 | −0.001 | −0.013 |
| LIDO-2025-A5 | +0.046 | +0.047 |

Two signs flip and the magnitudes for Uniswap fall by half or more. The report's explanation for Uniswap ("рост бирж на Solana") is directionally right, but it should add DefiLlama coverage changes, which METHOD names explicitly ("изменения методики данных").

## 5. Pattern rule

**The report's own claim is correct as stated.** Incentive decisions with a usage goal and an observable 12m window are LIDO-2025-A5 (+0.046), AAVE-2024-A2 (+0.060), SKY-2024-A3 (−0.042), UNI-2024-A1 (−0.717) and UNI-2024-A2 (−0.842). That gives 3 negative of 5 (60%) in 4 DAOs, below 2/3. Counting by DAO gives Lido +, Aave +, Sky −, Uniswap − (2 to 2). Counting URGP as one programme also gives 2 to 2. No reading of this subset qualifies.

**But "one type" is not defined in METHOD or CHANGES (must-fix).** METHOD defines classes (A/B/C) and line items. If "type" means the class, the observable class A decisions with a usage goal are these ten:

| | LIDO-25-A4 | LIDO-25-A5 | AAVE-24-A2 | SKY-23-A3 | SKY-24-A3 | UNI-23-A1 | UNI-24-A1 | UNI-24-A2 | UNI-24-A5 | UNI-25-A1 |
|---|---|---|---|---|---|---|---|---|---|---|
| 12m share | −0.001 | +0.046 | +0.060 | −0.024 | −0.042 | −0.285 | −0.717 | −0.842 | −0.280 | +0.064 |

That is 7 negative of 10 (70%), in 4 DAOs, with negatives in 3 of them (Lido, Sky, Uniswap). Read per decision, this **meets the rule**. A middle grouping, "growth spending" (incentives plus marketing/growth), gives 5 negative of 7 (71%), which also meets it.

Read per DAO, where METHOD itself uses "случай" to mean a protocol, the class-level set is Lido 1:1, Aave +, Sky −, Uniswap 1+:4−. That gives no three DAOs with the same sign. So the result depends on the reading.

There is also goal_map sensitivity. Reclassifying SKY-2024-A6 alone (§2) makes the incentives subset 4 of 6 = 67% negative, which meets the rule per decision.

Other type × goal cells cannot qualify. Monetization has only Aave (2 observable). Capital has only Uniswap (1). token_price has no observable window. Class B has nothing observable beyond 6m.

Required in the report:
- (a) State which reading was used (line item, per decision) and that it was not fixed before the join.
- (b) Report that under class-level grouping per decision there is a negative candidate (7 of 10), with the alternative explanations. Uniswap supplies 4 of the 7 negatives. Dexs coverage changes (§4) flip two signs. Sky's CDP share starts at 85–88%. Lido's −0.0008 is a zero.
- (c) Say that the incentives result moves to 4 of 6 with one reclassification.

The overall message ("not evidence that incentives do or don't work") survives all of this. The flat "закономерностей нет" does not.

## 6. data_scale.csv

- Spending matches the card inputs exactly: Lido 129.5 / – / 55.2 / 49.6; Aave 67.36 / 14.34 / 38.86 / 54.24; Sky 46.2 / 53.7 / 80.0 / 121.9; Uniswap – / 7.11 / 22.59 / 20.7.
- Calendar-year fees and revenue recomputed from `r4rep/raw/fees/*__dailyFees.json` and `r5/raw/rev/*.json` match every cell (for example, Lido 2024 fees 1,034.1 and revenue 51.6, Aave 2025 907.7 and 124.2, Sky 2025 410.7 and 239.9, Uniswap 2025 1,054.3 and 0.2). All years have 365/366 days of data except Uniswap revenue (2 days in 2022, 101 in 2023), which is zero anyway.
- Liquid treasury at year end equals the sum of the non-OwnTokens chains of `r6v/raw/treasury_*.json`. I reproduced 95.8 / 142.7 / 121.3 (Lido), 41.0 / 82.6 / 74.9 (Aave), 54.2 / 67.2 / 0.3 (Sky) and 0 (Uniswap). Runway = liquid treasury / spending (for example, Aave 2025: 74.9 / 54.24 = 1.38).
- Caveats to add (should-fix, short):
  - Sky's 0.3M at end-2025 is the SKY-2025-A3 transfer of the Pause Proxy treasury to SFF, which DefiLlama does not track. It is not a cash crisis. The report's reason ("оплачиваются из системного буфера") is true but incomplete.
  - Uniswap's 0 ignores the UF's own treasury (level 2), for example the $29M UNI-collateralised loan.
  - Lido's spending includes non-cash TRP (9.7M in 2024, 6.4M in 2025, paid in LDO), so runway against liquid assets slightly understates cash runway.
  - Uniswap 2025 spending is UF only. The DAO-level part (the $45M Aera vault, DUNI, UAC) is not reported, so spending/fees of 0.02 is a lower bound. The report flags this ("только фонд").
  - Uniswap 2025 spend/revenue in the CSV is 126.06 on revenue of 0.2M (fee switch from 2025-12-28). The report writes "нет выручки" next to a revenue cell of 0.2, so "почти нет" is more accurate.
  - DefiLlama Sky 2022 fees equal revenue (42.6). That is plausible with the DSR near zero, but low against Steakhouse. *Note.*

## 7. REPORT_R6.md

**Numbers.** I checked every number against the data files. All are correct within rounding:
- counts 112 / 79 / 33 / 17 / 40 / 55, and per-DAO decision counts;
- the scale table;
- runway "около 2,5" and 2.9→1.4;
- Lido −0.1%, +4.7%, take rate +27% (e^0.2375 − 1 = 26.8%), token −67% and −46%;
- Aave +6%, −9%, −13%, and "почти в пять раз" (4.7);
- Sky −2%, −4%, share near 90% (0.875 / 0.839), incentives $48M;
- Uniswap 8 measurable / 6 observable, −24% to −57% (−24.4, −24.8, −51.2, −56.9), +7% (6.6), TVL −16%, UF spending $7M→$21M.

No em dashes (0 occurrences of U+2014). En dashes appear only in ranges.

**Must-fix.**
1. §5: state the typing and counting choice and report the class-level negative candidate with its alternative explanations, and the one-reclassification sensitivity. Replace "повторяющихся закономерностей по заранее заданному правилу нет" with a statement conditional on the reading.
2. First headline: "У 40 решений цель не названа совсем" counts 21 line-item rows, which are aggregate year-on-year changes and have no decision text by construction (20 of the 40 "not named"). Among the 91 actual decisions: 17 measurable, 54 goal stated but no metric in data, 20 not named, 16 of which are Sky/Aave/Uniswap class B parameter changes. Among the 58 class A spending decisions, 54 state a goal and 14 map to public data. The finding is "DAOs almost always state a goal, but rarely one measurable in public data (14 of 58 spending decisions)", not "almost never say". Also "у 55 цель названа, но через показатели, которые нигде системно не публикуются": only about 8 of those 55 name any metric at all. Most state a purpose with no metric ("support development of v2"). Rephrase. "Почти никогда" is too strong for 17 of 112, and the 112 base is inflated by Sky's 26 SBE rows.

**Should-fix.**
3. Uniswap paragraph: add DefiLlama coverage changes to the Solana explanation (§4). Drop or soften "Крупнейший тратящий участник экосистемы, Uniswap Labs". Labs' spending is unknown, so this is not supported.
4. Aave paragraph: for Merit and Ahab, whose goal is DAO revenue, give revenue alongside take rate. Revenue 12m was +45% (AAVE-2024-A3) and −12% (AAVE-2025-A1). "При том что сами комиссии росли" alone reads as if the goal failed. Also qualify "упали почти в пять раз": the 2022 base (Llama) and 2023 (TokenLogic) come from different reporters, and 2022 includes the one-off $16.3M V3 retro funding.
5. Lido / NEST. "Расходы примерно равны выручке" is supported only with specifics. Spending/revenue is 1.07 in 2024 (55.2 / 51.6) and 1.19 in 2025 (49.6 / 41.6), so in 2025 spending exceeded revenue by $8M. Revenue is DefiLlama's: the DAO-treasury share of the 10% fee, net of the node-operator share. Spending includes non-cash TRP in LDO (9.7 and 6.4) and deposit referrals (3.1 and 4.1), which Lido itself books under cost of revenue. Excluding TRP, the ratios are 0.88 and 1.04. Suggested wording: "в 2024–2025 годах расходы составляли 1,07 и 1,19 выручки DAO по DefiLlama (доля казны в 10-процентной комиссии), без токенной части TRP 0,88 и 1,04". The NEST sentence is conditional ("если порог покупок привязан к расходам") and NEST was executed in 2026-08, outside the period. Mark it as a remark beyond the study, not a finding. Minor: the Curated Module change is dated 2025-12-20 here (Aragon #195) and 24 December in R5. Align them.
6. "их собирали исполнители без доступа к результатам": change to "без доступа к рядам результатов; случайные контакты с результатами записаны в журналах исполнителей".
7. Limitations: add (a) undefined typing/counting in the pattern rule; (b) DefiLlama coverage changes in categories; (c) several rows share one programme or one vote; (d) Sky contributes 45 of 112 rows, 26 of them SBE parameter changes, so per-decision shares are Sky-weighted; (e) token-only decisions were included provisionally when an aggregate cost passed the threshold and excluded otherwise; (f) token_vs_eth is not reported for all decisions, contrary to the method (or fix the script); (g) Uniswap's 2023 proxy denominator is 3.6 times the actual, so under the actual CLIP and UAGP would be selected.
8. Scale paragraph: add the Sky treasury-to-SFF reason, the UF treasury caveat for Uniswap, and that Aave excludes Umbrella (5.2M) as well as the Safety Module.

**Notes.**
9. "Что это значит": "по расходам ответить нельзя, потому что DAO почти не формулируют проверяемых целей" should become "...почти не связывают цели с публичными метриками". The RFC recommendation itself follows from the data.
10. Style for publication: the text has 20 colons, including four "Модель:" openers. If this goes out as a public text, rephrase them in running prose.
11. Sky 2025 spending would be about 127.7M with SFF's own level-2 spending. "Около 122" is fine if the definition says it is without SFF.

## Summary of classifications

- **Must-fix (2):** the pattern claim depends on an undocumented choice of "type" and counting unit, and class-level grouping per decision gives a qualifying negative candidate (7 of 10), with a 4-of-6 incentives sensitivity; the "goal not named in 40 of 112" headline is inflated by 21 line-item rows (the correct figures are 20 of 91 decisions, and 54 of 58 spending decisions state a goal).
- **Should-fix:**
  - DefiLlama adapter coverage flips 2 of 10 signs and halves the Uniswap effects;
  - token_vs_eth is computed for 17, not all 112, rows, which deviates from METHOD and is undocumented;
  - CHANGES was edited after the freeze and the frozen version was not kept;
  - data_scale.csv sits outside r6 with no script;
  - wording on Lido ≈ revenue (give 1.07 / 1.19 and the definition), Aave revenue vs take rate, Uniswap Labs, blinding, and treasury/runway caveats;
  - additional limitations.
- **Notes:** Sky SFF level-2 spending, Sky MKR price gap, sign without a dead zone, CSM v2 class B consistency, the asymmetric treatment of token-only decisions, and colons in the Russian text.

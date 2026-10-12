# Independent review of the W0 check (October 2022 to October 2023)

Reviewer scratch work is in /tmp/claude-0/review_w0/. No project files were changed apart from this one.

## Integrity and reproduction

- METHOD_W0.md matches METHOD_W0.sha256. The frozen time (2026-10-07T19:35:53Z = 02:35:53 +07) matches the file mtime. check_2022.py and check.log come before the freeze. The build and analysis scripts come after it, and so does the beethoven-x child fee aggregation (02:36:09), which W2 logs. All entries in SHA256SUMS_W0.txt verify.
- I rebuilt data/panel_w0.csv by running build_panel_w0.py from /home/claude/r4rep with PYTHONPATH set, and data/panel_r5_w0.csv and category_map_w0.csv by running build_r5_w0.py from /home/claude/r5. Output went to scratch. All three hashes match the archived files.
- Diffs. build_panel_w0.py differs from r4rep/build_panel_rep.py only in WINDOWS, the window label ("W0") and the output path. build_panel_rep.py in turn differs from the main build_panel.py only in the same three places. build_r5_w0.py differs from r5/build_r5.py only in the input and output paths (and `os.makedirs` became `pass`). analyze_r5_w0.py matches r5 h2/h3 apart from four things. Window FE is removed. Winsorisation runs on one window, which equals the per-window version. HC1 replaces protocol clustering. A n >= 15 gate is added. analyze_w0.py matches R4 R1 except that HC1 replaces clustering.
- HC1 is equivalent to clustering here. There are 29 unique groups for 29 observations, and with G = N statsmodels' cluster correction reduces to N/(N-K). I confirmed the SEs are identical (0.1357).

## Findings

### Must-fix

**M1. CHANGES W1 and the "uninformative" label understate how much the valuation result points against Research 5.** W1 is right that the frozen rule makes T2 and T3 inconsistent with Research 5, and right about the residual degrees of freedom (16 obs, 9 keys, 4 residual df). The exact structure is starker than W1 says. Six of the nine keys are singletons (Lido, GMX, Convex, Yearn, Synapse, Nexus Mutual). Those six have leverage 1 and a residual of exactly 0, so b_take and the T3 residual are identified only from 10 observations in 3 keys (Dexs 6, Lending 2, CDP 2). HC1 is anti-conservative with this leverage pattern (HC2 even gives p = 3e-7).

W1 leaves out one point, and it is in posthoc_w0.json. Classical small-sample t inference with 4 df still rejects at the frozen thresholds. T2 has two-sided p = 0.009. T3 has two-sided p = 0.064, which is one-sided p = 0.032 < 0.05. Leave-one-out on b_take across the 10 informative observations stays between 0.65 and 0.95, so no single point drives it. "The SEs are not credible" is therefore not what saves Research 5. What limits the result is that the effective sample is tiny and concentrated.

The post-hoc no-FE version is also not a test of the Research 5 model, which rests on category FE. W1's wording "both consistent with Research 5" should go, because a confounded cross-category slope gives no support either way.

Required wording: under the frozen rule T2 and T3 are inconsistent with Research 5, and this survives df-honest t inference. The result rests on 10 observations in 3 categories and on thin 2021–22 fee coverage, so it is weak contrary evidence that cannot outweigh the main periods (n = 120, b_take = −0.03). It is not support. The reclassification to "low weight" was made after the results were seen and should be labelled that way. Calling W0 simply "uninformative" while citing the no-FE "consistent" numbers reads as outcome-favourable.

### Should-fix

**S1. The survivorship check universe is incomplete, so "2 dead" is a lower bound.** Universe A is the protocols in today's fee dashboard. Universe B is protocols flagged `deadFrom` with a gecko_id. Several kinds of protocol fall through.
- Protocols that are alive in the DefiLlama listing, outside the fee dashboard and not flagged dead. There are 1,421 such gecko ids and none was checked. I spot-checked two. Serum (SRM) had a market cap of $285M on 2022-10-01 and a return of −3.36 log against ETH (FTX collapse), and it is in neither universe. Multichain had $76M and −0.72.
- Dead child protocols with no gecko_id whose token sits on a parent. There are 121 such children. For 100 of them the parent is not in universe A, and 49 parents have every child dead (Kujira, pSTAKE, Shade, Interlay and others). I did not verify their market caps.
- Protocols deleted from DefiLlama altogether. The check cannot see these at all, and that should be stated.
- 16 dead gecko ids whose CoinGecko download returned 404 (empty file) were dropped silently.
- Tokens with no end price (Pylon, April) are dropped from the medians, which pulls the dead median up.

Adding Serum alone moves the October dead group to n = 3 with median about −1.09. That does not overturn accepting October, because entrants (−0.66) and alive-uncovered tokens (−0.71) remain close. The omissions would only make April worse, so rejecting April is justified (10 dead with median −2.25 and 39 uncovered with median −0.81, against −0.47 for entrants). METHOD should still call the dead count a lower bound and name Serum.

**S2. Some outcomes were seen before the freeze.** check_2022.csv already held y_vs_eth for all 29 W0 entrants (median −0.66, 6.9% beating ETH), and the choice between October and April was made after looking at returns by group. METHOD discloses the check, but its title, "Frozen before computing", overstates it. The descriptive y figures (7%, −48%) were effectively known before the freeze. g and all regressions were not. The report should say this plainly.

**S3. The T1 verdict follows the frozen rule but is fragile, and the report should show that.** I reproduce b_g = 0.2134, SE 0.1357, one-sided p 0.0579 (normal) and n = 28, with categories Dexs 12 and other 16 (pooling below 10 is correct). Winsorisation at 2.5/97.5 and the C2 exclusion are correct (Defi Swap only). There are no supply artefacts or delistings, and the identity error is 4e-16. The frozen rule is positive with p < 0.10, so the result is consistent.

Under other choices it weakens. With t(20) p is 0.066. With HC3 it is 0.113. Unwinsorised it is 0.067. Dropping any one of LooksRare, Biswap or Osmosis pushes p above 0.10, and the 95% CI is [−0.05, 0.48]. Report it as weakly consistent, with a point estimate (0.21) close to the main-period 0.256.

**S4. Caveats are needed on the descriptive category numbers.**
- The −0.405 median category growth against ETH is just the Dexs value, because 12 of 25 observations are Dexs. The median across distinct keys is −0.14. Present it as the Dexs figure, or report the per-key median.
- The 72% losing share (18 of 25) and the median d_share of −0.297 reproduce. But the fee breakdown grew from 113 products on 2022-10-01 to 318 on 2023-10-01, so part of the share loss is mechanical coverage growth (Liquity going from 0.57 to 0.025 is one likely case). The main periods have the same problem (318 → 704 → 1432 products) and also show 72.5% losing share, so the comparison holds, but the caveat belongs next to the number.
- Coverage on 2021-10-01 (53 products) is why 7 observations lose prior_share_growth and why Biswap's value is +5.08.

**S5. The provenance of check_2022.csv is incomplete.** The `kind` column is not produced by the archived check_2022.py. The CSV is dated 3 minutes after check.log and is not in SHA256SUMS_W0.txt. METHOD's April figure of "37 uncovered" counts only "fee series starts later". The log shows 39 alive without fee data (37 plus 2 "no fee adapter at all"). Beets is labelled "no fee adapter at all" although it has child adapters (W2). The fix is to archive the labelling code, hash the CSV and correct the April count.

### Notes

- **N1. Undocumented working directories.** build_panel_w0.py only runs from /home/claude/r4rep with that directory on PYTHONPATH. build_r5_w0.py only runs from /home/claude/r5, because it uses relative raw/ paths. Neither is documented.
- **N2. Revenue downloads.** METHOD says revenue was "downloaded for the new groups". In fact every W0 group already had an r5/raw/rev file, and nothing in that directory changed after 2026-10-07. This is harmless, but the sentence should be corrected.
- **N3. C2 coverage.** Every W0 entrant also appears in the main or replication R4 panels, so the C2 list was already reviewed for each of them. THORChain, Osmosis and Ankr are kept there as well.
- **N4. Remaining descriptive numbers reproduce.** 7.1% beat ETH, which is 2 of 28 (Liquity at +0.002 log and Frax at +0.09), so the "7%" rests on one token that is essentially flat. The median is −0.661 log, or −48.4%. Variance shares are 0.71 for g, 0.19 for m and 0.10 for −s, so g is the largest, as in R4.
- **N5. Survivorship check against the panel.** The check's fee rule ignores C1 child summing, but its 29 October entrants match the panel's 29 gecko ids exactly.
- **N6. T2 interval.** The T2 95% interval [0.37, 1.28] includes 1, and `ci_excludes_1` = false is reported correctly.

## Bottom line

The code is faithful to the frozen method and to the R4/R5 code, and all numbers reproduce. T1 is consistent by the frozen rule but only weakly so. T2/T3 are inconsistent by the frozen rule. The honest reading is weak, low-weight evidence against Research 5 from 10 effective observations. It is not "uninformative" with a consistent post-hoc version attached. The October survivorship check undercounts dead and uncovered tokens (Serum, for example), but not by enough to reverse accepting October or rejecting April.

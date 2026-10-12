# Review of Research 4 (independent referee)

Reviewed 2026-10-06. No existing file was modified. The whole pipeline was re-run in /tmp/r4review. Checks were done in the order requested.

## 0. Summary

The pipeline is clean and reproduces byte-for-byte. The frozen hashes match. The decomposition identity holds. Merges neither duplicate nor lose rows. Most numbers in INTERIM_R4.md trace to the outputs. Four things must be fixed before publication.

1. Survivorship. Dead tokens leave the sample without any disclosure, and the frozen delisting rule never fires.
2. Two analysis deviations from the frozen method that CHANGES_R4.md does not log. The H1 variance shares use the wrong sample, and the secondary outcome pools categories the wrong way. The second one changes a robustness count in the text.
3. One arithmetic error in the Lido section.
4. Several overclaims. These are "almost all of the return difference is fee growth", the conclusions paragraph, and the robustness counts in stage 4.

## 1. Frozen methods and undisclosed deviations

**Hashes (fine).** sha256sum of METHOD_R4.md, METHOD_R4_STAGE2/3/4.md matches the .sha256 files: afa0248a…, 6a479d8d…, 092488f3…, 4eb716ad…. File mtimes fit the logged freeze and change times. C1/C2 are logged at 14:09:01Z and panel.csv/results.json were written at 14:10Z. C4 is the only entry with no timestamp.

### Must fix

**D1. Variance shares (H1) use the wrong sample.** In analyze.py `run()`, the shares are computed on `d = base.dropna(subset=["g","m","s","beta","drawdown_start"])`, which is n = 175. METHOD_R4.md says the decomposition is computed "for every observation with F_start > 0 and F_end > 0". After the artefact and C2 exclusions that is n = 197. Neither CHANGES_R4.md nor the text logs the beta/drawdown filter.
- Reported (n = 175): g 1.02, m −0.05, −s 0.03.
- Frozen sample (n = 197): g 1.23, m −0.26, −s 0.03. By window, W1 1.06/−0.11/0.05, W2 1.10/−0.10/−0.01, W3 1.28/−0.32/0.04.
- The H1 verdict does not change. But the m share is about five times larger in magnitude, and the text (L28, L33) treats the m share as near zero.
- Fix: report the n = 197 shares as the main result, and keep the n = 175 shares as the "regression sample" version.

**D2. Wrong pooling rule for the secondary outcome.** METHOD_R4.md says "categories with fewer than 5 observations in the window pooled into 'other'". analyze.py uses `cats()` instead (`sec["cat2"] = cats(sec)`), which pools categories with fewer than 10 observations over all windows. I re-ran it with the frozen rule:
- H3 now fails (ΔR² 0.023 against the 0.02 threshold).
- H4 still fails (−0.0475, p = 0.085).
- H_start is 0.37, p = 0.036. R2 beta is −0.90, p = 0.002.
- Consequence for INTERIM L30: H3 robustness becomes **5 of 9, not 6 of 9**. The counts of significant H_start and beta runs ("6 of 10") are unchanged.

**D3. Survivorship: dead tokens dropped silently (METHOD Universe 5).** fetch_prices.py writes an empty file when CoinGecko returns 404, and build_panel.py then skips the group without recording it. 26 of the 717 kept candidates have no price data. They include protocols that are known to be dead or delisted: vertex-protocol, kwenta, sonne-finance, vesta-finance, mars-protocol, reya, mento, swapr and others. As a result panel.csv has `delisted = 0` in all 214 rows, and the frozen rule "the last available price is used, the observation stays" never applies.
- Some of these tokens may well have had market cap of $50M or more at a window start (Vertex at 2024-10-01, Kwenta at 2023-10-01 are worth checking). The headline "almost all DeFi tokens lose to ETH" is therefore probably biased upward, and so are the window medians.
- Fix: pull history for the 26 ids from another source, such as coins.llama.fi/chart/coingecko:<id> or the CoinGecko API market_chart. Apply the $50M entry rule and the delisting rule. At minimum, log this in CHANGES and in the "Оговорки" section.

### Should consider

- **C9 changes the stage-3 variable after stage-3 results existed.** results_stage3_gross.json was written at C9's own timestamp, so stage 3 had already been estimated on the frozen gross definition. CHANGES says the gross result is kept, but INTERIM never reports it. Under the frozen definition H2a = −1.45, p = 0.044, and corr(s, s_issue) = 0.34 instead of 0.185. The verdict and the robustness pattern are the same (significant only in main and no-winsor). The motivating case, CAKE, is a BSC token and is not in the stage-3 sample. Add one sentence giving the frozen-definition result.
- **The C7 flag shares (71/39/20%) are computed on all 200 main observations.** In the H2b regression sample they are 69/34/15% (results_stage3.json flag_share 0.343). This is consistent, but say which sample each number comes from.
- **The "complete" flag is not used.** METHOD_R4_STAGE3 says a token is used only if its reconstruction is complete. morpho and usual have `complete = False` in onchain_supply.csv but enter W3 through their NET values. After C5 the flag probably just means "all four dates exist", which is harmless. State that.
- **Extra stage-4 run.** `drop_recount_cases` in analyze_stage4.py is not in the frozen stage-4 robustness list. Label it as additional.

## 2. Code correctness

**Fine as is**
- The decomposition identity holds (max error 1.3e−15). y, g, m, s and ln M_start follow the method. Annualising F in ln M_start does not affect m.
- `at()` takes the median of the 7 daily values ending at the date. `sum90` covers the 90 days ending at the date. Both include the start day itself, which is a one-day overlap and negligible.
- beta is the polyfit slope over 365 days with at least 250 pairs. drawdown is ln(median P0 / max daily close) and is ≤ 0.
- No duplicates on (window, group) or (window, gecko_id). The stage-2 left merge keeps all 214 rows.
- Clustering by group via factorize. Category dummies (≥10 obs) come out the same in the 200, 175 and 152 samples (Dexs, Lending, Liquid Staking, Derivatives). Winsorization is applied within window to y and to every continuous regressor, on the estimation sample.
- Hack matching. Only 165 of 1293 hack records carry parentProtocolId. I rebuilt the flag through the child → parentProtocol map in protocols.json and it is identical: 25 hacks, 0 differences.
- Treasury. Every key in raw/treasury that contains "-" is a "-OwnTokens" key, so excluding "-" keys equals the frozen rule.
- No look-ahead in the start-of-window variables: H_start, ln M_start, beta, drawdown and the $50M entry test all use data up to the start date.

**Should consider**
- **Incomplete end-window fee data drives extreme g.** There is no coverage check on F_end. Six observations in the R1 sample have fewer than 80 fee days in the end window: ShibaSwap W1 (8), Reserve W1 (6), Orderly W3 (30), Moonwell Apollo W3 (24), KyberSwap W3 (76), Euler W3 (79). Reserve W1 has g = −3.06 while y = +0.87. That is a data gap, not a business change.
  - Dropping these 6 makes H3 fail (ΔR² 0.027) and pushes H4 to p = 0.063. H_start becomes 0.42, p = 0.004.
  - This was not frozen, so it is not a verdict issue. But it shows H3 and H4 depend on six data-gap observations. Report it as a data-quality check.
- **H_start = 0 where it should be missing.** When the holders-revenue series begins after the start window, `sum90` returns 0 and H_start is set to 0. The frozen intent is "no series → missing". This affects 21 observations. Examples: Pendle W1 (series starts 2023-10-09, H_end 0.77), ApeX W3 (H_end 0.50), Bancor, Across, DODO, Synapse, Marinade W3. It biases H_start down and dH up. Set H to missing when the series starts after start minus 90 days.
- **Observations with F_end = 0 are dropped.** Ribbon W2, NFPrompt W2 and ZORA W3 have F_end = 0 and y between −1.5 and −1.9. The frozen rule drops them from the decomposition and from all regressions. That is per method, but it is selection on survival of fees. The text says 197 observations "entered" the sample. In fact 200 entered and 3 were dropped for this reason.

## 3. Reproducibility

`build_panel.py`, `analyze.py`, `build_stage2.py`, `analyze_stage2.py`, `analyze_stage3.py` and `analyze_stage4.py run` all ran with no errors in /tmp/r4review. panel*.csv, results*.json and runs_summary_stage2/3/4.csv are **byte-identical** to the originals.

Gaps:
- No script produces data/runs_summary.csv. I checked it against results.json and it matches.
- The NXM / Bancor / Olympus post-hoc runs in INTERIM have no script. I reproduced them:
  - stage 3 without NXM: −1.334, p = 0.072
  - stage 4 without NXM: p = 0.088
  - stage 4 without all three: −0.86, p = 0.209
  - Add a script.
- "Цены выборочно сверены с независимым источником DefiLlama" (L102) has no code or output behind it.
- The GOOSE report figure (21%, L51) has no citation.

## 4. Numeric claims in INTERIM_R4.md

Everything below checks out unless it is listed under mismatches.
- 106 protocols and 197 obs (the decomposable main sample). 175 obs in regressions, with all 22 losses due to missing beta.
- Beat ETH 18 / 9 / 24%. Median token −27 / −58 / −42%.
- Within-window quintiles: top +16% (g +24%), bottom −80% (g −68%).
- 10% fee growth gives about 2.5%. Median CoinGecko supply growth 7–11%.
- The H1–H4 table, apart from D1 and D2. H4 4/9, H_start 6/10, beta 6/10.
- LDO y −50 / −46 / −34. CoinGecko +9.3% / −7.4% against on-chain +0.5% / −1.9%. Corrected multiples −46 / −23 / −16% and g −6 / −29 / −23%.
- Peer ranks and medians: 4th of 6 at −24%, 3rd of 12 at −66%, 4th of 13 at −45%. Sanctum +1%. MC/revenue 43 → 12. Multiple changes −42 vs −34, −21 vs −60, −38 vs −23. Revenue −2%. Take rate 4.9 → 6.2%. LST shares 88 / 74 / 50 / 53%.
- Stage 2 numbers: 0.13 (p 0.26), 0.07 (p 0.21), H8 p 0.40 with n = 33, hack −25% (p 0.051), robustness p range 0.04–0.12.
- Stage 3 numbers: 53 tokens and 105 obs. 48% zero change. 30 tokens with changes, median 1%. 21 decreasing obs. NXM −20% to −48%. −1.27 gives −11% for 10% issuance. Counts 2/6 and 1/7.
- Stage 4 numbers: 60 tokens and 116 obs. Audit 13 real (3 partly) / 6 recount / 1 unclear, names as listed. −1.21 (p 0.03). H9 −0.32 (p 0.16), audited −0.44 (p 0.16).

**Mismatches**

| Line | Text | Correct |
|---|---|---|
| L28, L33 | H1 shares "около 1,0 / −0,05 / 0,03" | Frozen sample: 1.23 / −0.26 / 0.03 (D1) |
| L30 | H3 robustness 6 of 9 | 5 of 9 with the frozen secondary-outcome rule (D2) |
| L41 | "в казну пришло 19,4 млн LDO, а за весь год из неё ушло около 7,3 млн, так что чистый прирост 17,3 млн" | 19.4 − 7.3 ≠ 17.3. From raw/ldo_agent_tx_1.json for W3: inflow 25.0M (19.4M from 0xf6f0…1e96 in Jun–Sep 2026, 5.2M in Nov 2025 from about 120 small senders), outflow **7.7M** (7.57M to 0x8345…b759, 0.13M to 0x12a4…9030), net +17.3M |
| L41 | Jun–Sep inflow "объясняется покупками ... по мандату Growth Committee" | Nothing in the repo shows that 0xf6f0… is a buyback/GC address. Cite the transactions or forum post, or soften |
| L41 | LDO W3 −34% | −34.5%. Trivial, but the panel gives −35 under round-half-up |
| L49 | "за доллар выручки рынок стал платить на 38% меньше" | −38% uses CoinGecko supply. With the on-chain correction used in L41 it is about −34%. Say which basis you use. The W1 peer median (−34%) rests on only 4 peers with revenue data |
| L93 | H2a-wide "значимо в 6 из 8" | That count includes main, "audited" (identical to main for s_issue alone, by construction) and the non-frozen drop_recount_cases. Over the frozen robustness runs it is 3 of 5: no-winsor, drop W3 and Ethereum-only pass; drop W1 (p 0.13) and drop W2 (p 0.15) fail |

## 5. Overclaiming

**Must fix**
- **L14, "Почти вся разница в доходности между токенами связана с разницей в росте комиссий".** A g share of about 1 means cov(g, y)/var(y) ≈ 1, that is, y loads fully on g. It does not mean g explains y. Within window, corr(g, y) = 0.50, so g alone explains about **25%** of the variance in returns. sd(g) is about 2× sd(y), and g and m are strongly negatively correlated (−0.86). Suggested wording: "Of the three parts, only fee growth moves with the return. But fees swing about twice as much as the price, and most of that swing is absorbed by the multiple."
- **L14, "рынок явно не верит, что скачок комиссий сохранится".** A pass-through of 0.26 is just as consistent with measurement error in DefiLlama fees, which attenuates the coefficient. The text itself notes adapter artefacts at L102, and see the end-coverage point in section 2. Present the market-belief reading as one possible explanation.
- **L16, "Новая эмиссия связана с доходностью отрицательно и заметно".** H2a fails in all three drop-window runs in stage 3. Without NXM, Bancor and Olympus the coefficient is −0.84, p = 0.18 (stage 3) and −0.86, p = 0.21 (stage 4). Among the 55 observations with any change the median change is 1%, and 21 of them are supply reductions. The result is mostly "tokens with shrinking supply did better", not "issuance hurts". Make it "a negative association, fragile, driven by a few tokens with burns".
- **L37, conclusions.**
  - "что растит комиссии" is presented as a DAO decision. It was never tested as one, and the only decision proxies (H5, H6) are null.
  - "Против работают ... взломы". Hacks were a control variable with p = 0.051, and L68 itself says this is an observation, not a finding.
  - "Механизмы возврата ... дают небольшую добавку". H_start is a fee share, not a mechanism, and its effect drops out without W3.
  - Rewrite this paragraph so it reflects the confirmed hypotheses only.
- **L96, "На расширенной выборке эффект эмиссии держится лучше".** The wide sample is the stage-3 Ethereum sample plus 11 observations. The stage-4 Ethereum-only run reproduces stage-3 main exactly (−1.2698, p = 0.0207). Two of three drop-window runs fail.

**Should consider**
- L20, "когда протоколы массово включали fee switch". This explanation was not tested. Label it as a hypothesis.
- L22, "систематически". Beta was not a hypothesis and is significant in 6 of 10 runs. "Заметно" is more accurate.
- L66, "то немногое ... проходит через сами комиссии". This interprets a coefficient that is not significant, and H7 was not supposed to be evaluated. Label it post hoc or drop it.
- L8 and L102 say the exclusions "ничего не меняет". That is true for the verdicts. It is not true for the survivorship issue (D3), which is not mentioned anywhere.

## 6. Other referee points (should consider)

- **Multiple testing.** There are 12 pre-registered tests (H1–H9, H2a, H2b, H2a-wide) and about 8 robustness runs each, and the text also highlights findings that were not hypotheses (beta, hack, H_start). No main-run p-value except g survives a Bonferroni or Holm correction across these tests. The closest is beta at 0.0095 against the 0.004 threshold. One sentence on this belongs in the caveats.
- **Stage-2 variables condition on success.** new_products and new_chains count products with fees > 0 at the window end. A launch that failed is not counted, and the count is concurrent with y. These variables are therefore partly outcomes, not decisions known at the start. R2t has 33 observations against about 16 parameters, so H8 is uninformative, not just underpowered.
- **Universe consistency with the C2 logic.** Several kept tokens look like the C2 exclusions:
  - Geodnet is DePIN (DePIN is an excluded category; DefiLlama files it as Oracle).
  - Launch Coin on Believe maps to gecko ben-pasternak, which is a memecoin-like token.
  - ZORA and World Liberty Financial are questionable as fee-backed protocol tokens.
  - Check two mappings in particular. "Velo Finance" (Dexs) maps to `velo`, which C8 itself describes as Velo Protocol native on Stellar, so this looks like a mismatch. "Veranta" maps to `avantis`.
  - The frozen_universe run shows C2 does not move the verdicts, so a quick re-check is enough.
- **Geodnet's audit note contradicts C8.** The audit says the move from Polygon to Solana makes the on-chain figure incomplete, while C8 kept Geodnet on the grounds that home-chain totalSupply covers the gross supply. Exclude it from s_issue for consistency. It is 1 observation.
- **One audit source is unstable.** The Compound source is a preview subdomain (bb-add-morpho-tvl.preview.tokenterminal.com). Replace it with a stable URL. The Stargate "recount" class is borderline, because the note itself describes a real STG → ZRO migration.
- **Sample weight by window.** W3 is 81 of 175 regression observations, and several effects (H_start, H2b) sit in one window. Per-window n should appear in the text.

---

# Second pass (2026-10-06)

The pipeline was re-run in /tmp/r4review2: build_panel, analyze, build_stage2, analyze_stage2, analyze_stage3, analyze_stage4 run, lido_peers and posthoc. All of them run without errors. panel*.csv, results*.json, runs_summary*.csv, lido_peers.csv, eth_lst_share.csv and posthoc.json are **byte-identical** to data/. The method hashes still match.

## Must-fix items from the first pass

| Item | Status |
|---|---|
| D1. H1 shares on the decomposable sample | **Fixed** (C12a). The shares are now 1.23 / −0.26 / 0.03 on n = 197, and the n = 175 shares are reported alongside |
| D2. Secondary-outcome pooling | **Fixed** (C12b). The code now pools categories with fewer than 5 observations in the window |
| D3. Survivorship | **Addressed** (C10), with the caveats below |
| H = 0 for late-starting series | **Fixed** (C11). `k0 > 0` / `k1 > 0` in build_panel.py match the CHANGES text |
| Geodnet | **Fixed** (C13) |
| LDO arithmetic | **Fixed**. The text now gives 25.0M in (19.42M from one address in Jun–Sep), 7.7M out and 17.3M net, all confirmed |
| Overclaims (fee-growth share, pass-through reading, issuance, the conclusions paragraph, "holds better on the wide sample") | **Addressed**. The new wording matches the results |
| Post-hoc scripts, runs_summary.csv producer, price-check artefact, GOOSE source | **Fixed**. The price check confirms 40 points, median deviation 1.85%, max 12.9% |

## Remaining problems

**Should fix (numbers)**
1. **L41, beta "значимо в 7 расчётах из 10".** The correct count is **8 of 10**: main, frozen_universe, no_winsor, with_artefacts, drop_W1, drop_W2, drop_largest_cat and secondary are below 0.05. Only H_missing_0 (0.20) and drop_W3 (0.088) are not.
2. **L52, "16 параметров".** R2t has **14** parameters. No category reaches 10 observations among the 31, so the model has no category dummies.
3. **L39, "исключении семи наблюдений".** Seven are dropped from the panel, but Ribbon W2 already has g missing. Only **6** leave the R1 sample.
4. **Inconsistent robustness counting.** The H-tables count robustness runs only (for example "3 из 8"). The text counts include the main run: H_start "8 из 10", beta "из 10", hack "7 из 9". Hack is 7 of 9 with main, which is 6 of 8 robustness runs. Choose one convention and state it.

**Should fix (C10 / L101, "ни один ... не проходил порог $50 млн")**
- This is stated more firmly than data/missing_cg_fdv.csv supports.
  - Vertex W2 has a fully diluted value of **$81M**. The circulating figure relies on an external April-2024 estimate, not a value at 2024-10-01.
  - Kwenta W1 is 95.93 × 505,775 = **$48.5M**, not "about $45M" as C10 says.
  - Mars (W1 price 0.044) and BlueMove (W1 price 0.033, W2 price 0.059) have prices but no supply in the file, so no bound was computed for them.
- No script in the repo produces missing_cg_fdv.csv, and the file does not say whether its prices are point values or 7-day medians.
- Suggested wording: "no token clearly passes; Vertex W2 is borderline by circulating estimate; Mars and BlueMove unchecked." Add the script.

**Should consider (interpretation)**
- **The holder-share result is new, and it comes from a post-review fix.** C11 moves H_start from 0.34 (p 0.04) to 0.56 (p 0.0001) and flips H3. The fix itself is correct. But the text now calls it the main post-review correction and lists it among the effects that survive a multiple-testing correction (L99). Two points belong next to that claim.
  - H_start was not itself a pre-registered test. H3 was about ΔR².
  - The effect disappears without W3 (p 0.12), without g (R2 p 0.16), and with H missing set to 0 (p 0.07).
  - The same applies to beta, which is a control and not a hypothesis. "Survives correction" should read "would survive, but was not pre-registered". L110 (freeze it and test it on the next window) is the right response.
- **L20 in "Главное" still lists issuance and hacks as associations in the first clause.** They are qualified in the next sentence, which is acceptable. The safer order is to put the fragility first.
- **The audit now covers 19 of the observations in the sample.** Geodnet, which was classed "unclear", is out after C13, so the top-20 |u| list no longer matches the sample. This is minor. Say "20 checked, 19 in the final sample".

**Confirmed numbers in the new INTERIM_R4.md:**
- Sample 202 / 110, with 38/69/95 by window. Beat ETH 18/9/24%. Medians −27/−60/−42%.
- Shares 1.23/−0.26/0.03. corr(g, y) 0.55 (R² 0.30). corr(g, m) −0.89. sd ratio about 2.2. Pass-through 2.5%. Quintiles 16/24 and −80/−68.
- H2 −0.32 (p 0.14, 0/9). H3 ΔR² 0.046 (holds 1/9). H4 −0.06 (p 0.03, 4/9; drops to p 0.06 post hoc).
- H_start 0.56 (p 0.0001, n 135). 18% at a 30% holder share. 8/10. Without W3 0.28 (p 0.12). In R2 0.30 (p 0.16).
- Beta 38% (p 0.001).
- H5 0.21 (p 0.06, 3/8). H6 0.08 (p 0.18, 0/8). H8 n 31. Hack −30% (p 0.02).
- H2a −1.27 (p 0.02, 2/6). H2a-wide n 115, −1.26 (p 0.02, 3 of 5 frozen). H2b −0.44 (p 0.30, 1/7). H9 −0.34 (p 0.12), audited −0.50 (p 0.10).
- Post hoc: −1.45 (p 0.04) on the gross definition; NXM p 0.07; −0.84 (p 0.18).
- 48% unchanged supply; 21 of 55 decreasing. Audit 13/6/1.
- LDO −50/−46/−34, corrected multiples −46/−23/−16, fees −6/−29/−23, supply −1.9%. 25.0 / 19.42 / 7.7 / 17.3M.
- Peers: −50 vs −24 (5 peers), −46 vs −66, −34 vs −45. MC/revenue 43 → 12. Revenue −2%. Take rate 4.9 → 6.2%. Multiple −34% corrected vs −23% for peers.
- LST shares 88/74/50/53%. Ribbon, NFPrompt and ZORA −78 to −85%. Price check 1.9% / 12.9%. The frozen universe gives the same verdicts in stages 1 and 2.

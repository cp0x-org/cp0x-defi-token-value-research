# Independent review of the R6 validation study (R6V)

Reviewed 2026-10-07. No existing file was modified. Scratch recomputations are in /tmp/claude-0/review_r6v/ (re-fetched raw transfers in `refetch/`, recomputed family P in `work/data/proxy_P_review.csv` and `work/data/P_outflows_*.csv.gz`).

## Bottom line

The verdict holds. Neither family passes, and none of the problems below comes close to changing that.

- **P1** fails C1 (median |ln r| 0.797 against a limit of 0.336), fails C2 (1 of 4 protocols inside [0.5, 2]) and fails C3 (5 of 8 pairs). After the de-duplication fix, P1 has a median |ln r| of 0.792 and still has only 1 of 4 protocols inside the band. Uniswap's median r is 6.36 and Sky's is 0.15. Both come from structural causes (DAO→Uniswap Foundation funding transfers, and Sky payments that never touch the Pause Proxy), not from code errors.
- **B1** fails the coverage rule with 9 units against the 10 required. It would also fail C1 (0.754) and C2 (1 of 4, with Uniswap at r 20.25) even if coverage held.

One finding does need fixing before the report. It concerns explanations and diagnostic numbers, not the verdict. The Sky mechanism stated in `manual_variant.py` is wrong, and the Sky "manual" figures are driven by treasury moves rather than payments.

## 0. Integrity

- `sha256(METHOD_R6V.md)` = 4dfa38a8…0815, which matches `METHOD_R6V.sha256`. Frozen at 2026-10-07T09:18:12Z.
- `sha256(data/reported_spending.csv)` = 16882766…e9f6, which matches `data/benchmark.sha256` (written 09:31Z). The file times are consistent with the claimed order: CHANGES and the benchmark at 16:31 local time, proxy_B at 16:33, P from 16:5x on.
- `raw/treasury.js` is byte-identical to `registries/treasury.js` at the recorded commit 07a9a470 (I checked the sha256 against raw.githubusercontent). There is no `projects/treasury/{lido,aave,maker,sky,uniswap}.js` at that commit, so the registry is the whole adapter.
- `data/treasury_sets.json` matches the Ethereum `owners` of `treasury/lido`, `treasury/aave` (5 addresses), `treasury/maker` (the Pause Proxy) and `treasury/uniswap` (3 addresses) exactly. The own-token lists also match.
- The block range is exact. Block 16308190 is at 2023-01-01 00:00:11 UTC (the previous block is 2022-12-31 23:59:59), and block 24136052 is at 2025-12-31 23:59:59 UTC (the next block is 2026-01-01 00:00:11).

## 1. Implementation against the frozen method

| Item | Code | Deviation? | In CHANGES? |
|---|---|---|---|
| Treasury sets = adapter Ethereum owners | exact | none | n/a |
| P0 / P1 (a) same-tx inflow, (b) non-multisig contract, (c) burn / P1c | as specified | (b) "multisig" requires a 32-byte return with 0 < threshold < 1000, which is stricter than "returns a value". Code state is read at `latest`, not at transfer time. 21 spot checks found no misclassification. | no (note) |
| Price "at the transfer day" | the nearest DefiLlama point within ±3 days | DefiLlama points carry 23:59 or 00:00 timestamps, so some flows are priced one day off: 50 of 244 Lido P1 flows ($28.3M), 7,050 of 34,794 Aave flows ($23.9M), 67 of 352 Sky flows ($8.6M) and 5 of 25 Uniswap flows ($140.5M, including the $138M UF transfer, which still gets the 3/21 close of $6.79). The offset is never more than 1 day and the effect is a few percent. | no (note) |
| Unpriced count and share reported | `P_diagnostics.csv` | none, but the shares are dominated by spam (see §2) | n/a |
| **Share of the treasury held on other chains reported** | **not computed anywhere** | **missing output** | no |
| B: chain keys + -OwnTokens, aggregate OwnTokens excluded | yes | none. The Ethereum and Ethereum-OwnTokens token sets are disjoint for Lido, Aave, Sky and Uniswap (and for every other chain pair). They overlap only for Olympus, where OHM is in both. | n/a |
| B absent-token rule; price on day d, else d−1 when units_d = 0 | yes | The code also falls back to d−1 when the token has units on day d but no USD entry. This is minor. | no (note) |
| B coverage "series covers the whole period" | `start > earliest date of any chain key` | Coverage is tested on the earliest key, not on every key. For example, Lido's Solana keys start on 2023-07-04, inside the May–Dec 2023 unit. That case is harmless because of the absent-token rule. For Olympus the Ethereum key starts in 2021 but the OwnTokens key starts on 2023-02-05, so a 2023 unit would wrongly count as covered. | no |
| C1, C2 (ceil(0.8·n) → 4 of 4), C3 (≥ 2/3, ≥ 3 pairs), coverage (≥ 4 protocols, ≥ 10 units) | correct | C2 with 4 protocols follows V3 | V3 |
| Decision rule | both fail, so case studies | none | n/a |
| Diagnostic "manual cleaned P1" | `manual_variant.py` adds back same-tx outflows for Aave and Sky and drops Ecosystem Reserve and Incentives Controller as sources | The method defines the manual variant as P1 minus documented buybacks, liquidity, incentives and migrations. The code does something different: it removes the same-tx exclusion and filters by source address. Its rules were chosen after the results were seen. It cannot affect the verdict. | **no, should be logged** |
| `B1_noown` | extra diagnostic | not in the method, harmless | no |

## 2. Bugs and data checks

**S1 (should-fix). De-duplication drops real transfers.** Routescan `tokentx` rows have **no `logIndex`** (none of the 413,295 rows has one). The key used in `fetch_transfers.py` (and `drop_duplicates()` in `build_P.py`) therefore merges distinct Transfer logs that share the same (hash, from, to, value, token). I re-fetched every address without de-duplication. The extra rows are 124 for the Pause Proxy, 45 for the Ecosystem Reserve, 17 for the Collector, 7 for Aave Grants DAO, 5 for the Incentives Controller and 2 for the Lido Agent. I confirmed with receipts that these are genuine separate logs. For example, tx 0xe90da77c… pays the same 41.67 MKR to each of 4 delegates twice, and tx 0xe9ea2ed0… pays 216 GHO five times. The Sky outflows lost this way are 194.46 MKR and 216k DAI.

I recomputed P with a cross-file count-max de-dup. The effect on P1:
- Sky 2024: 35.28 → 35.68M.
- Aave: +3k, +8k and +4k in 2023, 2024 and 2025.
- Everything else is unchanged.
- C1 moves from 0.797 to 0.792. The fix is immaterial to the verdict.

A related point is that `call()` silently returns `[]` when the API answers status 0 with a list. My re-fetched counts equal the stored counts plus the duplicates, so no data was lost this time.

**Period boundaries.** These are correct. Days are UTC (`unit="s"`), the end date is inclusive, and the global window is [2023-01-01, 2026-01-01). B steps use the window (start, end+1], which matches daily snapshots.

**Native ETH and internal transactions.** These are handled correctly. Failed and zero-value transactions are dropped, and internal transfers are keyed by `traceId`. ETH outflows appear only for Lido. The largest is 20,304 ETH ($39.25M) from the Agent to the stETH contract on 2023-06-30, which is excluded as a contract and therefore affects P0 only.

**Pricing and decimals.** I spot-checked the 10 largest P1 flows per protocol. All implied prices are plausible for their dates:
- stETH at 4,004, 3,010 and 2,076.
- LDO at 3.63.
- AAVE at 211 to 353.
- WETH at 2,614.
- INST at 3.91.
- MKR at 1,608 to 2,819.
- UNI at 4.00, 6.79, 9.74, 10.60 and 10.76.
- USDC and GHO at 1.00.

I found no decimal errors.

**Spam.** One spam token got a price: MAGA, $6.7k, which appears in Uniswap P0 only and not in P1. Spam dominates the unpriced counts:
- Uniswap: 9,500 of 9,514 2024 outflows are univ4.com airdrop spam. They are sent from adapter address 0x3d30b1ab…, which is an airdrop-spam sender and not a treasury.
- Aave: about 31k "aavepad.com" transfers and 12k "nft-aave.com" transfers.
- Lido: 467 "RewardLido.com" transfers.

So the reported "share of transfers unpriced" overstates the real problem. The real unpriced tokens are aEthWETH (786 transfers, 3,938 units, about $12–15M), aWETH (545 units) and aBUSD. All of these sit in same-tx flows, so they leave P1 unchanged and understate P0 only.

**Recipient classification.** I checked 21 recipients with eth_getCode and getThreshold/getOwners. All are classified correctly:
- EOAs: 0x5069a6…, 0xb39cb7…, 0x37305b….
- Safes: 0xe571dc… (4 of 9), 0x2d994f… (4 of 9), 0x3c5142…, 0x95b521…, 0xcdb4fa…, 0x1c037b…, 0x834560…, 0xca5183… (3 of 8).
- Contracts: 0x7c8406… (storage slot 0 holds the Uniswap timelock address), the 0xfb6b91… and 0x8d2642… EIP-1167 clones, 0x3b560d…, the three 4,941-byte stETH recipients 0xf4f6…, 0x7c2a… and 0x3e2d…, 0x3ea64b…, DaiUsds 0x322573…, and UNI-V2 0x517f9d….

`recipient_class_old.json` and the final class file agree on every shared address.

**Same-transaction-inflow rule.** No outflow is flagged only because of a zero-value inflow. However, **every aToken transfer out of the Aave Collector is flagged**. Aave v3 aTokens emit `Transfer(0x0 → Collector, accrued interest)` inside the same transaction. For example, BGD payments 0x85a50cd8… and 0xd84d544a… each carry a 0x0→Collector aEthDAI log of $11 to $1,472.

I tested a rule-based fix that ignores 0x0 mints of a token the treasury also sends out in that transaction. Aave P1 rises from 16.2, 72.2 and 63.1M to 18.7, 90.7 and 172.2M (r 1.53, 3.80 and 6.87). Sky 2025 rises from 4.2M to 144.6M, because MKR→SKY conversions mint SKY. This makes the fit worse (C2 2 of 4, Uniswap still 6.36), so the rule is not hiding a passing proxy. See §5.

**B family.** The chain-key and -OwnTokens token sets are disjoint for all four benchmark protocols, so there is no double counting from that source. The large outflow days, however, contain material effects that are adapter artefacts or that are not spending (S2).

**S2 (should-fix: disclose in the report; B1 stays as frozen for the verdict).**
- **Sky:** the adapter lists DAI but not USDS. DAI→USDS conversions through DaiUsds 0x3225737a… therefore count as outflows: **$104.9M in 2024 and $216.5M in 2025**. For example, on 2025-08-26 DAI fell by $62.1M. Without them, Sky B1 is about 42M in 2024 (r 0.60 instead of 2.12) and about 300M in 2025. The 2025 figure also contains 1.977B SKY ($121.5M) moved to Safe 0xca5183… on 2025-08-25, and a $34.6M SKY burn on 2025-06-30.
- **Lido:** 2025-12-19 shows −$9.2M of DAI and USDC. The benchmark notes describe this as a sUSDS conversion, which the adapter does not track either.
- **Uniswap:** 2025 B1 ($810M) includes the 100M UNI UNIfication burn on 2025-12-28 ($600.5M). B has no burn exclusion. Without the burn, B1 is about $209M (r ≈ 10).
- **Aave:** 2025-11-04 (−$21.7M aEthWETH) is a real transfer of 6,000 aEthWETH to 0xaa2461… on 11-03, not an artefact.

None of these brings B within C2: Uniswap stays ≥ 10× and Aave 4.9×. B also fails coverage regardless.

## 3. Benchmark

Every figure is supported by the bench notes, and the arithmetic is correct:
- **Aave**: 12,130,218 + 54,620 = 12,184,838; 22,069,698 + 1,810,000 = 23,879,698; 24,146,813 + 917,900 = 25,064,713. One note: Service Providers comes from the precise JSON values, while Other Expenses comes from rounded display values, so the error is under $5k.
- **Lido**: 28.8 + 9.7 + 1.5 + 0.9 = 40.9. For 2025 the components sum to 40.6 against a stated total of 40.7, which is rounding in the source. The May–Dec 2023 figure of 12.5M is LCG-only, and December is partly forecast. Both points are noted.
- **Sky**: 17.08 + 20.26 + 21.11 + 2.85 + 12.41 = 73.71. The 2023 figure of 53.7 includes MKR token expenses of 15.4. The appendix of the same report says 11.7, which is noted.
- **Uniswap**: 3.16 + 3.56 = 6.72; 9.9 + 5.79 = 15.69; 11.0 + 9.7 = 20.7.
- Partnerships, GHO and integration payments are excluded per V2.

Points to note (none changes the verdict):
- (i) Uniswap 2023 excludes $0.36M of legacy UGP grants that were actually disbursed. That money is grants paid, so 7.08M is arguably the consistent figure. It moves r from 6.36 to 6.04.
- (ii) The Sky 2025 alternative vintage is 67M.
- (iii) **CHANGES V1 is inaccurate.** It says Olympus's only actual is FY2025. In fact OIP-155 reports FY2023 (Jan 2023–Jan 2024, a 13-month period inside the window) as the 5.98M budget "executed with a savings … $817k", which implies an actual of 5.163M. That figure is derived, so excluding it is defensible, but the stated reason should be corrected. Including it would not change the verdict. P has no Olympus treasury set. The B1 unit would be $129.8M (r ≈ 25), and it would be wrongly marked covered with OHM double-counted (see §1).

## 4. Could any finding flip the verdict?

No. Effect sizes on the primary statistics:

| Change (scratch) | P1 median \|ln r\| | P1 protocols inside [0.5, 2] | B1 |
|---|---|---|---|
| as published | 0.797 | 1/4 (aave 2.52, lido 1.55, sky 0.15, uni 6.36) | 9 units, coverage fail; 0.754; 1/4 |
| de-dup fix (S1) | 0.792 | 1/4 (unchanged medians) | n/a |
| + aToken accrual fix | 0.556 | 2/4 (aave 3.80, sky 0.82) | n/a |
| benchmark alternatives (UF 7.08M, Sky 2025 67M) | 0.792 | 1/4 (uni 6.04) | n/a |
| B Sky without DAI→USDS conversions; Uniswap without the burn | n/a | n/a | still 9 units; uni about 10×, aave 4.9× |
| add Olympus FY2023 unit | P: no unit | n/a | 10 units, 5 protocols; Olympus r ≈ 25; C2 1/5 |

## 5. Are the per-protocol explanations supported?

**Lido (committee pre-funding, LDO to vesting): the first part is supported, the second is not.** P1 is $63.4M in 2024 and $63.0M in 2025, against reported figures of $40.9M and $40.7M. Almost all of it goes to Safes that draw funds ahead of spending:
- 0x95b521… received $32.3M in 2025, in USDC tranches of $2M.
- 0x9b1ceb… received $18.8M in 2024.
- 0x87d93d… received $11.2M and $8.3M, in stETH.
- PML 0x17f6b2… received $9.4M in 2024.
- LEGO 0x12a43b… received $1.25M and $1.12M.
- Part of this is liquidity funding (stETH), which the benchmark excludes: Liquidity Rewards were $11.2M in 2024 and $4.8M in 2025.

The LDO goes to a 4-of-9 Safe, 0x834560… ($3.3M, $12.8M and $6.8M; for example 735,138 LDO on 2024-02-26), **not to a vesting contract**. A vesting contract would have been excluded as "contract" anyway. Say "LDO to a committee/TRP multisig" unless the Safe is identified.

**Aave: the Ecosystem Reserve part is partly supported, the stream-withdrawal mechanism is wrong.** Ecosystem Reserve P1 is $12.3M, $39.8M and $50.2M for 2023–25, against the Staking line of $28.7M, $39.7M and $49.8M. Of that, `claimRewards` transactions account for $4.9M, $18.0M and $25.4M, which are clearly Safety Module rewards. Safe `execTransaction` calls account for $6.5M, $19.5M and $20.1M, which could be Safe-held reward claims or service-provider AAVE allowance pulls. The data do not settle which.

On the Collector side, the claim that "stream withdrawals [are] flagged as same-tx-inflow" does not match the data. `withdrawFromStream` explains only $0.47M of the Collector's flagged outflows. The real mechanism is the aToken accrual mint (§2): every aToken payment is flagged, whatever function calls it. The flagged volume is dominated by `execTransaction` ($238M in 2025), `transmit` ($53.7M and $47.7M) and `executePayload` (swaps, migrations and payments).

**Sky (payments minted via Vat.suck and forwarded in the same tx): refuted. This is the must-fix.** `sendPaymentFromSurplusBuffer` calls `vat.suck` and then `DaiJoin`/`UsdsJoin.exit(target)`, which mints DAI or USDS **directly to the recipient**. For example, tx 0xe90da77c… mints 4.5M DAI from 0x0 straight to 0x3c5142…. Those payments never appear as Pause Proxy transfers, so neither P1 nor the manual variant can see them. That explains why Sky P1 is MKR-only: P1c is 0 in every year.

The manual variant's Sky figures are not payments:
- 2024: $720M = $663.7M USDC + MKR. The USDC part is the PSM swap described below.
- 2025: $145M, of which $121.5M is the SKY move to Safe 0xca5183…. Only $1.26M is not own-token.

The statement in `manual_variant.py`, and any text built on it, should be corrected. The Sky manual figures (r 10.4 and 1.97) should be dropped or relabelled.

**Uniswap (lumpy DAO→UF transfers): supported.**
- 2023-10-20: 10,685,984.71 UNI ($42.74M) went to the UF custody Safe 0xe571dC… (4 of 9). UF reports receiving $43.41M in 2023.
- 2025-03-21: 20,320,405 UNI ($137.98M) went to **0x5069a6…, which is a genuine EOA**. It is UF-controlled. On 03-10 it received a 10 UNI test transfer from 0xe571dC… and returned 0.1 UNI on 03-11. On 03-21 it forwarded the UNI onward in roughly 5M UNI chunks. This matches UF's "UNI 20.3M" Unleashed receipt, booked at $140M.
- 2025-09-10: 1,583,493 UNI ($15.42M) went to the DUNI Safe 0x2d994f…. This is a legal and tax prefund.
- Without these transfers, P1 is about $0 in 2023 and about $2.9M in 2025, against UF spend of $6.72M and $20.7M. P measures the DAO's funding of UF, not UF's spending, because UF wallets are not in T. This is structural.

**Sky 2024 ~$664M USDC to 0x37305b… (EOA).** These are three `cast()` spells:
- 20.0M on 2024-07-30.
- 401.6M on 08-26.
- 242.4M on 10-07.

In each spell, DAI is burned into the PSM, USDC comes back from the USDC PSM join 0x0a5964…, and the USDC is forwarded to the EOA. The EOA then trades through CoW (GPv2Settlement). This is a treasury or RWA allocation, not spending. P1 excludes it correctly through the same-tx rule. Only the manual variant counts it, and P0 counts the move twice: $663.4M of DAI burned plus $663.7M of USDC.

## Findings by class

**Must-fix** (diagnostic numbers and explanations; verdict unaffected)
1. The Sky mechanism is wrong (direct mint to recipients). The Sky manual-variant figures are driven by the $664M USDC RWA allocation (2024) and the $121.5M SKY treasury move (2025), so they must be corrected or dropped before the report.

**Should-fix**
1. S1: de-duplication drops real repeated transfers because tokentx has no logIndex. P1 changes by +$0.40M for Sky 2024 and less than $10k for Aave.
2. S2: disclose the B artefacts. These are the Sky DAI→USDS conversions ($104.9M and $216.5M), the Lido sUSDS conversion ($9.2M), the Uniswap 100M UNI burn ($600.5M) and the SKY move ($121.5M).
3. Report the non-Ethereum share of the treasury, which the method requires. Computed from the DefiLlama series at 2024-01-01, 2025-01-01 and 2025-12-31: Aave 14.0%, 7.6% and 16.4%; Lido 0.4%, 1.0% and 0.0%; Sky 0.0%, 0.0% and 0.2%; Uniswap 0%.
4. Correct the Aave explanation. The cause is aToken accrual mints, not stream withdrawals; the rule-based fix worsens the fit.
5. Log in CHANGES that `manual_variant.py` departs from the method's definition of the manual variant.
6. Correct the Olympus reasoning in CHANGES V1. Also, B coverage should be tested for each key.

**Note**
1. Prices use the nearest point within ±3 days, which in practice means a 1-day offset with a few-percent effect.
2. The multisig test is stricter than the method, and classification uses `latest` state.
3. B falls back to the d−1 price when a token has units on day d but no USD entry.
4. The unpriced-share diagnostic is mostly spam.
5. The Lido explanation should say "LDO to a multisig", not "to vesting".
6. Uniswap's legacy UGP grants ($0.36M) are excluded from 2023.
7. `fetch_transfers.call` silently returns `[]` on some API errors.
8. Stray files remain (`P_diag_part3.csv`, `proxy_P_part3.csv`, an empty `build_P_aave.log`). `manual_variant.py` rewrites `data/recipient_class.json` after `proxy_P.csv` was produced.

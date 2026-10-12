# Uniswap (DAO and Uniswap Foundation): case-card inputs for the decision table (Research 6)

Compiled 2026-10-07 under METHOD_R6.md (sections "Чьи расходы", "Три класса", "Отбор решений"). Companion file: `uniswap_decisions.csv` (30 rows). Format follows the frozen Lido table.

Sources used:
- gov.uniswap.org forum topics (raw endpoints `https://gov.uniswap.org/raw/<id>`, including the images in those posts).
- Snapshot space `uniswapgovernance.eth`. I pulled every proposal that ended 2022-10..2025-12 through the hub.snapshot.org GraphQL API (124 proposals) and screened them all.
- On-chain Governor Bravo `0x408ED6354d4973f66138C91495F2f2FCbd8724C3`. I pulled all `ProposalCreated` and `ProposalExecuted` logs from block 15.65M to 24.4M through the eth.blockscout.com API, which covers proposals #25–#93. I decoded the calldata to get UNI amounts and recipients.
- The UF summary financials for 2023, Q1–Q3 2024, FY2024, Q1–Q3 2025 and FY2025.
- The UAC Season 2 and Season 3 reports.
- `/home/claude/r6v/bench/uniswap.md`, used for cross-checks.

## 0. Blinding log

- I used no price, TVL, fee, revenue, volume or market-share series. I opened no DefiLlama, CoinGecko, Dune, Gauntlet, Forse or Merkl dashboards. I opened nothing under /home/claude/r4, r4rep, r5 or r6v/data.
- Incidental exposure, recorded for the auditor. None of it is recorded in the CSV or used for selection.
  - (a) **UNI prices in proposal texts.** Many proposals quote a contemporaneous UNI price or TWAP so they can convert a USD request into UNI. These appear in topics 17499 and 22020 and in on-chain proposals 59, 60, 65, 66, 70, 73, 76, 80, 83, 86, 87 and 90. The UAC S2 and S3 reports quote the prices they used for account balances. I read these in passing. I did not use any of them to convert UNI amounts, so UNI-only decisions are marked "USD not stated".
  - (b) **Implied UNI price in UF reports.** The Q1, Q2 and Q3 2025 and FY2025 UF reports give the USD market value of UF token holdings at each quarter end, plus the year-end market value of the 20.3M UNI received under Unleashed. Both imply UNI prices after the decisions. The bench file repeats the year-end figure. Read, not used.
  - (c) **Usage and TVL figures inside proposals.** Proposal texts contain pre-decision usage, volume and TVL figures:
    - UNIfication: cumulative protocol volume, plus Unichain annualised DEX volume and sequencer fees.
    - BoB, Gnosis, Celo, Mantle and X Layer proposals: chain-level Uniswap TVL and volume, with DefiLlama and Dune links that I did not open.
    - The Forse proposal (#72): per-chain volume table.
    - "Mobilizing the Uniswap Treasury": treasury USD value.
    - LTIPP thread 24066: a pointer to "basic metrics from the previous initiative" (the 2023 Arbitrum programme). I did not read that block.
  - (d) **Evaluative statements in the UAC S3 report.** The report says some URGP campaigns "were successful, while others were not" and links a Forse results dashboard, which I did not open.
  - (e) **"Impact" column in UF FY2024 grant tables.** This column reports outputs. Only the forward-looking "Target:" entry for Atrium Hook Incubator #2 is used, as an expected metric.
  - (f) **UAGP review and extension posts.** These contain ARB price commentary and grantee volume KPIs. Only the stated budget ("~$1.1m in USDC terms") is used.
- The CSV does not say whether any decision "worked".

## 1. Denominators (levels 1+2) and treatment rules

**Levels.**
- Level 1 is the DAO: direct treasury payments to grantees, the UAC-escrowed programmes, and DAO-funded incentives.
- Level 2 is the Uniswap Foundation, plus DAO-funded committees: the UAC, the UADP/UAGP, the UTWG and the Delegate Reward WG. DUNI becomes part of level 2 from 2025-09.
- Level 3 is Uniswap Labs (see below).
- Transfers from the DAO to the UF ($43.41M booked in 2023; 20.3M UNI in 2025) are **funding, not spending**. Spending is what the UF reports as grants disbursed plus opex accrued. The decision to fund the UF still appears as a class A budget decision (UNI-2023-A1, UNI-2025-A1), in the same way the Lido table treats grants to BORG foundations.

**Liquidity incentives.** DAO-funded incentive programmes are class A "incentives to users/integrations" at level 1 (DAO) or level 2 (UF). They include:
- UNI from the treasury distributed by the UAC (URGP onboarding packages, the Gnosis, Sonic, Celo and BoB packages, and LTIPP matching);
- the $45M Gauntlet-managed Aera-vault programme for v4 and Unichain (proposal 82);
- the 2M ARB CLIP programme, paid from the DAO's own ARB airdrop;
- UF incentive-type grants (Gauntlet v4 Ecosystem Liquidity Campaign, Morpho and EulerSwap lending incentives, router rebates).

Gauntlet, Merkl and OpenBlock fees for running a programme are counted with that programme. Oku front-end integration costs inside onboarding packages are counted with the package, as the UAC does. **Excluded as third-party money:**
- partner-chain matching (MANTA, GLMR, S, CELO, BOB and OP commitments);
- Arbitrum's 1M ARB LTIPP grant;
- the 2022–23 Optimism-funded OP liquidity-mining programme.

**Execution year.** A decision's year is the year its execution starts. UF grant decisions are dated by the quarter in which the UF reports the commitment.

| Decisions in | Denominator year | Figure used (USD) | Type | Composition | 10% | 5% |
|---|---|---|---|---|---|---|
| 2023 | 2022 | **25.46M**, FLAGGED: no full 2022 year exists (the UF started in Aug 2022), so per the method the approved budget of the current year (2023) is used | approved 2023 budget (proxy) | UF ops for 2023 per the Create-UF budget table: Year 1 H2 $2.02M + Year 2 H3 $2.17M = 4.19M; UF grants $60M ÷ "approximately 3 years" = 20.0M (my division); UAC "maximum estimated budget ... $170,000 for a year" = 0.17M; UAGP "~$1.1m in USDC terms" = 1.1M. CLIP 2M ARB excluded (USD not stated) | 2.546M | 1.273M |
| 2024 | 2023 | **7.11M**, FLAGGED as a lower bound | actual (unaudited UF) + DAO-level items with stated USD | UF grants disbursed 3.16 + legacy UGP grants 0.36 + UF opex 3.56 (= 7.08), plus UAC Season 1 payroll ~0.03. Excluded because no USD is stated: the 2023 share of CLIP (2M ARB, paid out over 8 months from Sep 2023) and of UAGP (Oct 2023 start, ARB) | 0.711M | 0.356M |
| 2025 | 2024 | **22.59M**, FLAGGED: DAO-level part partly derived | actual UF + DAO-level reported figures | UF grants disbursed 9.9 + opex 5.79 (= 15.69); DAO incentives ~6.0 ("A total of ~$6 million was distributed via the UAC as of January 20, 2025", UAC S3); governance 0.478 (delegate reward cycle 1 $216k, Delegate Reward WG retro $64k, UAC S2 payroll + overtime $72k, UAC S3 Oct–Dec ≈ $66k derived from "$132k" Oct–Mar, UTWG $60k); AlphaGrowth $420k "disbursed ... upon passing" | 2.259M | 1.129M |
| (reference) | 2025 | UF only: 20.7M (grants 11.0 + opex 9.7) | actual UF | DAO-level 2025 actuals not reported (§7) | – | – |

Notes and sensitivity:
- **2022.** The partial actuals that exist are UF opex for Q3–Q4 2022 of $0.92M and UF grant commitments for 2022 of $2.78M (disbursements not reported). Using them would make almost every 2023 item selectable, which would not be meaningful. The proxy is circular in one respect: the UF's own Oct-2023 re-sizing is UNI-2023-A1. Under the proxy, CLIP (2M ARB; about $2M if valued at the UAGP's own stated inception conversion) is 7.9% and is not selected. If the 2023 actual (7.11M) were used for the 2023 decisions, CLIP and UAGP would be selected.
- **2023.** Adding the CLIP 2023 share would raise the denominator, and three rows would then drop below 10%: UNI-2024-A4 LTIPP at $7.5M, UNI-2024-A13 TLDR at $8.21M, and UNI-2024-A10 OpenZeppelin at $8.5M. These are flagged in the CSV.
- **2024.**
  - The incentive figure is the UAC's cumulative "~$6M" through 2025-01-20. It may include LTIPP matching, and it covers 20 days of 2025.
  - The lower alternative is "over $4M of DAO-funded UNI" deployed by mid-Aug 2024 (UAC S2) plus Gnosis $0.25M. That gives a denominator of about 20.6M and a 10% threshold of 2.06M.
  - The upper alternative adds LTIPP $0.75M, UAGP about $0.6M (ARB-funded, mostly 2024) and delegate cycle 2 Sep–Dec (about $0.36M). That gives about 24.3M and a threshold of 2.43M.
  - Only one selection changes across this range. The UF commitment "Unichain Partners - 2025" ($2.09M) would be selected under the lower alternative (§6).
- **Excluded from all denominators:** UF employee token awards in UNI (0.15M / 0.28M / 0.45M UNI, no USD given), the DEF grant (1M UNI, no USD), and the UF's 2024 interest income ($1.11M), which is not netted.
- **Level 3 (Uniswap Labs).** No Labs spending figures were found in governance sources. Labs is a private company. UNIfication makes Labs DAO-funded from 2026-01-01 (20M UNI per year; row UNI-2025-A5). A 2026 forum post (topic 26160) mentions a "$15.5M Uniswap Labs bug bounty program operated by Cantina" with the UF as "funder-of-record". I did not verify this; it does not appear in UF grant commitments and is not used. Labs is noted as a limitation only.

## 2. Mapping table: report categories to our class A line items

Written before the numbers in §3 were filled in.

| Report / source category | Source | Our line item |
|---|---|---|
| UF opex: Payroll | UF 2023, FY2024, FY2025 reports | contributors/core team (excludes UNI token awards) |
| UF opex: Contract & professional fees; Office; Insurance; Internal Ops | same | legal/ops (contract fees include "technical audit", which cannot be separated) |
| UF opex: External events; Advertising & marketing; Hackathons | same | marketing/growth |
| UF grants 2023: Protocol Growth – Interfaces, DevX, Integrations; Protocol Growth – Protocol Development; R&D – Protocol; R&D – Incentive Programs; legacy UGP grants | UF 2023 report (pie shares) | grants |
| UF grants 2023: Incentive Programs | same | incentives to users/integrations |
| UF grants 2023: Community Growth | same | marketing/growth |
| UF grants 2023: Governance Stewardship | same | governance |
| UF grants 2024: Developers, Research, Protocol, Innovation | FY2024 report (pie shares) | grants (incentive-type items inside Protocol/Innovation cannot be separated in 2024) |
| UF grants 2024: Security | same | security |
| UF grants 2024: Governance | same | governance |
| UF grants 2025, item level: Community / sponsorships | 2025 quarterly disbursement tables | marketing/growth |
| UF grants 2025: Areta Security Fund / audit subsidy, security audits, v4 hook audits, Security category | same | security |
| UF grants 2025: lending incentives (EulerSwap, Morpho), v4 Liquidity Campaign, v4 Ecosystem Liquidity Campaign, gas and router rebates, Gauntlet Incentive Optimization | same | incentives to users/integrations |
| UF grants 2025: DUNA legal review; Cooley legal-entity exploration | same | legal/ops |
| UF grants 2025: other Governance items (Agora, Butter, governance audits/UX, Blockful, Certora, Chainsecurity, Scopelift) | same | governance |
| UF grants 2025: Developers, Research & Implementation, Infrastructure, Hook Design Lab (development), Unichain Growth (non-incentive), Morpho CFM winner | same | grants |
| DAO: URGP onboarding packages, chain incentive packages, LTIPP matching, CLIP (ARB), $45M Aera vault | UAC reports; proposals 45, 59, 60, 65, 66, 76, 77, 82, 84 | incentives to users/integrations (incl. Merkl/Gauntlet/Oku costs of the package) |
| DAO: delegate rewards, Delegate Reward WG, UAC payroll/ops, UTWG, Tally grant, Forse analytics | UAC reports; proposals 37, 62, 64, 68, 70, 74, 80, 86, 87 | governance |
| DAO: Growth Program Trial (AlphaGrowth, UEII success fees) | proposal 73 | marketing/growth |
| DAO: DEF grant, DUNI legal/tax prefund, Cowrie | proposals 63, 90 | legal/ops |
| DAO: UAGP grants (ARB) | 47, 24372 | grants |
| DAO: UNIfication growth budget to Labs | 93 | contributors/core team incl. development |
| Unichain Integration Partners (UF) | FY2024, Q4 2025 | incentives to users/integrations (payments to integrate Unichain); assignment to be confirmed, the alternative is grants |

## 3. Class A line items by year (USD M)

| Our line item | 2022 (partial, UF from Aug) | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| contributors/core team | 0.48 (UF payroll Q3–Q4) | 1.933 | 3.150 | 5.040 (+ growth budget to Labs from 2026, not in 2025) |
| grants | commitments 2.78 (disbursed n/a) | 2.749 (UF 2.389 + legacy UGP 0.36); UAGP ARB n/a | 6.732 (pie: Research 21%, Protocol 11%, Developers 28%, Innovation 8% of 9.9); UAGP about 0.5 excluded | 6.094 |
| security | – | not separable (inside contract fees) | 1.980 (Security 20% of 9.9) | 2.437 |
| incentives to users/integrations | n/a (OP LM was Optimism-funded) | 0.436 (UF Incentive Programs 13.8%); CLIP 2,000,000 ARB, USD not stated | ~6.0 (UAC; may include LTIPP 0.75) | UF 0.981 actual; DAO $45M vault approved, actual not reported; UAC 2025 packages not reported |
| governance | n/a | 0.144 (UF 0.114 + UAC S1 ~0.03) | 1.765 (UF 1.287 + DAO 0.478) | UF 0.863; DAO budgets ≈1.22 (Tally 0.25, delegate cycle 3 0.54, UAC S4 0.37, Forse 0.06), actual not reported |
| marketing/growth | 0.004 + events 0.009 | 0.484 (UF Community 0.221 + events 0.128 + adv. 0.107 + hackathons 0.028) | 0.920 (UF 0.50 + AlphaGrowth 0.42) | 0.751 UF (+ UEII success fees ≈0.205 paid Feb/Apr 2025, "41% of its budget") |
| legal/ops | 0.425 | 1.364 | 2.150 (+ DEF 1M UNI, USD n/s) | 4.491 (opex 4.12 + UF legal grants 0.371) (+ DUNI prefund spending n/s) |
| **total (levels 1+2)** | **not a full year** | **7.11** (+ARB programmes) | **22.59** (line items sum to 22.70: UF pie shares sum to 101% and opex sub-items to 5.80 vs 5.79) | **UF 20.7; DAO-level not determinable** |

Derivations:
- 2025 UF grant split, summed by me from the four quarterly item tables:
  - Q1: grants 1.416, security 0.138, incentives 0.023, governance 0.220, legal 0.045, marketing 0.271.
  - Q2: grants 2.790, security 1.030, incentives 0.638, governance 0.271, legal 0.175, marketing 0.001.
  - Q3: grants 0.825, security 0.636, incentives 0.050, governance 0.300, legal 0.131. The source's Q3 Governance subtotal ($530,716) exceeds its rows by $61,250; the difference is kept under governance.
  - Q4: grants 1.063, security 0.633, incentives 0.270, governance 0.072, legal 0.020, marketing 0.030.
  - The total is 11.047, against 11.0 reported.
- 2025 opex comes from the FY'25 table: payroll 5.04, contract 2.32, office 1.58, insurance 0.22, events 0.29, advertising 0.16, which sums to 9.61 against 9.7 reported. The Q4 advertising figure (0.3) exceeds the FY figure (0.16) in the source.

Line-item change test (more than 25% year on year and at least 5% of the denominator):
- **2022→2023:** not testable, because 2022 is a partial year.
- **2023→2024** (5% = 0.356M):
  - Selected: contributors +1.217 (+63%, LI1); grants +3.983 (+145%, LI2); incentives +5.564 (LI3); governance +1.621 (LI4); marketing/growth +0.436 (+90%, LI5); legal/ops +0.786 (+58%, LI6).
  - Security cannot be tested, because 2023 security is not separately reported. Auditor candidate: 2024 UF security grants of 1.98M created as a new category.
  - Caveats: the UF changed its grant categories between 2023 and 2024, and 2023 incentives exclude the ARB-funded CLIP.
- **2024→2025** (5% = 1.129M):
  - Selected: contributors +1.89 (+60%, LI1); legal/ops +2.341 (+109%, LI2); incentives (LI3), based on the ceiling ($45M approved; 2025 actual not reported), flagged in the same way as the Lido precedent.
  - Not selected: grants −0.64 (−9%); security +0.457 (+23%); governance (UF −0.42; DAO 2025 actual not reported, budgets suggest roughly +17%); marketing about +0.04.

## 4. Selected decisions (summary; details in the CSV)

| id | class | amount USD | materiality | rule |
|---|---|---|---|---|
| UNI-2023-A1 UF second tranche | A | 46.2M | 1.815 | ≥10% (proxy denominator) |
| UNI-2024-A1 URGP wave 1 (8 chains) | A | 3.5M | 0.492 | incentives ≥10% |
| UNI-2024-A2 Onboarding Package Bundle | A | 1.25M | 0.176 | incentives ≥10% |
| UNI-2024-A3 DeFi Education Fund | A | n/s (1M UNI) | not computable | ≥10%, provisional |
| UNI-2024-A4 Arbitrum LTIPP matching | A | 0.75M | 0.105 | incentives ≥10%, sensitive |
| UNI-2024-A5 Growth Program Trial | A | 0.92M | 0.129 | ≥10% |
| UNI-2024-A6 UF: Auditless Protocol Grants | A | 1.2M | 0.169 | ≥10%, UF level 2 |
| UNI-2024-A7 UF: v4 audits | A | 1.654M | 0.233 | ≥10%, UF level 2 |
| UNI-2024-A8 UF: Atrium Hook Incubator #2 | A | 1.41M | 0.198 | ≥10%, UF level 2 |
| UNI-2024-A9 UF: Areta Security Fund | A | 1.2M | 0.169 | ≥10%, UF level 2 |
| UNI-2024-A10 UF: OpenZeppelin Hooks Library | A | 0.85M | 0.120 | ≥10%, UF level 2, sensitive |
| UNI-2024-A11 UF: Unichain Integration Partners 2024 | A | 1.56M | 0.219 | incentives ≥10%, UF level 2 |
| UNI-2024-A12 UF: Gauntlet incentive optimisation + v4 campaign | A | 1.247M | 0.175 | incentives ≥10%, UF level 2 |
| UNI-2024-A13 UF: TLDR | A | 0.821M | 0.115 | ≥10%, UF level 2, sensitive |
| UNI-2024-LI1..LI6 | A | +1.217 / +3.983 / +5.564 / +1.621 / +0.436 / +0.786 | 0.171 / 0.560 / 0.783 / 0.228 / 0.061 / 0.111 | line-item |
| UNI-2025-A1 Uniswap Unleashed | A | 120.5M | 5.334 | ≥10% |
| UNI-2025-A2 v4 + Unichain incentives ($45M) | A | 45.0M | 1.992 | incentives ≥10% |
| UNI-2025-A3 DUNI + prefund | A | 16.575M | 0.734 | ≥10% |
| UNI-2025-A4 UF: Unichain Integration Partners Q4 2025 | A | 4.018M | 0.178 | ≥10%, UF level 2 |
| UNI-2025-A5 UNIfication growth budget (40M UNI over 2 years) | A | n/s | not computable | ≥10%, provisional; spending starts 2026 |
| UNI-2025-LI1 / LI2 / LI3 | A | +1.89 / +2.341 / +39.98 (ceiling) | 0.084 / 0.104 / 1.770 | line-item |
| UNI-2025-B1 UNIfication fee switch → burn | B | n/a | n/a | every class B |
| UNI-2025-B2 UNIfication 100M UNI burn | B | n/a | n/a | every class B |

Notes:
- **One vote, three rows.** UNI-2025-A5, B1 and B2 come from one on-chain proposal (#93, executed 2025-12-27). They are split because they are distinct instruments: a spending budget, a fee switch and a one-off burn. The reviewer may merge them.
- **B1 execution date.** It is the on-chain execution: v3 factory ownership passes to the fee controller, and v2 `feeTo` is set to TokenJar. Pool-level v3 fee activation and the start of fee collection were not checked, because doing so would require looking at fee data.
- **A5 inclusion.** The vote and the UNI approve() executed inside the period, but vesting and spending start 2026-01-01. A5 is included provisionally, and the reviewer should decide whether it counts as executed in-period.
- **UF level-2 rows (A6–A13, 2025-A4).** These are UF-internal grant commitments, not DAO votes. The amounts are commitments as restated in the FY tables, not disbursements.

## 5. Class C decisions (descriptive, no threshold)

| # | Decision | Approved | Executed | Size (as stated) | Source |
|---|---|---|---|---|---|
| C1 | Delegation of 10M treasury UNI via Franchiser to 7 "active but underrepresented" delegates, with a 1-year term and an 80% participation requirement. Voting power only, no spending | Snapshot 2023-11-06 and 2023-11-22 (competition) | on-chain #54 executed 2023-12-15 | 10,000,000 UNI approved to Franchiser factory | gov.uniswap.org/t/22397 |
| C2 | UF treasury diversification policy (level 2): stablecoins, 6 months of cash in an FDIC-insured account, the remainder in "a low-risk yield bearing asset"; UNI kept for employee awards | inside UNI-2023-A1 | 2023-10 onward | – | 22020 |
| C3 | UAGP committee swaps 599k ARB to USDC to secure runway (committee-level) | committee decision, Feb 2024 | 2024-02-29 | 599k ARB → 1.195M USDC (as stated) | 23369 |
| C4 | Mobilizing the Uniswap Treasury: creates the Uniswap Treasury Working Group (research on treasury management); report delivered Dec 2024 | Snapshot 2024-03-31; election 2024-04-20 | #62 executed 2024-05-07 | 6,000 UNI ($60k payroll; class A governance spend, below threshold) | 23397, 25467 |
| C5 | UF (level 2) takes a loan against 5M UNI collateral "to access immediate fiat (USD) liquidity while minimizing market impact", and plans to hold "~50% of requested funds in UNI in the near term" | UF decision; Unleashed FAQ | Q1 2025 | $29M loan / 5M UNI collateral | 25622, 25251 |
| C6 | Treasury Delegation Round 2 and GLI Treasury delegation Round 2 (re-delegation of treasury UNI) | Snapshots 2025-04-01, 2025-04-29, 2025-09-07; elections 2025-10-04 | execution not verified (no Governor proposal in 2025) | not stated in the Snapshot titles read | Snapshot 0x04af1fcb…, 0x46fef087…, 0x0d56ae30…, 0x9a52a7fc… |
| C7 | GLI Incentivized Delegation Vaults | Snapshot 2025-09-07 (For 17.29M / Against 5.03M) | execution not verified | – | Snapshot 0x14237319… |
| C8 | Discretionary budget: allow the UAC to spend account surpluses on co-incentive campaigns (no new funds) | Snapshot 2024-12-24 | – | – | Snapshot 0x90fab9ab… |
| C9 | Structure of the $45M incentive budget: the DAO-owned Aera vault, from which governance "can withdraw unspent funds at any time" | with UNI-2025-A2 | 2025-03-21 | 7,588,532 UNI | 25250 |
| C10 | DUNI prefund held as a reserve in a DUNI-owned wallet (spending is class A, UNI-2025-A3; actual use not reported) | with UNI-2025-A3 | 2025-09-10 | 1,583,493 UNI | 25770 |
| C11 | UNIVesting: "UNI stays in treasury until vested and unvested UNI can be cancelled" | with UNI-2025-A5 | 2025-12-27 | 40,000,000 UNI approved | 25881 |

Not in period or not executed:
- The Ekubo investment Temperature Check passed (2023-10-28), but no on-chain proposal was found, so it was not executed.
- Unisocks liquidity migration (UNIfication item 8): not among the 8 on-chain calls of #93.

## 6. Considered and rejected (one line each)

Thresholds: 2023 = 2.546M / 1.273M; 2024 = 0.711M / 0.356M; 2025 = 2.259M / 1.129M.

**2023**
- Create the Uniswap Accountability Committee (Snapshot 2023-03-03; #37 executed 2023-04-23; 14,333 UNI; "maximum estimated budget ... $170,000 for a year"): 0.7%.
- Fund Combined Liquidity Incentivization Program, CLIP (#45 executed 2023-09-02; 2,000,000 ARB from the DAO's ARB airdrop; Gauntlet fee 150k ARB, OpenBlock 15k ARB): USD not stated. At the UAGP's own stated inception conversion it is about $2M, or 7.9%, so it is not selected. **Sensitive:** it would be selected against the 2023 actual.
- UNI-ARB Grant Program and Protocol Delegate Program (#47 executed 2023-09-22; 1.1M ARB for grants, "~$1.1m in USDC terms", plus 1.1M ARB for Arbitrum governance participation): 4.3%. The delegation half carries no spending.
- ARB Distribution Proposal Poll (Snapshot 2023-07-04): a poll, implemented through #45 and #47.
- Delegation of 10M UNI (#54): class C (C1).
- Turkey earthquake relief 80k UNI (Snapshots 2023-02): no on-chain proposal, not executed.
- **Fee switch 2023**, "Making Protocol Fees Operational" (three Snapshots ending 2023-06-01): "No Fee" won with 18.43M against 17.22M for "1/5", and nothing was executed. Class B, not executed.
- Optimism LM programme updates (Snapshots 2023-01-13): OP supplied by Optimism, not DAO-funded.
- Deployments (Boba, BNB, Avalanche, zkEVM, Gnosis, Moonbeam, Base, Linea, FVM, Scroll, Celo bridge migration) and the 1bp fee tier on Arbitrum (#32): protocol parameters, no spending decision.
- Uniswap Cross-chain Bridge Assessment ($289k inside UF ops): below threshold.
- UF 2023 grant commitments: $2.93M in total, so no single grant reaches 2.546M. The largest UF grant to that date (Oku, $1.6M) was committed in 2022.
- Create the Uniswap Foundation ($74M, Aug 2022; tranche 1 paid 2022-08-25): approved and partly executed before the period. Tranche 2 is UNI-2023-A1.

**2024**
- Lower Onchain Proposal Threshold (#55), Rootstock (#56), Zora (#57), V2 on all chains (#58), Update deployment process (#61), Base 2/3/4 bp fee tiers (#69): no spending.
- Delegate Reward Cycle 1 (#64; $280k including the WG retro): 3.9%.
- Onboarding Package for Gnosis Chain (#66; $250k + $105k Oku + $21.6k Merkl): 5.3%.
- X Layer deployment with $105k Oku subsidy (#67; not paid out, per UAC S3): 1.5%.
- Delegate Reward Cycle 2 (#68; 84,000 UNI; up to $6,000 per delegate per month for 15–16 delegates over 6 months, total USD not quoted in the text read): about 7.6%.
- UAC S3 Renewal and Rebalance (#70; $242.6k + $248.2k rebalance + $36k): about 7.4%.
- Forse analytics (#72; $60k): 0.8%.
- Tally development grant (#74 executed 2024-12-01; $500k paid quarterly over 2025–2026): 7.0%.
- Mobilizing the Uniswap Treasury / UTWG (#62): class C (C4).
- Onboarding Package for Lisk (Snapshot 2024-10-13, For 20.99M / Against 17.28M): never went on-chain.
- Metal L2 (Snapshot rejected), EF Attackathon sponsorship (rejected), Visa card (rejected): not approved.
- **Activate Uniswap Protocol Governance** (fee-switch/staking upgrade; Snapshot 2024-03-06 passed with 54.55M): the on-chain vote was never held, and the UF FAQ says "various concerns emerged relating to liability, tax, and securities concerns". Class B, not executed.
- **Uniswap V3 Fees: Factory Owner Amendment** (Snapshot 2024-03-09): rejected 30.06M to 20.14M. Class B, not approved.
- UF 2024 grants below 0.711M: Atrium Hook Incubator #1 $600k; GovSwap $515k; UnitZero $512.9k (Q2 commitment); Agora $480k; Allium $480k; Panoptic $379k; Edge City $348k; Cooley $240k; Butter $200k; Doppler, CBER, ETHGlobal and others.
- Line-item candidate not testable: security 2023→2024 (2023 not reported as a category).

**2025**
- Incentive Package for Sonic (#76, $250k): 1.1%. Scale Uniswap Liquidity on Celo (#77, $355k): 1.6%. BoB Incentives Package (#84, $375k): 1.7%.
- Delegate Reward Cycle 3 (#80, $540k): 2.4%.
- UAC Renewal S4 (#87, $370k) and Rebalancing S4 (#86, $280k): 1.6% and 1.2%.
- Scaling V4 and Supporting Unichain (#89; $250k + $90k): 1.5%.
- Strategic Renewal of Gnosis, Linea, Mantle (#92, $180k): 0.8%.
- Uniswap DAO Principles (#78), SEAL Safe Harbor (#79), Establish Uniswap v4 Licensing Process (#85): no spending.
- Unichain USDS/sUSDS Co-Incentives Growth Management Plan: Snapshot 2025-06-22 passed, but on-chain #91 (430,500 UNI) has no ProposalExecuted event, so it was not executed.
- Ronin co-incentives $500k (Snapshot 2025-09-06), Plasma $250k (Snapshot 2025-10-12), Delegate Reward Cycle 4 (Snapshot 2025-08-18): no on-chain proposal found. They may have been funded from the UAC surplus (C8), which is not verified. All are below threshold.
- Saga (rejected), Etherlink (rejected), Technical Advisory Board (rejected), Uniswap Community Proposal Factory (rejected): not approved.
- UF commitment "Unichain Partners - 2025" ($2,091,586, Q1 2025): 9.3%. **Sensitive:** it would be selected if the 2024 denominator were below $20.9M (lower alternative 20.6M).
- UF commitment "Unichain Partners - 2026 and Beyond" ($9,875,100, Q1 2025): committed in-period, but it is "for grants in 2026 through 2029", so execution falls after the period. Flagged for the reviewer.
- UF 2025 commitments below 2.259M: Areta Security Fund $1.72M (Q2) and $90k (Q4); Butter CFM $950k; Atrium Hooks Incubator $990k (Q4); EulerSwap $460k + $200k; and others.
- UNIfication items not executed in 2025: aggregator hooks, PFDA, v4/L2 fee adapters ("will be introduced through future governance proposals"), Unisocks migration. Protocol Fee Expansion and v4 fee votes are 2026, out of period.
- Unichain Growth Reserve, and the UVN 65% share of net chain revenue: UF/Labs announcements, not DAO votes. The reserve is spent through UF programmes and reported inside UF quarterlies.
- Line-item candidates not selected (2024→2025): grants −0.64; security +0.457 (+23%); governance (UF −0.42, DAO actual not reported); marketing about +0.04.

## 7. Gaps

1. **No full 2022 year.** The UF began operating in Aug 2022, and pre-UF UGP 2022 spending was not reported. The 2023-decision denominator is therefore a budget proxy that rests partly on my division of the $60M three-year grants budget.
2. **ARB-funded DAO programmes (CLIP, UAGP)** have no USD values for the years in which they paid out, so the 2023 denominator is a lower bound. The CLIP split between 2023 and 2024 is unknown.
3. **DAO-level 2024 actuals** are taken from UAC season reports, not calendar-year statements:
   - "~$6M distributed via the UAC as of January 20, 2025" mixes timing, and possibly the LTIPP matching.
   - Delegate cycle 2 and Oku integration payments are not itemised by calendar year.
   - The DEF grant has no USD value.
4. **DAO-level 2025 actuals are not reported** in the sources read: spending from the $45M Aera vault, DUNI prefund use, UAC 2025 outflows and delegate rewards. Gauntlet and Merkl dashboards were not consulted, per the blinding rule. 2025 can therefore only be shown at the UF level.
5. **UF 2024 grant split** comes from pie-chart shares that sum to 101%. Incentive-type UF grants inside the 2024 "Protocol" and "Innovation" categories cannot be separated.
6. **UF opex excludes employee UNI token awards** (0.15M, 0.28M and 0.45M UNI), which have no USD value.
7. **UF grant decisions are dated only to the quarter** of commitment and use FY-restated commitment amounts. Some grants marked "*" in the FY2024 tables combine commitments from several quarters.
8. **Token-denominated decisions without USD:** DEF 1M UNI, UNIfication growth budget 40M UNI, CLIP 2M ARB, UAGP delegation 1.1M ARB. Their materiality is provisional or not computed.
9. **Execution dates** are on-chain execution dates (Governor `ProposalExecuted`). The approval date is the end of the Snapshot temperature check. Draw-down dates by the UAC and the UF were not collected.
10. **Source inconsistencies:**
    - UF Q3 2025 Governance subtotal versus its rows (+$61,250).
    - FY2025 advertising (0.16) is less than the Q4 2025 figure (0.3).
    - FY2024 commitments were restated ("some numbers have changed").
    - Q3 2025 YTD commitments (18.8M) are less than H1 (18.9M) plus Q3 (0.8M).
11. **Treasury Delegation Round 2 and GLI vaults:** execution was not verified.

# Aave DAO: case-card inputs for the decision table (Research 6)

Compiled 2026-10-07 under METHOD_R6.md (sections "Чьи расходы", "Три класса", "Отбор решений"). Companion file: `aave_decisions.csv` (23 rows). Format follows `lido_decisions.csv` / `lido_card_inputs.md`.

Sources used:
- governance.aave.com forum posts (raw endpoints `https://governance.aave.com/raw/<id>/1`, topic JSON for later posts, images in posts where needed).
- Snapshot space `aavedao.eth` (older links use `aave.eth`), hub.snapshot.org GraphQL, all 740 proposals created 2022-11-01..2025-12-31 listed and screened by title; the spending, incentive, treasury, Safety Module and tokenomics ones were opened.
- On-chain Governance v3 AIPs 0–432 from the public cache `github.com/bgd-labs/v3-governance-cache` (proposal state, IPFS title, Ethereum payload `PayloadExecuted` timestamps). Titles missing from the cache were resolved through an IPFS gateway.
- Governance v2 AIPs (all 2023 decisions) only through links in forum threads. Public RPC nodes refused archive log queries, so v2 execution blocks were not retrieved (see Gaps).
- Reported spending: `/home/claude/r6v/bench/aave.md` (TokenLogic income statement on insights.aave.com, values as already collected) and the Llama "Q4 2022 Financial Report" (topic 11418, image "Income Statement (January - December 2022)").

## 0. Blinding log

- I used no token price, TVL, fee, revenue or market-share series, and no DefiLlama, CoinGecko, Dune or insights dashboards. I did not open insights.aave.com myself; dashboard values come from the bench file. I did not open anything under /home/claude/r4, r4rep, r5 or r6v/data.
- Incidental exposure, recorded for the auditor (nothing below is recorded in the CSV or used in selection):
  - (a) `r6v/bench/aave.md` contains the Total Revenue / Net Income rows for 2023–2025 next to the expense rows. I read them while taking the expense rows.
  - (b) Llama Q4 2022 report (topic 11418): the 2022 income statement image also shows revenue by market, and other slides show TVL, gross profit and treasury holdings for Q4 2022. These are pre-period, and only the cost lines are used.
  - (c) Several approving proposals carry outcome-type context in their motivation sections, and I read these while extracting amounts and goals:
    - "Merit is Forever" (17336) cites round-1 results (ETH moved from Morpho, stkGHO/GHO supply growth, peg time in range, GHO revenue, "excess annual net profit").
    - ALC Phase V/VI/VII (20043, 21682, 23143) give GHO peg, pool TVL and supply growth.
    - The Safety Module emission updates (22554, 23103) and stkABPT update (21683) include AAVE price assumptions, staked amounts, LP returns and buyback totals.
    - Aavenomics Part One (21248) mentions market share and cash reserves.
    - TokenLogic+karpatkey Phase II (18285) mentions treasury size and revenue vs. burn.
    - Buybacks update (23290) asserts "strong success of the program".
    - BGD Phase 3 and 6 (16893, 23191) mention market share and revenue.
    - Base Incentive Campaign (21983) gives Base collector revenue.
    - Umbrella Coverage Expansion (23224) gives Core debt growth.
    - The Chaos early renewal (22346) and the V4 TEMP CHECK (17541) give deposits and TVL.
    - The V3 retroactive funding ARC (9250, 2022) gives a market size.
  - (d) **ACI Retrospective 2024-present (topic 21825)**. A keyword grep printed its incentive-campaign table lines ("Total TVL Growth", "TVL growth per dollar spent"). This is explicit outcome data for incentive decisions. I stopped reading the post, did not record any of it, and used nothing from it.
- The CSV does not say whether any decision "worked".

## 1. Denominators (levels 1+2)

Definition applied: level 1 + level 2 class A spending, meaning service providers (BGD, Aave Labs, ACI, Chaos, Gauntlet, Certora, LlamaRisk, TokenLogic, karpatkey, Llama), Aave Grants DAO, events, Orbit delegates, and incentives paid by the DAO (liquidity mining, Merit, ALC/GLC, GHO incentives).

It excludes:
- Safety Module staking rewards and Umbrella rewards (the decision is explained below);
- buybacks, which are class B;
- treasury operations, which are class C.

A decision's year is the year its execution starts (on-chain AIP execution). So, for example, AIP 222 (executed 2024-12-29) is a 2024 decision.

| Decisions in | Denominator year | Figure used (USD) | Type | Composition | 10% threshold | 5% threshold | Source |
|---|---|---|---|---|---|---|---|
| 2023 | 2022 | **67,356,074** | actual (Llama, "Income Statement (January - December 2022)", YTD) | "Third party expenses" 38,536,657 + "Liquidity Incentives" 28,819,417 | 6.74M | 3.37M | https://governance.aave.com/t/q4-2022-financial-report/11418 (4th image) |
| 2024 | 2023 | **14,343,428** | actual (TokenLogic income statement) | Service Providers 12,130,218 + Incentives 18,590 + GHO 2,140,000 + Partnerships 0 + Other 54,620 | 1.43M | 0.72M | insights.aave.com dashboard via r6v/bench/aave.md (cross-check: Total Expenses 43,002,847 − Staking 28.66M = 14.34M) |
| 2025 | 2024 | **38,859,698** | actual (TokenLogic income statement) | Service Providers 22,069,698 + Incentives 9.59M + GHO 2.44M + Partnerships 2.95M + Other 1.81M | 3.89M | 1.94M | same (cross-check: 78,510,654 − Staking 39.65M = 38.86M) |
| (reference) | 2025 | 54,244,713 | actual | Service Providers 24,146,813 + Incentives 19.45M + GHO 8.49M + Partnerships 1.24M + Other 0.918M | – | – | same (cross-check: 109,230,898 − Staking 49.78M − Insurance 5.2M) |

All three years are actual figures, so no budget proxy was needed.

**Safety Module staking rewards are excluded from the denominator.** Reasons:
1. They are AAVE emissions from the Ecosystem Reserve paid to stkAAVE/stkBPT/stkGHO holders in exchange for backstop capital exposed to slashing. That makes them an insurance or cost-of-capital payment, the analogue of Lido node-operator rewards, which were also excluded. They are not a discretionary investment in users or integrations.
2. Both reporters keep them out of the operating lines: Llama shows "Staking rewards" as its own cost line, and TokenLogic shows "Staking" (and from 2025 "Insurance (Umbrella)") as separate rows.
3. The DAO itself handled SM emission changes as treasury and emissions management (e.g. "[ARFC] Treasury Management - Amend Safety Module AAVE Emissions", topic 14936) and as part of Aavenomics/Umbrella, not as incentive programmes.

Exception flagged for the reviewer: stkGHO emissions (from Jan 2024) were explicitly "to support GHO stability" (topic 16640), so they are incentive-like. They cannot be separated from the "Staking" row, so they stay excluded too. All SM and Umbrella decisions are listed descriptively in §5b.

Sensitivity (if staking were included): the denominators become 2022 106.84M (staking 39.48M), 2023 43.00M and 2024 78.51M. The 10% thresholds become 10.7M, 4.30M and 7.85M.
- 2023: no selection changes.
- 2024: A1 (BGD 3.5M), A5 (Chaos 2.0M), A6 (Certora 1.7M), A7 (BGD 2.3M) and A8 (ALC 2.0M) would drop out. A2, A3 and A4 would stay.
- 2025: A2 (CEX 5M) and A4 (SP reform 4M) would drop. A1 and A3 would stay.

The choice matters mostly because 2023 spending was unusually low.

Notes and flags on the denominators:
- **2022 (Llama).**
  - This is a single report slide with no methodology. It is not stated how AAVE-denominated payments were valued, or whether transfers to Aave Grants DAO (a level-2 entity) are booked as expense when transferred or when AGD spent them.
  - "Third party expenses" includes the one-off Aave V3 retroactive funding of $16.28M to Aave Companies (ARC 9250, Aug 2022, "$15 million (incurred work) and $1.28 million (audit)") and BGD Phase 1. Excluding the retro funding, the denominator would be about 51.1M (thresholds 5.11M and 2.55M), and no 2023 selection would change.
- **2023–2025 (TokenLogic).**
  - No row definitions are published.
  - Whether AGD funding, events and Orbit sit in "Service Providers", "Partnerships" or "Other" is unknown.
  - The "GHO" row is undefined. It is assumed to be GHO liquidity and peg costs (GLC/ALC, GHO incentives).
  - The source is "not audited financial or corporate reporting".
- **Comparability.** 2022 (Llama) and 2023+ (TokenLogic) come from different reporters, so the 2022→2023 line-item changes are flagged.
- **Level 3** (developer companies outside the DAO): not quantified. One example is Aave Labs' own spending outside its DAO grant, including incentives that Aave Labs proposed to fund for Horizon (21898). This is noted as a limitation only.

## 2. Mapping table: report categories to our class A line items

Written before the numbers in §3 were filled in.

| Report / source category | Source | Our line item |
|---|---|---|
| "Third party expenses" (2022) | Llama 11418 | service providers and DAO-funded entities, unallocated |
| "Liquidity Incentives" (2022) | Llama 11418 | incentives to users/integrations |
| "Staking rewards" (2022) | Llama 11418 | excluded (Safety Module, see §1) |
| "Service Providers" (2023–2025) | TokenLogic | service providers and DAO-funded entities, unallocated (development, risk/security, finance, growth/governance, grants, events: not separable from the actuals) |
| "Incentives" | TokenLogic | incentives to users/integrations |
| "GHO" | TokenLogic | incentives to users/integrations (assumed GHO liquidity/peg; definition unknown) |
| "Partnerships" | TokenLogic | other (undefined) |
| "Other Expenses" | TokenLogic | other |
| "Staking" | TokenLogic | excluded (Safety Module) |
| "Insurance" (Umbrella, 2025) | TokenLogic | excluded (Safety Module successor) |
| AAVE buybacks | not an expense row | class B (not class A spending) |
| Decision-level mapping (for CSV line_item only): BGD, Aave Labs → development; Chaos, Gauntlet, LlamaRisk, Certora, Sigma, bounties/contests → security; TokenLogic/karpatkey/Llama → legal/ops (finance); ACI, Orbit → governance/growth; AGD → grants; events → marketing/growth; Merit, Ahab, ALC/GLC, CEX Earn → incentives | proposals | as stated |

## 3. Class A line items by year (USD M)

| Our line item | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| service providers & funded entities (unallocated) | 38.54 | 12.13 | 22.07 | 24.15 |
| incentives to users/integrations | 28.82 | 2.16 (0.019 + GHO 2.14) | 12.03 (9.59 + GHO 2.44) | 27.94 (19.45 + GHO 8.49) |
| other (Partnerships + Other Expenses) | not separated | 0.055 | 4.76 (2.95 + 1.81) | 2.16 (1.24 + 0.92) |
| **total (levels 1+2)** | **67.36** | **14.34** | **38.86** | **54.24** |
| memo: Safety Module staking (excluded) | 39.48 | 28.66 | 39.65 | 49.78 |
| memo: Umbrella (excluded) | – | – | – | 5.2 |

The SP line cannot be split by our categories from actuals. As a memo only (a budget run-rate, not an actual), the TokenLogic Funding Insights post (topic 24192, Feb 2026, from the bench) gives the annualised stablecoin streams before April 2026:
- development: BGD 4.4;
- security/risk: Chaos 2.55 + Certora 2.628 + LlamaRisk 1.0;
- finance: TokenLogic 2.5;
- growth/governance: ACI 3.0;
- total 16.08M, plus 26,850 AAVE per year.

Line-item change test (more than 25% year on year and at least 5% of the denominator):
- 2022→2023 (5% = 3.37M), both flagged for comparability:
  - Service providers −26.41M (−68.5%): selected (`AAVE-2023-LI1`).
  - Incentives −26.66M (−92.5%): selected (`AAVE-2023-LI2`).
- 2023→2024 (0.72M):
  - Service providers +9.94M (+81.9%): selected (`LI1`).
  - Incentives +9.87M (+457%): selected (`LI2`).
  - Other +4.71M: selected (`LI3`), flagged because the rows are undefined.
- 2024→2025 (1.94M):
  - Incentives +15.91M (+132%): selected (`LI1`).
  - Other −2.60M (−54.7%): selected (`LI2`), flagged.
  - Service providers +2.08M (+9.4%): **not selected**.

## 4. Selected decisions (summary; details in the CSV)

| id | class | amount USD | materiality | rule |
|---|---|---|---|---|
| AAVE-2023-B1 GHO launch with 30% stkAAVE discount | B | n/a | n/a | every class B |
| AAVE-2023-LI1 service providers 2022→23 | A | −26.41M | 0.392 | line-item (flagged) |
| AAVE-2023-LI2 incentives 2022→23 | A | −26.66M | 0.396 | line-item (flagged) |
| AAVE-2024-A1 BGD Phase 3 | A | 3.5M + 12,500 AAVE | 0.244 | ≥10% |
| AAVE-2024-A2 Merit initial 90 days | A | 5.0M | 0.349 | incentives ≥10% |
| AAVE-2024-A3 Merit is Forever (incl. Ahab) | A | 20.0M | 1.394 | incentives ≥10% |
| AAVE-2024-A4 Aave Labs V4 service provider | A | 12.0M | 0.837 | ≥10% |
| AAVE-2024-A5 Chaos Labs renewal | A | 2.0M | 0.139 | ≥10% |
| AAVE-2024-A6 Certora renewal | A | 1.7M | 0.119 | ≥10% |
| AAVE-2024-A7 BGD Phase 4 | A | 2.3M + 5,000 AAVE | 0.160 | ≥10% |
| AAVE-2024-A8 ALC Phase V | A | 2.0M GHO | 0.139 | incentives ≥10% |
| AAVE-2024-LI1 / LI2 / LI3 | A | +9.94M / +9.87M / +4.71M | 0.693 / 0.688 / 0.328 | line-item |
| AAVE-2025-A1 Merit + Ahab 2025 continuation | A | 20.0M/yr | 0.515 | incentives ≥10% (flagged: series of funding AIPs) |
| AAVE-2025-A2 GHO CEX Earn | A | 5.0M GHO | 0.129 | incentives ≥10% |
| AAVE-2025-A3 Extend Ahab funding | A | 15M stables + 6,000 WETH (ceilings) | 0.386 | incentives ≥10% (flagged) |
| AAVE-2025-A4 SP Compensation Reform (AAVE grants) | A | 4.0M in AAVE | 0.103 | ≥10% |
| AAVE-2025-LI1 / LI2 | A | +15.91M / −2.60M | 0.409 / 0.067 | line-item |
| AAVE-2025-B1 Aavenomics Part One (buy & distribute) | B | n/a ($1M/week) | n/a | every class B |
| AAVE-2025-B2 v3.4 removal of GHO discount | B | n/a | n/a | every class B |
| AAVE-2025-B3 Buyback programme $50M/yr | B | n/a | n/a | every class B |

Count: 23 rows in total.
- Class A decisions: 12 (2023: 0, 2024: 8, 2025: 4).
- Class A line-item rows: 7 (2023: 2, 2024: 3, 2025: 2).
- Class B: 4 (2023: 1, 2025: 3).
- Class C: 21 entries, descriptive only (§5).

Notes:
- **No class A decision executed in 2023 reached 6.74M.** The largest were AGD renewal 3.25M, Gauntlet 2M/1.6M, BGD Phase 2 1.9M + 6,000 AAVE, Chaos 2023 renewal 1.6M and Certora 1.5M. The 2023 rows are therefore line-item changes and one class B decision.
- **2024 has many selections because the 2023 denominator is low (14.34M).** See the sensitivity in §1.
- **Contributing decisions behind AAVE-2023-LI1** (not separate rows):
  - Llama stream cancelled (Snapshot 2023-08-03, "save up to approximately $240k");
  - Certora price cut "from $2.7M to $1.5M";
  - AGD renewal at $3.25M vs $4.0M first asked;
  - Gauntlet fee cut to $1.6M (Dec 2023).
  The 2022 base also contained one-offs (V3 retroactive funding, BGD Phase 1).
- **Class B assignments B1 and B2** (stkAAVE GHO borrow discount and its removal) are in-kind benefits to stakers, not cash payouts. They are flagged for the reviewer.
- **Anti-GHO** (50% of GHO revenue to stakers, approved in principle in B1) was not found live in 2025. A forum post on 2025-06-12 asks when it is coming, and the v3.4 text says it "will not be in sync with v3.4". It is not treated as executed.
- **Umbrella** rewards are described in Aavenomics as "redistributing part of the Aave DAO excess revenue to Umbrella aToken stakers". They are kept with the Safety Module (§5b), not class B. Reviewer to confirm.

## 5. Class C decisions (descriptive, no threshold)

| # | Decision | Approved (Snapshot end) | Executed | Size (as stated) | Source |
|---|---|---|---|---|---|
| C1 | Migrate & consolidate Polygon treasury | 2023-03-19 | AIP v2, date not retrieved | – | topic 12248 |
| C2 | Deploy BAL & aBAL from the Collector (veBAL lock won) | 2023-03-16 | AIP v2 | – | topic 9747 |
| C3 | Deploy aCRV & CRV ("YAE - sdCRV" 361,861 vs veCRV 223,863) | 2023-03-30 | AIP v2 | – | topic 11628 |
| C4 | Consolidate Collector & secure SP runway; migrate v2→v3 and acquire wstETH and rETH; acquire bb-a-USD and deposit into Balancer/Aura | 2023-05-17 / 05-19 | AIP v2 (2023) | wstETH and rETH legs ~$693,770 each (table in post) | topic 12205 |
| C5 | Avalanche v2→v3 treasury migration | 2023-09-01 | AIP v2 | – | topic 14469 |
| C6 | Acquire AURA; then "Enhancing Aave DAO's Liquidity Incentive Strategy on Balancer" (400k USDC of AURA OTM + OTC 2,965.35 AAVE + 200k USDC for 477,088.51 AURA); vlAURA lock; deploy AURA to vlAURA | 2023-09-07; 2023-10-15; 2023-11-11; 2023-12-06 | AIP v2 (2023) | as listed | topics 14683, 15061, 15323, 15669 |
| C7 | RWA allocation via Centrifuge Prime ($1M USDC into Anemoy LTF) | 2023-09-16 | AIP v2 (2023/24; "Update on AIP-331" topic 16952) | $1M | topic 14790 |
| C8 | Update Balancer ecosystem holdings (Option 3 won, 311,353); auraBAL (YAE 208,028 / ABSTAIN 354,615, outcome not determined) | 2023-10-04; 2023-11-17 | AIP v2 | – | topics 14955, 15421 |
| C9 | Transfer assets Polygon→Ethereum; add to rETH holding; Aave Funding Update (swap holdings to GHO, 6-month runway plan "Total: 5.1M USD"); Tooling upgrade; Aave Swap upgrade | 2023-10-14 … 2023-11-10 | AIP v2 | as stated | topics 15044, 15123, 15194, 15201, 15311 |
| C10 | RWA allocation with Maple: **rejected** (NAY 368,689) | 2023-12-10 | – | – | topic 15619 |
| C11 | GSM funding & RWA strategy preparations (Parts 1 and 2) | 2024-01-19 | AIP 14 (2024-02-05), AIP 35 (2024-02-28) | – | topic 16128 |
| C12 | "Frontier": DAO-run validators (128 wETH multisig); expansion (allowance "equivalent to 2,493 ETH") | 2024-01-24; 2024-05-31 | AIP 14 (2024-02-05); May 2024 Funding Update | 128 wETH; ~2,493 ETH | topics 16225, 17749, 17768 |
| C13 | Aave Protocol Embassy (APE) multisig seeded with Arbitrum collector ARB | 2024-02-09 | AIP 34 (Arbitrum payload, 2024-02) | ARB balance, not stated | topic 16445 |
| C14 | Fund USDC & USDT GSMs | 2024-05-14 | 2024 | – | topic 17566 |
| C15 | Aave Finance Steward (2024); Finance Steward modules (2025); MainnetSwapSteward & RewardsSteward | 2024-05-20; 2025-03-27; 2025-09-16 | AIP 279 (2025-04-03); AIP 386 (2025-10-08) | – | topics 17570, 21495, 23070 |
| C16 | Onboard GHO and migrate streams to Lido/Prime instance; deploy 10M GHO into Lido instance | 2024-11-22 | AIP 214 (2024-12-15); AIP 227 (2025-01-12) | 10M GHO | topic 19686 |
| C17 | AGD treasury returned to Aave DAO (wind-down of Aave Grants DAO) | 2025-02-14 | 2025 | AGD balances | topics 20897, 20792 |
| C18 | Creation of the Aave Finance Committee (inside AAVE-2025-B1) and monthly Funding Update AIPs (asset consolidation, swaps to GHO, deposits into Aave) | 2025-03-18; monthly | AIPs 246, 259, 293, 304, 321, 324, 327, 349, 370, 413, 425 | – | topic 21248 and Funding Update topics |
| C19 | Horizon RWA instance with a dedicated GHO direct-minting facilitator (1M, scalable to 5M GHO) | 2025-05-05 | 2025 | 1M–5M GHO capacity | topic 21898 |
| C20 | Deploy 5M USDC for GHO market making on Gnosis: **rejected** (Against 418,440) | 2025-05-15 | – | 5M USDC | topic 21931 |
| C21 | Buyback update mandate to use Frontier wETH and collector BTC reserves as collateral for growth (inside AAVE-2025-B3) | 2025-10-31 | – | – | topic 23290 |

Not in period: ParaSwap fee claimer and Ethereum v2 collector consolidation (both Snapshot 2022); Winding down the LEND migration contract (Snapshot 2025-11-25, AIP 480 executed 2026-05-09).

## 5b. Safety Module and Umbrella decisions (outside class A by the §1 choice, descriptive)

| Decision | Approved | Executed | Change (as stated) | Source |
|---|---|---|---|---|
| Amend SM AAVE emissions (−30%) | 2023-10-03 | AIP v2 (2023) | "from 1,100 AAVE/day to 770 AAVE/day" | topic 14936 |
| Upgrade SM with stkGHO | 2023-12-01 | AIP 7 "StkGHO Activation" (2024-01-25) | new stkGHO category | topic 15635 |
| Amend SM emissions (shift to stkGHO "to support GHO stability", total unchanged) | 2024-02-24 | AIP 45 (2024-03-14) | redistribution across categories | topic 16640 |
| stkGHO rewards adjustment | 2024-05-10 | 2024 | stkGHO "receives 100 AAVE/day" before change | topic 17518 |
| stkGHO incentives; stkAAVE re-enable rewards | 2024 | AIP 194 (2024-11-05); AIP 199 (2024-11-17) | – | AIP titles |
| stkBPT incentives; stkABPT emissions update | 2025-02; 2025-04-12 | AIP 250 (2025-02-18); AIP 298 (2025-04-29) | stkBPT "360 AAVE per day" → "240 AAVE/day" | topic 21683 |
| stkGHO emissions; stkAAVE emissions | 2025-05 | AIP 307 (2025-05-11); AIP 315 (2025-05-27) | – | AIP titles |
| **Aave Umbrella activation** (replaces SM slashing with aToken staking covered by DAO-paid rewards) | 2025-05-27 | AIP 320 (2025-06-05) | Umbrella budget later stated as "$8.7M budget, consisting of 7.2M stablecoins and 550 WETH" (topic 22554) | topic 21521 |
| SM emission update | 2025-07-20 | AIP 342 (2025-07-29) | "531 AAVE/day to 390 AAVE/day" | topic 22554 |
| SM & Umbrella emission update | 2025-09-21 | AIP 385 (2025-10-08) | "from 390 AAVE/day to 300 AAVE/day"; waETH max emission 550→500 | topic 23103 |
| SM emissions update; renewal of Umbrella reward allowances; Umbrella coverage expansion | 2025-11 / 12 | AIP 405 (2025-11-11); AIP 417 (2025-12-09); Snapshot 2025-12-02 | – | AIP titles; topic 23224 |

If staking were included in class A, these would be emission-level decisions on a ~29–50M per year line. Their USD sizes are not stated in USD by the DAO at decision time except as AAVE/day, so materiality is not computed.

## 6. Considered and rejected (one line each)

Thresholds: 2023 = 6.74M / 3.37M; 2024 = 1.43M / 0.72M; 2025 = 3.89M / 1.94M. Percentages are of the relevant denominator.

2023 executions:
- Gauntlet <> Aave renewal (Snapshot 2022-12-19, "$2 million fixed fee" for 12 months): 3.0%. Execution early 2023 is assumed, not verified.
- Chaos Labs Aave v2 coverage (Snapshot 2022-12-24, $250k over 5 months): 0.4%.
- Aave Grants DAO renewal (Snapshot 2023-01-12, executed end of January 2023, $3.25M for 2 quarters): 4.8%. This is funding to a level-2 entity, and AGD's own spending is inside the SP actuals.
- Compensate Bug Bounty Contributor (2023-01-28): immaterial.
- ACI 6-month (250,000 aUSDT, Snapshot 2023-04-07): 0.4%.
- Immunefi bug bounty programme, up to $1M (2023-05-05): a reserve, 1.5%.
- Incentivized Delegate Campaign TEMP CHECK (2023-04-10); gas rebates for delegates (2023-07-02, 2023-09-07): small or temp check.
- GHO Liquidity Pools initial strategy (2023-07-30); GHO Liquidity Committee (2023-09-30, 406k GHO over 3 months); GHO Funding (2023-09-26): below 1%.
- Cancel Llama service-provider stream (2023-08-03, saves "up to approximately $240k"): 0.4%. It contributes to LI1.
- Chaos Labs scope and compensation amendment (+$400k, 2023-08-18): 0.6%.
- Sigma Prime audit budget extension (162,000 USDT, 2023-08-18): 0.2%.
- BGD Phase 2 ("1'900'000 USD in stablecoins and 6'000 AAVE", 2023-08-25): 2.8% for the stablecoin part. The AAVE part has no USD value in the source.
- TokenLogic 6-month SP ($350k per 15194, 2023-09-16); TokenLogic retrospective (+$115k, 2023-11-11): below 1%.
- Expansion of Orbit (75,000 GHO per quarter, 2023-09-21): 0.1%.
- Aave Events & Sponsorship 2023 ($550,000 GHO, 2023-10-20): 0.8%.
- ACI Phase II (375k GHO, 2023-10-26): 0.6%.
- Chaos Labs renewal 2023 (Snapshot 2023-11-05; $1.6M per 17324's "$400,000 increase, bringing our total annual compensation to $2M"): 2.4%.
- Gauntlet renewal 2023 (Snapshot passed 2023-12-01; reduced to "$1.6M service partnership"; AIP v2 #396): 2.4%. Gauntlet terminated the engagement in Feb 2024 (topic 16700), and AIP 38 "Cut Gauntlet Service Provider Stream" was cancelled.
- Certora continuous security (Snapshot 2023-12-12, $1.5M, of which $1M GHO and $0.5M AAVE, retroactive from 2023-09-14; AIP v2 #410 submitted 2023-12-15, so executed December 2023): 2.2%. If it was executed in January 2024 instead, it would be 10.5% of D2023 and selectable (see Gaps).
- TokenLogic & karpatkey FSP (400k GHO over 180 days, Snapshot 2023-12-14): 0.6% of D2022, or 2.8% of D2023 if executed in 2024.
- BGD security budget, December 2023 ($121.2k + $30k refund): immaterial.
- TEMP CHECK "Allocating part of GHO Revenue to Safety Incentives" (2023-07-02): would have been class B, but no ARFC or AIP was found, so it was **not executed**.

2024 executions:
- Updated Aave Grants Continuation (Snapshot 2024-01-11, +$328,000 GHO allowance): 2.3%.
- Retroactive bug bounties pre-Immunefi ($86,500), and Request for Bounty Payout AIPs (Jan and Jun 2024): immaterial.
- Orbit renewals (80,000 GHO + 4.6755 ETH in Feb 2024; May 2024; 60,000 GHO + 4.3 ETH in Q3; 60,000 GHO in Q4): below 0.6% each.
- ALC Phase I (500k GHO, 2024-03-10): 3.5%. Phase III (600k GHO Ethereum + Arbitrum budget, 2024-06-23): about 4%. Phase IV (950k GHO, AIP 179 executed 2024-10-09): 6.6%. All below 10%.
- Chaos Labs engagement amendment (+$400k, 2024-04-19, AIP 85): 2.8%.
- LlamaRisk onboarding ($250,000 for 6 months, AIP 90 executed 2024-05-01): 1.7%. LlamaRisk renewal ($400,000 for 6 months, AIP 185 executed 2024-10-23): 2.8%.
- ACI Phase III "Ad Astra" (1M GHO for one year, AIP 99 executed 2024-05-11): 7.0%.
- BGD Aave v3.1 Cantina competition ($195,000): 1.4%.
- TokenLogic + karpatkey Phase II (500k GHO, AIP 142 executed 2024-08-07): 3.5%.
- Aave Events & Sponsorship 2024 (650,000 GHO; TEMP CHECK asked $850,000; AIP 136 executed 2024-08-04): 4.5%.
- Merit Base Incentives and Superfest Matching (up to 150k OP at max $2, paid in GHO, i.e. up to $300k; AIP 150 executed 2024-08-19): 2.1%.
- TokenLogic Financial Services Provider (1,000,000 GHO over 365 days, AIP 222 executed 2024-12-29): 7.0%.
- PYUSD incentive campaign (Snapshot 2024-11-02): rewards funded by Trident Digital/PayPal, not by the DAO, so out of scope.
- Arbitrum LTIPP ARB incentives (750,000 ARB, via "Set ACI as Emission Manager"): third-party funded, out of scope.
- Onboard Catapulta as deployment service provider (2024-04-06): the amount was not collected. It is a deployment SP with no indication of size near 1.43M, but this is not verified.
- TEMP CHECK "Aave 2030" (15M GHO + 25,000 stkAAVE): superseded by the AL Service Provider Proposal (`AAVE-2024-A4`), not executed in that form.
- TEMP CHECK "AAVEnomics update" (2024-08-03): temp check only. Implemented as `AAVE-2025-B1`.
- Frontier, APE, GSM funding, Finance Steward: class C (§5). stkGHO and SM emission changes: §5b.

2025 executions:
- karpatkey GHO Growth SP (250k GHO over 180 days, AIP 229 executed 2025-01-14): 0.6%.
- Aave v3.3 Sherlock contest ($230,000): 0.6%.
- Orbit renewals 2025 (60,000, 45,000 and 90,000 GHO): below 0.3%.
- LlamaRisk epoch 3 ($1M per year, AIP 297 executed 2025-04-29): 2.6%.
- ALC Phase VI (3.5M GHO allowance, AIP 296 executed 2025-04-21): 9.0%, close to the threshold but below it. ALC Phase VII (2.5M aEthLidoGHO, AIP 382 executed 2025-10-08): 6.4%.
- ACI Phase IV "Road to 80" (3M aEthLidoGHO, AIP 301 executed 2025-05-03): 7.7%.
- BGD Phase 5 (2.3M stablecoins + 4,000 AAVE, AIP 302 executed 2025-05-04): 5.9% for the stablecoin part. The AAVE part was not valued; it would push the decision over 10% only if worth more than about $1.59M (not computed).
- BGD Phase 6 & Project E (2.2M stablecoins + 3,000 AAVE, AIP 404 executed 2025-11-09): 5.7% for the stablecoin part, AAVE not valued.
- Chaos Labs early renewal ($3,000,000: $2.55M aEthLidoGHO + $0.45M AAVE; AIP 335 executed 2025-07-07): 7.7%.
- Aave Events & Sponsorship 2025 ($750,000 GHO, AIP 325 executed 2025-06-24): 1.9%.
- Sonic incentive campaign (0.8M aEthUSDC allowance in the April 2025 Funding Update): 2.1%. stS Loop Incentive Program (40,000 wS for the first month): no USD in source, small.
- Base Incentive Campaign Funding (2025-05-23): funded by "all the revenues currently accrued to the Aave Collector on Base", with the total not stated, so materiality cannot be computed.
- TokenLogic Phase II (2.5M GHO per year, Snapshot 2025-10-17, implemented with AIP 401): 6.4%.
- Certora security services for v4 ($2.39M) and for current infrastructure ($238k), AIPs 403/402 executed 2025-11-08: 6.2% and 0.6%.
- Aave V4 Security Funding ($1.5M, Snapshot 2025-10-31; "$1.47M spent in Q4 2025" per the bench): 3.9%.
- Joint Incentive Program with Polygon (TEMP CHECK 2025-01-26): **rejected by vote** (NAY 695,301).
- $AAVE token alignment Phase 1 - Ownership (2025-12-26): **rejected by vote** (NAY 994,842). It concerns brand and IP ownership and is not class B.
- "AAVE Improvement Proposal (AIP): Immediate $20M Token Buyback" (forum 23265, Oct 2025) and the Ekubo TWAMM buyback pilot (21699, Apr 2025): no Snapshot vote found, so they are not decisions.
- Winding down the LEND migration contract (Snapshot 2025-11-25): executed 2026-05-09, out of period.
- Line-item candidate not selected: service providers 2024→2025, +2.08M (+9.4%, below 25%).

## 7. Gaps

1. **Governance v2 execution dates (all 2023 AIPs) were not retrieved.** Public RPCs refused archive `eth_getLogs`, and the v3 cache does not cover v2. Years were assigned from Snapshot and AIP submission dates in forum threads. The assignment matters for:
   - Certora 2023 (AIP v2 #410, submitted 2023-12-15) and Gauntlet 2023 (AIP v2 #396, published about 2023-12-04). If either executed in January 2024, it would be selectable under the 2024 threshold (10.5% and 11.2% of D2023).
   - TokenLogic & karpatkey (Dec 2023), which is not selectable either way.
   The GHO launch (AIP v2 #268) is dated only to July 2023 (voting began 2023-07-11).
2. **2022 denominator** is one Llama slide. The method for valuing AAVE, the treatment of AGD transfers and the inclusion of one-offs are not documented.
3. **TokenLogic rows are undefined** ("Service Providers", "GHO", "Partnerships", "Other"). This is why the LI3 and 2025-LI2 "other" rows are flagged.
4. **Service-provider spending cannot be split** by our categories from actuals in any year. Only budget run-rates exist (memo in §3).
5. **Token-denominated amounts are not valued**: BGD AAVE parts (12,500 / 5,000 / 4,000 / 3,000 / 6,000 AAVE), Certora/Chaos AAVE parts, Ahab ETH (645–800 ETH per quarter, 6,000 WETH ceiling), Frontier ETH. SP reform amounts are stated in USD worth of AAVE.
6. **Merit/Ahab implementation**: the 2024 first allowance AIP after "Merit is Forever" was not individually identified, and Merit actual spend is not reported separately (it sits inside the "Incentives"/"GHO" rows). AAVE-2025-A1 is a programme row built from implementing Funding Update AIPs, not one ARFC.
7. **Buyback programme update** (`AAVE-2025-B3`): no dedicated AIP found. Execution is through AFC allowances, and the start date is approximate. Anti-GHO implementation was not found in 2025.
8. **GHO discount parameter changes between 2023 and 2025** (if any) were not screened individually. Only the launch (B1) and the removal (B2) are recorded.
9. **Snapshot screening was by title.** Proposals whose titles do not reveal a spending or tokenomics component could have been missed. Direct-to-AIP proposals with no Snapshot were covered only through the v3 AIP title list.
10. **Approved vs actual** (for the case card): actuals per decision were not found. The bench gives the 2025 SP run-rate ($16.08M stablecoins + 26,850 AAVE per year), ACI's figure of "$21.2M from DAO treasury" for 2025 incentives, and "$1.47M spent" of the $1.5M V4 security budget.

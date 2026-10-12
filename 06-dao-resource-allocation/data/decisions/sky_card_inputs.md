# Sky (formerly MakerDAO): case-card inputs for the decision table (Research 6)

Compiled 2026-10-07 under METHOD_R6.md (sections "Чьи расходы", "Три класса", "Отбор решений"). Companion file: `sky_decisions.csv` (45 rows: 19 class A including 3 line-item rows, 26 class B). Class C decisions are listed descriptively in §5 and are not in the CSV, as in the Lido file.

Sources used:
- Executive vote write-ups, 2023-01..2025-12: `makerdao/community` repository (`governance/votes/`, 70 files for 2023–2025) and `sky-ecosystem/executive-votes` (`2025/`, 15 files).
- Spell code: `sky-ecosystem/spells-mainnet` (`archive/2023-01-11` .. `archive/2025-12-11`, 83 spells), used to confirm parameter values.
- Poll texts: `makerdao/community/governance/polls` (polls up to mid-2025) and the vote.sky.money polling API (polls 1504–1613: dates, titles, discussion links, winning option).
- Forum posts on forum.sky.money (formerly forum.makerdao.com), read through `/raw/<topic>` endpoints. The topic numbers are given in the CSV.
- Ecosystem team "Capital Transparency" reports (topics 23438, 24674, 26028, 26863, 27326).
- Steakhouse 2023 financial report (expense lines only) and the Steakhouse 2022 report page (expense lines only).
- SFF / Block Analitica figures as already collected in `/home/claude/r6v/bench/sky.md`. I did not reopen the SFF reports themselves.

## 0. Blinding log

I used no price, TVL, fee, revenue, USDS-supply or market-share series. I did not open DefiLlama, makerburn, Dune, info.sky.money or CoinGecko, and nothing under /home/claude/r4, r4rep, r5 or r6v/data. The CSV does not say whether any decision "worked".

Incidental exposure, recorded for the auditor:
- (a) **Steakhouse 2023 PDF.** I extracted it to text and grepped for expense lines. The neighbouring summary bullets (vault balances, DSR balance at year end, "MKR burns and Dai/MKR LP purchases" for 2023, change in surplus) were visible. None were recorded or used.
- (b) **Steakhouse 2022 page.** The WebFetch summary returned 2021–2022 net revenue and earnings alongside the expense lines. These are pre-period figures. Not recorded.
- (c) **`bench/sky.md`.** It contains SSR expense, "Revenue Allocation", buyback totals and the SFF SKY purchase figure. Only the expense lines (opex, Sky Rewards, Integration Expenses) and the SFF purchase amount were used. The purchase amount is used only as the size of decision SKY-2025-B14, not as an outcome.
- (d) **Capital Transparency report 27326.** It shows the average USDS price of SKY in its market-making swap tables. Seen, not recorded.
- (e) **SBE forum posts** (21545, 22876, 23441, 23888, 25078, 26033, 26130, 26201, 26702). They mention Uniswap pool sizes or "TVL", ETH price, Surplus Buffer balances, and phrases such as "substantial increase to net revenue" and "In the current declining crypto market environment". Seen, not recorded.
- (f) **Atlas edits 25324 and 25552.** They contain an "Estimated Net protocol Income" figure in the Splitter parameter document. Seen, not recorded.
- (g) **Exec vote 2025-10-06.** It states a 0.04 USDS cap for the Lockstake capped SKY oracle, which is a price parameter. Seen, not recorded.
- (h) **Forum comment in 21468 (2023).** It mentions "the Surplus Buffer is shrinking and the buyback paused". Seen, not used.

## 1. Denominators (levels 1+2) and treatment of incentives

**Definitions applied:**
- Level 1 + level 2 = DAO operating expenses plus DAO-paid incentives.
- DAO operating expenses include Core Units, Responsible/Scope Facilitators, Ecosystem Actors, Aligned Delegates and AVCs, the Launch Project, Atlas budgets, keepers, and MKR/SKY token compensation valued by the preparer.
- Spending of DAO-funded foundations counts as level 2.
- A decision's year is the year its execution starts, as in the Lido file.

**Explicit treatment:**
- **Sky Token Rewards (USDS→SKY farming, "Sky Rewards for Supplying USDS")** are class A incentives to users and are included in the denominator. They are SKY paid by the DAO: minted until 2025-05-29, then vested from Pause Proxy treasury SKY.
- **Integration Boost and Accessibility Reward / distribution payments to integrators** are class A incentives to integrations and are included where they are reported. They appear as "Integration Expenses" in the SFF P&L from 2025 only.
- **Liquidity Bootstrapping (exchange listings, market making)** is treated as class A incentives (liquidity) with a flag, because the Atlas requires leftover value to be returned.
- **DSR, EDSR, SSR, the stUSDS rate and the Gnosis SSR–DSR differential payment** are excluded as cost of revenue per the method, together with all DSR/SSR rate decisions.
- **USDS and SKY staking rewards paid to SKY/MKR stakers out of the Splitter, and SKY rewards to stakers,** are class B (distribution to holders). They are not class A and are not in the denominator.
- **SBE buybacks** are class B.
- **Grants to the Sky Frontier Foundation and Fortification Foundation, and Genesis Capital to agents,** are financing, not expense. What the foundations spend is level 2.

| Decisions in | Denominator year | Figure used (USD) | Type | Composition | 10% threshold | 5% threshold | Source |
|---|---|---|---|---|---|---|---|
| 2023 | 2022 | **46.2M** | actual (cash basis, Steakhouse "MakerGAAP", as restated in the 2023 report) | Total operating expenses. The Steakhouse 2022 report splits ~46M into Core Unit Overhead 30M, MKR Token Vesting 12M and Direct Payments & Grants 4M. No DAO-paid user incentives were found in 2022. | 4.62M | 2.31M | Steakhouse 2023 report p.13 ("Total operating expenses ... (46.2) [2022]"). https://steakhouse.financial/projects/maker-financial-report-2022 |
| 2024 | 2023 | **53.7M** | actual (Steakhouse) | Direct to Third Party 20.1 + Keeper Maintenance 0.4 + Workforce 17.8 + MKR token expenses 15.4. No DAO-paid incentives in 2023: EDSR is a savings-rate expense and is excluded. | 5.37M | 2.685M | Steakhouse 2023 report p.15 |
| 2025 | 2024 | **80.0M** | actual (SFF / Block Analitica dashboard data, as reported) | "Operational Expenses" 69 + "Sky Rewards for Supplying USDS" 11. SSR (141) excluded. | 8.0M | 4.0M | SFF Q4 2025 report (bench/sky.md row 2024) |
| (reference) | 2025 | ~121.9M (+5.8M SFF own spend = ~127.7M) | actual, mixed vintages | Opex 73.71 (incl. Q4 "Buffers" 12.41) + Sky Rewards 21 (Q4-2025 vintage) + Integration Expenses 27.16 (Q1-2026 vintage). SFF spent 5.83M from inception to year-end 2025 (level 2). | – | – | bench/sky.md |

Notes and flags on the denominators:
- **2022.**
  - The 2022 report shows 46M (rounded) and the 2023 report restates it as 46.2M; 46.2M is used.
  - Category labels differ between the two reports (see §2).
  - MKR token expenses are valued in DAI at payout by Steakhouse. I did no valuation of my own.
- **2023.**
  - The Steakhouse appendix shows "Issuance for MKR token expenses" of 11.7 where the main statement uses 15.4, an internal inconsistency. With 11.7 the total would be 50.0M and the thresholds 5.0M and 2.5M. No selection changes.
  - The Capital Transparency report gives Atlas-enabled spending May–Dec 2023 of 21.2M DAI + 6,835 MKR, by work area. This is a subset of the Steakhouse total.
- **2024.**
  - What the SFF "Operational Expenses" line includes is described only loosely. It is not known whether it includes:
    - SKY/MKR-denominated compensation;
    - Launch Project disbursements, which Capital Transparency counts when they leave the Launch Project wallet, while the dashboards count them when they leave the buffer;
    - Liquidity Bootstrapping (10M USDS + 320M SKY in Sep 2024, +10M USDS in Nov 2024);
    - the Integration Boost (6M USDS sent to the multisig in Nov 2024).
  - The FY24 total in the Q4-2025 report is 221 = 69 + 141 + 11, so in that vintage any Integration Boost spending must sit inside the SSR line (141) or inside opex. This is a gap.
  - **Sensitivity:**
    - 69M (opex only), thresholds 6.9M and 3.45M: no selection changes.
    - 86M (adding the 6M Integration Boost transfers), thresholds 8.6M and 4.3M: SKY-2025-A5 still passes on its 10M budget (11.6%), but its 8M transfer alone would not (9.3%).
- **Level 3 (outside the comparison).** Spending by Phoenix Labs/Spark, Grove, Keel, Obex, Launch Agents and other agent companies from their own resources. Genesis Capital is financing, and its use by the agents is not reported.

## 2. Mapping table: report categories to our class A line items

Written after reading the report category names and before computing the line-item changes in §3.

| Report / source category | Source | Our line item |
|---|---|---|
| Core Unit Overhead (2022) / Workforce Expenses (2023) | Steakhouse 2022, 2023 | contributors/core team (cash) |
| MKR Token Vesting (2022) / MKR token expenses (2023) | Steakhouse 2022, 2023 | contributors/core team (token compensation). Also contains MKR paid to delegates, AVCs, Ecosystem Actors and the Launch Project, which is not separable. |
| Direct Payments & Grants (2022) / Direct to Third Party Expenses (2023) | Steakhouse 2022, 2023 | other/unallocated (third-party vendors: Ecosystem Actors, Launch Project transfers, delegate compensation in DAI, grants; not split by function) |
| Keeper Maintenance (2023) | Steakhouse 2023 | legal/ops (operations) |
| "Operational/Operating Expenses" (2024, 2025) | SFF / Block Analitica | opex, unallocated |
| "Operating Expenses – Buffers" / "Security and Maintenance" (Q4 2025) | SFF Q1-2026 / Q2-2026 reports | governance (Core Council and Aligned Delegate funding) |
| Sky Rewards for Supplying USDS (STR) | SFF | incentives to users/integrations |
| Integration Expenses (Integration Boost, Accessibility Reward / distribution payments) | SFF Q1-2026 report | incentives to users/integrations |
| Liquidity Bootstrapping budget | Atlas A.5.6.1.9; Capital Transparency | incentives to users/integrations (liquidity), flagged partly class C |
| Launch Project budget | Atlas / MIP108 s.9; Capital Transparency | other/unallocated (work areas: branding & marketing, frontend, protocol development, AI, etc.) |
| Aligned Delegate / AVC compensation | exec votes | governance (inside third-party or MKR in 2023, inside opex 2024–25) |
| Bug bounty, whistleblower | exec votes | security |
| Ecosystem Entity grants (SFF, Fortification); Genesis Capital | Atlas A.2.14, A.2.10 | foundation/agent funding (financing). SFF's own spending is level 2. |
| SSR / DSR / EDSR / stUSDS rate / Gnosis SSR payment | – | excluded (cost of revenue) |
| Splitter USDS rewards to stakers; SKY/SPK rewards to stakers; SBE buybacks; SKY burns | – | class B |
| Capital Transparency work areas | forum reports | memo only. They are not calendar-year and count expenses on a different basis. |

## 3. Class A line items by year (USD M)

| Our line item | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| contributors/core team (cash) | 30 (CU overhead) | 17.8 (workforce) | inside opex 69 | inside opex 73.71 |
| contributors/core team (token) | 12 | 15.4 | inside opex (not stated) | inside opex (not stated) |
| other/unallocated third-party (EAs, Launch Project, delegates, grants) | 4 | 20.1 | inside opex | inside opex |
| legal/ops (keepers) | not separate | 0.4 | inside opex | inside opex |
| governance (Core Council/AD buffers) | – | – | – | 12.41 (Q4 only, reclassified out of opex; included in the 73.71) |
| incentives to users/integrations | 0 (none found) | 0 (EDSR excluded) | 11 (STR). Integration Boost 2024 not separately reported. Liquidity Bootstrapping not separately reported. | 48.16 = STR 21 + Integration Expenses 27.16 |
| **total (levels 1+2)** | **46.2** | **53.7** | **80.0** | **~121.9** (mixed vintages; +5.83 SFF own spend) |

Memo (not calendar-year; Capital Transparency, USD at transaction-date prices as stated by the source):
- 2023 Atlas spend by work area (DAI part, May–Dec 2023): Protocol Development 5.76, Frontend 3.34, Risk 2.65, Collateral/RWA ops 2.34, Branding & Marketing 2.30, Legal 1.11, Infrastructure 1.09, GovOps 0.83, Smart Contract Auditing 0.65, AI 0.50, GovSec 0.30, Keepers 0.29, Bug Bounty 0.04. Total 21.2M DAI + 6,835 MKR.
- May 2023–Dec 2024 cumulative: 139.1M USD. Ecosystem Adoption & Growth (Integration Boost, listings, market making) was 37.8M of that.
- Launch Project lifetime: 77.9M USDS + 360M SKY spent, "$105.8 M over its lifetime".

Line-item change test (more than 25% year on year and at least 5% of the denominator):
- **2022→2023** (5% = 2.31M):
  - Third-party/unallocated 4 → 20.1 (+16.1, +403%): selected (`SKY-2023-LI1`).
  - Contributors (cash + token) 42 → 33.2 (−8.8, −21%): no.
  - Incentives 0 → 0: no.
  - **Caution.** If cash and token compensation were separate lines, workforce −12.2 (−41%) and MKR token +3.4 (+28%) would each pass. The pre-written mapping puts both under contributors/core team, the same convention as the Lido TRP. Most of the structural shift is the Endgame move from Core Units to third-party Ecosystem Actors. Combined third-party + contributors spending went 46 → 53.3 (+16%).
- **2023→2024** (5% = 2.685M):
  - Incentives 0 → 11 (STR): selected (`SKY-2024-LI1`).
  - No other line can be tested, because the 2024 opex is reported as one number. Total opex 53.7 → 69 (+28%) is a total, not a line, so it is not selected.
- **2024→2025** (5% = 4.0M):
  - Incentives 11 → 48.16 (+37.2, +338%): selected (`SKY-2025-LI1`). STR alone, +10 (+91%), also passes.
  - Opex 69 → 73.71 (+6.8%): no.
  - The governance "Buffers" line exists only from Q4 2025 as a reclassification and cannot be compared.

## 4. Selected decisions (summary; details in the CSV)

| id | class | amount USD | materiality | rule |
|---|---|---|---|---|
| SKY-2023-A1 Constitution facilitator budget streams | A | 7.86M (+1,642 MKR) | 0.170 | ≥10% |
| SKY-2023-A2 Launch Project created (SP8) | A | 6.4M (+3,647 MKR) | 0.139 | ≥10% |
| SKY-2023-A3 Launch Project → 20M DAI (SP13) | A | +13.6M | 0.294 | ≥10% |
| SKY-2023-LI1 third-party payments 2022→23 | A | +16.1M | 0.348 | line-item |
| SKY-2024-A1 Launch Project → 40M (SP34) | A | +20M | 0.372 | ≥10% |
| SKY-2024-A2 Launch Project → 60M (Atlas v2) | A | +20M | 0.372 | ≥10% (approval date flagged) |
| SKY-2024-A3 Sky Token Rewards 600M SKY/yr | A | not stated (SKY) | not computable | incentives ≥10%, provisional (reported 11M in 2024) |
| SKY-2024-A4 Liquidity Bootstrapping 10M USDS + 320M SKY | A | 10M | 0.186 | incentives ≥10% |
| SKY-2024-A5 Liquidity Bootstrapping +10M USDS | A | 10M | 0.186 | incentives ≥10% |
| SKY-2024-A6 Integration Boost | A | 6M (2024 transfers) | 0.112 | incentives ≥10%, provisional (open-ended) |
| SKY-2024-LI1 incentives 2023→24 | A | +11M | 0.205 | line-item |
| SKY-2025-A1 Launch Project → 80M | A | +20M | 0.250 | ≥10% |
| SKY-2025-A2 Spark Genesis Capital | A | 20.6M | 0.258 | ≥10% (C-alternative flagged) |
| SKY-2025-A3 Sky Frontier Foundation grant | A | 50M USDS + other treasury assets | 0.625 | ≥10% |
| SKY-2025-A4 Fortification Foundation grant | A | 10M + 200M SKY | 0.125 | ≥10% |
| SKY-2025-A5 Core Simplification Buffer Budget | A | 10M budget (8M paid) | 0.125 | ≥10% (borderline) |
| SKY-2025-A6 Launch Agent 4 Genesis Capital | A | 21M | 0.263 | ≥10% (C-alternative flagged) |
| SKY-2025-A7 Core Council Executor Agent 1 Genesis Capital | A | 25M | 0.312 | ≥10% |
| SKY-2025-LI1 incentives 2024→25 | A | +37.16M | 0.465 | line-item |
| SKY-2023-B1..B3, SKY-2024-B1..B9, SKY-2025-B1..B14 | B | n/a | n/a | every class B |

Notes on the selected decisions:
- **Launch Project.** It was one budget raised five times: SP8 6.4M DAI → SP13 20M → SP34 40M → Atlas v2 60M → Nov 2024 80M USDS + 360M SKY. Each raise is a separate approved budget decision and is selected on its increment.
  - Execution dates are the first transfer that needed the new cap. The figures below count Launch Project wallet receipts plus the 2.964M Jetstream stream:
    - 40M was reached exactly at the 2024-09-05 transfer;
    - the 2024-11-28 transfer took cumulative receipts to 50M;
    - 60M was reached at the 2025-01-23 transfer;
    - the 2025-03-06 transfer took cumulative receipts to 65M.
  - These totals reconcile with the close-out figure of 77,035,993 USDS received by the Launch Project wallet.
  - Transfers inside a cap are executions and are not rows.
- **SKY-2024-A2 (Atlas v2).** The Atlas v2 text (poll ended 2024-09-12) shows 60M USDS + 240M SKY. Capital Transparency dates the raise "October 2024". The approval date should be confirmed by the reviewer.
- **SKY-2024-A3 (STR).** Treated like the Lido TRP. The decision is token-denominated with no USD in the source, and it is included provisionally because the reported FY24 cost (11M) exceeds the 5.37M threshold. Later rate "rebalances" are listed in §6.
- **SKY-2024-A4/A5 (Liquidity Bootstrapping).** Materiality uses the USDS part only. The 320M SKY are not valued.
- **SKY-2025-A3 (SFF grant).** The bench file dates SFF funding to "June 2025", but the executive vote that paid the grant is dated 2025-08-21 (poll 1551, Atlas edit 27008). The exec date is used here.
- **SFF and Genesis Capital (class).** Both are class A as funding of entities, as with the Lido BORG foundation grants.
  - The Atlas states that Sky receives agent tokens in return for Genesis Capital. The SFF grant also seeds an "Unsellable SKY Frontier Endowment". Both are flagged as possible class C.
- **Class B scope.** The B rows include:
  - every SBE parameter or mechanism change;
  - every change of the Splitter split between buyback and staker rewards;
  - staking reward programmes (USDS from the Splitter, SKY farm, SPK farm);
  - the 426.3M SKY treasury burn;
  - the SBE LP unwind.
- **Surplus Buffer Upper Limit (`vow.hump`).** The task lists surplus buffer changes under class C. The executive votes label these changes as SBE parameters (they set the buyback trigger), so changes bundled with SBE decisions are inside B rows. SKY-2024-B4 (50→55M) is a hump-only change, kept in B because the exec vote titles it "Smart Burn Engine Parameter Updates". All hump changes are cross-listed in §5. The reviewer may reclassify them.
- **SKY-2025-B14.** Purchases by the Sky Frontier Foundation (level 2), with no DAO vote. The figure is taken from the bench file and was not re-verified.
- **Execution dates.** These are executive-vote / spell dates. Spells are cast after the GSM pause delay, a few days later. Exact cast blocks were not collected.

## 5. Class C decisions (descriptive, no threshold)

| # | Decision | Approved | Executed | Size (as stated) | Source |
|---|---|---|---|---|---|
| C1 | Stablecoin vault offboarding (USDC-A, USDP-A, GUSD-A) and PSM parameter changes; PSM-USDP-A line 450M→1B (Mar 11), then normalised to 500M; PSM-USDC-A `tin` 0→1%→0; gaps changed | polls Jan–Mar 2023 | 2023-03-08, 03-11, 03-29 | as stated | exec votes 2023-03-08/11/29 |
| C2 | MIP65 Monetalis Clydesdale (RWA007-A) debt ceiling 500M→1.25B; later updates and DAO resolutions; deprecated and set to 0 | poll 2023-03-13; resolutions 2023-09-27, 2024-08-12 | 2023; 0 on 2024-10-17 | 1.25B DAI line | polls; exec votes |
| C3 | Spark Lend D3M onboarding and ceiling path: 5M→20M→200M→400M→800M→1.2B→1.5B→2.5B DAI; D3M to Spark DAI Morpho Vault 100M→1B; SparkLend DDM deactivated 2025-05-29; Morpho DDM deactivated 2025-08-07 | MIP116 poll 2023-03; various | 2023-04-28 .. 2025-08-07 | as listed | exec votes |
| C4 | Coinbase Custody (RWA014-A) USDC custody: onboarding 500M; raised to 1.5B (2023-11-29); DAO resolutions 2023-06-16, 2024-05-06, 2024-08-12 | 2023-04-26 legal agreement | 2023-05-24 | 500M→1.5B DAI | exec votes |
| C5 | BlockTower Andromeda (RWA015-A) T-bill vault: onboarding at 2.5M, DC-IAM line 1.28B; Andromeda legal expense reimbursements (~0.2M each); line set to 0 2025-06-12 (with RWA012/013) | poll 2023-06 | 2023-06-14 / 06-28; 2025-06-12 | 1.28B DAI | exec votes |
| C6 | Surplus Buffer Upper Limit changes: 250→50M (2023-07-14, in B1), 50→55M (2024-05-30, B4), 55M→60M (2024-10-17, B8), 60→120M (2024-11-28, B9), 120→70M (2025-02-21, B2), 70→50M (2025-06-26, B8), 50→1M (2025-08-21, B11); Kicker allowing SBE below zero to −200M (2025-10-30, B12) | see B rows | see B rows | see B rows | see B rows |
| C7 | Old Aave v2 D3M caged (2023-01-27); new Aave v2 D3M onboarded at 5M of 20M approved (2023-02-22); Aave v2 and Compound v2 D3M lines set to 0 (2023-08-18) | 2023-01/02 | 2023-01-27; 2023-02-22; 2023-08-18 | 5M | exec votes |
| C8 | PSM-GUSD-A and PSM-PAX-A ceilings to 0 (removed from Cash Stablecoin list) | Stability Scope | 2023-11-29; 2024-01-24 | – | exec votes |
| C9 | LitePSM: DAO resolution (Coinbase Prime W3W), Phase 1 (2024-07-25), migration of all but 200M USDC (2024-08-22, LitePSM line to 7.5B), final migration (2024-10-04) | 2024-07-04 | 2024-07-25 .. 10-04 | 7.5B line | exec votes; https://forum.sky.money/t/litepsm-lite-psm-usdc-a-introduction-and-overview/24512 |
| C10 | Aave Lido Market USDS DDM 100M→200M; set to 0 2025-04-17 | 2024-10 | 2024-10-04; 2024-11-28; 2025-04-17 | 200M | exec votes |
| C11 | Star/Agent Allocation System: ALLOCATOR-SPARK-A line 10M→100M→1B→5B→10B; ALLOCATOR-NOVA-A (60M); ALLOCATOR-BLOOM-A (Grove) 10M→100M→2.5B; ALLOCATOR-OBEX-A 10M→2.5B | Ecosystem/Facilitator approvals; polls 1235, 1243, 1520 | 2024-10-31 .. 2025-11-13 | as listed | exec votes |
| C12 | Spark Tokenization Grand Prix DAO resolution; Spark→Grove transfer of BUIDL/JTRSY (temporary Bloom gap 1.25B) | 2025-04-03; poll 1533 | 2025-04-03; 2025-07-24 | as stated | exec votes |
| C13 | ConsolFreight RWA003 default management (2023-08-30), write-off (2024-11-14) and sweep of 406,451.52 DAI recovered to the Surplus Buffer (2025-02-06); RWA009 HV Bank, RWAF, Harbor, Fortunafi, New Silver resolutions and offboardings | various | 2023–2025 | as stated | exec votes |
| C14 | Treasury Management Function (Atlas edit poll 1601): 20% of "Step 1 Capital" to the Core Council Buffer and 1% to the Aligned Delegates Buffer; Monthly Settlement Cycles with Spark/Grove (Sep–Nov 2025) | 2025-10-30 | 2025-10-30, 2025-11-27 | transfers 3.88M+0.19M; 3.18M+0.16M | exec votes 2025-10-30, 2025-11-27 |
| C15 | MKR→SKY conversion of Pause Proxy MKR (13,334 MKR in Sep 2024 for Liquidity Bootstrapping; full balance in phase 3, 2025-06-26) | Atlas | 2024-09-27; 2025-06-26 | as stated | exec votes |

Not in period: anything executed in 2026 (for example the 2026-08-13 Splitter change to 55% burn seen in the spell archive).

## 6. Considered and rejected (one line each)

Thresholds: 2023 = 4.62M / 2.31M; 2024 = 5.37M / 2.685M; 2025 = 8.0M / 4.0M.

**Spending and budget decisions below the threshold:**
- Core Unit budgets in Jan–Mar 2023: SES 3.2M, DUX 1.61M, RISK 2.76M, SF 2.41M, TechOps 1.67M, SAS 1.13M, DIN 1.08M, GovAlpha 0.9M DAI. Each is below 4.62M.
- **PullUp Incubating EA** (poll 2023-04-27, exec 2023-05-10). 3.3M DAI (7.1%) + 4,000 MKR over two years. **FLAG:** the MKR is unvalued in the source, and the total could exceed 10% if valued.
- **Chronicle Labs EA streams** (exec 2023-07-14). 3.72M DAI (8.1%) + 2,216.4 MKR. **FLAG:** same as PullUp.
- Phoenix Labs (Spark) EA, May 2023: 1.85M DAI + 986.25 MKR. Spark Lend SPF: 347,100 DAI. Phoenix Labs initial SPF: 50k. All below.
- GovSec Engineering 2.2M and Multichain Engineering 2.3M DAI streams (2023-05-17): below 4.62M.
- Jetstream EA (2.964M DAI + 1,619.93 MKR, 2023-07-14): inside the Launch Project budget (SKY-2023-A2).
- Small payments throughout 2023–2025, all far below threshold:
  - Recognized, Aligned and Ranked Delegate compensation: ~0.1M DAI/month in early 2023, then ~200–280 MKR/month, then ~20–30k USDS/month.
  - AVC participation rewards.
  - Governance and Ecosystem Facilitator streams: 1.008M DAI + 432 MKR, and 0.504M + 216 MKR.
  - CAIS bootstrap 100k; SPF 209k; COM-001 offboarding 147k; Andromeda legal ~0.2M.
- Early Bird Rewards: 27,222,832.8 SKY minted to a multisig on 2024-10-17 (estimated need 22.69M, remainder to be burned). An incentive, but USD is not stated, so materiality is not computable.
- USDS→01 farming (2024-09-13): points programme, no cost.
- Sky on Solana strategy (Atlas 2024-10-24): up to 2M SKY/week paid from the Launch Project budget, so already inside the caps.
- Atlas Core Development payments (from Nov 2024: ~66–126k USDS + 0.33–0.99M SKY per month); new SKY treasury vest of 14.256M SKY for facilitators (2025-01-23): below or unvalued.
- Accessibility Reward budget transfer of 3M USDS (poll 1561, exec 2025-09-04): 3.75%.
- **Core Council and Aligned Delegate buffer funding under the Treasury Management Function** (exec 2025-10-30 and 2025-11-27). 7.41M in 2025 (9.3%) under an open-ended rule (20% / 1% of "Step 1 Capital"). Below 10% but borderline. Listed as C14 for the rule itself.
- Spark–Aave revenue share payments (3k–315k per quarter), bug bounties (up to 110k), whistleblower payments, the Resilience Research grant (32k): below threshold.

**Executions under decisions already selected:**
- Integration Boost top-ups in 2025 (21.5M total), Launch Project transfers 2023–2025, the 2M USDS Liquidity Bootstrapping transfer in Aug 2025, and the 1M Integration Boost funding in Oct 2025. Their decisions are SKY-2024-A6, the Launch Project rows and SKY-2024-A5.

**Incentive changes without a USD figure:**
- **Sky Token Rewards rebalances**, each a new SKY stream intended to "match the SSR":
  - 2025-04-17: 160M SKY / 182 days;
  - 2025-05-29: 137.5M SKY / 182 days, with the source switched from minting to the treasury;
  - 2025-07-24: 100.85M;
  - 2025-09-04: 76.74M;
  - 2025-10-06: 68.38M;
  - 2025-12-11: 60.30M.
  
  Each is SKY-denominated with no USD, so individual materiality is not computable. They are covered by `SKY-2025-LI1`. **FLAG:** the reviewer may prefer to give each one a row with materiality marked not computable.

**Excluded by definition:**
- EDSR activation (2023-08-02) and all DSR/SSR changes 2023–2025: savings-rate expense is cost of revenue.
- stUSDS onboarding (2025-09-04) and BEAM rate updates: rate products, cost of revenue.
- Payment to Gnosis of 1.81M USDS (SSR–DSR differential, 2025-11-27): cost of revenue.
- USDP-PSM incentives (2023-10-11): income from Paxos to Maker, not a spend.

**Class B candidates not selected:**
- MIP74c1-SP1 "Restart a $100/day micro-burn of MKR" (poll 2023-02-13..16): status "Rejected", so not approved. It would have been class B.
- Delayed Upgrade Penalty for MKR→SKY at 1% (2025-09-18), raised to 2% (2025-12-11): a token-migration parameter, not a buyback or distribution. **FLAG:** it can be argued to be class B because it reduces SKY issued to late upgraders.
- Other MKR→SKY upgrade phases (2025-05-15, 05-29, 06-26) other than the burn in B9: token migration, no value transfer to holders.

**Not spending decisions, or covered elsewhere:**
- Core Unit offboardings (COM-001 Jan 2023; DUX Jul 2023; GovAlpha Aug 2023; IS-001 Nov 2023; SES/DECO Jan 2024; Steakhouse/TechOps streams ended Nov 2023): no single amount at or above threshold. Covered by the line-item row SKY-2023-LI1.
- Monthly Settlement Cycles (Sep–Nov 2025) and transfers of USDS to the Spark/Grove SubProxies within them: settlements of agent economics, not spending. Class C14.
- Sky Ecosystem Liquidity Bootstrapping 2.4M + 2.0M USDS passed to Spark (2024–25): treated as an advance against Spark's Genesis Capital (inside SKY-2025-A2).

**Line-item candidates not selected:** 2022→23 contributors (cash + token) −21%; 2023→24 total opex +28% (a total, not a line); 2024→25 opex +6.8%.

## 7. Gaps

1. **2024 and 2025 class A spending is reported as one opex number** (SFF / Block Analitica). There is no split by function, and it is not stated whether SKY/MKR compensation, Launch Project disbursements, Liquidity Bootstrapping or the 2024 Integration Boost are inside it. No Steakhouse-type report exists for 2024 or 2025.
2. **Category labels changed** between the Steakhouse 2022 report (CU overhead / MKR vesting / direct payments) and the 2023 report (workforce / MKR token / third party / keepers). The 2022 split is rounded (30 / 12 / 4).
3. **Integration Boost 2024** is not separately reported. The Q4-2025 vintage puts it inside SSR, while the Q1-2026 vintage separates it from 2025 onward. The 2025 incentives total mixes two report vintages.
4. **Token-denominated decisions with no USD in source:**
   - MKR in 2023 facilitator, EA and Launch Project budgets;
   - STR 600M SKY/yr and its rebalances;
   - Early Bird 27.2M SKY;
   - Liquidity Bootstrapping 320M SKY;
   - Fortification 200M SKY;
   - SFF SKY;
   - SPK farms 3.25B SPK;
   - lsSKY farm 1B SKY.
   
   Per the blinding rule I did not value them.
5. **Approval dates** for 2023 Responsible Facilitator polls (QmRxNdG7 and others) and for exec-only items ("Ecosystem Approval", Stability Facilitator approvals) are given as the forum or exec date. The pass/fail result of pre-2025 polls was inferred from subsequent execution, not read from tallies.
6. **Execution dates** are spell or exec-vote dates, not cast blocks.
7. **Launch Project raise to 60M:** approval date ambiguous (Atlas v2 text 2024-09-12 vs Capital Transparency "October 2024").
8. **SFF actions** (SKY purchases of 45.1M USD, the 500M SKY gift) come from the bench file without exact dates. SFF and Fortification Foundation spending after the grant is level 2 and known only in aggregate: SFF 5.83M to year-end 2025, Fortification not found.
9. **Genesis Capital use by agents** (Spark, Launch Agent 4, Core Council Executor Agent 1) is not reported. Grove, Keel and Launch Agent 3 are listed as Genesis Agents, but no Sky cash contribution to them was found in 2025 executive votes.
10. **The expenses.makerdao.network dashboard** was unavailable (per bench) and was not used.

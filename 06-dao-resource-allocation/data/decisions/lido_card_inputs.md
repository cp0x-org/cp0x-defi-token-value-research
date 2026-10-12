# Lido DAO: case-card inputs for the decision table (Research 6)

Compiled 2026-10-07 under METHOD_R6.md (sections "Чьи расходы", "Три класса", "Отбор решений"). Companion file: `lido_decisions.csv` (14 rows).

Sources used: research.lido.fi forum posts (raw endpoints `https://research.lido.fi/raw/<id>`, including images in those posts), Snapshot space `lido-snapshot.eth` (hub.snapshot.org GraphQL, proposals created 2022-11-01..2025-12-31, 274 proposals listed and screened), and Aragon vote descriptions from the public `lidofinance/scripts` repository (`archive/scripts/vote_2023_*..vote_2025_*.py`). That archive is not a complete list of Aragon votes (see Gaps).

## 0. Blinding log

- I used no price, TVL, fee, revenue or market-share series, and no DefiLlama, CoinGecko or Dune dashboards. I did not open anything under /home/claude/r4, r4rep or r5.
- Incidental exposure, recorded for the auditor:
  - (a) The GOOSE-2025 final report (topic 11304) puts revenue lines and some delegate comments about 2025 results in the same table and thread as the expense figures. I read them while extracting the expense table and did not record or use them.
  - (b) The LIDO-v2 economics image (topic 4476) contains 2021–2022 revenue lines. These are pre-period, and only its expense lines are used here.
  - (c) In topic 6054 I cropped only the header of a Dune "Lido P&L" chart, saw that it was a chart with no expense numbers, and did not view the rest.
  - (d) The NEST thread (topic 10894) was read only to find the execution date, which was August 2026.
- The CSV does not say whether any decision "worked".

## 1. Denominators (levels 1+2)

Definition applied: level 1 + level 2 spending, meaning everything the DAO and its funded committees and foundations spent on class A items. That includes contributor cash and token compensation (TRP), LEGO grants and liquidity and referral incentives. It excludes node-operator rewards (cost of revenue), treasury transfers to multisigs that were not spent, and treasury operations. A decision's year is the year its execution starts, so st2024 v1 (approved 2023-12-14, executed 2024) and Multi-EGG (approved 2024-12-23, executed 2025) take the next year's denominator.

| Decisions in | Denominator year | Figure used (USD) | Type | Composition | 10% threshold | 5% threshold | Source |
|---|---|---|---|---|---|---|---|
| 2023 | 2022 | **129.5M** | actual, "estimated protocol economics based on publicly available blockchain data" (Steakhouse) | Operating Expenses 28.1M + Liquidity Rewards 69.5M + Domain Incentives 31.9M (= "Sales & Marketing Incentives" 101.4M) | 12.95M | 6.48M | https://research.lido.fi/t/lido-v2-may-1-2023-december-31-2023-lido-ongoing-grant-request/4476, image "Overview of Budget Request for LIDO-v2", 2022 column |
| 2024 | 2023 | **65.1M**, FLAGGED: no 2023 full-year actual exists, so per the method the approved 2024 budget is used | approved budget of the current year (2024) | st2024 v1 LCG 22.5M + LOL 8.5M; st2024 v2 LCG 24.6M + LOL 7.1M + CLI 0.4M; LEGO ongoing 4 × 0.5M = 2.0M | 6.51M | 3.26M | 6054, 7697, LEGO Q4-2023 report https://research.lido.fi/t/6501 ("The LEGO budget will remain at $500,000") |
| 2025 | 2024 | **55.2M** | actual (restated, accrual) | Total Foundations' Expenses 52.1M (Operating Expenses 28.8 + TRP 9.7 + LEGO 1.5 + Other 0.9 + Liquidity Rewards 11.2) + deposit referrals 3.1M (Rewards Share, shown by the report under Cost of Revenue) | 5.52M | 2.76M | https://research.lido.fi/t/goose-2025-eggs-2025-final-report/11304, "Overview" table, column 2024Y |
| (reference) | 2025 | 49.6M | actual | 45.5M + deposit referrals 4.1M | – | – | same, column 2025Y |

Notes and flags on the denominators:
- **2022.**
  - The figure is an on-chain estimate published in a grant request, not an audited statement. Incentives are mostly LDO valued in USD by Steakhouse, and the table gives no valuation method.
  - Whether the 28.1M of operating expenses includes LEGO grants or contributor LDO is not stated. TRP did not exist as a programme until 2023 (its term starts 2022-11-01).
  - Using opex only (28.1M) would cut the 2023 threshold to 2.81M. The method's definition of class A includes incentives, so 129.5M is used. This choice matters: under opex only, the LIDO-v2 4M reWARDS cap (14% of 28.1M) would become selectable on its own.
- **2023.**
  - The 2024-budget proxy is circular: the decisions it is used to test (st2024 v1 and v2) make up 96% of it.
  - Excluded from it: the 10% st2024 v1 contingency, the LDO grants (200k + 180k LDO, no USD given), TRP, the Rewards Share stETH pool, the delegate programme ($150k, Sep-2024 to Feb-2025) and Lido Alliance ($125k, inside st2024 v2).
  - Alternative: the stated "Total Budget Request" fields, 34.0M + 31.8M + LEGO 2.0M = 67.8M, which changes no selection.
  - The partial 2023 actuals that exist are listed in §3.
- **2024.**
  - The alternatives are 52.1M (without deposit referrals) and 40.9M ("Total Operating Expenses", which excludes liquidity). With 52.1M the thresholds become 5.21M and 2.61M, and no selection changes. With 40.9M (4.09M and 2.05M) the selections are also unchanged.
  - The deposit referrals were included because the 2022 "Domain Incentives" line also included referral payments, which keeps the years comparable.
- Level 3 (developer companies outside the DAO): not quantified. Examples are P2P's own spending on Lido on Solana ("approximately $700,000" in 2022–2023, https://research.lido.fi/t/5371) and Shard Labs on Polygon. These are noted as a limitation only.

## 2. Mapping table: report categories to our class A line items

Written before the numbers in §3 were filled in.

| Report / source category | Source | Our line item |
|---|---|---|
| Operating Expenses (2022, unsplit) | LIDO-v2 economics image | split not possible; shown as "opex, unallocated" |
| Liquidity Rewards (2022, 2024, 2025) | 4476 image; 11304 | incentives to users/integrations |
| Domain Incentives (2022) | 4476 image | incentives to users/integrations (referral programmes and Lido-on-X incentives) |
| reWARDS / LOL budgets and grants | reWARDS monthly posts; EGGs | incentives to users/integrations |
| Referral programme / Rewards Share / "Cost of Revenue (deposit referrals)" | 4243, 4851, 6812; 11304 | incentives to users/integrations |
| LCG "General & Administrative" (RCC/PML/ATC) | 4476, 6054 | legal/ops (including the G&A staff of contributors) |
| LCG "Research & Development" | 4476, 6054 | development (contractor engineers, audits included) |
| LCG "Education, Advocacy & Outreach" | 4476, 6054 | marketing/growth |
| Compensation and Service Fees (2024–25) | 11304 post #6 image | contributors/core team (development staff included; not separable in 2024, rough 2025 split given as a memo) |
| TRP costs | 11304 | contributors/core team (token compensation) |
| Audit & Testing | 11304 post #6 | security |
| Legal | 11304 post #6 | legal/ops |
| Infra & SaaS | 11304 post #6 | legal/ops (operations) |
| Events & Marketing | 11304 post #6 | marketing/growth |
| Other expenses; Other income and expenses | 11304 | other |
| LEGO grants | 11304; LEGO quarterly reports | grants |
| Delegate Incentivization Programme | 7858, 2533 snapshot | governance (no separate actual found, so it is inside opex or LEGO) |
| Bug bounty reserve | 9067 | security (a reserve; spent only on payouts) |
| Lido Alliance BORG, CLI | 8173, 9068, 7527 | marketing/growth (Alliance); grants (CLI); no separate actuals |

## 3. Class A line items by year (USD M)

| Our line item | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| contributors/core team | in opex 28.1 (unsplit) | LCG partial actuals: Jan–Mar 3.71 (G&A 1.32, R&D 1.89, EAO 0.50); Apr not reported; May–Dec 12.5 (G&A 4.8, R&D 6.2, EAO 1.5). TRP: no 2023 cost reported | 27.8 = Comp & Service Fees 18.1 + TRP 9.7 | 29.6 = Comp & Service Fees 23.2 + TRP 6.4 (memo: R&D 16.0 [core 11.3, new products 4.7], G&A 4.6, Ecosystem Growth & Comms 2.6, all within the 23.2) |
| development (non-staff) | n/a | inside LCG R&D above | not separable | not separable |
| grants (LEGO) | n/a | 1.71 *allocated* (Q1 0.629, Q2 0.242, Q3 0.546, Q4 0.297) | 1.5 (accrual incl. LDO; allocations 0.92) | 1.1 |
| security | n/a | not reported | 2.3 | 3.0 |
| incentives to users/integrations | 101.4 (liquidity 69.5 + domain 31.9) | ceiling 14 ("total max spend in all sales & marketing incentives"); reWARDS Jan–May budgets in LDO: 2,896,300 / 2,146,320 (stated $4,347,000) / 1,291,400 / 788,700 / 503,800 LDO; Jun–Dec cap 4m DAI-equiv; Rewards Share pool 3,000 stETH. Actual not reported | 14.3 = Liquidity Rewards 11.2 + deposit referrals 3.1 | 8.9 = 4.8 + 4.1 |
| governance | n/a | n/a | inside opex | inside opex (0.3 approved) |
| marketing/growth | inside opex | inside LCG EAO above | 4.3 | 2.2 |
| legal/ops | inside opex | inside LCG G&A above | 3.1 = Legal 1.3 + Infra 1.8 | 3.7 = 1.7 + 2.0 |
| other | – | – | 1.8 = Other expenses 0.9 + Other income/expenses 0.9 | 1.1 = 1.0 + 0.1 |
| **total (levels 1+2)** | **129.5** | **not determinable** | **55.2** | **49.6** |

The 2024 and 2025 sub-lines are summed from the OPEX breakdown image (11304 post #6). They sum to 28.7 and 33.1 against the reported 28.8 and 33.0 because of rounding in the source.

Line-item change test (more than 25% year on year and at least 5% of the denominator):
- 2022→2023, incentives: 101.4 → at most 14 (ceiling). This is selected (`LIDO-2023-LI1`) with the flag that the 2023 value is a ceiling, not an actual. No other line can be tested.
- 2023→2024: no line can be tested, because 2023 actuals are partial and on a different basis. A candidate the auditor should note: contributors/opex 2023 LCG at least 16.2 (excluding April, TRP and LEGO) against 2024 opex 28.8. That looks like more than 25% and more than 3.26M, but the scopes are not comparable, so it is **not selected**.
- 2024→2025, by line:
  - Incentives −5.4 (−38%): selected (`LIDO-2025-LI1`).
  - Contributors +1.8 (+6%): no.
  - Marketing −2.1 (−49%, but below 2.76): no.
  - Security +0.7 (+30%, below 2.76): no.
  - Legal/ops +0.6 (+19%): no.
  - Other −0.7: no.
  - Grants −0.4: no.
- One caution: if TRP were treated as its own line, TRP −3.3 (−34%) and Comp & Service Fees +5.1 (+28%) would each pass. The pre-written mapping puts both under contributors/core team, so neither is selected.

## 4. Selected decisions (summary; details in the CSV)

| id | class | amount USD | materiality | rule |
|---|---|---|---|---|
| LIDO-2023-A1 TRP 22M LDO | A | not stated (LDO) | not computable | ≥10%, provisional |
| LIDO-2023-A2 LIDO-v2 LCG | A | 20.5M | 0.158 | ≥10% |
| LIDO-2023-LI1 incentives cut 2022→23 | A | −87.4M (ceiling-based) | 0.675 | line-item |
| LIDO-2024-A1 st2024 v1 LCG | A | 22.5M | 0.346 | ≥10% |
| LIDO-2024-A2 st2024 v1 LOL | A | 8.5M | 0.131 | incentives ≥10% |
| LIDO-2024-A3 st2024 v2 LCG | A | 24.6M | 0.378 | ≥10% |
| LIDO-2024-A4 st2024 v2 LOL | A | 7.1M | 0.109 | incentives ≥10% |
| LIDO-2025-A1 Multi-EGG LCG Q1 | A | 11.1M | 0.201 | ≥10% |
| LIDO-2025-A2 Multi-EGG LOL H1 | A | 8.5M | 0.154 | incentives ≥10% |
| LIDO-2025-A3 Lido Labs BORG Foundation | A | 34.88M | 0.632 | ≥10% |
| LIDO-2025-A4 Lido Ecosystem BORG Foundation | A | 10.61M | 0.192 | ≥10% |
| LIDO-2025-A5 LOL H2 (via LEF request) | A | 8.5M | 0.154 | incentives ≥10% |
| LIDO-2025-LI1 incentives 2024→25 | A | −5.4M | 0.098 | line-item |
| LIDO-2025-B1 Curated Module fee split | B | n/a | n/a | every class B |

Notes on the selected decisions:
- **LIDO-2023-A1 (TRP).** USD is not stated in the source. The opt-in policy price of 1.5294 LDO/USD appears in the post, but I did not multiply it out, per the instruction not to compute prices. The provisional inclusion rests on reported TRP accrual costs (2024 9.7 + 2025 6.4 = 16.1M, above the 12.95M threshold).
- **LIDO-2025-B1 (class).** The class B assignment is arguable. The decision moves 1.5% of curated-module rewards from node operators to the DAO treasury and is not a payout to LDO holders.
- **No other class B decision was executed in 2023–2025** (see §6).

## 5. Class C decisions (descriptive, no threshold)

| # | Decision | Approved | Executed | Size (as stated) | Source |
|---|---|---|---|---|---|
| C1 | Treasury Management Principles and formation of the Treasury Management Committee (ETH as unit of account; "All treasury ETH must be staked using Lido") | Snapshot 2023-04-27 | 2023 | – | https://research.lido.fi/t/4279 ; snapshot 0xac31f800288c68e32d1eb3cea7a525022faae3eb3bf805d1b3d248cda5375a13 |
| C2 | TMC-0: stake all treasury ETH in Lido | TMC poll to 2023-06-03 | Aragon vote executed 2023-06-30 (block 17593968) | 20,304.357 ETH | https://research.lido.fi/t/4744 ; scripts vote_2023_06_20_2.py |
| C3 | TMC-1: pipeline to sell surplus stETH for stablecoins (12 months of working capital when 3 months remain); implemented via Stonks Easy Track factories | TMC poll to 2023-08-04; Aragon 2024-03 | Aragon vote executed 2024-03-22 (block 19491793) | Easy Track limit 9,000 stETH | https://research.lido.fi/t/5059 ; https://research.lido.fi/t/6860 ; scripts vote_2024_03_19.py |
| C4 | Stablecoin payments for the LCG via Easy Track (DAI/USDT/USDC) and stETH top-up factories for RCC/PML/ATC; one-off stETH transfers to the LCG (Nov–Dec 2023: 272+434+380 stETH, then 224+359+314 stETH) | 2023-11 / 2024-01 | Aragon 2023-11-10, 2023-12 / 2024-01 | as listed | scripts vote_2023_11_07.py, vote_2023_12_18.py, vote_2024_01_23.py; https://research.lido.fi/t/6375 |
| C5 | TMC-4: raise Stonks stETH limit from 9k to 12k and reset spent amount | TMC poll to 2024-10-16 | Aragon vote executed 2024-12-20 (block 21444425) | 12,000 stETH per 6 months | https://research.lido.fi/t/8616 ; scripts vote_2024_12_17.py |
| C6 | TMC-3: repatriate remaining ~13k stSOL from the Lido on Solana treasury, sell for USDC to the Aragon Agent | TMC (2025) | 2025, exact date not found; post marked "Closed" | ~13k stSOL / ~14k SOL | https://research.lido.fi/t/8615 |
| C7 | TMC-5: transfer 508,106 MATIC to the LOL multisig (recorded as LOL 2025 spending) | TMC poll to 2025-10-24 | Aragon vote #195 executed 2025-12-20 | "~$96k" | https://research.lido.fi/t/10814 ; scripts vote_2025_12_15.py |
| C8 | TMC-6: convert treasury stablecoins into sUSDS or TMMFs; add sUSDS to the allowed tokens and Easy Track payments (2,000,000 sUSDS limit) | Snapshot 2025-12-01 (0x4dd947f5…) | Aragon vote #195 executed 2025-12-20 | full stablecoin balance (amount not stated in the vote) | https://research.lido.fi/t/10868 |
| C9 | Bug bounty reserve, "to be drawn down only in the event of payout events" (reserve; spend is class A security, below threshold) | Snapshot 2024-12-23 | 2025 ("largely unused") | 2.0M DAI | https://research.lido.fi/t/9067 ; 11304 |

Not in period: Treasury Diversification #2 (2022, topic 2570); the Feb-2023 "Should LidoDAO sell treasury ETH?" and related polls (topic 3868; no Snapshot vote found, superseded by C1); Lido Earn treasury allocation (2026, topic 11228).

## 6. Considered and rejected (one line each)

Thresholds: 2023 = 12.95M / 6.48M; 2024 = 6.51M / 3.26M; 2025 = 5.52M / 2.76M.

- [LIDO-1] Nov-2022–Apr-2023 LCG grant 11.2M DAI (Snapshot 2022-11-10): execution started before 2023-01-01, and it is below 12.95M anyway.
- Lido on Polygon incentive structure (Snapshot restart 2023-01-18) and 150,000 LDO milestone payment (Aragon 2023-01-27): LDO-only, no USD in source, a small token amount.
- Retire Ethereum and Solana Referral Programs (Snapshot 2023-04-14): no amount. Covered as a contributing decision inside `LIDO-2023-LI1`, not a separate row.
- LIDO-v2 reWARDS cap 4M DAI-equiv (2023-05-11): 3.1% of D2022 as a spend decision. Covered as a contributing decision inside `LIDO-2023-LI1`.
- reWARDS monthly budgets Jan–May 2023: committee budgets under earlier authority, not DAO votes. The 170 stETH June 2023 top-up (Aragon 2023-05-26) is small.
- Liquidity Observation Lab relaunch (topic 5335, Aug 2023): no new funds; it ran inside the LIDO-v2 4M cap.
- Tiered Rewards Share Program (Snapshot 2023-06-29), initial pool 3,000 stETH: no USD in source, so materiality cannot be shown. The 2024 reported deposit referrals (3.1M) are below 12.95M.
- Rewards-Share Program 2024 (Snapshot 2024-03-21): no new funds (remaining 2,866.969 stETH of the 3,000 pool).
- RockLogic slashing compensation, 13.46 stETH burned (Snapshot 2023-04-27, Aragon 2023-06-30): immaterial.
- Sushi recovery 39.8 ETH (May 2023): "No action" won.
- Nethermind validator-set mechanism Phase II (2023-03), Launchnodes Impact Staking LEGO grant (2023-06), Community Lifeguards Initiative (2023-06): small grants far below 12.95M.
- Lido on Solana funding request of 1.5M USD/year (topic 5371): the DAO voted to sunset instead (Snapshot 2023-10-05). No spend was approved.
- GOOSE (2023-09), GOOSE 2023 goals (2023-11), ReGOOSE (2024-05), GOOSE 2024 goals (2024-11), GOOSE-3 goals (2025-12): goal-setting, no money. They are the source of the goals quoted in the EGGs.
- "Proposal to burn 30% of the LDO supply" (Snapshot 2023-09-13): community spam with 6,066 LDO voting, far below quorum. Not a decision. It would have been class B.
- "Proposed Overhaul of the TRP" (several community Snapshots, 2023-09): below quorum, so not decisions.
- st2024 v1 10% contingency (2.25M): reserved, not approved as a grant.
- Community Lifeguards Initiative 2024 (0.4M within st2024 v2; Snapshot 2024-07-04): 0.6%.
- Lido Alliance (Snapshot 2024-05-23, endorsement framework, no grants); Lido Alliance BORG setup $125k (2024-09-05); Lido Alliance grant $300k (2024-12-23); Lido Alliance Foundation 2025 $0.3M: all below threshold.
- Public Delegate Platform and Delegate Incentivization $150k in LDO (2024-08-08); extension through 2025 (2025-04-28, total 2025 programme $0.3M): below threshold.
- Activate Lido Protocol Governance with Revenue Share Staking (Snapshot 2024-04-08): **rejected by vote** (No 2.67M vs Yes 2.07M LDO). Class B, not approved.
- Change Easy Track limits for PML and ATC (2024-10 / Aragon 2024-12-20), and Increasing LOL Easy Track limits (2025-04-28): procedural, within approved grants.
- Network Expansion Committee (2024-11-28), stVaults Committee (2025-09-29), Auxiliary Proposer Mechanisms Committee (2025-05): no budget attached.
- LEGO ongoing grant $0.5M per quarter: approved 2022-10-20 (out of period), and $2M/yr is 3.1–3.6% of the denominators.
- Bug bounty reserve 2M DAI (Multi-EGG): 3.6% of D2024. It is listed under class C as a reserve.
- Establishment of the Lido Labs and Lido Ecosystem BORG Foundations (Snapshot 2025-01-30): governance and legal wrappers, no amount. Funding came through rows A3–A5.
- Transfer TRP to Lido Labs Foundation and amend TRP terms (Snapshot 2025-11-07; Easy Track TRP limit 15M LDO set by Aragon #195 on 2025-12-20; new vesting by Aragon #197 executed 2026-01-01): no new allocation ("No change from 22,000,000 LDO allocated"), and it reallocates 6,992,835 LDO without USD. Not selectable.
- CSM parameters, CSM v2 fee structure (2025-05-28), SSV Lido Module (2025-03): protocol parameters with no spending decision found.
- NEST – Network Economic Support Tokenomics (Snapshot 2025-09-29, approval of the mechanism only, "This proposal does not suggest enacting a first distribution"); follow-up NEST buyback Snapshot and Aragon vote #204 executed in **2026-08**. Class B, **executed after 2025-12-31, so out of period**.
- Dynamic Buyback Program for LDO (topic 10494, 2025-08), Enable LDO staking with revenue sharing (topic 10195, 2025-06), Align LDO with protocol fees (topic 10589): discussion only, no Snapshot vote found in 2025.
- 2026 EGG: Executing GOOSE-3 (Snapshot 2025-12-19): execution 2026, out of period.
- Line-item candidates not selected: 2024→2025 marketing −2.1M (below 2.76M), security +0.7M, legal/ops +0.6M, other −0.7M, grants −0.4M; 2023→2024 contributors/opex (non-comparable data, §3).

## 7. Gaps

1. **2023 full-year actual spending is not reported anywhere I found.** Available pieces:
   - LCG Jan–Mar 3.71M and May–Dec 12.5M ("Actuals Dec 23" in a 2023-12-01 post, so December is probably partly a forecast);
   - LEGO allocations 1.71M;
   - incentive budgets in LDO only.
   April 2023, the 2023 TRP cost, actual 2023 liquidity and referral spending, and Rewards Share payouts are all missing. As a result, the 2024 denominator is a circular budget proxy.
2. **2022 denominator** is a Steakhouse on-chain estimate. LDO incentive valuation is not documented, and opex is not split by category.
3. **Line items 2022–2023** cannot be mapped to our categories beyond G&A, R&D and EAO for the LCG. Security, legal, governance and marketing are not separable before 2024.
4. **Development vs contributors:** not separable in 2024. The 2025 split is described by the source as "a rough indication".
5. **Governance (delegate incentives), CLI, Alliance:** no separate actuals; they sit inside opex or LEGO.
6. **Token-denominated decisions** (TRP 22M LDO, LIDO-v2 200k LDO, st2024 v1 200k LDO, st2024 v2 180k LDO, Rewards Share 3,000 stETH): no USD value in the sources, so materiality is not computed.
7. **Aragon coverage:** the vote list comes from the `lidofinance/scripts` archive, which is incomplete (for example, vote #160, the LDO transfer under LIDO-v2, is not in it). Public RPC endpoints refused archive log queries, so on-chain `StartVote` events were not enumerated. Some Aragon-only decisions may be missing, although every grant and budget decision I found went through Snapshot first.
8. **Execution dates** for grants are the grant periods. Actual Easy Track draw-down dates were not collected. Grants are "drawn monthly based on actuals", per topic 9708.
9. **Actual versus approved for selected grants** (for the case card): 2023 LCG 12.5M of 20.5M; st2024 v1 YTD 9.9M of 22.5M through about mid-May 2024; st2024 v2 6.9M of 24.6M through September 2024; 2025 total 45.5M against 77M approved (sources 6054, 7697, 11304). Per-grant actuals for 2025 were not found.

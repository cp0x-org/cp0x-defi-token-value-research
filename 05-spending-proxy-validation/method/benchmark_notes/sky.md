# Sky (formerly MakerDAO): reported operating expenses benchmark, 2023 to 2025

Collected 2026-10-07. Sources are published reports only: the Steakhouse Financial annual report and the Sky Frontier Foundation (SFF) quarterly and annual reports. SFF's figures come from the Block Analitica dashboards (info.sky.money / info.skyeco.com). No on-chain analysis was done.

## 1. Benchmark table

| period_start | period_end | amount_usd | type | included | excluded | source URL | exact quote / table reference |
|---|---|---|---|---|---|---|---|
| 2023-01-01 | 2023-12-31 | **53.7M (DAI ~ USD)** | actual (cash basis, Steakhouse) | Direct to Third Party Expenses 20.1 + Keeper Maintenance 0.4 + Workforce Expenses 17.8 + MKR token expenses 15.4 | DSR 32.7, shown above the line under "Direct expenses". Smart Burn Engine / MKR burns of 59.6M are not opex. Liquidations are netted into revenue. | https://kitchen.steakhouse.financial/p/makerdao-financial-report-2023 (PDF: https://aqua-hollow-alpaca-520.mypinata.cloud/ipfs/QmdPmF9EuogwY5F2VHbYXG6eke8hYBvBc5p5rXQtvg1WtM) | p.13 "Consolidated Statement of Earnings … Year ended December … Total operating expenses (22.2) [2021] (46.2) [2022] (53.7) [2023]". p.15 monthly table, 2023 column: "Direct to Third Party Expenses (20.1) / Keeper Maintenance (0.4) / Workforce Expenses (17.8) / MKR token expenses (15.4) / Total operating expenses (53.7)" with "DSR (32.7)" under Direct expenses. Units: "in millions of Dai". |
| 2024-01-01 | 2024-12-31 | **69M** | actual (dashboard data, as reported by SFF) | "Operational Expenses" line | Sky Savings Rate (SSR) 141, "Sky Rewards for Supplying USDS" 11 (Total Expenses 221) | https://insights.skyeco.com/insights/sky-ecosystem-q4-update-and-2026-outlook-summary (PDF: https://cdn.prod.website-files.com/695f9feb261706edf90af3b3/699498a875d54c0082bd88d0_Sky%20Ecosystem%20Q4%20and%202026%20Outlook.pdf) | "Protocol Expenses ($M) … FY '24 … Operational Expenses 69 … Sky Savings Rate (SSR) 141 … Sky Rewards for Supplying USDS 11 … Total Expenses 221". Source line: "Info.sky.money; data as of December 31, 2025." The 2024 quarterly split is not published (only Q4 '24 = 24). |
| 2025-01-01 | 2025-12-31 | **73.71M (preferred)** | actual (dashboard data, SFF Q1 2026 report vintage) | Operating Expenses Q1 17.08 + Q2 20.26 + Q3 21.11 + Q4 2.85, plus Q4 "Operating Expenses – Buffers" 12.41 (governance funding for Sky Core Council and Aligned Delegates, reclassified out of Opex from Q4 2025) | Direct Expenses (SSR/DSR/staking/SKY rewards) 77.55/40.48/30.05/45.52. Integration Expenses 14.89/3.88/2.02/6.37 (= 27.16, Integration Boost / distribution payments to integrators and agents, treated as incentives). Revenue Allocation (buybacks). | https://insights.skyeco.com/insights/sky-ecosystem-q1-2026-quarterly-report-summary (PDF: https://cdn.prod.website-files.com/695f9feb261706edf90af3b3/6a46c053e218f8e0a415b0bc_SFF-Q1-Report.pdf) | Appendix "Full Quarterly P&L 2025 to 2026": "Operating Expenses $17.08M $20.26M $21.11M $2.85M" (Q1–Q4 '25). "Operating Expenses / Buffers — — — $12.41M" (Q4 '25). Text: "Beginning in Q4 2025, governance funding for the Sky Core Council and Aligned Delegates was reclassified from Operating Expenses to a new line item, Operating Expense (Buffers). This reclassification, not a reduction in actual spending…". Sum of 4 quarters plus buffer = 73.71. |
| 2025-01-01 | 2025-12-31 | 67M (alternative, earlier vintage) | actual (dashboard data as of 2025-12-31) | "Operational Expenses" Q1 17 + Q2 20 + Q3 21 + Q4 8.8 | SSR 194, Sky Rewards 21, stUSDS staking 2.6 (Total Expenses 285) | Q4 2025 report PDF above | "Operational Expenses 24 [Q4'24] 17 [Q1'25] 20 [Q2'25] 21 [Q3'25] 8.8 [Q4'25] 69 [FY'24] 67 [FY'25]". Q4 '25 was later restated (see notes). |
| 2025-06 (inception) | 2025-12-31 | 5.83M (SFF entity only, not protocol) | actual (SFF's own books) | SFF Costs 2,326,538 + Public Goods 3,503,364 | n/a | https://insights.skyeco.com/insights/sff-q1-2026-transparency-report | "Total operating expenses from inception through year-end 2025 came in at $5,829,902 … $2,326,538 in SFF Costs and $3,503,364 in Public Goods." Funded out of the SFF grant below. Do not add it to the protocol figure. |
| n/a (snapshot 2025-01-01 vs 2025-12-15) | | 113.4M → 43.6M | annualized run-rate, NOT a period total | "Annualized Operational Expenses" | | https://insights.skyeco.com/insights/annual-state-of-sky-ecosystem (PDF SFF_Report_2025.pdf) | "Annualized Operational Expenses $113.4M $43.6M -61.5%". Not usable as a calendar-year figure. Listed for reference only. |

**Recommended benchmark values**
- 2023 = 53.7M DAI (Steakhouse)
- 2024 = 69M (SFF / Block Analitica)
- 2025 = 73.71M (SFF Q1 2026 report, old basis including Buffers). The SFF Q4 2025 report gives 67M.

The 2023 figure and the 2024–25 figures come from different preparers and methodologies, so the series is not strictly comparable.

## 2. Scope notes

**How Sky pays expenses**
- Most contributor and budget payments are executed by executive spells. They take one of three forms:
  - Direct DAI/USDS transfers out of the MCD Pause Proxy (0xBE8E3e3618f7474F8cB1d074A26afFef007E98FB). In practice this is DAI/USDS minted against the Surplus Buffer via `Vat.suck`, then joined out (DssExecLib `sendPaymentFromSurplusBuffer`).
  - DssVest streams. DssVestSuckable mints DAI/USDS directly from the Vat via `suck`, while DssVestMintable/Transferrable streams cover MKR/SKY compensation.
  - Transfers of MKR/SKY held by the Pause Proxy treasury.
- Examples include monthly spells titled "Aligned Delegate compensation", "Atlas Core Development payments" and "Launch Project funding" (e.g. v2.vote.makerdao.com executive of 2025-04-17 and 2025-07-24).
- `suck`-funded payments reduce the Surplus Buffer without passing through a separate treasury wallet. That is why Steakhouse records them as expenses against surplus rather than treasury outflows.

**2023 (Steakhouse)**
- Cash-basis "MakerGAAP".
- "MKR token expenses" (15.4M) are valued in DAI at payout and are offset in the statement of changes by "Issuance for MKR token expenses 15.4". An appendix table later in the same PDF shows 11.7 for the same line total, which is an internal inconsistency; the main statement uses 15.4.
- Workforce Expenses include negative or near-zero months (Nov +0.5, Sep (0.1)), which reflects Core Unit refunds or returns of surplus.
- "Direct to Third Party Expenses" (20.1) is not broken down further in the report. It likely covers Ecosystem Actors, Aligned Delegates and similar payees.

**2024/2025 (SFF / Block Analitica)**
- What "Operating/Operational Expenses" includes is described only loosely: "controllable overhead (security, oracles, smart contract execution, contributor costs)" plus Core Council / Aligned Delegate governance funding (moved to "Buffers" / "Security and Maintenance" from Q4 2025).
- The reports do not state whether SKY/MKR-denominated compensation (vesting) is included or at what valuation. This is a gap.

**Restatements**
- Block Analitica restates history. The Q2 2026 report gives Q2'25 20.64, Q3'25 21.41 and Q4'25 3.24 (+12.41 "Security and Maintenance").
- Combining that vintage with Q1'25 = 17.08 (Q1 2026 vintage) gives 74.78M for 2025. This mixes two report vintages and is not recommended.
- The Q2 2026 report also restates total Q1'25 expenses to 109.74 (vs 109.52).

**Double-counting risks**
- The SFF grant (≥$50M USDS plus other assets, June 2025) funds SFF's own opex (5.83M in 2025). Counting both double counts.
- Genesis Capital given to Sky Agents (Spark, Grove, etc.) funds those agents' own spending.

**Reclassification**
- The Q4 2025 headline drop in opex ("-63% YoY", "$8.8 million in Q4") is largely a reclassification to Buffers, per SFF's own Q1 2026 note.

## 3. Spending flows outside the reported operating expenses

- **Savings rate expense.** DSR in 2023 was 32.7M. SSR was 141M in 2024 and 194M in 2025, per the Q4 2025 report. These are excluded by definition.
- **Token incentives.** Sky Token Rewards / "Sky Rewards for Supplying USDS" were 11M (2024) and 21M (2025). stUSDS staking was 2.6M (2025). SKY staking rewards and Spark incentives are also outside opex.
- **Integration Expenses (2025).** Integration Boost and Distribution Rewards to integrators and agents total 14.89 + 3.88 + 2.02 + 6.37 = 27.16M (Q1 2026 report vintage). These are excluded as incentives, but arguably they are business-development spend.
- **Buybacks.** The Smart Burn Engine bought MKR/LP worth 59.6M DAI in 2023 (Steakhouse). "Revenue Allocation" in 2025 was 77.47/40.19/14.64/19.35 (Q2 2026 report). The SFF 2025 report says "Sky Buybacks $92.2M".
- **Sky Frontier Foundation endowment.** "SFF's initial grant comprising $50M USDS alongside various other assets", received June 2025. The SFF 2025 annual report says R&D costs were "reallocated … to external entities such as the Sky Frontier Foundation, which received endowment capital". This is not in protocol opex.
  - SFF later spent $45.1M buying SKY and gifted 500M SKY back to the Pause Proxy, both in H2 2025.
- **Launch Project and Genesis Capital.** Launch Project funding and Genesis Capital for new Sky Agents were paid by spells (e.g. the 2025-04-17 executive). The reports do not show these in the Operating Expenses line, and their inclusion is unclear. Genesis capitalization was sunset in June 2026.
- **Not found.** The expenses.makerdao.network dashboard returned an error (HTTP 521) and was not used. No Steakhouse annual report exists for 2024 or 2025. There is no published quarterly split of 2024 opex beyond Q4 '24 = 24M.

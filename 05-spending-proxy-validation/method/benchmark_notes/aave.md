# Aave DAO — reported spending benchmark, 2023–2025

Collected 2026-10-07. Sources are published statements only: the Aave Insights income statement (data supplied by TokenLogic) and governance-forum posts by TokenLogic and ACI. No on-chain analysis and no DefiLlama data were used.

## 1. Main table

The primary series is the "Service Providers" line of the annual Income Statement on Aave Insights. The page footer says "Data supplied by TokenLogic". The figures below are the values embedded in the page's JSON (`"label":"Service Providers" ... "yearly":[...]`), and the rendered table shows them rounded.

| period_start | period_end | amount_usd | type | included | excluded | source URL | exact quote / table reference |
|---|---|---|---|---|---|---|---|
| 2023-01-01 | 2023-12-31 | 12,130,218.18 (shown as "-$12.13M") | actual (dashboard income statement) | "Service Providers" line: DAO service-provider compensation. The page does not give a methodology, so it is unknown whether AAVE-denominated streams and Aave Grants DAO are inside this line (see notes). | Separate lines that are not in this figure: Staking -$28.66M, Incentives -$18.59K, GHO -$2.14M, Insurance —, Partnerships —, Other Expenses -$54.62K | https://insights.aave.com/dashboard | Income Statement, "Annual" tab, column "2023", row "Service Providers": "-$12.13M"; JSON yearly[0] = -12130218.179211784 |
| 2024-01-01 | 2024-12-31 | 22,069,698.40 (shown as "-$22.07M") | actual (dashboard income statement) | same as above | Staking -$39.65M, Incentives -$9.59M, GHO -$2.44M, Partnerships -$2.95M, Other Expenses -$1.81M | https://insights.aave.com/dashboard | column "2024", row "Service Providers": "-$22.07M"; JSON yearly[1] = -22069698.399726976 |
| 2025-01-01 | 2025-12-31 | 24,146,813.32 (shown as "-$24.15M") | actual (dashboard income statement) | same as above | Staking -$49.78M, Incentives -$19.45M, GHO -$8.49M, Insurance (Umbrella) -$5.2M, Partnerships -$1.24M, Other Expenses -$917.9K | https://insights.aave.com/dashboard | column "2025", row "Service Providers": "-$24.15M"; JSON yearly[2] = -24146813.31614495 |

The same table also reports these totals:

| Year | Total Revenue | Total Expenses (all lines) | Net Income |
|---|---|---|---|
| 2023 | $25.62M | -$43M (-43,002,847.33) | -$17.38M |
| 2024 | $96.09M | -$78.51M (-78,510,654.24) | $17.58M |
| 2025 | $152.44M | -$109.23M (-109,230,897.64) | $43.21M |

A broader alternative is possible if a consumer wants "opex" to include every non-incentive and non-staking line, that is Service Providers + Partnerships + Other Expenses (+ GHO). For 2023 that gives 12.13 + 0 + 0.05 (+2.14). For 2024 it gives 22.07 + 2.95 + 1.81 (+2.44). For 2025 it gives 24.15 + 1.24 + 0.92 (+8.49). This sum is derived and the source does not state it. The page does not define the GHO line, which is probably GHO liquidity or peg costs such as GLC/ALC, so it is listed separately.

### Supplementary or cross-check figures (budgets, run-rates and partial figures, not calendar-year actuals)

| period | amount | type | source | quote |
|---|---|---|---|---|
| 2025 (annualised) | ~$16M stablecoins (table total 16,078,000 GHO/yr) plus 26,850 AAVE/yr (7,800 allowance + 19,050 stream) | budget (annualised run-rate) | https://governance.aave.com/t/aave-dao-funding-insights/24192 (TokenLogic, 2026-02-28) | "total SP stablecoin costs rise from ~$16M in stablecoins during 2025 to approximately $51M in 2026"; "The total annualised AAVE emissions to SPs projected forward into 2026, based upon 2025 spend is 26,850". Table "Before 1st April 2026 … Total Annualised Spend 16,078,000" (BGD 4.4M, ACI 3.0M, Chaos 2.55M, Certora 2.628M, TokenLogic 2.5M, LlamaRisk 1.0M) |
| 2025 | $40–45M "total budget (outside umbrella & buyback financing)" | budget (projection, includes incentives such as Merit) | https://governance.aave.com/t/arfc-aavenomics-implementation-part-one/21248 (ACI, Mar 2025) | "we believe a $40–45M total budget (outside umbrella & buyback financing) is a credible conservative higher range scenario for the 2025 budget"; also "Half of the 2024 budget went to support Aave Labs for the creation of V4" |
| 2023 (risk only) | $3.5M | budget (partial category) | https://governance.aave.com/t/arfc-aave-funding-update/15194 (TokenLogic, Oct 2023) | "During 2023, the Risk Service provider budget was $3.5M nominated in AAVE, aUSDC and aEthUSDT." |
| 2024-05 run-rate | ~$12M/yr | delegate comment, not a report | https://governance.aave.com/t/temp-check-aave-2030/17539 (post #8, 0xkeyrock.eth) | "the current Aave costs are around $12m / year" |
| Feb 2026 run-rate | ~$30.5M/yr (all SPs) / $16.5M/yr (all SPs excluding Labs) | run-rate (2026, outside the window) | https://governance.aave.com/t/aci-full-transparency-report/24085 ; https://governance.aave.com/t/aave-labs-86-million-23-of-the-token-supply-and-this-is-their-track-record/24159 | "The entire service provider ecosystem costs ~$30.5M per year"; "All other service providers combined cost $16.5M per year" |

Not found: any audited or forum-published Aave DAO annual financial statement for 2023, 2024 or 2025, and any TokenLogic, karpatkey or AFC report that states realised calendar-year totals on the forum. Llama's 2023 monthly and quarterly financial reports (Jan–Aug 2023, plus Q1 2023) exist as PDFs at llama.xyz/reports/aave/…, but those PDFs could not be retrieved, and the forum posts give only revenue and treasury key takeaways. Because of this, no H1-2023 sub-period sum could be built from them.

## 2. Scope notes

- **Entity and nature of the source.** Aave DAO, all networks. The figures come from the "Income Statement" on insights.aave.com, which is Aave's official site with "Data supplied by TokenLogic", TokenLogic being the DAO's finance service provider. The page disclaimer reads: "Aave Insights presents onchain data and analytics … Methodologies may differ from conventional financial reporting … not audited financial or corporate reporting." So these are figures published by a service provider, derived from on-chain data and calculated by TokenLogic, not by us. They are realised flows rather than budgets.
- **Methodology gap.** No definition is published for "Service Providers", "Partnerships", "GHO" or "Other Expenses". It is unknown whether:
  - AAVE-paid compensation (e.g. BGD and Chaos AAVE streams, the KPI program) is valued inside "Service Providers". It probably is, since the line is in USD, but this is not stated.
  - Aave Grants DAO (2023 GHO, aUSDT and ARB allowances, ~$616k GHO plus 612k aUSDT per 6 months per the Oct-2023 funding update) and events and sponsorship budgets (Aave Companies, $550k per quarter in 2023) sit in "Service Providers", "Partnerships" or "Other".
  - Orbit delegate compensation sits in "Service Providers" or "Other".
- **Exclusions match the benchmark definition where the table separates them.** Staking (SM / stkAAVE / stkABPT emissions), Insurance (Umbrella emissions, from 2025), Incentives (LM / Merit) and buybacks are not inside "Service Providers". Buybacks do not appear as an expense line at all. The cost of revenue paid to depositors is not in the statement, because revenue is net protocol revenue.
- **Labs V4 funding.** The 2024 figure most likely includes the Aave Labs V4 development grant ($12M GHO, approved in 2024; ACI says "Half of the 2024 budget went to support Aave Labs for the creation of V4"). Whether it is booked by stream accrual or by claim date is not stated.
- **Payment rails.** Per the forum proposals, SP compensation is paid from the Aave Collector on Ethereum (0x464C71f6c2F760DdA6093dCB91C24c39e5d6e18c) via Sablier-style collector streams (e.g. stream IDs 100004–100017 in the Oct-2023 table) and direct allowances or transfers in GHO, aUSDC, aUSDT and DAI. AAVE compensation comes from the Ecosystem Reserve and its controller (allowances and streams). TokenLogic notes that assets "are periodically consolidated on Ethereum, from which the vast majority of the DAO's costs are incurred". Some ARB was paid to AGD, and some L2 collectors exist. The dashboard does not split by chain.
- **Double counting.** The TokenLogic 2025 run-rate ($16.08M stablecoins plus 26,850 AAVE) and the dashboard 2025 actual ($24.15M) overlap and must not be added together. The dashboard figure plausibly equals stablecoins plus AAVE at market value plus one-offs such as the V4 security budget ($1.5M approved, $1.47M spent in Q4 2025 per the TokenLogic Funding Insights post).

## 3. Other spending flows not in the "Service Providers" figure

From the same insights.aave.com income statement:

| Year | Staking (SM) | Incentives | GHO | Insurance (Umbrella) | Partnerships | Other |
|---|---|---|---|---|---|---|
| 2023 | -$28.66M | -$18.59K | -$2.14M | — | — | -$54.62K |
| 2024 | -$39.65M | -$9.59M | -$2.44M | — | -$2.95M | -$1.81M |
| 2025 | -$49.78M | -$19.45M | -$8.49M | -$5.2M | -$1.24M | -$917.9K |

Other flows mentioned in the forum but not shown in the statement:
- **AAVE buybacks** (from 2025-04-09). Blockworks Advisory says "The Aave DAO spent about $35M on buybacks in 2025" (https://governance.aave.com/t/temp-check-aave-will-win-framework/24055, post #27). TokenLogic says "$42M has been allocated to acquiring 205,000 AAVE over the 10-month period" to Feb 2026 (Funding Insights 24192).
- **Treasury-funded incentives.** ACI reports "$21.2M from DAO treasury" in 2025 incentives (24085). The Horizon Merkl incentives were ~$4.2M from Aug 2025.
- **Aave Liquidity Committee and GHO liquidity.** Spend fell "from ~$12M" toward $7M (24192). This probably sits in the "GHO" or "Incentives" line.
- **CEX Earn and market-making** for GHO in 2025, via separate SAFEs (24192).
- **Immunefi / BGD bug-bounty payouts**, made by separate "Request for Bounty Payout" AIPs. Their classification is unknown.
- **Gas rebates** for delegates and service providers. Classification is unknown.

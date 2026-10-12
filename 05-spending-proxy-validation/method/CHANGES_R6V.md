# Changes and clarifications after freezing METHOD_R6V.md

All entries below were decided before any proxy total was computed or viewed.

V1 (benchmark, clarification). Only realised (actual) figures enter the benchmark; approved budgets are not reported spending. Consequence: Olympus has no unit. Its only published actual (about $1.33M) covers Feb 2025 to Feb 2026, outside the 2023-2025 window, and comes from a community post. Olympus is reported descriptively only.

V2 (benchmark choices). Aave: Service Providers + Other Expenses rows of the TokenLogic income statement; Partnerships excluded for consistency with Sky, whose integration payments are excluded as incentives. Sky 2025: 73.71M including the Q4 2025 Buffers line, because SFF states it is a reclassification of the same governance funding. Uniswap: Uniswap Foundation grants paid plus opex (commitments not used). Lido 2023: May-Dec contributors-group actual (narrower scope, gap noted).

V3 (criterion C2, interpretation). With 4 protocols holding units, "at least 80% of protocols" means all 4.

V4 (coverage for family B, consequence of frozen rule). DefiLlama token balance series start on 2023-02-04 (Sky 2023-10-19), so calendar 2023 units are not covered in family B except Lido May-Dec 2023.

## After the first computation (independent review, REVIEW_R6V.md). None of these changes the verdict.

V5 (bug fix). The transfer download de-duplicated rows on a key without log index, merging identical transfers inside one transaction. De-duplication removed from fetch_transfers.py and build_P.py; all address histories re-downloaded except the Aave Collector and Ecosystem Reserve, where the reviewer measured the effect at under $10k in total. Sky 2024 P1 changed from 35.28M to 35.68M; median |ln r| for P1 from 0.797 to 0.792.

V6 (implementation detail). Transfer prices use the nearest DefiLlama daily point within 3 days of the transfer day (in practice at most 1 day off).

V7 (implementation detail). Multisig test: getThreshold() returns a value between 1 and 999.

V8 (implementation detail). Family B coverage is tested on the earliest chain key. For Lido May-Dec 2023 the Solana key starts in July 2023; Solana is under 1% of the Lido treasury.

V9 (method item computed). Share of the DefiLlama treasury outside Ethereum, yearly mean of daily shares: Aave 16.6% / 10.9% / 10.4% (2023/2024/2025), Lido 0.1-0.8%, Sky 0, Uniswap 0.

V10 (diagnostic variant). The manually cleaned variant (manual_variant.py) was defined after seeing P1 results and is diagnostic only. Its Sky figures are not payments: 2024 is dominated by $663.7M of USDC sent to EOA 0x37305b after a PSM swap (a treasury allocation), 2025 by $121.5M of SKY moved to Safe 0xca5183.

V11 (correction of V1). For Olympus, Jan 2023-Jan 2024 spending can be derived as budget $5.98M minus stated savings $0.817M = $5.163M, but no report states it and the period ends in Jan 2024. Kept out. Including it would not change the verdict.

V12 (explanations corrected). Sky: spells mint DAI/USDS directly to recipients, so these payments never appear as Pause Proxy outflows. Aave: aToken payments from the Collector carry a small interest mint to the Collector in the same transaction, so the same-transaction-inflow rule flags them; stream withdrawals explain only $0.47M. Lido: LDO goes to a 4-of-9 Safe, not a vesting contract.

V13 (disclosure, family B). The Sky adapter does not track USDS, so DAI to USDS conversions appear as outflows ($104.9M in 2024, $216.5M in 2025); Lido has a similar $9.2M sUSDS conversion; B counts Uniswap's 100M UNI burn ($600.5M, Dec 2025).

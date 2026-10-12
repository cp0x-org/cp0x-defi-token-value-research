# Changes after the method freeze

## C1. Fees for parent groups without a parent-level series (2026-10-06T14:09:01Z)
DefiLlama returns "not found" for some parent slugs (ether-fi, maker, venus-finance, trader-joe, kamino-finance, astherus, lombard-finance, marinade-finance, origin-defi). For these, fees and holders revenue are the sum of the children's series (fetch_fees_children.py). This is an implementation of the frozen rule "grouped by parentProtocol", not a change of the rule.

## C2. Universe: tokens that are not protocol tokens (2026-10-06T14:09:01Z)
Found while checking the token mapping, before any outcome (y, g, m, s) was printed or inspected.
The plan agreed with the user excludes L1/L2 tokens, stablecoins and memecoins, but the frozen category rule lets some through because DefiLlama files them under DeFi categories.
Excluded in the main run by token identity:
- stablecoins and yield-bearing stablecoins: savings-xdai (sDAI), usdx-money-usdx
- native gas tokens of general-purpose L1/L2 chains: crypto-com-chain (CRO, mapped to Defi Swap), near (mapped to a bridge), arbitrum (mapped to Timeboost/MEV)
- memecoins: baby-doge-coin
- non-DeFi categories missing from the frozen exclusion list: Decentralized AI (flock-2), Video Infrastructure (livepeer)
Kept on purpose: app-chain tokens whose chain exists to run the DeFi product (hyperliquid, dydx-chain, thorchain, osmosis).
The frozen universe without these exclusions is reported as a robustness run ("frozen_universe").

## C3. Stage 2: source of the hack indicator (2026-10-06T14:22:39Z)
The stage-2 method says "the DefiLlama hacks record of the protocol". The per-protocol treasury/protocol objects carry an empty hacks field, so the indicator is taken from api.llama.fi/hacks, matched by parentProtocolId or defillamaId. Clarification of the source, rule unchanged.

## C4. Stage 2: treasury coverage
Only 37 of 214 observations have DefiLlama treasury data with at least $1M of non-native reserves at window start (33 in the regression sample). H8 is estimated as frozen but is underpowered; the verdict is reported with that caveat.

## Note. LDO supply check (stage 1 limitation)
On-chain proxy for LDO circulating supply = 1B total minus the Aragon Agent balance, reconstructed from current balance and all Agent LDO transfers since block 18251964: 890.6M (2023-10-01), 895.3M (2024-10-01), 895.8M (2025-10-01), 878.5M (2026-10-01). CoinGecko implies 819.1M, 895.6M, 896.3M, 829.6M. CoinGecko's W1 +9% and W3 -7% are recounts; the on-chain changes are +0.5% and -1.9%. y and g are unaffected, s and m shift by the same amount.

## C5. Stage 3: totalSupply read directly at historical blocks (2026-10-06T14:45:57Z)
The frozen stage-3 method reconstructs past totalSupply from current supply and mint/burn logs. For tokens with frequent mints (CRV) this needs tens of thousands of log pages. Public archive RPC endpoints (drpc, mevblocker, blastapi, tenderly) answer eth_call at historical blocks, so totalSupply is read directly at the same blocks. The definition (ERC-20 totalSupply at the last block before 00:00 UTC of the date) is unchanged; only the way of obtaining it changed. Log-based values for the three tokens finished before the switch (UNI, LDO, AAVE) match the direct reads.

## C6. Stage 3: bridged or legacy Ethereum contracts (2026-10-06T14:45:57Z)
Found while checking s_issue values, before y was looked at. For two tokens the Ethereum contract DefiLlama lists is not the native token: axelar (AXL is native to the Axelar chain, the ERC-20 supply grows with bridging) and dydx-chain (the native token lives on the dYdX chain, the ERC-20 is the legacy ethDYDX). Both are excluded from s_issue. Sky's MKR-to-SKY migration does not touch the sample, because sky is only in W3, after the migration.

## C7. Stage 3: recount detector (2026-10-06T14:46:36Z)
In the CoinGecko CSV the daily price is a close and the daily market cap is taken at a different time of day, so the day-over-day implied supply moves by about 5% on a typical day and by up to 30% with no recount. The frozen rule (any day-over-day change above 15%) flags almost every observation and the H2b regression cannot be estimated. Replaced, before any H2b estimate was seen, by a level-shift rule: the 7-day median of implied supply after a day differs from the 7-day median before it by more than the threshold, while the 7-day median price moved by less than 15%. Flag shares: 71% at 10%, 39% at 15%, 20% at 25%. The detector cannot tell a recount from a genuine cliff unlock, so H2b removes some real dilution events as well; H2a is the cleaner test.

## C8. Stage 4: tokens on other EVM chains excluded from s_issue (2026-10-06T15:17:54Z)
Checked per token from documentation and contract reads before any stage-4 value was computed (table in data/stage4_bridging_check.md):
- gains-network (GNS): minted and burned natively on Polygon, Arbitrum and Base; Polygon totalSupply is a minority of supply.
- moonwell-artemis (WELL): the listed Base address is xWELL, an xERC20 minted on Base, Ethereum and OP.
- velo (Velo Protocol): native on Stellar; the BSC contract is a wrapped representation with a fixed 30B totalSupply.
Kept: pancakeswap-token, aerodrome-finance, venus, velodrome-finance, lista, thena, geodnet (home-chain totalSupply covers the gross supply; bridges lock on the home chain).
Known limitation: totalSupply is gross, so tokens sent to dead addresses as a "burn" (e.g. part of LISTA) still count.

## C9. Stage 3 and 4: burns to dead addresses (2026-10-06T15:20:25Z)
Found on CAKE before any stage-4 outcome was computed: CAKE "burns" are transfers to 0x000000000000000000000000000000000000dEaD, so gross totalSupply grew from 1.39B to 5.46B while supply net of the dead address fell from 399M to 348M. s_issue is therefore redefined, for all tokens and both stages, as the log change of (totalSupply minus balances of 0x...dEaD and 0x0) at the same blocks. Stage 3 is recomputed with this definition; the stage-3 result on gross totalSupply stays in data/results_stage3_gross.json for comparison.

## Note on C4
C4 was written at 2026-10-06T14:2xZ together with C3; its timestamp was omitted.

# Changes after the independent review (REVIEW_R4.md)

## C10. Survivorship check (2026-10-06T16:01:44Z)
26 of the 717 candidates have no CoinGecko CSV (404), so they never entered the panel; the delisting rule never fired because CoinGecko keeps exporting series for inactive coins it still lists. For the 26, prices at window starts were taken from DefiLlama coins (coingecko ids are still served there) and an upper bound on market cap was computed as price x current on-chain totalSupply (data/missing_cg_fdv.csv). No token clearly reaches $50M at any window start. Borderline: Vertex W2 (fully diluted $81M; circulating was about 21% of supply in April 2024 per an outside analysis, not measured at the window start). Upper bounds below $50M: Kwenta W1 ($48.5M at 505,775 current supply), Vesta W1 ($46M). Mars and BlueMove: prices available but no supply, not bounded. Prices are DefiLlama point values with a 2-day search width (script survivorship_check.py). Twelve have no price at any window start (launched later or not tracked). So the panel is very unlikely to miss a dead token that the frozen entry rule would have admitted; Vertex W2 is the one borderline case. A residual risk remains that DefiLlama drops protocols from overview/fees altogether; this cannot be checked from the data.

## C11. Holder share for series that start late (2026-10-06T16:01:44Z)
Bug: when the holders-revenue series exists but has no data in the 90 days before a date, H was computed as 0 instead of missing (21 observations). The frozen rule says H is missing when there is no holders-revenue series; the fix applies the same rule per date: H is missing when the holders-revenue series has no data in the 90-day window. Stage 1 and 2 are re-estimated.

## C12. Variance shares and secondary outcome as frozen (2026-10-06T16:01:44Z)
Two departures from METHOD_R4.md found by the reviewer: (a) the H1 variance shares were computed on the regression sample (n=175) instead of all decomposable observations; (b) the secondary outcome pooled categories with the regression rule (>= 10 overall) instead of the frozen rule (< 5 in the window). Both now follow the frozen text; the regression-sample shares are reported alongside.

## C13. Geodnet out of s_issue (2026-10-06T16:01:44Z)
The stage-4 audit found GEOD moved from Polygon to Solana in Q3 2025, so the Polygon contract does not hold the full supply. Excluded from s_issue (one observation).

## Post-hoc checks (labelled as such in the write-up)
Dropping observations with fewer than 80 days of fee data in the end window; dropping NXM; dropping NXM, Bancor and Olympus. Script: posthoc.py.

## Second review pass
Corrections to counts and wording in the write-up only (beta and hack counts, H8 parameter count, number of dropped regression observations, survivorship wording); C10 text corrected as above. See REVIEW_R4.md, Second pass.

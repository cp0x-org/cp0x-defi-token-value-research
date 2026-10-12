# Research 4, stage 3. Supply re-check (frozen before computing)

Frozen 2026-10-06. Builds on METHOD_R4.md, CHANGES_R4.md and stage 2. Purpose: give hypothesis H2 (dilution hurts) a test that does not depend on CoinGecko's circulating-supply estimate, which the LDO check showed is sometimes recounted.

## New variables
- s_issue (on-chain issuance): for tokens whose DefiLlama token address is on Ethereum mainnet, s_issue = ln(TS_end / TS_start), where TS is the ERC-20 totalSupply at the last block before 00:00 UTC of the date. TS at a date is reconstructed as current totalSupply (eth_call at latest block) minus net mints (Transfer events from the zero address) plus burns (Transfer events to the zero address) after that block. Source: Ethereum public RPC for totalSupply, Routescan Etherscan-compatible API for logs and block numbers. A token is used only if the reconstruction is complete (all log pages fetched). s_issue measures new issuance only; unlocks of already-minted tokens are not in it.
- recount flag: an observation is flagged if CoinGecko-implied daily supply (market cap / price, both daily values) shows any day-over-day change larger than 15% in either direction inside the window, on a day when the price itself changed by less than 15%.

## Hypotheses
- H2a. New issuance hurts: in R1 with s replaced by s_issue, on the Ethereum-token sample, the coefficient on s_issue is negative with p < 0.05.
- H2b. Dilution hurts once recounts are removed: in R1 (CoinGecko s) on the main sample without recount-flagged observations, the coefficient on s is negative with p < 0.05.

## Regressions
Same specification, winsorization, fixed effects and clustering as R1 in METHOD_R4.md. For H2a, m is not used; R1 does not contain m.

## Reported alongside
Correlation between s and s_issue on the Ethereum sample; share of observations flagged as recounts; R1 with CoinGecko s on the Ethereum sample (so the two measures are compared on the same observations).

## Robustness
No winsorization; drop each window; recount threshold 10% and 25%; for H2a, both s_issue and s in the same regression.

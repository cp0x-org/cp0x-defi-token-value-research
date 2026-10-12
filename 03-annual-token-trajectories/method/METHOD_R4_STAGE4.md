# Research 4, stage 4. Unlocks and wider on-chain issuance (frozen before computing)

Frozen 2026-10-06. Builds on stages 1 to 3 and CHANGES_R4.md C1 to C7.

## Why
Stage 3 measured new issuance on Ethereum only. Dilution also comes from unlocks of tokens that already exist (team, investors, treasury releases). No free source of vesting schedules is available (the DefiLlama unlocks data is paid and its adapters are no longer public), so unlocks are approached through the gap between CoinGecko circulating supply and on-chain issuance, with a manual audit of the largest gaps.

## Wider issuance sample
s_issue is extended to tokens whose DefiLlama address is on BSC, Base, OP Mainnet or Polygon, using archive eth_call where a public endpoint serves historical state (BSC: blastapi; Base: drpc, blastapi; OP Mainnet: drpc; Polygon: drpc). Block at a date: binary search on block timestamps over the same endpoint. Arbitrum and Avalanche are not covered (no public archive endpoint found). A token is excluded from s_issue if its supply is minted and burned across several chains (a burn-and-mint bridge), because one chain's totalSupply is then not the token's supply; this is checked per token from the token's own documentation before outcomes are looked at, and every exclusion is logged with its source. The Ethereum exclusions of C6 stay.

## Unlock residual
u = s - s_issue, where s is the CoinGecko-based log change of circulating supply from stage 1. u contains unlocks of existing tokens, changes in what CoinGecko counts as circulating, and recounts. It is defined only where s_issue is defined.

## Hypothesis
- H9. Unlock dilution hurts: in R1 with both s_issue and u (in place of s), the coefficient on u is negative with p < 0.05.
H2a is re-estimated on the wider sample and reported as H2a-wide; the stage-3 verdict on the Ethereum sample is not replaced.

## Manual audit
The 20 observations with the largest |u| in the regression sample are checked against public sources (protocol docs and blogs, governance forums, token-unlock news, CoinGecko supply notes). Each is classified, without looking at the outcome y, as:
- real: an unlock, treasury release, or migration that put tokens into circulation (or took them out) as CoinGecko shows,
- recount: CoinGecko changed what it counts without tokens moving,
- unclear.
Robustness run "audited": u set to 0 for observations classified as recount. The classification table with sources is published.

## Regressions
R1 specification, winsorization, fixed effects and clustering as in METHOD_R4.md.

## Robustness
No winsorization; drop each window; Ethereum-only sample; audited.

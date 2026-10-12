# Research 6, validation step. Can treasury outflows stand in for reported DAO spending? (frozen before computing)

Frozen 2026-10-07. Purpose: decide whether an automatically computed treasury-outflow measure tracks the spending that DAOs report closely enough to be used across the Research 4 sample. If it does, Research 6 may be built on it. If it does not, Research 6 becomes a set of case studies and no attempt is made to rescue the quantitative design.

## Protocols and benchmark
Five protocols with reported spending for two or more years: Uniswap (Uniswap Foundation), Aave, Sky (formerly Maker), Lido, Olympus.

Benchmark = reported spending: operating expenses, grants and contributor compensation paid in any asset (own-token compensation included at the value the report gives), taken from the protocol's own financial reports or reports it commissioned (for example Steakhouse, Karpatkey, TokenLogic, Uniswap Foundation financial reports). Excluded from the benchmark when the report separates them: cost of revenue paid to third parties (node operators, liquidity providers, depositors), token incentives to users and liquidity mining, buybacks, staking/safety-module rewards. Where a report does not separate an item, the reported figure is used as is and the gap is noted.

Unit of comparison: a protocol and a reported period inside 2023-01-01 to 2025-12-31. Calendar years are used where available (quarterly or monthly reports are summed only when every sub-period of the year exists). Otherwise a reported period of at least 6 months is used as is. No annualisation.

The benchmark table (data/reported_spending.csv: protocol, period start, period end, amount USD, what it includes, source URL, scope note) is collected and frozen with a sha256 hash before any proxy total is looked at.

## Treasury definition
The treasury of a protocol is exactly the set of addresses in its DefiLlama treasury adapter (DefiLlama-Adapters, registries/treasury.js and projects/treasury, checked out 2026-10-07). No addresses are added or removed by hand, because the measure must scale to protocols that were not inspected.

## Proxy family P (transfer-based, Ethereum mainnet)
Data: all ERC-20 transfers, normal transactions and internal transactions from the routescan Etherscan-compatible API in which an address of the treasury set T sends value, over each unit's dates. USD value at the transfer day from DefiLlama coins historical prices by token address. Tokens without a price get no value; their count and the share of transfers affected are reported.
- P0, gross external outflow: every outflow from T to an address outside T.
- P1, rule-based net external outflow (primary): P0 minus (a) every outflow in a transaction in which T also receives any token or ETH (swaps, deposits and withdrawals, wraps, claims); (b) outflows to contracts that are not multisigs (contract = non-empty code that is not an EIP-7702 delegation; multisig = getThreshold() returns a value); (c) transfers to 0x0 and 0x…dead (burns).
- P1c: P1 without the protocol's own token (cash-like outflow).
Only Ethereum mainnet is covered; the share of the DefiLlama treasury held on other chains is reported.

## Proxy family B (balance-based, all chains)
Data: DefiLlama treasury API, daily token unit balances and USD values for every chain key (chain keys and their -OwnTokens keys; the aggregate OwnTokens key is not used, to avoid double counting). Daily price of a token = USD value / units.
- Value change of token k on step d = (units_d − units_d−1) × price on day d (price on day d−1 if units_d = 0). A step is skipped for a token that is absent from the list on either day (adapter artefact rule).
- B1, daily net outflow (primary): sum over days of max(0, −sum over tokens of value change). Daily netting removes most swaps and internal moves.
- B0, gross: sum over days and tokens of max(0, −value change).
A unit is used in family B only if the series covers the whole period.

## Criteria (applied to each family's primary variant, P1 and B1)
For each unit, r = proxy / reported.
- C1 accuracy: median |ln r| over all units ≤ ln 1.4 (about 0.34, i.e. a typical error within roughly 30–40%).
- C2 no systematic bias: the median r of a protocol lies within [0.5, 2] for at least 4 of 5 protocols (for at least 80% of protocols with units).
- C3 dynamics: across consecutive units of the same protocol, the direction of change of the proxy matches that of the reported figure in at least 2/3 of pairs. If fewer than 3 pairs exist, C3 is reported as not evaluable and the verdict rests on C1 and C2.
- Coverage: at least 4 protocols and 10 units with a benchmark; otherwise the result is inconclusive and treated as a fail.
A family passes only if all applicable criteria hold. Spearman correlation per family is reported descriptively.

## Decision rule
- A family that passes may be used in Research 6 under the name "net external treasury outflow" (P) or "net treasury outflow" (B), never "spending". If both pass, the one with the smaller median |ln r| is used.
- If neither passes, Research 6 is done as case studies (5–10 DAOs). No new proxy is designed after seeing these results.
- Diagnostic variants (P0, P1c, B0, and a manually cleaned P1 that removes documented buybacks, liquidity deployment, incentives and migrations) are reported to explain the outcome. They cannot change the verdict, because manual cleaning does not scale.

## Common rules
Deterministic scripts, raw downloads stored. Any change after freezing is logged in CHANGES_R6V.md with its reason. An independent reviewer checks code and results before the report.

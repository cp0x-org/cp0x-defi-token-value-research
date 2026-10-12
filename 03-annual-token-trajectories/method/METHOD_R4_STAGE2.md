# Research 4, stage 2. Method (frozen before any stage-2 variable is computed)

Frozen 2026-10-06. Builds on METHOD_R4.md and CHANGES_R4.md. Same windows, same main sample, same outcome y, same controls.

## New variables (per protocol x window)
- new_products: number of product versions (child protocol names in the DefiLlama fees breakdown, summed over chains) with fees > 0 in the 90 days ending at window end and zero or no fees in the 90 days ending at window start. Enters as ln(1 + count).
- new_chains: same rule for chains.
- lost_products, lost_chains: the reverse (fees > 0 at start, none at end). Reported, used as controls in a robustness run.
- treasury_change: (T_end - T_start) / MC_start, where T is the DefiLlama treasury value excluding the protocol's own token (sum of chain series without the "-OwnTokens" suffix), point value on the date or the last value within 7 days before it. Computed only when T_start >= $1M; missing otherwise.
- hack: 1 if the DefiLlama "hacks" record of the protocol lists an incident with a date inside the window, else 0.
Source: api.llama.fi/summary/fees/<slug>?dataType=dailyFees (with breakdown) and api.llama.fi/treasury/<slug>. For parent groups without parent-level data, children are summed as in CHANGES_R4.md C1.

## Hypotheses
- H5. Launching new products is associated with better returns: in R2s the coefficient on ln(1+new_products) is positive with p < 0.05.
- H6. Expanding to new chains is associated with better returns: in R2s the coefficient on ln(1+new_chains) is positive with p < 0.05.
- H7. Evaluated only for H5 or H6 that hold: the effect works through business growth, i.e. adding g (R1s) reduces the coefficient by at least half.
- H8. Building non-native reserves is associated with better returns: in R2t the coefficient on treasury_change is positive with p < 0.05.

## Regressions
OLS, window FE, SE clustered by protocol, winsorization of continuous variables at 2.5/97.5 within window (ln(1+count) variables included), as in stage 1.
- R2s: y ~ ln(1+new_products) + ln(1+new_chains) + s + H_start + dH + ln M_start + ln MC_start + beta + drawdown_start + hack + C(cat) + C(window). Sample: stage-1 R1h sample (non-missing H).
- R1s: R2s + g.
- R2t: R2s + treasury_change. Sample: R2s sample with non-missing treasury_change.

## Robustness (reported, not used for verdicts)
No winsorization; H missing set to 0 (full stage-1 sample); add lost_products and lost_chains; drop each window; frozen universe without C2 exclusions; count variables as raw counts capped at 10.

## Known limitation carried from stage 1
CoinGecko circulating supply is sometimes recounted (LDO: CoinGecko implies -7.4% in W3, the on-chain proxy 1B minus treasury gives -1.9%). This moves s and m but not y or g. Stage 2 does not change s; a supply re-check on a subsample is a separate task.

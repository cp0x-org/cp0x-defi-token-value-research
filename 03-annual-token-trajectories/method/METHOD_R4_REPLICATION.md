# Research 4, replication of the holder-share result (frozen before computing)

Frozen 2026-10-06, after Research 4 was frozen (Research4_frozen_20261006.zip). Written before any shifted-window variable or outcome is computed.

## Why
After the C11 fix, the stage-1 regression R1h shows that, at equal fee growth, a larger holder share of fees at the window start goes with better returns against ETH (coefficient 0.56, p = 0.0001). This was not a pre-registered hypothesis in that direction (H3 predicted the opposite), it rests mostly on the last window, and it moved most during the review. It is therefore tested again on windows it was not found on, and forward on a window that has not happened yet.

## Part A. Shifted windows (computed now)
Windows start in April instead of October: A1 2023-04-01 to 2024-04-01, A2 2024-04-01 to 2025-04-01, A3 2025-04-01 to 2026-04-01. Each overlaps two of the original windows by half, so this is a check against a one-window accident, not an independent sample.

Everything else is exactly as in METHOD_R4.md with CHANGES C1, C2 (same token exclusions), C11 and C12: same candidate list (data/candidates.csv), same entry rule ($50M market cap at window start, at least 80 of 90 days of fee data, positive 90-day fees), same measurement, same supply-artefact rule, same winsorization, fixed effects and clustering. Fee and holders-revenue series for groups that enter only at April dates are downloaded with the same endpoints and the C1 child aggregation.

Tests, on the R1h specification of METHOD_R4.md (R1 plus H_start and dH):
- HR1 (replication): pooled A1-A3, coefficient on H_start > 0 with p < 0.05.
- HR2 (not only the most recent period): A1 and A2 only (both end by April 2025), coefficient on H_start > 0 with p < 0.10. The looser threshold is fixed here because the subsample is smaller.
Reported alongside, not used for verdicts: the R-squared gain from H_start and dH; the coefficient in each window separately; R2 (without fee growth); no winsorization.

How the write-up will use the result, fixed now:
- HR1 fails: the holder-share result is described as found in one specification and not replicated.
- HR1 holds, HR2 fails: described as replicated but concentrated in the most recent period.
- Both hold: described as replicated on shifted windows, with the overlap caveat.

## Part B. Forward test (computed after the window ends)
Window F: 2026-10-01 to 2027-10-01. The eligible protocols and all start-of-window variables (market cap, fees, H_start, beta, drawdown, ln M_start, category) are computed now, saved as data/forward_start_2026-10-01.csv and hashed in this file's companion .sha256, so they cannot be adjusted after the outcome is known.
- HF: in R1h estimated on window F alone (no window fixed effects), coefficient on H_start > 0 with p < 0.05.
The outcome side (prices, market caps, fees at 2027-10-01) is collected with the same sources after 2027-10-08.

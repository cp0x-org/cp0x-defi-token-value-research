# Correction of 2026-10-08: pre-event run-up measured in calendar days

**What was wrong.** `class_cut.py` measured the token's run-up before each event (`pre90`) as the change over the last 90 price observations (`pre.iloc[-90]`), not over 90 calendar days. The price series have gaps, so 90 observations could span much more than 90 days. This is the same kind of error that the external audit found and fixed in the matching step (twin selection), but the run-up variable in `class_cut.py` was not corrected at the time and the study did not flag it. It was found during preparation for publication.

**What was done.** `code/fix_pre90_calendar.py` recomputes the run-up on calendar days with the rule `matching_v2.py` already uses (last observation on or before the event date minus 90 days, at most 7 days earlier). Nothing else was recomputed, because no other result uses this variable. The original values are kept in `data/class_cut_events_v2_pre90_calendar.csv` as `pre90_rows_superseded`.

**Effect.** For 40 of 43 events the value changed (3 events have too little price history in either version).

| Subset | Basket, before (n) | Basket, corrected (n) | Twins, before (n) | Twins, corrected (n) |
|---|---|---|---|---|
| All events | +0.10 (39) | +0.04 (39) | -0.08 (35) | -0.21 (35) |
| Decisions and activations | +0.23 (22) | +0.22 (22) | -0.12 (21) | -0.19 (21) |

The signs on the two control layers remain opposite in both subsets, so the conclusion is unchanged. The study found no evidence that the run-up before an event predicts the result after it. The pre-registered prediction that a run-up goes with a weaker outcome (expected correlation -0.23) is still not confirmed on both layers and stays dropped.

Medians of the run-up by class and stage (`med_pre90` in `data/class_cut_v2.csv`) also change; corrected values are in `data/class_cut_v2_pre90_calendar.csv`. They are descriptive and were not used for any conclusion.

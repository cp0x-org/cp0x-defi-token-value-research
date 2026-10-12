# Code for study 1, buyback event study

Scripts are copied as they were used in the study (internal name Research 2, version 2). They expect one working folder that holds the scripts, `config.json`, `events.csv` and a `data/` subfolder. Requirements are Python 3 with pandas, numpy, matplotlib and requests. No API keys are needed.

## Setup

```
mkdir work && cp code/*.py code/config.json work/
cp data/events.csv work/events.csv
mkdir work/data && cp data/revenue.csv work/data/
cd work
```

## Run order

1. `python3 collect_prices.py` downloads daily prices from the DefiLlama coins API into `data/prices.csv`. Prices are not shipped in this repository because they are keyed by CoinGecko IDs and CoinGecko terms restrict redistribution.
2. Optional. `python3 collect_fundamentals.py` downloads DefiLlama revenue and single-venue volumes (OKX, Coinbase fallback) into `data/revenue.csv` and `data/volumes.csv`. Volumes are needed only to rebuild `intensity.csv` with `analyze.intensity_metrics()`.
3. `python3 matching_v2.py` selects up to three twins per event under the frozen method and writes `data/matched_controls_v2.csv`. With `EXCLUDE_SUBJECTS=1` it writes the sensitivity variant `data/matched_controls_v2_nosubjects.csv`.
4. `class_cut.py` is the unchanged script of the frozen version. It reads `data/matched_controls.csv` and overwrites `data/class_cut.csv` and `data/class_cut_events.csv`. To get the version 2 cells, copy `data/matched_controls_v2.csv` to `data/matched_controls.csv` in a scratch copy of the working folder, run `python3 class_cut.py`, and rename the outputs to `class_cut_v2.csv` and `class_cut_events_v2.csv`. Repeat with the `_nosubjects` file for the sensitivity variant.
5. `python3 placebo_v2.py 1000` runs the placebo test on both layers (seed 42) and writes `data/placebo_v2_results.json`.
6. `python3 lido_mandate_calendar.py` recomputes the Lido mandate case and writes `data/lido_mandate_events_calendar.csv`. It imports `stage3_outcomes.py`, the calendar engine of study 2 in this series, which is included only as this dependency.
7. Audit only. `python3 matching_calendar.py` reproduces the audit's single-twin calendar matching in `data/matched_controls_calendar.csv`.

`analyze.py` and `matching_control.py` are imported as modules (price ratios and the outcome function). Running `analyze.py` directly writes `data/event_summary.csv` and charts; that file measures the basket outcome as a ratio of growth factors and is not the source of the report's numbers, which are differences of simple returns.

`data/cells_v2_both_layers.csv` and the slice tables (fate of bought tokens, execution, funding source) have no separate script. They are medians, counts and IQRs of `vs_basket_30d` and of `vs_match_30d` (rows with `match_dist` of 0.25 or less) in `class_cut_events_v2.csv`, grouped by class and stage or joined with `mechanism_type`, `discretion` and `funding_source` from `events.csv`.

Prices downloaded later than the study's data run (last price 2026-10-03) can shift the tail windows of the latest events.

License MIT.

## Correction script (2026-10-08)

`fix_pre90_calendar.py` recomputes the pre-event run-up on calendar days after `class_cut.py` and writes `data/class_cut_events_v2_pre90_calendar.csv` and `data/class_cut_v2_pre90_calendar.csv`. Run it from this folder after downloading prices (see above). See `../method/CORRECTION_2026-10-08_pre90.md`.

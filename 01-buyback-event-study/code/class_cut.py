"""Class cut: aggregates event outcomes by mechanism class (demand / payout / supply)
and event stage (proposal / decision / flow start / activation-param), with dispersion
and the pre-event 90d run-up as a conditioning variable. Uses day-precision events only,
skips rows marked as context. Outputs data/class_cut.csv and a correlation check between
pre-event run-up and post-event twin-relative outcome (the anticipation effect)."""
import pathlib
import pandas as pd
from analyze import load_ratios, CFG
from matching_control import fwd

HERE = pathlib.Path(__file__).parent

REDUCES_SET = {("sushi", "2022-12-05"), ("sushi", "2022-12-19"), ("sushi", "2023-01-23"), ("aave", "2026-03-04"), ("gmx", "2026-03-04"), ("gains", "2026-06-15"), ("looksrare", "2023-04-13")}
CLASS = {"buyback_treasury": "demand", "buyback_burn": "demand", "buyback_distribute": "demand",
         "buyback_revenue_gated": "demand", "buyback_treasury_gated": "demand",
         "buyback_treasury_price_capped": "demand", "buyback_immutable": "demand", "fee_share": "payout", "emission_cut": "supply"}
STAGE = {"forum_proposal": "proposal", "vote_passed": "decision", "first_execution": "flow_start",
         "mechanism_upgrade": "activation", "param_change": "activation", "schedule_effective": "activation"}

def main():
    ratios = load_ratios()
    ctrl = [c for c in CFG["control_tokens"] if c in ratios.columns]
    ev = pd.read_csv(HERE / "events.csv", parse_dates=["date"])
    ctx = (ev["notes"].fillna("") + " " + ev["confounders"].fillna("")).str.contains("context row")
    ev = ev[(ev["date_precision"] == "day") & (~ctx)]
    mc = pd.read_csv(HERE / "data" / "matched_controls.csv")
    mc_key = {(r["program"], r["date"]): r for _, r in mc.iterrows()}
    rows = []
    for _, e in ev.iterrows():
        tok, t0 = e["token_coingecko"], e["date"]
        if tok not in ratios.columns:
            continue
        s = ratios[tok].dropna()
        pre = s.loc[:t0]
        pre90 = pre.iloc[-1] / pre.iloc[-90] - 1 if len(pre) >= 90 else None
        basket = {}
        for w in (30, 90):
            a = fwd(ratios[tok], t0, w)
            bs = [fwd(ratios[c], t0, w) for c in ctrl]
            bs = [b for b in bs if b is not None]
            basket[w] = a - pd.Series(bs).median() if a is not None and bs else None
        m = mc_key.get((e["protocol"], str(t0.date())))
        rows.append({"class": CLASS.get(e["mechanism_type"], "other"),
                     "direction": "reduces_return" if (e["protocol"], str(t0.date())) in REDUCES_SET else "expands_return",
                     "stage": STAGE.get(e["event_type"], "other"),
                     "protocol": e["protocol"], "date": str(t0.date()), "pre90": pre90,
                     "vs_basket_30d": basket[30], "vs_basket_90d": basket[90],
                     "vs_match_30d": m["diff_vs_match_30d"] if m is not None else None,
                     "vs_match_90d": m["diff_vs_match_90d"] if m is not None else None,
                     "match_dist": m["match_dist"] if m is not None else None})
    df = pd.DataFrame(rows)
    df.to_csv(HERE / "data" / "class_cut_events.csv", index=False)
    # matched-статистики агрегатов только по пригодным матчам (дистанция <= 0.25)
    df.loc[df["match_dist"] > 0.25, ["vs_match_30d", "vs_match_90d"]] = None
    agg = df.groupby(["class", "stage"]).agg(
        n=("date", "count"),
        med_basket_30=("vs_basket_30d", "median"), med_basket_90=("vs_basket_90d", "median"),
        med_match_30=("vs_match_30d", "median"), n_match=("vs_match_30d", "count"),
        iqr_match_30=("vs_match_30d", lambda x: x.quantile(0.75) - x.quantile(0.25)),
        med_pre90=("pre90", "median")).round(3)
    agg.to_csv(HERE / "data" / "class_cut.csv")
    pd.set_option("display.width", 200)
    print(agg.to_string())
    both = df.dropna(subset=["pre90", "vs_match_30d"])
    print(f"\nanticipation check (n={len(both)}): corr(pre90, vs_match_30d) = {both['pre90'].corr(both['vs_match_30d']):.2f}")
    dec = both[both["stage"].isin(["decision", "activation"])]
    print(f"decisions+activations only (n={len(dec)}): corr = {dec['pre90'].corr(dec['vs_match_30d']):.2f}")

if __name__ == "__main__":
    main()

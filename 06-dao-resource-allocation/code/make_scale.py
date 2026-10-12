"""Research 6 card scale table: spending (levels 1+2, from decisions/*_card_inputs.md section 3) vs DefiLlama fees, revenue and liquid treasury."""
import sys, json, numpy as np, pandas as pd
sys.argv = ["x"]; exec(open("/home/claude/r6/join_outcomes.py").read().split("G = pd.read_csv(")[0])
SP = {"lido": {2022: 129.5, 2023: np.nan, 2024: 55.2, 2025: 49.6}, "aave": {2022: 67.36, 2023: 14.34, 2024: 38.86, 2025: 54.24},
      "sky": {2022: 46.2, 2023: 53.7, 2024: 80.0, 2025: 121.9}, "uniswap": {2022: np.nan, 2023: 7.11, 2024: 22.59, 2025: 20.7}}
rows = []
for p in SP:
    tr = json.load(open(f"/home/claude/r6v/raw/treasury_{p}.json")); liq = {}
    for ck, v in tr["chainTvls"].items():
        if ck.endswith("OwnTokens"): continue
        for x in v["tvl"]:
            d = pd.Timestamp(x["date"], unit="s").normalize(); liq[d] = liq.get(d, 0) + x["totalLiquidityUSD"]
    L = pd.Series(liq).sort_index()
    for y in (2022, 2023, 2024, 2025):
        f = F[p].loc[f"{y}-01-01":f"{y}-12-31"].sum() / 1e6; r = R[p].loc[f"{y}-01-01":f"{y}-12-31"].sum() / 1e6
        l = L.loc[:f"{y}-12-31"]; lq = l.iloc[-1] / 1e6 if len(l) and l.index[-1] >= pd.Timestamp(f"{y}-12-01") else np.nan
        s = SP[p][y]
        rows.append(dict(protocol=p, year=y, spend=s, fees=round(f, 1), revenue=round(r, 1), liquid_treasury_end=round(lq, 1) if lq == lq else np.nan,
                         spend_to_rev=round(s / r, 2) if r > 0 and s == s else np.nan, spend_to_fees=round(s / f, 3) if s == s else np.nan,
                         runway_years=round(lq / s, 1) if s == s and lq == lq else np.nan))
pd.DataFrame(rows).to_csv("/home/claude/r6/data_scale.csv", index=False); print(pd.DataFrame(rows).to_string())

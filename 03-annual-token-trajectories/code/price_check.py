"""Cross-check CoinGecko CSV prices (7-day median) against DefiLlama coins historical prices for a random sample of observations.
-> data/price_check.csv. Seeded sample of 20 observations, both window ends."""
import json, subprocess, pandas as pd, numpy as np
P = pd.read_csv("data/panel.csv")
s = P.sample(20, random_state=1)
rows = []
for _, r in s.iterrows():
    for d, p in ((r.start, r.p_start), (r["end"], r.p_end)):
        ts = int(pd.Timestamp(d).timestamp())
        j = json.loads(subprocess.run(["curl", "-s", "-m", "20", f"https://coins.llama.fi/prices/historical/{ts}/coingecko:{r.gecko_id}?searchWidth=12h"],
                                      capture_output=True, text=True).stdout or "{}")
        q = j.get("coins", {}).get(f"coingecko:{r.gecko_id}", {}).get("price")
        rows.append(dict(window=r.window, name=r["name"], date=d, coingecko_7d_median=p, defillama_point=q, ratio=(p / q) if q else np.nan))
D = pd.DataFrame(rows); D.to_csv("data/price_check.csv", index=False)
x = (D.ratio - 1).abs()
print("n", int(D.ratio.notna().sum()), "median |diff|", round(float(x.median()) * 100, 1), "%  p90", round(float(x.quantile(0.9)) * 100, 1), "%  max", round(float(x.max()) * 100, 1), "%")

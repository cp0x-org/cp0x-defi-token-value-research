"""Download CoinGecko public CSV exports (price, market cap, volume) for every kept candidate and ETH."""
import os, time, subprocess, pandas as pd
c = pd.read_csv("data/candidates.csv", dtype=str, keep_default_na=False)
ids = ["ethereum"] + sorted(set(c[c.excluded == ""].gecko_id))
os.makedirs("raw/cg", exist_ok=True)
for i, g in enumerate(ids):
    out = f"raw/cg/{g}.csv"
    if os.path.exists(out) and os.path.getsize(out) > 0: continue
    for attempt in range(6):
        r = subprocess.run(["curl", "-s", "-m", "30", "-o", out, "-w", "%{http_code}",
                            f"https://www.coingecko.com/price_charts/export/{g}/usd.csv"], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == "200": break
        if code == "404": open(out, "w").close(); break
        time.sleep(20 * (attempt + 1))
    else:
        print("FAILED", g, code, flush=True)
    if i % 50 == 0: print(i, g, code, flush=True)
    time.sleep(2)
print("done")

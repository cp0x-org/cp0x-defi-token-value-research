"""Download DefiLlama daily fees and holders revenue for candidates that reach $50M market cap at any window start."""
import os, json, time, subprocess, pandas as pd
from common import load_cg, at
DATES = ['2023-04-01', '2024-04-01', '2025-04-01', '2026-10-01']
c = pd.read_csv("data/candidates.csv", dtype=str, keep_default_na=False)
c = c[c.excluded == ""]
os.makedirs("raw/fees", exist_ok=True)
need = []
for _, r in c.iterrows():
    cg = load_cg(r.gecko_id)
    if cg is None: continue
    if any((at(cg, s, "mc") or 0) >= 50e6 for s in DATES): need.append(r)
print("groups to fetch:", len(need), flush=True)
for r in need:
    for t in ("dailyFees", "dailyHoldersRevenue"):
        out = f"raw/fees/{r.slug}__{t}.json"
        if os.path.exists(out) and os.path.getsize(out) > 0: continue
        for attempt in range(4):
            p = subprocess.run(["curl", "-s", "-m", "90", "-o", out, "-w", "%{http_code}",
                f"https://api.llama.fi/summary/fees/{r.slug}?dataType={t}&excludeTotalDataChartBreakdown=true"],
                capture_output=True, text=True)
            if p.stdout.strip() in ("200", "404", "400"): break
            time.sleep(10 * (attempt + 1))
        time.sleep(0.5)
print("done")

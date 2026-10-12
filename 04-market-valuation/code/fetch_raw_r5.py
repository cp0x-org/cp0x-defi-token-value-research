"""Download the DefiLlama raw files used by Research 5 (study 4).

Added at publication (2026-10-08). The original downloads were made on 2026-10-07 with the
endpoints named in METHOD_R5.md; this script reproduces those requests. DefiLlama serves
current data, so a new download will not be byte-identical to the stored files. Compare
with data/raw/RAW_HASHES.sha256 to see whether you have the original version.

Writes into ./raw relative to the working directory:
  raw/overview_fees_breakdown.json   daily fees by product (about 28 MB, not in the repo)
  raw/rev/<slug>.json                daily revenue per group (also stored in data/raw/rev)
Fee summary series raw/fees/<slug>__dailyFees.json come from the Research 4 download
(fetch_fees.py and fetch_fees_children.py in the Research 4 folder) and are stored in data/raw/fees.
No API key is needed.
"""
import os, sys, time, subprocess, pandas as pd

def get(url, out):
    for attempt in range(4):
        p = subprocess.run(["curl", "-s", "-m", "300", "-o", out, "-w", "%{http_code}", url], capture_output=True, text=True)
        if p.stdout.strip() in ("200", "404", "400"): return p.stdout.strip()
        time.sleep(10 * (attempt + 1))
    return p.stdout.strip()

os.makedirs("raw/rev", exist_ok=True)
print("breakdown", get("https://api.llama.fi/overview/fees?excludeTotalDataChart=false&excludeTotalDataChartBreakdown=false",
                       "raw/overview_fees_breakdown.json"))
panel = sys.argv[1] if len(sys.argv) > 1 else "data/panel_r5.csv"
for slug in sorted(pd.read_csv(panel).slug.unique()):
    out = f"raw/rev/{slug}.json"
    if os.path.exists(out) and os.path.getsize(out) > 0: continue
    get(f"https://api.llama.fi/summary/fees/{slug}?dataType=dailyRevenue&excludeTotalDataChartBreakdown=true", out)
    time.sleep(0.5)
print("done")

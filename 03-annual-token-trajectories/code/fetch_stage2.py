"""Stage 2 downloads: fees breakdown (chain x product) and treasury, for every group in the stage-1 panel."""
import os, json, time, subprocess, collections, pandas as pd
P = pd.read_csv("data/panel.csv")
slugs = sorted(set(P.slug))
ov = json.load(open("raw/overview_fees.json"))["protocols"]
kids = collections.defaultdict(list)
for o in ov:
    if o.get("parentProtocol"): kids[o["parentProtocol"].split("#", 1)[1]].append(o["slug"])
os.makedirs("raw/bd", exist_ok=True); os.makedirs("raw/treasury", exist_ok=True)
def curl(url, out):
    if os.path.exists(out) and os.path.getsize(out) > 0: return
    for a in range(4):
        p = subprocess.run(["curl", "-s", "-m", "120", "-o", out, "-w", "%{http_code}", url], capture_output=True, text=True)
        if p.stdout.strip() in ("200", "404", "400"): break
        time.sleep(10 * (a + 1))
    time.sleep(0.4)
def ok(path):
    try: return bool(json.load(open(path)))
    except Exception: return False
for s in slugs:
    out = f"raw/bd/{s}.json"
    curl(f"https://api.llama.fi/summary/fees/{s}?dataType=dailyFees", out)
    if not ok(out) and s in kids:
        for k in kids[s]: curl(f"https://api.llama.fi/summary/fees/{k}?dataType=dailyFees", f"raw/bd/child__{s}__{k}.json")
    curl(f"https://api.llama.fi/treasury/{s}", f"raw/treasury/{s}.json")
print("done", len(slugs))

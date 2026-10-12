"""For parent groups where DefiLlama has no parent-level series, fetch every child and sum them.
Result is written in the same format as the parent file, with an 'aggregated_from' field."""
import json, os, time, subprocess, collections
ov = json.load(open("raw/overview_fees.json"))["protocols"]
kids = collections.defaultdict(list)
for o in ov:
    if o.get("parentProtocol"): kids[o["parentProtocol"].split("#", 1)[1]].append(o["slug"])
os.makedirs("raw/fees_children", exist_ok=True)
def get(slug, kind):
    out = f"raw/fees_children/{slug}__{kind}.json"
    if not (os.path.exists(out) and os.path.getsize(out) > 0):
        for a in range(4):
            p = subprocess.run(["curl", "-s", "-m", "90", "-o", out, "-w", "%{http_code}",
                f"https://api.llama.fi/summary/fees/{slug}?dataType={kind}&excludeTotalDataChartBreakdown=true"], capture_output=True, text=True)
            if p.stdout.strip() in ("200", "404", "400"): break
            time.sleep(10 * (a + 1))
        time.sleep(0.4)
    try: return json.load(open(out)).get("totalDataChart") or []
    except Exception: return []
fixed = []
for f in sorted(os.listdir("raw/fees")):
    path = f"raw/fees/{f}"
    txt = open(path).read(300)
    if not txt.startswith("Fees for"): continue
    slug, kind = f[:-5].split("__")
    if slug not in kids: continue
    tot = collections.Counter(); used = []
    for k in kids[slug]:
        ch = get(k, kind)
        if ch: used.append(k)
        for t, v in ch: tot[int(t)] += float(v)
    if tot:
        json.dump({"aggregated_from": used, "totalDataChart": sorted([[t, v] for t, v in tot.items()])}, open(path, "w"))
        fixed.append((slug, kind, len(used)))
print("aggregated:", fixed)
still = [f for f in os.listdir("raw/fees") if open(f"raw/fees/{f}").read(20).startswith("Fees for")]
print("still missing:", sorted(still))

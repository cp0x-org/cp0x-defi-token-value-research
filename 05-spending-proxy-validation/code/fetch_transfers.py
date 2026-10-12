"""Family P raw data: all token transfers, normal and internal txs of treasury addresses (Ethereum), 2023-01-01..2026-01-01.
Routescan Etherscan-compatible API; block ranges are split recursively when a query hits the 10,000-row cap."""
import json, os, sys, time, urllib.request, urllib.parse
R = "https://api.routescan.io/v2/network/mainnet/evm/1/etherscan/api"
B0, B1 = 16308190, 24136052  # first block >= 2023-01-01, last block < 2026-01-01
CAP = 10000
os.makedirs("raw/tx", exist_ok=True)

def call(params, tries=8):
    q = R + "?" + urllib.parse.urlencode(params)
    for k in range(tries):
        try:
            with urllib.request.urlopen(q, timeout=120) as r:
                d = json.load(r)
            if d.get("status") == "1" or d.get("message", "").startswith("No transactions"):
                return d.get("result") or []
            if "rate" in str(d).lower() or "limit" in str(d.get("result", "")).lower():
                time.sleep(2 + 2 * k); continue
            if d.get("status") == "0" and isinstance(d.get("result"), list):
                return []
            raise RuntimeError(str(d)[:300])
        except RuntimeError:
            raise
        except Exception as e:
            time.sleep(2 + 2 * k)
    raise RuntimeError("failed " + q)

def fetch(addr, action, lo, hi, out):
    res = call({"module": "account", "action": action, "address": addr, "startblock": lo, "endblock": hi, "page": 1, "offset": CAP, "sort": "asc"})
    if len(res) >= CAP and hi > lo:
        mid = (lo + hi) // 2
        fetch(addr, action, lo, mid, out); fetch(addr, action, mid + 1, hi, out)
    else:
        out.extend(res)
    time.sleep(0.3)

if __name__ == "__main__":
    sets = json.load(open("data/treasury_sets.json"))
    for p, v in sets.items():
        for a in v["owners"]:
            if len(sys.argv) > 1 and a not in sys.argv[1:]: continue
            for action in ("tokentx", "txlist", "txlistinternal"):
                fn = f"raw/tx/{a}_{action}.json"
                if os.path.exists(fn): continue
                out = []; fetch(a, action, B0, B1, out)
                ded = out  # no de-duplication: split ranges are disjoint, and the API gives no log index (CHANGES V5)
                json.dump(ded, open(fn, "w"))
                print(p, a, action, len(ded), flush=True)

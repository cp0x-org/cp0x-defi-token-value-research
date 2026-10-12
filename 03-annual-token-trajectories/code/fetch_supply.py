"""Stage 3: ERC-20 totalSupply at window dates via archive eth_call (METHOD_R4_STAGE3.md, CHANGES C5)."""
import json, os, time, subprocess, pandas as pd
B = "https://api.routescan.io/v2/network/mainnet/evm/1/etherscan/api"
RPCS = ["https://eth.drpc.org", "https://rpc.mevblocker.io", "https://eth-mainnet.public.blastapi.io", "https://gateway.tenderly.co/public/mainnet"]
DATES = ["2023-10-01", "2024-10-01", "2025-10-01", "2026-10-01"]

def call(to, data, block):
    d = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params": [{"to": to, "data": data}, hex(block)]})
    errs = []
    for a in range(3):
        for u in RPCS:
            r = subprocess.run(["curl", "-s", "-m", "30", "-X", "POST", u, "-H", "content-type: application/json", "-d", d], capture_output=True, text=True)
            try:
                j = json.loads(r.stdout)
                if "result" in j: return j["result"], u
                errs.append(str(j.get("error"))[:80])
            except Exception as e:
                errs.append(str(e)[:40])
        time.sleep(3)
    raise RuntimeError("; ".join(errs[-3:]))

blocks = {}
for d in DATES:
    ts = int(pd.Timestamp(d).timestamp())
    r = subprocess.run(["curl", "-s", "-m", "30", f"{B}?module=block&action=getblocknobytime&timestamp={ts}&closest=before"], capture_output=True, text=True)
    blocks[d] = int(json.loads(r.stdout)["result"])
A = pd.read_csv("data/token_addresses.csv", dtype=str, keep_default_na=False)
A = A[A.chain == "ethereum"]
out = []
for _, r in A.iterrows():
    addr = r.address.split(":")[-1].lower()
    rec = {"gecko_id": r.gecko_id, "address": addr, "complete": False}
    try:
        dec_hex, _ = call(addr, "0x313ce567", blocks[DATES[-1]])
        dec = int(dec_hex, 16); rec["decimals"] = dec
        for d, b in blocks.items():
            try:
                v, u = call(addr, "0x18160ddd", b)
                rec[f"TS_{d}"] = int(v, 16) / 10 ** dec if v and v != "0x" else None
                rec[f"rpc_{d}"] = u
            except RuntimeError as e:
                rec[f"TS_{d}"] = None; rec[f"err_{d}"] = str(e)[:120]
        rec["complete"] = all(rec.get(f"TS_{d}") for d in DATES[1:])
    except Exception as e:
        rec["error"] = str(e)[:200]
    out.append(rec)
    print(r.gecko_id, rec["complete"], {d: rec.get(f"TS_{d}") for d in DATES}, flush=True)
    time.sleep(0.3)
json.dump({"blocks": blocks}, open("data/supply_blocks.json", "w"))
pd.DataFrame(out).to_csv("data/onchain_supply.csv", index=False)
print("done", sum(o["complete"] for o in out), "of", len(out))

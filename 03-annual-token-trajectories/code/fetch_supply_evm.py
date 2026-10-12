"""Stage 4: totalSupply on BSC, Base, OP Mainnet, Polygon at window dates via archive eth_call (METHOD_R4_STAGE4.md, C8)."""
import json, subprocess, time, pandas as pd
EP = {"bsc": ["https://bsc-mainnet.public.blastapi.io"], "base": ["https://base.drpc.org", "https://base-mainnet.public.blastapi.io"],
      "optimism": ["https://optimism.drpc.org"], "polygon": ["https://polygon.drpc.org"]}
KEEP = {"pancakeswap-token", "aerodrome-finance", "venus", "velodrome-finance", "lista", "thena", "geodnet"}
DATES = ["2023-10-01", "2024-10-01", "2025-10-01", "2026-10-01"]
def rpc(chain, m, p):
    for a in range(4):
        for u in EP[chain]:
            r = subprocess.run(["curl", "-s", "-m", "30", "-X", "POST", u, "-H", "content-type: application/json",
                                "-d", json.dumps({"jsonrpc": "2.0", "id": 1, "method": m, "params": p})], capture_output=True, text=True)
            try:
                j = json.loads(r.stdout)
                if "result" in j: return j["result"]
            except Exception: pass
        time.sleep(2 * (a + 1))
    raise RuntimeError(f"{chain} {m} failed")
def block_ts(chain, b): return int(rpc(chain, "eth_getBlockByNumber", [hex(b), False])["timestamp"], 16)
def block_before(chain, ts):
    hi = int(rpc(chain, "eth_blockNumber", []), 16); lo = 1
    if block_ts(chain, hi) <= ts: return hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if block_ts(chain, mid) <= ts: lo = mid
        else: hi = mid
    return lo
A = pd.read_csv("data/token_addresses.csv", dtype=str, keep_default_na=False)
A = A[A.chain.isin(EP) & A.gecko_id.isin(KEEP)]
blocks = {c: {d: block_before(c, int(pd.Timestamp(d).timestamp())) for d in DATES} for c in set(A.chain)}
print(blocks, flush=True)
out = []
for _, r in A.iterrows():
    addr = r.address.split(":")[-1]
    rec = {"gecko_id": r.gecko_id, "chain": r.chain, "address": addr}
    dec = int(rpc(r.chain, "eth_call", [{"to": addr, "data": "0x313ce567"}, "latest"]), 16)
    for d, b in blocks[r.chain].items():
        try:
            v = rpc(r.chain, "eth_call", [{"to": addr, "data": "0x18160ddd"}, hex(b)])
            rec[f"TS_{d}"] = int(v, 16) / 10 ** dec if v and v != "0x" else None
        except RuntimeError: rec[f"TS_{d}"] = None
    out.append(rec); print(rec, flush=True)
json.dump(blocks, open("data/supply_blocks_evm.json", "w"))
pd.DataFrame(out).to_csv("data/onchain_supply_evm.csv", index=False)

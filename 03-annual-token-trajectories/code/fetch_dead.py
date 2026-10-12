"""C9: balances of 0x...dEaD and 0x0 at the same blocks as totalSupply, for Ethereum and other EVM tokens."""
import json, subprocess, time, pandas as pd
EP = {"ethereum": ["https://eth.drpc.org", "https://rpc.mevblocker.io", "https://eth-mainnet.public.blastapi.io", "https://gateway.tenderly.co/public/mainnet"],
      "bsc": ["https://bsc-mainnet.public.blastapi.io"], "base": ["https://base.drpc.org", "https://base-mainnet.public.blastapi.io"],
      "optimism": ["https://optimism.drpc.org"], "polygon": ["https://polygon.drpc.org"]}
HOLD = {"dead": "000000000000000000000000000000000000000000000000000000000000dead", "zero": "0" * 64}
DATES = ["2023-10-01", "2024-10-01", "2025-10-01", "2026-10-01"]
def call(chain, to, data, block):
    for a in range(4):
        for u in EP[chain]:
            r = subprocess.run(["curl", "-s", "-m", "30", "-X", "POST", u, "-H", "content-type: application/json",
                "-d", json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params": [{"to": to, "data": data}, hex(block)]})], capture_output=True, text=True)
            try:
                j = json.loads(r.stdout)
                if "result" in j: return j["result"]
            except Exception: pass
        time.sleep(2 * (a + 1))
    return None
eb = json.load(open("data/supply_blocks.json"))["blocks"]; ob = json.load(open("data/supply_blocks_evm.json"))
frames = []
for f, chainfn, blk in [("data/onchain_supply_gross.csv", lambda r: "ethereum", lambda c: eb), ("data/onchain_supply_evm.csv", lambda r: r["chain"], lambda c: ob[c])]:
    S = pd.read_csv(f)
    for i, r in S.iterrows():
        c = chainfn(r); dec = int(r["decimals"]) if "decimals" in S.columns and pd.notna(r.get("decimals")) else None
        if dec is None:
            v = call(c, r.address, "0x313ce567", blk(c)[DATES[-1]]); dec = int(v, 16) if (v and v != "0x") else 18
        for d in DATES:
            ts = r.get(f"TS_{d}")
            if pd.isna(ts): S.loc[i, f"NET_{d}"] = None; continue
            burned = 0.0
            for k, h in HOLD.items():
                v = call(c, r.address, "0x70a08231" + h, blk(c)[d])
                burned += int(v, 16) / 10 ** dec if v and v != "0x" else 0.0
            S.loc[i, f"BURNED_{d}"] = burned; S.loc[i, f"NET_{d}"] = ts - burned
        print(r.gecko_id, [round(S.loc[i, f"NET_{d}"] / 1e6, 2) if pd.notna(S.loc[i, f"NET_{d}"]) else None for d in DATES], flush=True)
    frames.append(S)
frames[0].to_csv("data/onchain_supply.csv", index=False)
frames[1].to_csv("data/onchain_supply_evm.csv", index=False)

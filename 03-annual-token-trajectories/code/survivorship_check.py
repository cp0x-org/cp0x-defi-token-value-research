"""C10: upper-bound market caps for candidates without a CoinGecko CSV. Prices: DefiLlama coins historical point values
(searchWidth 2d) at window starts; supply: current on-chain totalSupply (latest block). -> data/missing_cg_fdv.csv"""
import json, subprocess, time, pandas as pd
M = pd.read_csv("data/missing_cg_meta.csv")
RPC = {"ethereum": "https://eth.drpc.org", "arbitrum": "https://arbitrum.drpc.org", "optimism": "https://optimism.drpc.org", "base": "https://base.drpc.org",
       "polygon": "https://polygon.drpc.org", "bsc": "https://bsc-mainnet.public.blastapi.io", "fantom": "https://fantom.drpc.org", "moonbeam": "https://moonbeam.drpc.org",
       "avax": "https://avalanche.drpc.org", "cronos": "https://cronos.drpc.org", "celo": "https://celo.drpc.org", "telos": "https://rpc.telos.net/evm", "boba": "https://mainnet.boba.network"}
FIX = {"kwenta": ("optimism", "0x920cf626a271321c151d027030d5d08af699456b")}  # DefiLlama lists the address without chain; the token is on OP Mainnet
def rpc(u, to, data):
    r = subprocess.run(["curl", "-s", "-m", "20", "-X", "POST", u, "-H", "content-type: application/json",
        "-d", json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_call", "params": [{"to": to, "data": data}, "latest"]})], capture_output=True, text=True)
    try: return json.loads(r.stdout).get("result")
    except Exception: return None
rows = []
for _, r in M.iterrows():
    a = str(r.address) if pd.notna(r.address) else ""
    chain, addr = (a.split(":")[0], a.split(":")[1]) if ":" in a else (("ethereum", a) if a.startswith("0x") else ("", ""))
    if r.gecko_id in FIX: chain, addr = FIX[r.gecko_id]
    ts = None
    if chain in RPC and addr.startswith("0x"):
        t, d = rpc(RPC[chain], addr, "0x18160ddd"), rpc(RPC[chain], addr, "0x313ce567")
        if t and t != "0x" and d and d != "0x": ts = int(t, 16) / 10 ** int(d, 16)
    rec = {"gecko_id": r.gecko_id, "name": r["name"], "chain": chain, "supply_latest": ts}
    for dte in ["2023-10-01", "2024-10-01", "2025-10-01"]:
        tt = int(pd.Timestamp(dte).timestamp())
        j = json.loads(subprocess.run(["curl", "-s", "-m", "20", f"https://coins.llama.fi/prices/historical/{tt}/coingecko:{r.gecko_id}?searchWidth=2d"], capture_output=True, text=True).stdout or "{}")
        p = j.get("coins", {}).get(f"coingecko:{r.gecko_id}", {}).get("price")
        rec[f"p_{dte}"] = p; rec[f"fdv_{dte}"] = p * ts if (p and ts) else None
        time.sleep(0.3)
    rows.append(rec)
D = pd.DataFrame(rows); D.to_csv("data/missing_cg_fdv.csv", index=False); print(D.to_string())

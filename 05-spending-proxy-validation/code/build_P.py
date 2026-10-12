"""Family P: transfer-based outflows of DefiLlama treasury address sets on Ethereum (METHOD_R6V)."""
import json, os, time, urllib.request, numpy as np, pandas as pd
SETS = json.load(open("data/treasury_sets.json"))
PKEY = {"lido": "lido", "aave": "aave", "sky": "maker", "uniswap": "uniswap"}
OWN = {"lido": {"0x5a98fcbea516cf06857215779fd812ca3bef1b32"},
       "aave": {"0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9"},
       "uniswap": {"0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"},
       "sky": {"0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2", "0x56072c95faa701256059aa122697b133aded9279",
               "0xc20059e0317de91738d13af027dfc4a50781b066", "0xb30fe1cf884b48a22a50d22a9282004f2c5e9406"}}
ETH = "native"
BURN = {"0x0000000000000000000000000000000000000000", "0x000000000000000000000000000000000000dead"}
RPCS = ["https://eth.drpc.org", "https://rpc.mevblocker.io", "https://eth-mainnet.public.blastapi.io"]
os.makedirs("raw/prices", exist_ok=True)

def load(p):
    T = set(SETS[PKEY[p]]["owners"]); rows = []
    for a in T:
        for x in json.load(open(f"raw/tx/{a}_tokentx.json")):
            rows.append(dict(hash=x["hash"], ts=int(x["timeStamp"]), frm=x["from"].lower(), to=x["to"].lower(), token=x["contractAddress"].lower(),
                             sym=x.get("tokenSymbol"), amt=int(x["value"]) / 10 ** int(x.get("tokenDecimal") or 18), kind="erc20", li=str(x.get("logIndex"))))
        for kind in ("txlist", "txlistinternal"):
            for x in json.load(open(f"raw/tx/{a}_{kind}.json")):
                if x.get("isError", "0") != "0" or int(x.get("value") or 0) == 0: continue
                rows.append(dict(hash=x["hash"], ts=int(x["timeStamp"]), frm=x["from"].lower(), to=(x.get("to") or x.get("contractAddress") or "").lower(),
                                 token=ETH, sym="ETH", amt=int(x["value"]) / 1e18, kind=kind, li=str(x.get("traceId", ""))))
    D = pd.DataFrame(rows)
    # no de-duplication: the API gives no log index, so identical rows inside one transaction are separate transfers;
    # a row appears in two address files only when both ends are in T, and such internal rows are neither out nor in (CHANGES V5)
    D["out"] = D.frm.isin(T) & ~D.to.isin(T); D["inn"] = D.to.isin(T) & ~D.frm.isin(T)
    D["day"] = pd.to_datetime(D.ts, unit="s").dt.normalize()
    return D, T

def rpc(batch, need_result=False):
    for k in range(12):
        url = RPCS[k % len(RPCS)]
        try:
            req = urllib.request.Request(url, data=json.dumps(batch).encode(), headers={"Content-Type": "application/json", "User-Agent": "r6v"})
            with urllib.request.urlopen(req, timeout=60) as r: res = json.load(r)
            if isinstance(res, list) and len(res) == len(batch) and all(("result" in x) if need_result else ("result" in x or "error" in x) for x in res):
                return {x["id"]: x for x in res}
        except Exception: pass
        time.sleep(2 + k)
    raise RuntimeError("rpc failed")

def classify(addrs):
    fn = "data/recipient_class.json"; C = json.load(open(fn)) if os.path.exists(fn) else {}
    todo = [a for a in addrs if a not in C and a not in BURN]
    from concurrent.futures import ThreadPoolExecutor
    chunks = [todo[i:i + 40] for i in range(0, len(todo), 40)]
    def one(chunk):
        r1 = rpc([{"jsonrpc": "2.0", "id": j, "method": "eth_getCode", "params": [a, "latest"]} for j, a in enumerate(chunk)], need_result=True)
        r2 = rpc([{"jsonrpc": "2.0", "id": j, "method": "eth_call", "params": [{"to": a, "data": "0xe75235b8"}, "latest"]} for j, a in enumerate(chunk)])
        return chunk, r1, r2
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(one, chunks))
    for chunk, r1, r2 in results:
        for j, a in enumerate(chunk):
            code = (r1.get(j, {}).get("result") or "0x")
            thr = r2.get(j, {}).get("result")
            if code in ("0x", "") or code.startswith("0xef0100"): C[a] = "eoa"
            elif thr and len(thr) == 66 and 0 < int(thr, 16) < 1000: C[a] = "multisig"
            else: C[a] = "contract"
    json.dump(C, open(fn, "w"))
    for a in BURN: C[a] = "burn"
    return C

def price_series(token):
    fn = f"raw/prices/{token}.json"
    if not os.path.exists(fn):
        cid = "coingecko:ethereum" if token == ETH else f"ethereum:{token}"
        pts = []
        for st in (1672531200, 1672531200 + 499 * 86400, 1672531200 + 998 * 86400):
            for k in range(5):
                try:
                    with urllib.request.urlopen(f"https://coins.llama.fi/chart/{cid}?start={st}&span=499&period=1d&searchWidth=600", timeout=60) as r:
                        d = json.load(r); break
                except Exception: time.sleep(2 + k); d = {}
            pts += (d.get("coins", {}).get(cid, {}) or {}).get("prices", [])
        json.dump(pts, open(fn, "w")); time.sleep(0.2)
    pts = json.load(open(fn))
    if not pts: return None
    s = pd.Series({pd.Timestamp(x["timestamp"], unit="s").normalize(): x["price"] for x in pts}).groupby(level=0).last().sort_index()
    return s

def value(D):
    D = D.copy(); D["usd"] = np.nan
    for tok, g in D.groupby("token"):
        s = price_series(tok)
        if s is None: continue
        idx = s.index.get_indexer(g.day, method="nearest")
        ok = np.abs((s.index[idx] - g.day.values).days) <= 3
        D.loc[g.index, "usd"] = np.where(ok, g.amt.values * s.values[idx], np.nan)
    return D

if __name__ == "__main__":
    bench = pd.read_csv("data/reported_spending.csv")
    res, diag = [], []
    import sys
    for p in (sys.argv[1:] or PKEY):
        D, T = load(p)
        D = D[(D.day >= "2023-01-01") & (D.day < "2026-01-01")]
        inflow_tx = set(D[D.inn].hash)
        O = D[D.out].copy()
        O["swap_tx"] = O.hash.isin(inflow_tx)
        O["own"] = O.token.isin(OWN[p])
        O = value(O)
        # recipients are classified only where classification can matter (priced, non-swap outflows)
        need = sorted(set(O[O.usd.notna() & (O.usd > 0) & ~O.swap_tx].to))
        C = classify(need)
        O["rclass"] = O.to.map(C).fillna("not_needed")
        O["p1"] = ~O.swap_tx & O.rclass.isin(["eoa", "multisig"])
        O.to_csv(f"data/P_outflows_{p}.csv.gz", index=False)
        for _, r in bench[bench.protocol == p].iterrows():
            w = O[(O.day >= r.period_start) & (O.day <= r.period_end)]
            v = w.usd.fillna(0)
            res.append(dict(protocol=p, period_start=r.period_start, period_end=r.period_end,
                            P0=float(v.sum()), P1=float(v[w.p1].sum()), P1c=float(v[w.p1 & ~w.own].sum()),
                            excl_swap=float(v[w.swap_tx].sum()), excl_contract=float(v[~w.swap_tx & (w.rclass == "contract")].sum()),
                            excl_burn=float(v[~w.swap_tx & (w.rclass == "burn")].sum()),
                            n_out=len(w), n_unpriced=int(w.usd.isna().sum())))
        diag.append(dict(protocol=p, outflows=len(O), unpriced=int(O.usd.isna().sum()), unpriced_tokens=", ".join(sorted(set(O[O.usd.isna()].sym.astype(str))))[:300]))
    R = pd.DataFrame(res); R.to_csv("data/proxy_P.csv", index=False)
    pd.DataFrame(diag).to_csv("data/P_diagnostics.csv", index=False)
    pd.set_option("display.width", 250); print(R.round(0).to_string()); print(pd.DataFrame(diag).to_string())

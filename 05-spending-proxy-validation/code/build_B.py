"""Family B: balance-based outflows from DefiLlama treasury token series (METHOD_R6V)."""
import json, numpy as np, pandas as pd
SLUG = {"lido": "lido", "aave": "aave", "sky": "sky", "uniswap": "uniswap", "olympus": "olympus-dao"}

def daily_steps(slug):
    d = json.load(open(f"raw/treasury_{slug}.json"))
    rows = []
    for ck, v in d["chainTvls"].items():
        if ck == "OwnTokens": continue  # aggregate key, would double count
        own = ck.endswith("-OwnTokens")
        U = {pd.Timestamp(x["date"], unit="s").normalize(): x["tokens"] for x in v.get("tokens", [])}
        V = {pd.Timestamp(x["date"], unit="s").normalize(): x["tokens"] for x in v.get("tokensInUsd", [])}
        days = sorted(set(U) & set(V))
        for a, b in zip(days[:-1], days[1:]):
            ua, ub, vb, va = U[a], U[b], V[b], V[a]
            for k in set(ua) | set(ub):
                if k not in ua or k not in ub: continue  # adapter artefact rule
                du = (ub[k] or 0) - (ua[k] or 0)
                if du == 0: continue
                if ub[k] and ub[k] > 0 and k in vb: p = vb[k] / ub[k]
                elif ua[k] and ua[k] > 0 and k in va: p = va[k] / ua[k]
                else: continue
                rows.append((b, ck, own, k, du * p))
    S = pd.DataFrame(rows, columns=["day", "chain", "own", "token", "dv"])
    first = min(pd.Timestamp(x["date"], unit="s").normalize() for ck, v in d["chainTvls"].items() if ck != "OwnTokens" for x in v.get("tokens", [])[:1])
    return S, first

def proxies(S, start, end, first):
    if pd.Timestamp(start) <= first: return dict(B1=np.nan, B0=np.nan, B1_noown=np.nan, covered=False)
    w = S[(S.day > pd.Timestamp(start)) & (S.day <= pd.Timestamp(end) + pd.Timedelta(days=1))]
    net = w.groupby("day").dv.sum()
    net_noown = w[~w.own].groupby("day").dv.sum()
    return dict(B1=float((-net).clip(lower=0).sum()), B0=float((-w.dv).clip(lower=0).sum()),
                B1_noown=float((-net_noown).clip(lower=0).sum()), covered=True)

if __name__ == "__main__":
    bench = pd.read_csv("data/reported_spending.csv")
    out = []; top = []
    for p, slug in SLUG.items():
        S, first = daily_steps(slug)
        S.to_csv(f"data/B_steps_{p}.csv.gz", index=False)
        for _, r in bench[bench.protocol == p].iterrows():
            out.append(dict(protocol=p, period_start=r.period_start, period_end=r.period_end, series_start=str(first.date()), **proxies(S, r.period_start, r.period_end, first)))
        net = S.groupby("day").dv.sum().sort_values()
        for day, v in net.head(5).items(): top.append(dict(protocol=p, day=str(day.date()), net_dv=v))
    pd.DataFrame(out).to_csv("data/proxy_B.csv", index=False)
    pd.DataFrame(top).to_csv("data/B_largest_outflow_days.csv", index=False)
    print(pd.DataFrame(out).to_string())

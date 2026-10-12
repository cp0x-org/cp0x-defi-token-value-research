"""Research 5 data build (METHOD_R5.md). Writes data/category_map.csv and data/panel_r5.csv."""
import json, os, sys, numpy as np, pandas as pd
sys.path.insert(0, "/home/claude/r4rep")
from common import load_fees, sum90  # raw/fees is a link to the Research 4 replication fee series
pass
d = json.load(open("raw/overview_fees_breakdown.json"))
P = d["protocols"]
SPLIT = {"Liquid Staking", "Liquid Restaking", "Restaking"}
ETHL2 = {"Ethereum", "Arbitrum", "Base", "OP Mainnet", "Optimism", "Linea", "Scroll", "zkSync Era", "ZKsync Era", "Mantle", "Blast", "Unichain"}
ASSET = {"Solana": "SOL", "BSC": "BNB", "Avalanche": "AVAX", "Sui": "SUI", "Aptos": "APT", "Polygon": "POL"}
COSMOS = {"Cosmos", "Osmosis", "Stride", "Persistence", "Celestia", "Injective", "Neutron", "Juno", "Evmos", "Kava", "Sei", "Dymension", "Stargaze", "Terra2", "Archway", "Quicksilver", "Agoric"}
def asset(chains):
    c = (chains or ["?"])[0]
    if c in ETHL2: return "ETH"
    if c in ASSET: return ASSET[c]
    if c in COSMOS: return c
    return "other"
rows = []
for p in P:
    cat = p.get("category")
    key = f"{cat}|{asset(p.get('chains'))}" if cat in SPLIT else cat
    grp = p.get("parentProtocol") or f"id#{p['defillamaId']}"
    rows.append(dict(name=p["name"], group=grp, category=cat, chain0=(p.get("chains") or [""])[0], key=key, key_nosplit=cat, fees_all_time=p.get("totalAllTime") or 0))
META = pd.DataFrame(rows)
main_key = META.sort_values("fees_all_time", ascending=False).groupby("group").first()[["key", "key_nosplit"]].rename(columns={"key": "main_key", "key_nosplit": "main_key_nosplit"})
META = META.merge(main_key, left_on="group", right_index=True, how="left")
META.to_csv("/home/claude/r22/data/category_map_w0.csv", index=False)

# daily fees by product
recs = {}
for ts, row in d["totalDataChartBreakdown"]:
    day = pd.Timestamp(ts, unit="s").normalize()
    for name, v in row.items(): recs[(day, name)] = float(v or 0)
FE = pd.Series(recs).unstack(fill_value=np.nan).sort_index()
def s90(cols, date):
    d1 = pd.Timestamp(date); w = FE.loc[d1 - pd.Timedelta(days=89): d1, [c for c in cols if c in FE.columns]]
    return float(w.sum().sum()) if w.shape[1] else 0.0
prod_by_key = META.groupby("key").name.apply(list).to_dict(); prod_by_key_ns = META.groupby("key_nosplit").name.apply(list).to_dict()
prod_by_group = META.groupby("group").name.apply(list).to_dict()
mk = META.drop_duplicates("group").set_index("group")[["main_key", "main_key_nosplit"]]

def rev(slug):
    try: dd = json.load(open(f"raw/rev/{slug}.json"))
    except Exception: return None
    ch = dd.get("totalDataChart") or []
    if not ch: return None
    return pd.Series({pd.Timestamp(t, unit="s").normalize(): float(v) for t, v in ch}).groupby(level=0).sum().sort_index()
def r90(R, date):
    if R is None: return np.nan
    d1 = pd.Timestamp(date); w = R.loc[d1 - pd.Timedelta(days=89): d1]
    return float(w.sum()) if len(w) else np.nan

C2 = {"savings-xdai", "usdx-money-usdx", "crypto-com-chain", "near", "arbitrum", "baby-doge-coin", "flock-2", "livepeer"}
panels = [pd.read_csv("/home/claude/r22/data/panel_w0.csv")]
out = []
for Pn in panels:
    for _, r in Pn[~Pn.gecko_id.isin(C2) & ~Pn.supply_artefact].iterrows():
        g = r.group
        if g not in mk.index: continue
        prods = prod_by_group.get(g, []); key = mk.loc[g, "main_key"]; keyns = mk.loc[g, "main_key_nosplit"]
        main_prods = META[(META.group == g) & (META.key == key)].name.tolist()
        main_prods_ns = META[(META.group == g) & (META.key_nosplit == keyns)].name.tolist()
        R = rev(r.slug)
        FS = load_fees(r.slug, "dailyFees")  # CHANGES_R5 R1: group fees from the same summary source as revenue
        rec = dict(window=r.window, group=g, slug=r.slug, name=r["name"], gecko_id=r.gecko_id, key=key, key_nosplit=keyns, start=r.start, end=r["end"],
                   y=r.y, eth_ret=r.eth_ret, mc_start=r.mc_start, mc_end=r.mc_end, s_cg=r.s, beta=r.beta, drawdown_start=r.drawdown_start, ln_mc_start=r.ln_mc_start)
        for tag, dt in (("0", r.start), ("1", r["end"]), ("p", str((pd.Timestamp(r.start) - pd.Timedelta(days=365)).date()))):
            Fb = s90(prods, dt); Fm = s90(main_prods, dt); C = s90(prod_by_key.get(key, []), dt)
            F = sum90(FS, dt)[0] if FS is not None else np.nan
            Fm_ns = s90(main_prods_ns, dt); C_ns = s90(prod_by_key_ns.get(keyns, []), dt)
            rec.update({f"F{tag}": F, f"Fbreak{tag}": Fb, f"Fmain{tag}": Fm, f"C{tag}": C, f"Fmain_ns{tag}": Fm_ns, f"C_ns{tag}": C_ns, f"R{tag}": r90(R, dt)})
        out.append(rec)
X = pd.DataFrame(out)
lg = lambda a, b: np.log(a / b) if (a > 0 and b > 0) else np.nan
X["share0"] = X.Fmain0 / X.C0; X["share1"] = X.Fmain1 / X.C1; X["sharep"] = X.Fmainp / X.Cp
X["take0"] = X.R0 / X.F0; X["take1"] = X.R1 / X.F1
X["d_C"] = [lg(a, b) for a, b in zip(X.C1, X.C0)]; X["d_C_eth"] = X.d_C - X.eth_ret
X["d_share"] = [lg(a, b) for a, b in zip(X.share1, X.share0)]
X["d_D"] = [lg(a1 / b1, a0 / b0) if min(a1, b1, a0, b0) > 0 else np.nan for a1, b1, a0, b0 in zip(X.F1, X.Fmain1, X.F0, X.Fmain0)]
X["d_take"] = [lg(a, b) for a, b in zip(X.take1, X.take0)]
X["d_MF"] = [lg(m1 / f1, m0 / f0) if min(f1, f0) > 0 else np.nan for m1, f1, m0, f0 in zip(X.mc_end, X.F1, X.mc_start, X.F0)]
X["d_MR"] = [lg(m1 / r1, m0 / r0) if (r1 > 0 and r0 > 0) else np.nan for m1, r1, m0, r0 in zip(X.mc_end, X.R1, X.mc_start, X.R0)]
X["rev_variant"] = (X.R0 >= 0.01 * X.F0) & (X.R1 >= 0.01 * X.F1) & X.d_MR.notna()
X["err_fee"] = X.y - (X.d_C_eth + X.d_share + X.d_D + X.d_MF - X.s_cg)
X["err_rev"] = np.where(X.rev_variant, X.y - (X.d_C_eth + X.d_share + X.d_D + X.d_take + X.d_MR - X.s_cg), np.nan)
X["ln_F0"] = np.log(X.F0.where(X.F0 > 0)); X["ln_take0"] = np.log(X.take0.where(X.take0 > 0))
X["prior_share_growth"] = [lg(a, b) for a, b in zip(X.share0, X.sharep)]
X["rev_start_ok"] = X.R0 >= 0.01 * X.F0
X["d_share_ns"] = [lg(a1 / c1, a0 / c0) if min(a1, c1, a0, c0) > 0 else np.nan for a1, c1, a0, c0 in zip(X.Fmain_ns1, X.C_ns1, X.Fmain_ns0, X.C_ns0)]
X["d_C_ns_eth"] = [lg(a, b) for a, b in zip(X.C_ns1, X.C_ns0)] - X.eth_ret
def _conf(a, b): return bool(a > 0 and b > 0 and abs(np.log(a / b)) > np.log(2))
X["conflict_start"] = [_conf(a, b) for a, b in zip(X.F0, X.Fbreak0)]  # CHANGES_R5 R1 (revised): stages 2-3 use the start date only
X["conflict_stage1"] = [_conf(a, b) or _conf(c, d) for a, b, c, d in zip(X.F0, X.Fbreak0, X.F1, X.Fbreak1)]  # stage 1: both dates, only where both sources are positive
X.to_csv("/home/claude/r22/data/panel_r5_w0.csv", index=False)
print("rows", len(X), X.window.value_counts().sort_index().to_dict())
print("fee-variant defined", int(X[["d_C_eth", "d_share", "d_D", "d_MF"]].notna().all(axis=1).sum()), "| revenue variant", int(X.rev_variant.sum()))
print("max identity error fee", float(X.err_fee.abs().max()), "rev", float(np.nanmax(np.abs(X.err_rev))))

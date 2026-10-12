"""Build Research4_data.xlsx from the current outputs."""
import json, sys, numpy as np, pandas as pd
out = sys.argv[1]
pct = lambda x: (np.exp(x) - 1)
P = pd.read_csv("data/panel_stage4.csv") if False else pd.read_csv("data/panel.csv")
C2 = {"savings-xdai", "usdx-money-usdx", "crypto-com-chain", "near", "arbitrum", "baby-doge-coin", "flock-2", "livepeer"}
P["in_main"] = ~P.supply_artefact & ~P.gecko_id.isin(C2) & P.g.notna()
cols = ["window", "name", "category", "gecko_id", "in_main", "mc_start", "mc_end", "fees90_start", "fees90_end", "fee_days_end", "H_start", "H_end", "y", "g", "m", "s", "beta", "drawdown_start", "ln_M_start"]
X = P[cols].copy()
for c in ["y", "g", "m", "s"]: X[c + "_pct"] = pct(X[c]).round(4)
M = P[P.in_main].copy()
M["quintile"] = M.groupby("window").y.transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=[1, 2, 3, 4, 5]))
Q = M.groupby("quintile")[["y", "g", "m", "s", "H_start", "beta"]].median()
for c in ["y", "g", "m", "s"]: Q[c + "_pct"] = pct(Q[c]).round(3)
Q["n"] = M.groupby("quintile").size()
S2 = pd.read_csv("data/panel_stage2.csv")[["window", "name", "gecko_id", "new_products", "lost_products", "new_chains", "lost_chains", "n_products_start", "n_chains_start", "T_start", "T_end", "treasury_change", "hack"]]
S4 = pd.read_csv("data/panel_stage4.csv")[["window", "name", "gecko_id", "supply_chain", "s", "s_issue", "u", "class"]]
for c in ["s", "s_issue", "u"]: S4[c + "_pct"] = pct(S4[c]).round(4)
L = pd.read_csv("data/lido_peers.csv")
for c in ["y", "g", "m", "s", "s_issue", "rev_growth_eth"]: L[c + "_pct"] = (pct(L[c]) * 100).round(1)
ldo = pd.DataFrame({"date": ["2023-10-01", "2024-10-01", "2025-10-01", "2026-10-01"], "coingecko_circulating_M": [819.1, 895.6, 896.3, 829.6], "onchain_1B_minus_treasury_M": [890.6, 895.3, 895.8, 878.5]})
ph = json.load(open("data/posthoc.json"))
PH = pd.DataFrame([{"check": k, "detail": json.dumps(v, default=float)} for k, v in ph.items()])
readme = pd.DataFrame({"sheet": ["panel", "quintiles", "stage1_runs", "stage2_vars", "stage2_runs", "stage3_runs", "stage4_supply", "stage4_runs", "stage4_audit", "bridging_check", "onchain_supply_eth", "onchain_supply_evm",
        "survivorship", "posthoc", "price_check", "lido_vs_peers", "eth_lst_fee_share", "ldo_supply_check", "candidates"],
    "content": ["protocol x window panel; y = log return vs ETH, g = log fee growth in ETH terms, m = log change of market cap / fees, s = log change of CoinGecko circulating supply; *_pct = exp(x)-1",
        "median components by quintile of y within window (main sample)", "stage 1 main run and robustness: variance shares, coefficients, verdicts H1-H4",
        "new products/chains, treasury, hacks", "stage 2 main run and robustness, verdicts H5-H8", "stage 3 (Ethereum, net supply) runs, H2a/H2b",
        "on-chain issuance s_issue, unlock residual u = s - s_issue, audit class", "stage 4 runs, H2a-wide and H9", "manual classification of the 20 largest residuals with sources",
        "per-token check of multi-chain mint/burn designs", "totalSupply and dead-address balances at window dates, Ethereum", "same for BSC, Base, OP Mainnet, Polygon",
        "upper-bound market caps of the 26 candidates without CoinGecko data", "post-hoc checks (not pre-registered)", "CoinGecko vs DefiLlama price cross-check",
        "descriptive comparison of Lido with staking peers", "Lido share of ETH liquid-staking fees among tracked protocols", "LDO circulating supply: CoinGecko vs on-chain proxy",
        "all candidate protocol groups and exclusion reasons"]})
sheets = [("README", readme), ("panel", X), ("quintiles", Q.reset_index()), ("stage1_runs", pd.read_csv("data/runs_summary.csv")), ("stage2_vars", S2),
          ("stage2_runs", pd.read_csv("data/runs_summary_stage2.csv")), ("stage3_runs", pd.read_csv("data/runs_summary_stage3.csv")), ("stage4_supply", S4),
          ("stage4_runs", pd.read_csv("data/runs_summary_stage4.csv")), ("stage4_audit", pd.read_csv("data/stage4_audit.csv")),
          ("bridging_check", pd.read_csv("data/stage4_bridging_check.md", sep="|", skipinitialspace=True).iloc[1:, 1:-1]),
          ("onchain_supply_eth", pd.read_csv("data/onchain_supply.csv")), ("onchain_supply_evm", pd.read_csv("data/onchain_supply_evm.csv")),
          ("survivorship", pd.read_csv("data/missing_cg_fdv.csv")), ("posthoc", PH), ("price_check", pd.read_csv("data/price_check.csv")),
          ("lido_vs_peers", L), ("eth_lst_fee_share", pd.read_csv("data/eth_lst_share.csv")), ("ldo_supply_check", ldo), ("candidates", pd.read_csv("data/candidates.csv"))]
with pd.ExcelWriter(out, engine="openpyxl") as w:
    for name, df in sheets:
        df.to_excel(w, sheet_name=name, index=False); ws = w.sheets[name]; ws.freeze_panes = "A2"
        for col in ws.columns:
            L_ = max(len(str(c.value or "")) for c in col[:200]); ws.column_dimensions[col[0].column_letter].width = min(max(9, L_ + 2), 45)
print("sheets", len(sheets))

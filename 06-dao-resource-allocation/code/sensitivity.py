"""Research 6, after the review (CHANGES D7): the pattern rule under three readings of "decision type",
with the frozen category-share measure and with a fixed-coverage category (products with fees at least 90 days before t0)."""
import json, numpy as np, pandas as pd
R6 = "/home/claude/r6"
meta = pd.read_csv("/home/claude/r5/data/category_map.csv")
bd = json.load(open("/home/claude/r5/raw/overview_fees_breakdown.json"))["totalDataChartBreakdown"]
rec = {}; first = {}
for ts, row in bd:
    day = pd.Timestamp(int(ts), unit="s").normalize()
    for n, v in row.items():
        v = float(v or 0); rec[(day, n)] = v
        if v > 0 and n not in first: first[n] = day
FE = pd.Series(rec).unstack(fill_value=np.nan).sort_index()
GROUP = {"lido": "id#182", "aave": "parent#aave", "sky": "parent#maker", "uniswap": "parent#uniswap"}
def share(p, d, cov=None):
    g = GROUP[p]; mk = meta[meta.group == g].main_key.iloc[0]
    own = meta[(meta.group == g) & (meta.key == mk)].name.tolist(); cat = meta[meta.key == mk].name.tolist()
    if cov is not None: cat = [n for n in cat if n in first and first[n] <= pd.Timestamp(cov) - pd.Timedelta(days=90)]
    d = pd.Timestamp(d); w = FE.loc[d - pd.Timedelta(days=89): d]
    a = w[[c for c in own if c in w.columns]].sum().sum(); b = w[[c for c in cat if c in w.columns]].sum().sum()
    return a / b

O = pd.read_csv(f"{R6}/data_outcomes.csv")
U = O[(O.goal_category == "usage_market") & O.primary_12m_sign.isin(["+", "-"])].copy()
U["base_12m"] = U.category_fee_share_12m.astype(float)
U["fixedcov_12m"] = [float(np.log(share(r.protocol, pd.Timestamp(r.t0) + pd.DateOffset(months=12), r.t0) / share(r.protocol, r.t0, r.t0))) for _, r in U.iterrows()]
base = U.line_item.str.split("(").str[0].str.strip().str.lower()  # line item as written before any parenthetical
U["type_line_item"] = np.where(base.str.startswith("incentives"), "incentives",
                       np.where(base.str.startswith("marketing"), "marketing/growth",
                       np.where(base.str.contains("uf funding|foundation"), "foundation budget", "other")))
U["type_class"] = "class " + U.cls

def check(df, typecol, valcol, per="decision"):
    out = []
    for t, g in df.groupby(typecol):
        if per == "dao":
            s = g.groupby("protocol")[valcol].apply(lambda x: np.sign(np.sign(x).sum()))  # majority sign within a DAO, 0 if tied
            n, neg, pos = len(s), int((s < 0).sum()), int((s > 0).sum())
        else:
            n, neg, pos = len(g), int((g[valcol] < 0).sum()), int((g[valcol] > 0).sum())
        daos = g.protocol.nunique(); k = max(neg, pos)
        meets = daos >= 3 and k >= 3 and k >= 2 / 3 * n
        out.append(dict(type=t, counting=per, measure=valcol, daos=daos, n=n, negative=neg, positive=pos, meets_rule=meets))
    return out
res = []
for typecol in ["type_line_item", "type_class"]:
    for valcol in ["base_12m", "fixedcov_12m"]:
        for per in ["decision", "dao"]:
            res += check(U, typecol, valcol, per)
R = pd.DataFrame(res); R.to_csv(f"{R6}/data_pattern_sensitivity.csv", index=False)
U[["protocol", "id", "t0", "type_line_item", "type_class", "base_12m", "fixedcov_12m"]].to_csv(f"{R6}/data_usage_decisions.csv", index=False)
pd.set_option("display.width", 200)
print(U[["protocol", "id", "t0", "type_line_item", "base_12m", "fixedcov_12m"]].round(3).to_string()); print(R.to_string())

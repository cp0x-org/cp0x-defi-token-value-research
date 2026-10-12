"""Step 1: candidate groups (parent protocol -> gecko_id, category). Rules from METHOD_R4.md, Universe 1-3."""
import json, collections, pandas as pd
EXCL = {"Chain","CEX","Gaming","Luck Games","Physical TCG","Gamified Mining","SoFi","AI Agents","DePIN","Domains",
        "Wallets","Developer Tools","Services","Payments","Privacy","Block Builders","DAO Service Provider","Telegram Bot","Token Locker"}
ov = json.load(open("raw/overview_fees.json"))["protocols"]
pr = {str(p["id"]): p for p in json.load(open("raw/protocols.json"))}
lite = json.load(open("raw/lite.json"))
parents = {p["id"]: p for p in lite["parentProtocols"]}
groups = collections.defaultdict(list)
for o in ov:
    key = o.get("parentProtocol") or f"id#{o['defillamaId']}"
    groups[key].append(o)
rows = []
for key, ch in groups.items():
    top = max(ch, key=lambda o: o.get("totalAllTime") or 0)
    cat = top.get("category")
    if key.startswith("parent#"):
        g = parents.get(key, {}).get("gecko_id")
        slug = key.split("#", 1)[1]
        name = parents.get(key, {}).get("name", slug)
    else:
        g = None; slug = top.get("slug"); name = top.get("name")
    child_ids = {pr.get(str(o["defillamaId"]), {}).get("gecko_id") for o in ch} - {None, ""}
    reason = ""
    if not g:
        if len(child_ids) == 1: g = next(iter(child_ids))
        elif len(child_ids) > 1: reason = "several_gecko_ids"
        else: reason = "no_gecko_id"
    if cat in EXCL: reason = reason or "excluded_category"
    rows.append(dict(group=key, slug=slug, name=name, category=cat, gecko_id=g or "", n_children=len(ch),
                     fees_all_time=round(sum(o.get("totalAllTime") or 0 for o in ch)), excluded=reason))
df = pd.DataFrame(rows).sort_values("fees_all_time", ascending=False)
df.to_csv("data/candidates.csv", index=False)
k = df[df.excluded == ""]
print(len(df), "groups;", len(k), "kept;", df.excluded.value_counts().to_dict())
print("duplicate gecko ids among kept:", k.gecko_id[k.gecko_id.duplicated()].tolist()[:20])

"""Automated first-pass C screening over the frozen universe.
C = fee_share_direct -> buyback_distribute. Screening only: produces a manual
fact-check queue, never writes to the mechanistic sample.
Sources: DefiLlama methodology (current form), DefiLlama adapter code (dated logic),
Snapshot proposals by brand, Bing RSS for the frozen C-query, Bing RSS discovery of
docs/governance pages with sentence extraction from fetched pages.
Usage: python3 c_screening.py [--only name1,name2] [--out file]"""
import json, re, sys, time, html, hashlib, pathlib, argparse, datetime as dt
import os
import requests
import pandas as pd

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "data" / "screen_cache"; CACHE.mkdir(parents=True, exist_ok=True)
DA_DIR = pathlib.Path(os.environ.get("DA_DIR", "/tmp/da"))  # git clone https://github.com/DefiLlama/dimension-adapters, commit 1029ba611a85d425d3a022d5f274fd3b9c6a29a0
UA = {"User-Agent": "Mozilla/5.0 (research screening; cp0x)"}
FROZEN_C = "{b} stakers previously earned ETH rewards now receive native token bought back from market rewards change protocol switched reward currency"
DISCOVERY = "{b} tokenomics staking rewards protocol fees stakers docs governance"
SUFFIX = re.compile(r"\b(v\d(\.\d)?|perps?|amm|dex|cl|clmm|spot|orderbook|fusion|integral|legacy|exchange|slipstream|perpetual|swap|finance|protocol|network|classic|elastic|infinity|dlmm|stableswap)\b", re.I)

def brand(name):
    b = SUFFIX.sub("", name)
    b = re.sub(r"\s+", " ", b).strip(" -")
    return b or name

def cached(key, fn):
    f = CACHE / (hashlib.sha1(key.encode()).hexdigest() + ".json")
    if f.exists():
        return json.loads(f.read_text())
    v = fn()
    f.write_text(json.dumps(v))
    return v

def bing_rss(q):
    def go():
        try:
            r = requests.get("https://www.bing.com/search", params={"q": q, "format": "rss", "count": 15}, headers=UA, timeout=30)
            items = re.findall(r"<item>(.*?)</item>", r.text, re.S)
            out = []
            for it in items:
                g = lambda t: html.unescape(re.sub(r"<.*?>", "", (re.search(rf"<{t}>(.*?)</{t}>", it, re.S) or [None, ""])[1]))
                out.append({"title": g("title"), "link": g("link"), "desc": g("description"), "date": g("pubDate")})
            time.sleep(1.5)
            return out
        except Exception as e:
            return [{"error": str(e)}]
    return cached("bing|" + q, go)

def fetch_text(url):
    def go():
        try:
            r = requests.get(url, headers=UA, timeout=25)
            if "text/html" not in r.headers.get("content-type", "") and "text/plain" not in r.headers.get("content-type", ""):
                return ""
            t = re.sub(r"(?s)<(script|style).*?</\1>", " ", r.text)
            t = html.unescape(re.sub(r"<[^>]+>", " ", t))
            return re.sub(r"\s+", " ", t)[:200000]
        except Exception:
            return ""
    return cached("page|" + url, go)

def llama_protocol(slug):
    def go():
        try:
            r = requests.get(f"https://api.llama.fi/protocol/{slug}", timeout=60).json()
            keep = {k: r.get(k) for k in ("name", "url", "github", "governanceID", "parentProtocol", "otherProtocols")}
            return keep
        except Exception as e:
            return {"error": str(e)}
    return cached("llama|" + slug, go)

def snapshot_space(space):
    def go():
        out, skip = [], 0
        q = """query($sp:String,$skip:Int){ proposals(first:1000, skip:$skip, where:{space:$sp}, orderBy:"created", orderDirection:asc)
               { id title body created space { id } } }"""
        while skip <= 3000:
            try:
                r = requests.post("https://hub.snapshot.org/graphql", json={"query": q, "variables": {"sp": space, "skip": skip}}, timeout=60).json()
            except Exception as e:
                return out + [{"error": str(e)}]
            ps = (r.get("data") or {}).get("proposals") or []
            out += [{"id": x["id"], "title": x["title"], "body": (x["body"] or "")[:20000], "created": x["created"], "space": x["space"]["id"]} for x in ps]
            if len(ps) < 1000: break
            skip += 1000; time.sleep(0.6)
        time.sleep(0.6)
        return out
    return cached("snapspace|" + space, go)

def snapshot(b):
    def go():
        q = """query($kw:String){ proposals(first:200, where:{title_contains:$kw}, orderBy:"created", orderDirection:asc)
               { id title body created space { id } } }"""
        try:
            r = requests.post("https://hub.snapshot.org/graphql", json={"query": q, "variables": {"kw": b}}, timeout=60).json()
            ps = (r.get("data") or {}).get("proposals") or []
            time.sleep(0.6)
            return [{"id": p["id"], "title": p["title"], "body": (p["body"] or "")[:20000], "created": p["created"], "space": p["space"]["id"]} for p in ps]
        except Exception as e:
            return [{"error": str(e)}]
    return cached("snap|" + b, go)

# sentence-level patterns
ASSET = r"(?:\bETH\b|\bWETH\b|\bUSDC\b|\bUSDT\b|\bDAI\b|\bAVAX\b|\bSOL\b|\bBNB\b|stablecoins?|stables?\b)"
RE_BUY = re.compile(r"buy[\s-]?backs?|bought back|repurchas", re.I)
RE_DIST = re.compile(r"distribut|to (?:the )?stakers|stakers? (?:receive|earn|get)|rewards? to|given back to", re.I)
RE_DIRECT = re.compile(rf"(?:distribut\w*|paid|pay(?:s|ing)?|earn\w*|receiv\w*|shar\w*)[^.]{{0,80}}{ASSET}|{ASSET}[^.]{{0,60}}(?:to|for) (?:\w+ )?(?:stakers|holders|lockers)", re.I)
RE_TRANS = re.compile(r"instead of|replac|switch|transition|no longer|rather than|migrat|changed? (?:from|the)|from [^.]{0,60} to ", re.I)
RE_BURN_ONLY = re.compile(r"buy[\s-]?back and burn|buyback-and-burn|burned|burnt", re.I)
RE_STAKE = re.compile(r"stak|holder|locker|\bve[A-Z]", re.I)

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if 30 < len(s) < 600]

def classify_sentence(s):
    tags = set()
    if RE_TRANS.search(s): tags.add("trans")
    if RE_BUY.search(s) and RE_DIST.search(s) and not RE_BURN_ONLY.search(s): tags.add("bbd")
    if RE_DIRECT.search(s) and not RE_BUY.search(s): tags.add("direct")
    if RE_BURN_ONLY.search(s): tags.add("burn")
    return tags

def current_form(meth):
    t = " ".join(str(v) for v in (meth or {}).values() if isinstance(v, str))
    hr = " ".join(str(v) for k, v in (meth or {}).items() if "Holder" in k) or t
    if not hr.strip(): return "unknown", ""
    if RE_BUY.search(hr) and RE_BURN_ONLY.search(hr) and not RE_DIST.search(hr): return "buyback_burn", hr[:300]
    if RE_BUY.search(hr) and RE_DIST.search(hr): return "buyback_distribute", hr[:300]
    if RE_BUY.search(hr): return "buyback_other", hr[:300]
    if RE_STAKE.search(hr) and re.search(r"distribut|goes to|to (?:\w+ )?(?:stakers|holders|lockers)|paid", hr, re.I): return "fee_share_direct", hr[:300]
    return "unknown", hr[:300]

def adapter_signal(module):
    if not module: return None
    for base in [DA_DIR / "fees", DA_DIR / "dexs", DA_DIR / "factory"]:
        for f in list(base.glob(f"{module}.ts")) + list(base.glob(f"{module}/*.ts")):
            t = f.read_text(errors="ignore")
            dated = re.findall(r"(?:timestamp|startOfDay|options\.startTimestamp)\s*[<>]=?\s*(\d{10})", t)
            hold = re.findall(r"HoldersRevenue['\"]?\s*:\s*['\"`]([^'\"`]{0,300})", t)
            if dated or hold:
                return {"file": str(f.relative_to(DA_DIR)), "dated_cutoffs": sorted({dt.datetime.fromtimestamp(int(x), dt.UTC).strftime("%Y-%m-%d") for x in dated})[:8], "holders_text": " | ".join(hold)[:400]}
    return None

def screen(row, meta):
    name = row["name"]; b = brand(name)
    rel = re.compile(re.escape(b.split()[0]), re.I)
    ev = []  # evidence rows
    cf, cf_txt = current_form(meta.get("methodology"))
    if cf_txt:
        ev.append({"source_type": "defillama_methodology", "source_url": meta.get("methodologyURL", ""), "date": "", "snippet": cf_txt, "tags": [cf]})
    ad = adapter_signal(meta.get("module"))
    if ad:
        ev.append({"source_type": "defillama_adapter", "source_url": ad["file"], "date": ",".join(ad["dated_cutoffs"]), "snippet": ad["holders_text"], "tags": ["dated_logic"] if ad["dated_cutoffs"] else []})
    # snapshot: governance spaces from DefiLlama metadata, plus brand-in-title search
    spaces = []
    for slug in {meta.get("slug"), (meta.get("parentProtocol") or "").replace("parent#", "")} - {None, ""}:
        lp = llama_protocol(slug)
        for g in (lp.get("governanceID") or []):
            if str(g).startswith("snapshot:"): spaces.append(g.split(":", 1)[1])
    props = []
    for sp in dict.fromkeys(spaces): props += snapshot_space(sp)
    props += snapshot(b)
    seen_ids = set()
    for p in props:
        if "error" in p or p["id"] in seen_ids: continue
        seen_ids.add(p["id"])
        if "error" in p: continue
        for s in sentences(p["title"] + ". " + p["body"]):
            tg = classify_sentence(s)
            if tg & {"bbd", "direct"} and RE_STAKE.search(s):
                ev.append({"source_type": "snapshot", "source_url": f"https://snapshot.org/#/{p['space']}/proposal/{p['id']}", "date": dt.datetime.fromtimestamp(p["created"], dt.UTC).strftime("%Y-%m-%d"), "snippet": s[:400], "tags": sorted(tg)})
    # bing: frozen C-query + discovery
    links = []
    for qtype, q in [("frozen_c_query", FROZEN_C.format(b=b)), ("discovery", DISCOVERY.format(b=b))]:
        for it in bing_rss(q):
            if "error" in it: continue
            txt = f"{it['title']}. {it['desc']}"
            if not rel.search(txt) and not rel.search(it["link"]): continue
            if not re.search(r"token|stak|defi|dao|crypto|protocol|dex|perp|governance|yield|onchain|on-chain|swap", txt, re.I): continue  # homonym filter
            if re.search(r"gmx", txt, re.I) and not re.search(r"gmx", b, re.I): continue  # calibration-document attractor
            links.append(it["link"])
            for s in sentences(txt) or [txt]:
                tg = classify_sentence(s)
                if tg & {"bbd", "direct", "trans"}:
                    ev.append({"source_type": qtype, "source_url": it["link"], "date": it["date"], "snippet": s[:400], "tags": sorted(tg)})
    # fetch top protocol-relevant pages
    for url in list(dict.fromkeys(links))[:4]:
        for s in sentences(fetch_text(url)):
            if not rel.search(s) and not RE_STAKE.search(s): continue
            tg = classify_sentence(s)
            if ("bbd" in tg or "direct" in tg) and RE_STAKE.search(s):
                ev.append({"source_type": "fetched_page", "source_url": url, "date": "", "snippet": s[:400], "tags": sorted(tg)})
    # decision
    has = lambda t: [e for e in ev if t in e["tags"]]
    c_sent = [e for e in ev if {"trans", "bbd"} <= set(e["tags"]) and re.search(ASSET, e["snippet"])]
    trans_bbd = [e for e in ev if {"trans", "bbd"} <= set(e["tags"])]
    direct_ev, bbd_ev = has("direct"), has("bbd")
    hist_ev = [e for e in ev if e["source_type"] in ("snapshot", "fetched_page", "frozen_c_query", "discovery")]
    old_c = "fee_share_direct" if direct_ev else ""
    new_c = "buyback_distribute" if (bbd_ev or cf == "buyback_distribute") else ""
    if c_sent:
        st, conf, why = "yes", "medium", "предложение с языком перехода, выкупом с раздачей и прежним активом комиссий"
        top = c_sent[0]
    elif trans_bbd or (direct_ev and (bbd_ev or cf in ("buyback_distribute", "buyback_burn", "buyback_other"))):
        st, conf, why = "unclear", "low", "признаки обеих форм или перехода к выкупу с раздачей без подтверждённой прежней прямой формы"
        top = (trans_bbd or bbd_ev or direct_ev)[0]
    elif cf == "buyback_distribute":
        st, conf, why = "unclear", "low", "текущая форма выкуп с раздачей, история формы до не найдена; C не исключается"
        top = ev[0]
    elif cf == "fee_share_direct" and len(hist_ev) >= 2 and not bbd_ev:
        st, conf, why = "no_supported", "medium", f"текущая форма {cf} и есть исторические источники без признаков перехода к выкупу с раздачей"
        top = hist_ev[0]
    elif len(hist_ev) >= 3 and not bbd_ev:
        st, conf, why = "no_supported", "low", "есть релевантные исторические источники по протоколу, выкуп с раздачей не упоминается"
        top = hist_ev[0]
    else:
        st, conf, why = "no_low_recall", "low", f"недостаточно релевантных данных: исторических свидетельств {len(hist_ev)}, текущая форма {cf}"
        top = ev[0] if ev else {"source_type": "", "source_url": "", "date": "", "snippet": ""}
    return {"protocol": name, "brand": b, "source_url": top["source_url"], "source_type": top["source_type"], "date": top["date"],
            "snippet": top["snippet"], "old_mechanism_candidate": old_c, "new_mechanism_candidate": new_c, "current_form_defillama": cf,
            "screening_status": st, "confidence": conf, "reason": why, "n_evidence": len(ev), "n_historical": len(hist_ev)}, ev

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default=""); ap.add_argument("--out", default="data/stage3_c_auto_screening.csv"); ap.add_argument("--start", type=int, default=0); ap.add_argument("--end", type=int, default=10**6)
    a = ap.parse_args()
    u = pd.read_csv(HERE / "data" / "stage3_universe_frozen.csv")
    raw = json.load(open(HERE / "data" / "holders_rev_raw.json"))
    byname = {p["name"]: p for p in raw}
    only = [x.strip().lower() for x in a.only.split(",") if x.strip()]
    rows, allev = [], []
    for i, r in u.iterrows():
        if not (a.start <= i < a.end): continue
        if only and not any(o in r["versions"].lower() for o in only): continue
        meta = byname.get(r["name"], {})
        res, ev = screen(r, meta)
        rows.append(res)
        for e in ev: allev.append({"protocol": r["name"], **{k: (",".join(v) if isinstance(v, list) else v) for k, v in e.items()}})
        print(f"{res['screening_status']:14s} {res['confidence']:6s} {r['name'][:28]:28s} ev={res['n_evidence']:3d} hist={res['n_historical']:3d} cur={res['current_form_defillama']}", flush=True)
    pd.DataFrame(rows).to_csv(HERE / a.out, index=False)
    pd.DataFrame(allev).to_csv(HERE / a.out.replace(".csv", "_evidence.csv"), index=False)

if __name__ == "__main__":
    main()

"""Static audit of the built site. Exit code 1 if any problem is found.
Run from anywhere:  python tools/audit.py
Checks: one H1, heading order, unique titles/descriptions per language, lang attribute, canonical,
hreflang pairs, Open Graph/Twitter tags, JSON-LD validity, alt text, internal links and anchors,
no email addresses or third-party requests, sitemap/robots, asset files, English/Spanish parity.
"""
import os, re, sys, json, collections
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C
URL = C.SITE["url"]

SKIP_DIRS = {"tools", "fonts", "photos", ".git", ".github", "node_modules", "tests"}


class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True)
        s.links, s.ids, s.heads, s.imgs, s.ld, s.metas, s.rels, s.srcs = [], set(), [], [], [], {}, [], []
        s.title, s._t, s._ld, s.lang, s.details, s.lis, s.json_i18n, s._json = "", False, False, None, 0, 0, [], False
        s.robots = None
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if tag == "a" and "href" in a: s.links.append(a["href"])
        if tag in ("link",) and "href" in a: s.rels.append((a.get("rel"), a.get("hreflang"), a["href"]))
        if tag in ("script", "img", "source") and a.get("src"): s.srcs.append(a["src"])
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"): s.heads.append(int(tag[1]))
        if tag == "title": s._t = True
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k: s.metas[k] = a.get("content")
        if tag == "img": s.imgs.append(a)
        if tag == "script" and a.get("type") == "application/ld+json": s._ld = True
        if tag == "script" and a.get("type") == "application/json": s._json = True
        if tag == "html": s.lang = a.get("lang")
        if tag == "details": s.details += 1
        if tag == "li": s.lis += 1
    def handle_endtag(s, tag):
        if tag == "title": s._t = False
        if tag == "script": s._ld = False; s._json = False
    def handle_data(s, d):
        if s._t: s.title += d
        if s._ld: s.ld.append(d)
        if s._json: s.json_i18n.append(d)


def pages():
    out = {}
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith(".")]
        for f in files:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(d, f), ROOT).replace("\\", "/")
                p = P(); p.feed(open(os.path.join(d, f), encoding="utf-8").read()); out[rel] = p
    return out


def main():
    info = pages()
    problems = []
    add = problems.append
    indexable = {k: v for k, v in info.items() if k != "404.html"}

    for f, p in indexable.items():
        lang = "es" if f.startswith("es/") else "en"
        d = os.path.dirname(f)
        if p.heads.count(1) != 1: add(f"{f}: {p.heads.count(1)} H1")
        for a, b in zip(p.heads, p.heads[1:]):
            if b > a + 1: add(f"{f}: heading jumps h{a} -> h{b}"); break
        if not p.title.strip(): add(f"{f}: missing title")
        if not p.metas.get("description"): add(f"{f}: missing meta description")
        if p.lang != lang: add(f"{f}: lang={p.lang}, expected {lang}")
        exp = f"{URL}/{f}"
        can = [h for r, _, h in p.rels if r == "canonical"]
        if can != [exp]: add(f"{f}: canonical {can} != {exp}")
        hl = {hl: h for r, hl, h in p.rels if r == "alternate" and hl}
        for l, path in (("en", f[3:] if lang == "es" else f), ("es", f if lang == "es" else "es/" + f), ("x-default", f[3:] if lang == "es" else f)):
            if hl.get(l) != f"{URL}/{path}": add(f"{f}: hreflang {l} = {hl.get(l)}")
            if not os.path.exists(os.path.join(ROOT, path)): add(f"{f}: hreflang target missing {path}")
        for k in ("og:title", "og:description", "og:url", "og:image", "twitter:card", "twitter:image"):
            if not p.metas.get(k): add(f"{f}: missing {k}")
        if not p.ld: add(f"{f}: no JSON-LD") if f.endswith(("index.html", "faq.html")) is False or True else None
        for blob in p.ld:
            try:
                j = json.loads(blob)
                if "aggregateRating" in blob: add(f"{f}: aggregateRating in schema (unverified rating)")
            except Exception as ex:
                add(f"{f}: invalid JSON-LD {ex}")
        for blob in p.json_i18n:
            try: json.loads(blob)
            except Exception as ex: add(f"{f}: invalid form-i18n {ex}")
        for im in p.imgs:
            if "alt" not in im: add(f"{f}: image without alt attribute {im.get('src')}")
            if im.get("alt") == "" and not any(x in (im.get("src") or "") for x in ("google-g.png", "logo-emblem")): add(f"{f}: empty alt on a non-decorative image {im.get('src')}")
            if not (im.get("width") and im.get("height")): add(f"{f}: image without width/height {im.get('src')}")
        for l in p.links:
            if l.startswith("mailto:") or "@" in l: add(f"{f}: email link {l}")
            if l.startswith(("tel:", "sms:")): continue
            if l.startswith("http"):
                if urlparse(l).netloc not in ("www.google.com", "search.google.com", "share.google"): add(f"{f}: unexpected external link {l}")
                continue
            path, _, frag = l.partition("#")
            tgt = os.path.normpath(os.path.join(d, path)).replace("\\", "/") if path else f
            if tgt not in info and not os.path.exists(os.path.join(ROOT, tgt)): add(f"{f}: broken link {l}"); continue
            if frag and tgt in info and frag not in info[tgt].ids: add(f"{f}: missing anchor {l}")
        for s in p.srcs:
            if s.startswith("http"): add(f"{f}: third-party resource {s}")
            else:
                sp = s.split("?")[0].split(" ")[0]
                if not os.path.exists(os.path.join(ROOT, d, sp)): add(f"{f}: missing asset {s}")
        for r, _, h in p.rels:
            if r == "stylesheet" and not os.path.exists(os.path.join(ROOT, d, h.split("?")[0])): add(f"{f}: missing stylesheet {h}")

    for lang in ("en", "es"):
        sub = {k: v for k, v in indexable.items() if k.startswith("es/") == (lang == "es")}
        for key, lab in (("title", "title"), ("desc", "meta description")):
            vals = collections.Counter(((v.title if key == "title" else v.metas.get("description")) or "").strip() for v in sub.values())
            for t, n in vals.items():
                if n > 1: add(f"[{lang}] duplicate {lab}: {t[:60]}")

    # English/Spanish parity
    for f, p in indexable.items():
        if f.startswith("es/"): continue
        q = info.get("es/" + f)
        if not q: add(f"{f}: no Spanish counterpart"); continue
        if (p.details, p.heads.count(2), len(p.imgs)) != (q.details, q.heads.count(2), len(q.imgs)):
            add(f"{f}: EN/ES structure differs (details/h2/img) {(p.details, p.heads.count(2), len(p.imgs))} vs {(q.details, q.heads.count(2), len(q.imgs))}")
        if len(p.links) != len(q.links): add(f"{f}: EN/ES link count differs {len(p.links)} vs {len(q.links)}")

    # sitemap / robots
    sm = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(sm): add("sitemap.xml missing")
    else:
        locs = re.findall(r"<loc>(.*?)</loc>", open(sm, encoding="utf-8").read())
        for l in locs:
            if not l.startswith(URL + "/"): add(f"sitemap: foreign URL {l}"); continue
            if not os.path.exists(os.path.join(ROOT, l[len(URL) + 1:])): add(f"sitemap: URL has no file {l}")
        for f, p in indexable.items():
            if "noindex" in p.metas.get("robots", ""): continue  # sample pages kept out of the sitemap
            if f"{URL}/{f}" not in locs: add(f"sitemap: missing {f}")
    rb = open(os.path.join(ROOT, "robots.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(ROOT, "robots.txt")) else ""
    if f"Sitemap: {URL}/sitemap.xml" not in rb: add("robots.txt: no Sitemap line")

    # repo hygiene: no email addresses in any text file
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in {".git", "node_modules", "photos", "fonts"} and not x.startswith("~")]
        for fn in files:
            if fn.endswith((".html", ".js", ".css", ".xml", ".txt", ".md", ".json", ".py", ".yml")):
                t = open(os.path.join(d, fn), encoding="utf-8", errors="ignore").read()
                if re.search(r"[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail)\.com", t):
                    add(f"{os.path.relpath(os.path.join(d, fn), ROOT)}: contains a personal email address")

    print(f"pages checked: {len(indexable)} (+404)")
    print(f"problems: {len(problems)}")
    for x in problems: print(" -", x)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

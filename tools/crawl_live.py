"""Crawl the LIVE site: every sitemap URL, every internal link, image, stylesheet, script and font.
Exit code 1 on any failure.   python tools/crawl_live.py [base_url]
"""
import os, re, sys, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C

BASE = (sys.argv[1] if len(sys.argv) > 1 else C.SITE["url"]).rstrip("/")
UA = {"User-Agent": "wolfs-site-check/1.0"}


def fetch(url, method="GET"):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA, method=method), timeout=30)
        return r.status, r.read() if method == "GET" else b"", r.headers
    except urllib.error.HTTPError as ex:
        return ex.code, b"", ex.headers
    except Exception as ex:
        return 0, str(ex).encode(), {}


class L(HTMLParser):
    def __init__(s):
        super().__init__(); s.urls, s.canon, s.ids = [], None, set()
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if tag == "a" and a.get("href"): s.urls.append(("a", a["href"]))
        if tag in ("img", "script", "source") and a.get("src"): s.urls.append(("asset", a["src"]))
        for key in ("srcset",):
            if a.get(key):
                for part in a[key].split(","):
                    s.urls.append(("asset", part.strip().split(" ")[0]))
        if tag == "link" and a.get("href"):
            if a.get("rel") == "canonical": s.canon = a["href"]
            elif a.get("rel") in ("stylesheet", "preload"): s.urls.append(("asset", a["href"]))


def main():
    problems, seen_pages, checked = [], {}, {}
    st, body, _ = fetch(BASE + "/sitemap.xml")
    if st != 200: problems.append(f"sitemap.xml -> {st}")
    pages = re.findall(r"<loc>(.*?)</loc>", body.decode("utf-8", "ignore"))
    for u in (BASE + "/robots.txt", BASE + "/llms.txt", BASE + "/og-image.jpg", BASE + "/nonexistent-page-check"):
        s, _, _ = fetch(u)
        if u.endswith("nonexistent-page-check"):
            if s != 404: problems.append(f"missing page should 404, got {s}")
        elif s != 200: problems.append(f"{u} -> {s}")
    for u in pages:
        s, b, h = fetch(u)
        if s != 200: problems.append(f"{u} -> {s}"); continue
        p = L(); p.feed(b.decode("utf-8", "ignore")); seen_pages[u] = p
        if p.canon != u: problems.append(f"{u}: canonical {p.canon}")
    for u, p in seen_pages.items():
        for kind, ref in p.urls:
            if ref.startswith(("tel:", "sms:", "mailto:", "data:")): continue
            full = urljoin(u, ref)
            nf, frag = urldefrag(full)
            if urlparse(nf).netloc != urlparse(BASE).netloc:
                if nf not in checked:
                    s, _, _ = fetch(nf, "HEAD")
                    if s in (405, 403, 400): s, _, _ = fetch(nf)
                    checked[nf] = s
                if checked[nf] not in (200, 301, 302, 303): problems.append(f"{u}: external {nf} -> {checked[nf]}")
                continue
            if nf not in checked:
                s, b2, _ = fetch(nf)
                checked[nf] = s
                if s == 200 and nf in seen_pages: pass
            if checked[nf] != 200: problems.append(f"{u}: {kind} {ref} -> {checked[nf]}")
            elif frag and nf in seen_pages and frag not in seen_pages[nf].ids: problems.append(f"{u}: missing anchor #{frag} in {nf}")
    print(f"live crawl of {BASE}: {len(pages)} sitemap pages, {len(checked)} unique URLs checked")
    print(f"problems: {len(problems)}")
    for x in problems: print(" -", x)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

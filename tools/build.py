"""Static site generator for Wolf's Landscaping Services (English + Spanish).
Run from anywhere:  python tools/build.py
Edit copy in tools/content.py, styles in styles.css, behavior in script.js.
"""
import urllib.parse
import os, re, json, hashlib, html, datetime
import content as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = C.SITE
URL = SITE["url"]
e = html.escape
TODAY = datetime.date.today().isoformat()
SLUGS = [s["slug"] for s in C.SERVICES]
SVC = {s["slug"]: s for s in C.SERVICES}
LANGS = ("en", "es")
LOCALE = {"en": "en_US", "es": "es_US"}


def h8(name):
    return hashlib.md5(open(os.path.join(ROOT, name), "rb").read()).hexdigest()[:8]


VER = {"css": h8("styles.css"), "js": h8("script.js")}


def fname(key):
    return "index.html" if key == "index" else key + ".html"


def prefix(lang):
    return "es/" if lang == "es" else ""


def asset(lang):
    return "../" if lang == "es" else ""


def g_icon(lang, cls="g-logo", size=24, alt=""):
    """Official Google 'G' (unaltered file from Google). Decorative by default (alt empty) when text next to it names Google."""
    return f'<img class="{cls}" src="{asset(lang)}brand/google-g.png" alt="{e(alt)}" width="{size}" height="{size}" decoding="async">'


# Material "call" handset icon (Apache 2.0)
PHONE_ICON = ('<svg class="ico-phone" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">'
              '<path fill="currentColor" d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.61 21 3 13.39 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1.02l-2.2 2.2z"/></svg>')


def rating_link(lang):
    """Stars + rating + 'Reviews from Google (N)' as a single link to the on-site Reviews page."""
    ui = C.UI[lang]
    return (f'<a class="rating-link" href="reviews.html" title="{e(ui["see_all"])}">{g_icon(lang, "g-logo", 24)}'
            f'<span class="stars" aria-hidden="true">★★★★★</span> <strong aria-hidden="true">{C.REVIEWS_META["rating"]}</strong>'
            f'<span class="sr-only">{e(ui["rating_sr"])}.</span> <span class="google-label">{e(ui["google_label"])} ({C.REVIEWS_META["count"]})</span>'
            f'<span class="sr-only"> &mdash; {e(ui["see_all"])}</span></a>')


def pub_url(lang, key):
    return f"{URL}/{prefix(lang)}{fname(key)}"


def other(lang):
    return "es" if lang == "en" else "en"


def md(text):
    """escape, then turn [label](page-key) into links"""
    t = e(text)
    return re.sub(r"\[(.+?)\]\(([a-z\-]+)\)", lambda m: f'<a href="{fname(m.group(2))}">{m.group(1)}</a>', t)


def write(lang, key, text):
    d = os.path.join(ROOT, prefix(lang).rstrip("/"))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, fname(key)), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ------------------------------------------------------------------ shared pieces
NOINDEX = set()


def head(lang, key, title, desc, schema=None):
    ui = C.UI[lang]
    a = asset(lang)
    full_title = f"{title} | {SITE['name']}"
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{pub_url(l, key)}">' for l in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{pub_url("en", key)}">'
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if key in NOINDEX else ""}
<meta name="theme-color" content="#1f3f28">
<link rel="canonical" href="{pub_url(lang, key)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(SITE['name'])}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{pub_url(lang, key)}">
<meta property="og:image" content="{URL}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(SITE['name'])}, {e(ui['footer_area'])}">
<meta property="og:locale" content="{LOCALE[lang]}">
<meta property="og:locale:alternate" content="{LOCALE[other(lang)]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(full_title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{URL}/og-image.jpg">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%232f5d3a'/%3E%3Cpath d='M16 6c4 4 7 8 7 12a7 7 0 0 1-14 0c0-4 3-8 7-12z' fill='%23f4efe4'/%3E%3C/svg%3E">
<link rel="preload" href="{a}fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{a}fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{a}styles.css?v={VER['css']}">
{ld}
</head>"""


def header(lang, key):
    ui = C.UI[lang]
    a = asset(lang)
    items = "".join(f'<li><a href="{s}.html">{e(SVC[s][lang]["name"])}</a></li>' for s in SLUGS)
    cur = lambda k: ' aria-current="page"' if key == k else ""
    other_href = (("../" if lang == "es" else "es/") + fname(key))
    return f"""<body>
<a class="skip" href="#top">{e(ui['skip'])}</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="index.html" aria-label="{e(SITE['name'])}">
      <svg viewBox="0 0 32 32" width="34" height="34" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#2f5d3a"/><path d="M16 6c4 4 7 8 7 12a7 7 0 0 1-14 0c0-4 3-8 7-12z" fill="#f4efe4"/></svg>
      <span>Wolf's <em>Landscaping</em></span>
    </a>
    <nav id="nav" aria-label="Main">
      <a href="index.html"{cur('index')}>{e(ui['nav_home'])}</a>
      <div class="dd"><a href="index.html#services">{e(ui['nav_services'])}</a><button class="dd-toggle" type="button" aria-expanded="false" aria-label="{e(ui['services_menu'])}"></button><ul class="dd-list">{items}</ul></div>
      <a href="about.html"{cur('about')}>{e(ui['nav_about'])}</a>
      <a href="gallery.html"{cur('gallery')}>{e(ui['nav_gallery'])}</a>
      <a href="reviews.html"{cur('reviews')}>{e(ui['nav_reviews'])}</a>
      <a href="faq.html"{cur('faq')}>{e(ui['nav_faq'])}</a>
      <a href="contact.html"{cur('contact')}>{e(ui['nav_contact'])}</a>
      <a href="join-the-team.html"{cur('join-the-team')}>{e(ui['nav_join'])}</a>
      <a class="btn btn-small" href="contact.html#estimate">{e(ui['nav_estimate'])}</a>
      <a class="lang lang-nav" href="{other_href}" hreflang="{other(lang)}" lang="{other(lang)}" title="{e(ui['switch_title'])}">{e(ui['switch_label'])}</a>
    </nav>
    <a class="call" href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a>
    <a class="lang lang-bar" href="{other_href}" hreflang="{other(lang)}" lang="{other(lang)}" title="{e(ui['switch_title'])}" aria-label="{e(ui['switch_label'])}">{e(ui['switch_short'])}</a>
    <button class="menu" type="button" aria-label="{e(ui['menu'])}" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  </div>
</header>"""


def addr_html(sep="<br>"):
    return f'{e(SITE["street"])}{sep}{e(SITE["city"])}, {e(SITE["state"])} {e(SITE["zip"])}'


def footer(lang):
    ui = C.UI[lang]
    a = asset(lang)
    other_home = ("../" if lang == "es" else "es/") + "index.html"
    return f"""<footer class="site-footer">
  <div class="wrap foot">
    <div><strong>{e(SITE['name'])}</strong><br>{e(ui['footer_area'])}</div>
    <div><address>{addr_html()}<br><a href="{SITE['maps_url']}" target="_blank" rel="noopener">{e(C.PAGES[lang]['view_map'])}</a></address></div>
    <div><a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></div>
    <div><a href="privacy.html">{e(ui['privacy'])}</a> &middot; <a href="join-the-team.html">{e(ui['join_link'])}</a> &middot; <a href="{other_home}" hreflang="{other(lang)}" lang="{other(lang)}">{e(ui['switch_label'])}</a> &middot; &copy; <span id="year"></span> {e(SITE['name'])}</div>
  </div>
  <a class="sticky-call" href="tel:{SITE['phone_tel']}">{e(ui['sticky_call'])}</a>
  <button class="to-top" type="button" aria-label="{e(ui['back_top'])}" hidden>&uarr;</button>
</footer>
<script src="{a}script.js?v={VER['js']}"></script>
</body>
</html>
"""


def crumbs(lang, trail):
    ui = C.UI[lang]
    parts = [f'<a href="index.html">{e(ui["crumb_home"])}</a>']
    for label, href in trail[:-1]:
        parts.append(f'<a href="{href}">{e(label)}</a>')
    parts.append(f'<span aria-current="page">{e(trail[-1][0])}</span>')
    return f'<nav class="crumbs" aria-label="{e(ui["crumb_label"])}">' + " / ".join(parts) + "</nav>"


def crumb_ld(lang, key, trail):
    items = [(C.UI[lang]["crumb_home"], pub_url(lang, "index"))]
    for label, href in trail[:-1]:
        items.append((label, f"{URL}/{prefix(lang)}{href}"))
    items.append((trail[-1][0], pub_url(lang, key)))
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def business_ld():
    return {
        "@type": "LandscapingBusiness", "@id": f"{URL}/#business", "name": SITE["name"], "url": URL + "/",
        "telephone": SITE["phone_tel"], "image": f"{URL}/og-image.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": SITE["street"], "addressLocality": SITE["city"], "addressRegion": SITE["state"], "postalCode": SITE["zip"], "addressCountry": "US"},
        "hasMap": SITE["maps_url"], "founder": {"@type": "Person", "name": C.OWNER["name"], "jobTitle": "Owner"},
        "description": "Owner-operated lawn care, landscape design, hardscaping and retaining walls in Royersford and Chester County, PA.",
        "areaServed": [{"@type": "City", "name": "Royersford", "address": {"@type": "PostalAddress", "addressRegion": "PA", "addressCountry": "US"}},
                       {"@type": "AdministrativeArea", "name": "Chester County, PA"}],
    }


def website_ld():
    return {"@type": "WebSite", "@id": f"{URL}/#website", "name": SITE["name"], "url": URL + "/", "inLanguage": ["en-US", "es-US"], "publisher": {"@id": f"{URL}/#business"}}


def hero(lang, trail, h1, lead, show_cta=True):
    ui = C.UI[lang]
    cta = f'<div class="cta-row"><a class="btn" href="contact.html#estimate">{e(ui["cta_btn"])}</a></div>' if show_cta else ""
    lead_html = f'<p class="lead">{e(lead)}</p>' if lead else ""
    return f"""<section class="hero page-hero"><div class="wrap hero-inner">
{crumbs(lang, trail)}
<h1>{e(h1)}</h1>
{lead_html}
{cta}
</div></section>"""


def picture(lang, key, which, alt, lazy=True):
    a = asset(lang)
    base = f"{a}photos/{key}-{which}"
    ws = ", ".join(f"{base}-{w}.webp {w}w" for w in (480, 800, 1168))
    js = f"{base}-480.jpg 480w, {base}-800.jpg 800w, {base}.jpg 1168w"
    ld = ' loading="lazy"' if lazy else ""
    return (f'<picture class="ba-{which}"><source type="image/webp" srcset="{ws}" sizes="(max-width: 700px) 92vw, 560px">'
            f'<img src="{base}-800.jpg" srcset="{js}" sizes="(max-width: 700px) 92vw, 560px" alt="{e(alt)}" width="1168" height="880"{ld} decoding="async"></picture>')


def slider(lang, sh):
    ui = C.UI[lang]
    t = sh[lang]
    # DOM order: after underneath, before on top (clipped)
    return f"""<figure class="ba">
  <div class="ba-box" style="--pos:50%">
    {picture(lang, sh['key'], 'after', f"{ui['after']}: {t['after']}")}
    {picture(lang, sh['key'], 'before', f"{ui['before']}: {t['before']}")}
    <span class="ba-tag ba-tag-b">{e(ui['before'])}</span><span class="ba-tag ba-tag-a">{e(ui['after'])}</span>
    <span class="ba-line" aria-hidden="true"></span>
    <input class="ba-range" type="range" min="0" max="100" value="50" aria-label="{e(ui['before'])} / {e(ui['after'])}: {e(t['title'])}">
  </div>
  <figcaption><strong>{e(t['title'])}</strong> <br><a href="{sh['link']}.html">{e(ui['about'])} {e(t['linkname'])} &rarr;</a></figcaption>
</figure>"""


def form(lang):
    f = C.PAGES[lang]["form"]
    ui = C.UI[lang]
    opts = "".join(f"<option>{e(s)}</option>" for s in f["services"])
    prefs = "".join(f"<option>{e(s)}</option>" for s in f["prefs"])
    i18n = {"hi": f["hi"], "lbl": f["lbl"], "copied": f["copied"], "copyfail": f["copyfail"], "tel": SITE["phone_tel"], "display": SITE["phone_display"]}
    return f"""<form id="estimate-form" aria-describedby="form-help">
  <label>{e(f['name'])}<input type="text" name="name" required autocomplete="name"></label>
  <div class="row">
    <label>{e(f['phone'])}<input name="phone" type="tel" required autocomplete="tel"></label>
    <label>{e(f['email'])}<input name="email" type="email" autocomplete="email"></label>
  </div>
  <label>{e(f['address'])}<input type="text" name="address" required autocomplete="address-level2"></label>
  <label>{e(f['service'])}
    <select name="service" required><option value="">{e(f['choose'])}</option>{opts}</select>
  </label>
  <label>{e(f['message'])}<textarea name="message" rows="4"></textarea></label>
  <label>{e(f['pref'])}<select name="contact_pref">{prefs}</select></label>
  <button class="btn" type="submit">{e(f['submit'])}</button>
  <p id="form-help" class="form-help">{e(f['help'])}</p>
  <div id="form-result" class="form-result" role="status" aria-live="polite" hidden>
    <p><strong>{e(f['ready'])}</strong> {e(f['choose_how'])}</p>
    <div class="result-actions">
      <a class="btn" id="open-sms" href="#">{e(f['text_btn'])}</a>
      <button class="btn btn-ghost dark" id="copy-msg" type="button">{e(f['copy_btn'])}</button>
      <a class="btn btn-ghost dark" href="tel:{SITE['phone_tel']}">{e(f['call_btn'])}</a>
    </div>
    <p class="form-help">{e(f['note'])}</p>
    <p id="copy-status" class="form-status"></p>
  </div>
  <script type="application/json" id="form-i18n">{json.dumps(i18n, ensure_ascii=False)}</script>
</form>"""


def faq_html(items):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{md(a)}</p></details>" for q, a in items) + "</div>"


def page(lang, key, title, desc, body, schema_graph=None):
    schema = {"@context": "https://schema.org", "@graph": schema_graph} if schema_graph else None
    write(lang, key, head(lang, key, title, desc, schema) + "\n" + header(lang, key) + f'\n<main id="top">\n{body}\n</main>\n' + footer(lang))


# ------------------------------------------------------------------ pages
def build_lang(lang):
    ui = C.UI[lang]
    P = C.PAGES[lang]

    # ---- home
    cards = "".join(
        f'<article class="card"><h3><a href="{k}.html">{e(n)}</a></h3><p>{e(d)}</p><ul>' + "".join(f"<li>{e(i)}</li>" for i in items) + f'</ul><p class="more"><a href="{k}.html">{e(ui["about"])} {e(n.lower())} &rarr;</a></p></article>'
        for k, n, d, items in P["cards"])
    proof = "".join(f"<li><strong>{e(a)}</strong> {e(b)}</li>" for a, b in P["proof"])
    trust = "".join(f"<span>{e(t)}</span>" for t in P["trust"])
    steps = "".join(f'<li><span>{i + 1}</span><h3>{e(h)}</h3><p>{e(t)}</p></li>' for i, (h, t) in enumerate(P["steps"]))
    def cite_of(r):
        who = e(r["reviewer"] or ui["anon_reviewer"])
        svc = (r.get("service") or {}).get(lang)
        return g_icon(lang, "g-mini", 16) + who + (f" &middot; {e(svc)}" if svc else "")
    quotes = "".join(f'<blockquote><p>“{e(r.get("excerpt") or r["text"])}”</p><cite>{cite_of(r)}</cite></blockquote>' for r in C.FEATURED)
    orig = f'<p class="sub">{e(ui["reviews_orig"])}</p>' if ui["reviews_orig"] else ""
    towns = "".join(f"<li>{e(t)}</li>" for t in C.TOWNS)
    why = "".join(f"<li>{e(w)}</li>" for w in P["why"])
    SHOT = {s["key"]: s for s in C.SHOTS}
    home_shots = "".join(slider(lang, SHOT[k]) for k in ("patio", "lighting", "lawn", "walkway"))
    home = f"""<section class="hero">
  <div class="wrap hero-inner">
    <p class="eyebrow">{e(P['eyebrow'])}</p>
    <h1>{e(P['h1'])}</h1>
    <p class="lead">{e(P['lead'])}</p>
    <p class="hero-rating">{rating_link(lang)}</p>
    <div class="cta-row">
      <a class="btn" href="contact.html#estimate">{e(ui['cta_btn'])}</a>
      <a class="btn btn-ghost btn-call" href="tel:{SITE['phone_tel']}" aria-label="{e(ui['call'])} {SITE['phone_display']}">{PHONE_ICON}<span class="call-text">{e(ui['call'])} {SITE['phone_display']}</span></a>
    </div>
    <p class="hero-review-cta"><a class="btn btn-small" href="{C.SITE['google_write_review_url']}" target="_blank" rel="noopener">{g_icon(lang, "g-mini", 18)}{e(ui['write_btn'])}</a></p>
    <ul class="proof">{proof}</ul>
  </div>
</section>
<section class="trust-strip" aria-label="{e(ui['nav_reviews'])}"><div class="wrap">{trust}</div></section>
<section id="services" class="section"><div class="wrap">
  <h2>{e(P['services_h'])}</h2><p class="sub">{e(P['services_sub'])}</p>
  <div class="grid cards">{cards}</div>
</div></section>
<section id="work" class="section alt"><div class="wrap">
  <h2>{e(P['work_h'])}</h2>
  <p class="sub">{e(ui['slider_hint'])}</p>
  <div class="ba-grid">{home_shots}</div>
  <p class="center"><a class="btn btn-ghost dark" href="gallery.html">{e(ui['see_more_ba'])}</a></p>
</div></section>
<section id="process" class="section"><div class="wrap">
  <h2>{e(P['process_h'])}</h2>
  <ol class="steps">{steps}</ol>
</div></section>
<section id="reviews" class="section alt"><div class="wrap">
  <h2>{e(P['reviews_h'])}</h2>
  <p class="sub reviews-head">{rating_link(lang)}</p>
  {orig}
  <div class="grid quotes">{quotes}</div>
  <p class="center btn-row"><a class="btn" href="{C.SITE['google_write_review_url']}" target="_blank" rel="noopener">{g_icon(lang, "g-mini", 18)}{e(ui['write_btn'])}</a></p>
</div></section>
<section id="areas" class="section"><div class="wrap two">
  <div><h2>{e(P['area_h'])}</h2><p>{e(P['area_p'])}</p><ul class="towns">{towns}</ul></div>
  <div class="callout"><h3>{e(P['why_h'])}</h3><ul class="checks">{why}</ul></div>
</div></section>
<section class="section cta-band"><div class="wrap center">
  <h2>{e(ui['cta_title'])}</h2><p>{e(ui['cta_text'])}</p>
  <p class="cta-row center-row"><a class="btn" href="contact.html#estimate">{e(ui['cta_btn'])}</a></p>
</div></section>"""
    page(lang, "index", P["home_title"], P["home_desc"], home, [business_ld(), website_ld()])

    # ---- service pages
    for s in C.SERVICES:
        d = s[lang]
        key = s["slug"]
        trail = [(ui["nav_services"], "index.html#services"), (d["name"], fname(key))]
        inc = "".join(f"<li>{e(i)}</li>" for i in d["includes"])
        how = "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(t)}</p></div>' for h, t in d["how"])
        rel = "".join(f'<a class="rel" href="{r}.html">{e(SVC[r][lang]["name"])}</a>' for s2 in [s] for r in s2["related"])
        extra = ""
        for i, (h, paras, bullets, closing) in enumerate(d.get("extra", [])):
            ul = f'<ul class="checks cols">{"".join(f"<li>{e(x)}</li>" for x in bullets)}</ul>' if bullets else ""
            tail = f"<p>{e(closing)}</p>" if closing else ""
            cls = "section alt" if i % 2 == 0 else "section"
            extra += f'<section class="{cls}"><div class="wrap narrow prose"><h2>{e(h)}</h2>{"".join(f"<p>{e(p)}</p>" for p in paras)}{ul}{tail}</div></section>'
        after = ""
        if d.get("aftercare"):
            cards = "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(t)}</p></div>' for h, t in d["aftercare"])
            after = f'<section class="section"><div class="wrap"><div class="grid cards">{cards}</div></div></section>'
        body = f"""{hero(lang, trail, d['name'], d['tag'])}
<section class="section"><div class="wrap two">
  <div class="prose">{''.join(f'<p>{e(p)}</p>' for p in d['intro'])}</div>
  <div class="callout"><h2 class="h3">{e(ui['included'])}</h2><ul class="checks">{inc}</ul></div>
</div></section>
{extra}{after}<section class="section alt"><div class="wrap"><h2>{e(ui['how_we_work'])}</h2><div class="grid cards">{how}</div></div></section>
<section class="section"><div class="wrap narrow"><h2>{e(ui['common_q'])}</h2>{faq_html(d['faq'])}
<p class="more"><a href="faq.html">{e(ui['more_q'])} &rarr;</a></p></div></section>
<section class="section cta-band"><div class="wrap center"><h2>{e(ui['cta_title'])}</h2><p>{e(ui['cta_text'])}</p>
<p class="cta-row center-row"><a class="btn" href="contact.html#estimate">{e(ui['cta_btn'])}</a></p></div></section>
<section class="section alt"><div class="wrap"><h2 class="h3">{e(ui['related'])}</h2><div class="rels">{rel}</div></div></section>"""
        graph = [
            {"@type": "Service", "name": d["name"], "description": d["desc"], "inLanguage": lang, "provider": {"@id": f"{URL}/#business"},
             "areaServed": [{"@type": "City", "name": "Royersford"}, {"@type": "AdministrativeArea", "name": "Chester County, PA"}]},
            crumb_ld(lang, key, trail),
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\[(.+?)\]\(([a-z\-]+)\)", r"\1", a)}} for q, a in d["faq"]]},
        ]
        page(lang, key, d["title"], d["desc"], body, graph)

    # ---- reviews
    trail = [(ui["nav_reviews"], "reviews.html")]
    def review_card(r):
        who = e(r["reviewer"] or ui["anon_reviewer"])
        link = (f' <a class="review-link" href="{e(r["url"])}" target="_blank" rel="noopener">{e(ui["view_on_google"])} &rarr;</a>' if r.get("url") else "")
        return (f'<article class="review"><header>{g_icon(lang, "g-mini", 18)}<strong>{who}</strong>'
                f'<span class="stars" aria-hidden="true">{"★" * int(r["stars"])}</span><span class="sr-only">{r["stars"]} / 5</span>'
                + (f'<span class="when">{e(r["when"])}</span>' if r.get("when") else "")
                + "</header>" + (f'<p>{e(r["text"])}</p>' if r.get("text") else "") + f'{link}</article>')
    n_listed, total = len(C.ALL_REVIEWS), int(C.REVIEWS_META["count"])
    partial = (f'<p class="notice">{e(P["reviews_partial"].format(n=n_listed, total=total))} '
               f'<a href="{C.SITE["google_reviews_url"]}" target="_blank" rel="noopener">{e(ui["google_btn"])}</a></p>') if n_listed < total else ""
    body = f"""{hero(lang, trail, P['rpage_h'], P['reviews_lead'], show_cta=False)}
<section class="section"><div class="wrap">
<p class="sub google-line">{g_icon(lang, "g-logo", 24)}<span class="stars" aria-hidden="true">★★★★★</span> <strong>{C.REVIEWS_META["rating"]}</strong> <span class="sr-only">{e(ui['rating_sr'])}</span> <span class="google-label">{e(ui['google_label'])} ({total})</span></p>
<p class="btn-row left"><a class="btn" href="{C.SITE['google_write_review_url']}" target="_blank" rel="noopener">{g_icon(lang, "g-mini", 18)}{e(ui['write_btn'])}</a> <a class="btn btn-ghost dark" href="{C.SITE['google_reviews_url']}" target="_blank" rel="noopener">{g_icon(lang, "g-mini", 18)}{e(ui['google_btn'])}</a></p>
{partial}
<div class="reviews-grid">{"".join(review_card(r) for r in C.ALL_REVIEWS)}</div>
<p class="sub review-note">{e(P['reviews_note'])}</p>
</div></section>"""
    page(lang, "reviews", P["reviews_title"], P["reviews_desc"], body, [crumb_ld(lang, "reviews", trail)])

    # ---- about
    trail = [(ui["nav_about"], "about.html")]
    who = "".join(f"<p>{e(p)}</p>" for p in P["about_who"])
    values = "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(t)}</p></div>' for h, t in P["about_values"])
    quotes = "".join(f'<blockquote><p>“{e(q)}”</p><cite>{g_icon(lang, "g-mini", 16)}{e(n)}</cite></blockquote>' for q, n in P["about_quotes"])
    owner_html = ""
    if C.OWNER["name"]:
        role = f' <span class="role">&middot; {e(C.OWNER["role"][lang])}</span>' if C.OWNER.get("role") else ""
        owner_html += f'<section class="section"><div class="wrap narrow prose"><h2>{e(P["about_owner_h"])}</h2><p class="owner-name"><strong>{e(C.OWNER["name"])}</strong>{role}</p></div></section>'
    if C.OWNER["story"][lang]:
        owner_html += f'<section class="section alt"><div class="wrap narrow prose"><h2>{e(P["about_story_h"])}</h2>' + "".join(f"<p>{e(p)}</p>" for p in C.OWNER["story"][lang]) + "</div></section>"
    if C.OWNER["credentials"][lang]:
        owner_html += f'<section class="section"><div class="wrap narrow"><h2>{e(P["about_creds_h"])}</h2><ul class="checks">' + "".join(f"<li>{e(c)}</li>" for c in C.OWNER["credentials"][lang]) + "</ul></div></section>"
    body = f"""{hero(lang, trail, P['about_h'], P['about_lead'])}
<section class="section"><div class="wrap narrow prose"><h2>{e(P['about_who_h'])}</h2>{who}</div></section>
{owner_html}
<section class="section alt"><div class="wrap"><h2>{e(P['about_work_h'])}</h2><div class="grid cards cards-4">{values}</div></div></section>
<section class="section"><div class="wrap"><h2>{e(P['about_say_h'])}</h2><p class="sub google-line">{g_icon(lang, "g-logo", 24)}{e(ui['google_label'])}</p><div class="grid quotes">{quotes}</div>
<p class="center"><a class="btn btn-ghost dark" href="index.html#reviews">{e(ui['nav_reviews'])} &rarr;</a></p></div></section>
<section class="section cta-band"><div class="wrap center"><h2>{e(ui['cta_title'])}</h2><p>{e(ui['cta_text'])}</p>
<p class="cta-row center-row"><a class="btn" href="contact.html#estimate">{e(ui['cta_btn'])}</a></p></div></section>"""
    page(lang, "about", P["about_title"], P["about_desc"], body, [{"@type": "AboutPage", "name": P["about_h"], "inLanguage": lang, "about": {"@id": f"{URL}/#business"}}, crumb_ld(lang, "about", trail)])

    # ---- gallery
    trail = [(P["gallery_h"], "gallery.html")]
    shots = "".join(slider(lang, s) for s in C.SHOTS)
    body = f"""{hero(lang, trail, P['gallery_h'], ui['slider_hint'], show_cta=False)}
<section class="section"><div class="wrap">
<div class="ba-grid">{shots}</div>
<p class="more">{e(ui['gallery_cta'])} <a href="contact.html#estimate">{e(ui['cta_btn'])}</a> &middot; <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p>
</div></section>"""
    page(lang, "gallery", P["gallery_title"], P["gallery_desc"], body, [crumb_ld(lang, "gallery", trail)])

    # ---- faq
    trail = [(P["faq_h"], "faq.html")]
    groups = "".join(f"<h2>{e(g)}</h2>{faq_html(qs)}" for g, qs in C.FAQ_GEN[lang])
    body = f"""{hero(lang, trail, P['faq_h'], "", show_cta=False)}
<section class="section"><div class="wrap narrow">{groups}
<p class="more">{e(P['faq_foot'])} <a href="contact.html#estimate">{e(P['faq_foot_link'])}</a> &middot; <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p></div></section>"""
    qa = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\[(.+?)\]\(([a-z\-]+)\)", r"\1", a)}} for _, qs in C.FAQ_GEN[lang] for q, a in qs]
    page(lang, "faq", P["faq_title"], P["faq_desc"], body, [{"@type": "FAQPage", "mainEntity": qa}, crumb_ld(lang, "faq", trail)])

    # ---- contact
    trail = [(ui["nav_contact"], "contact.html")]
    body = f"""{hero(lang, trail, P['contact_h'], P['contact_lead'], show_cta=False)}
<section class="section"><div class="wrap two">
  <div class="quote-copy">
    <p class="phone">{e(P['contact_call'])} <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a></p>
    <p>{e(P['contact_miss'])}</p>
    <h2 class="h3">{e(P['visit_h'])}</h2>
    <address class="visit"><strong>{e(SITE['name'])}</strong><br>{addr_html()}</address>
    <p class="visit-links"><a class="btn btn-small" href="{SITE['directions_url']}" target="_blank" rel="noopener">{e(P['directions'])}</a> <a class="btn btn-ghost btn-small dark" href="{SITE['maps_url']}" target="_blank" rel="noopener">{g_icon(lang, "g-mini", 18)}{e(P['view_map'])}</a></p>
    <h2 class="h3">{e(P['area_h'])}</h2>
    <p>{e(P['area_p'])}</p>
    <ul class="towns">{towns}</ul>
  </div>
  <div id="estimate">{form(lang)}</div>
</div></section>"""
    page(lang, "contact", P["contact_title"], P["contact_desc"], body, [crumb_ld(lang, "contact", trail)])

    # ---- privacy
    trail = [(ui["privacy"], "privacy.html")]
    parts = "".join(f"<{t}>{e(x)}</{t}>" for t, x in P["privacy"])
    body = f"""{hero(lang, trail, P['privacy_h'], "", show_cta=False)}
<section class="section"><div class="wrap narrow prose"><p class="notice">{e(P['privacy_draft'])}</p>{parts}</div></section>"""
    page(lang, "privacy", P["privacy_title"], P["privacy_desc"], body, [crumb_ld(lang, "privacy", trail)])

    # ---- join the team
    trail = [(P["join_h"], "join-the-team.html")]
    a = asset(lang)
    def jpic(name, alt, w, h, sizes, lazy=True):
        base = f"{a}photos/{name}"
        ld = ' loading="lazy"' if lazy else ""
        return (f'<picture><source type="image/webp" srcset="{base}-480.webp 480w, {base}-800.webp 800w, {base}-1200.webp 1200w" sizes="{sizes}">'
                f'<img src="{base}-800.jpg" alt="{e(alt)}" width="{w}" height="{h}"{ld} decoding="async"></picture>') if name == "join-poster" else (
                f'<picture><source type="image/webp" srcset="{base}-320.webp 320w, {base}-640.webp 640w" sizes="{sizes}">'
                f'<img src="{base}-640.jpg" alt="{e(alt)}" width="{w}" height="{h}"{ld} decoding="async"></picture>')
    roles = "".join(
        f'<a class="join-card" href="{svc}.html">{jpic("join-" + img, alt, 685, 940, "(max-width: 640px) 44vw, 260px")}'
        f'<span class="join-card-text"><strong>{e(name)}</strong> {e(txt)}</span></a>'
        for name, txt, svc, img, alt in P["join_roles"])
    look = "".join(f"<li>{e(x)}</li>" for x in P["join_look"])
    sms_body = urllib.parse.quote(P["join_sms_body"], safe="")
    intro = "".join(f"<p>{e(x)}</p>" for x in P["join_intro"])
    body = f"""{hero(lang, trail, P['join_h'], P['join_lead'], show_cta=False)}
<section class="section"><div class="wrap two join-top">
  <div class="join-poster">{jpic("join-poster", P["join_poster_alt"], 1496, 1735, "(max-width: 900px) 92vw, 480px", lazy=False)}</div>
  <div class="prose">{intro}
    <h2 class="h3">{e(P['join_look_h'])}</h2><ul class="checks">{look}</ul>
    <h2 class="h3">{e(P['join_apply_h'])}</h2><p>{e(P['join_apply_p'])}</p>
    <p class="btn-row left"><a class="btn" href="sms:{SITE['phone_tel']}?&amp;body={sms_body}">{e(P['join_sms'])} {SITE['phone_display']}</a> <a class="btn btn-ghost dark" href="tel:{SITE['phone_tel']}">{e(P['join_call'])} {SITE['phone_display']}</a></p>
  </div>
</div></section>
<section class="section alt"><div class="wrap"><h2>{e(P['join_roles_h'])}</h2><div class="join-grid">{roles}</div>
<p class="more">{e(P['join_note'])} <a href="contact.html#estimate">{e(ui['cta_btn'])}</a></p></div></section>"""
    page(lang, "join-the-team", P["join_title"], P["join_desc"], body, [crumb_ld(lang, "join-the-team", trail)])


for lg in LANGS:
    build_lang(lg)

# ------------------------------------------------------------------ crawl files
KEYS = ["index"] + SLUGS + ["about", "reviews", "gallery", "faq", "contact", "join-the-team", "privacy"]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for lg in LANGS:
    for k in KEYS:
        sm.append("<url>")
        sm.append(f"<loc>{pub_url(lg, k)}</loc>")
        sm.append(f"<lastmod>{TODAY}</lastmod>")
        for l2 in LANGS:
            sm.append(f'<xhtml:link rel="alternate" hreflang="{l2}" href="{pub_url(l2, k)}"/>')
        sm.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{pub_url("en", k)}"/>')
        sm.append("</url>")
sm.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write("\n".join(sm) + "\n")

robots = f"""User-agent: *
Allow: /

# Search and answer-engine crawlers are welcome
User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {URL}/sitemap.xml
"""
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(robots)

llms = f"""# {SITE['name']}

> Owner-operated landscaping company serving Royersford and Chester County, Pennsylvania. Lawn care, landscape design, hardscaping, retaining walls, drainage and grading, aeration, sod and seeding, seasonal cleanup, tree work and snow removal. Free estimates. Phone: {SITE['phone_display']}.

## Pages
""" + "\n".join(f"- [{SVC[s]['en']['name']}]({URL}/{s}.html): {SVC[s]['en']['desc']}" for s in SLUGS) + f"""
- [About]({URL}/about.html)
- [Customer reviews]({URL}/reviews.html): reviews from the Google listing
- [FAQ]({URL}/faq.html)
- [Contact and free estimate]({URL}/contact.html)
- [Join the team]({URL}/join-the-team.html): work with the crew
- [Gallery]({URL}/gallery.html): before and after comparisons for retaining walls, walkways, patios, driveways, garden beds and lawns
- [Español]({URL}/es/index.html): Spanish version of this site
"""
open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8", newline="\n").write(llms)

not_found = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<base href="{URL}/"><meta name="robots" content="noindex">
<title>Page not found | {e(SITE['name'])}</title>
<link rel="stylesheet" href="styles.css?v={VER['css']}"></head>
<body><main id="top"><section class="section"><div class="wrap narrow center">
<h1>Page not found</h1><p>That page doesn't exist. Try the <a href="index.html">home page</a>, our <a href="contact.html">contact page</a>, or call <a href="tel:{SITE['phone_tel']}">{SITE['phone_display']}</a>.</p>
<p><a href="es/index.html" lang="es" hreflang="es">Ver este sitio en español</a></p>
</div></section></main></body></html>
"""
open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8", newline="\n").write(not_found)

n = sum(len(f) for _, _, f in os.walk(ROOT) if False)
print("built", len(KEYS) * 2, "pages +404, sitemap.xml, robots.txt, llms.txt | css v", VER["css"], "js v", VER["js"])

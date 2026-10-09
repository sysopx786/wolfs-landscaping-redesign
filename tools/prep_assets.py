"""One-time asset prep: self-hosted fonts, responsive WebP/JPEG images, social preview image, contrast check.
Run from the repo root:  python tools/prep_assets.py
"""
import os, re, urllib.request
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read()


# ---------- fonts (latin subset only; covers Spanish accents and inverted punctuation) ----------
def fonts():
    os.makedirs(os.path.join(ROOT, "fonts"), exist_ok=True)
    css = get("https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&display=swap").decode()
    out = []
    for block in re.findall(r"/\* (\S+) \*/\s*(@font-face \{.*?\})", css, flags=re.S):
        subset, face = block
        if subset != "latin":
            continue
        fam = re.search(r"font-family: '([^']+)'", face).group(1)
        url = re.search(r"url\((https://[^)]+\.woff2)\)", face).group(1)
        fn = fam.lower() + "-latin.woff2"
        open(os.path.join(ROOT, "fonts", fn), "wb").write(get(url))
        weight = re.search(r"font-weight: ([^;]+);", face).group(1)
        rng = re.search(r"unicode-range: ([^;]+);", face).group(1)
        out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{weight};font-display:swap;src:url(fonts/{fn}) format('woff2');unicode-range:{rng}}}")
    css_out = "\n".join(out) + "\n"
    open(os.path.join(ROOT, "fonts", "fonts.css"), "w").write(css_out)
    print("fonts:", os.listdir(os.path.join(ROOT, "fonts")))


# ---------- images ----------
def images():
    src = os.path.join(ROOT, "photos")
    for f in sorted(os.listdir(src)):
        if not re.fullmatch(r"[a-z]+-(before|after)\.jpg", f):
            continue
        base = f[:-4]
        im = Image.open(os.path.join(src, f)).convert("RGB")
        for w in (480, 800, 1168):
            r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS) if w != im.width else im
            r.save(os.path.join(src, f"{base}-{w}.webp"), "WEBP", quality=78, method=6)
            if w != 1168:
                r.save(os.path.join(src, f"{base}-{w}.jpg"), "JPEG", quality=80, optimize=True, progressive=True)
    print("images:", len(os.listdir(src)), "files")


# ---------- social preview (branded graphic, not an AI project image) ----------
def og():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#0d0e0a")
    d = ImageDraw.Draw(im)
    for i in range(H):  # subtle vertical gradient, black to deep olive
        t = i / H
        d.line([(0, i), (W, i)], fill=(int(13 + t * 24), int(14 + t * 30), int(10 + t * 8)))
    def font(names, size):
        for n in names:
            try:
                return ImageFont.truetype(n, size)
            except OSError:
                pass
        return ImageFont.load_default()
    serif = ["georgiab.ttf", "georgia.ttf", "times.ttf"]
    sans = ["segoeui.ttf", "arial.ttf"]
    k = 80 / 32
    d.rounded_rectangle([80, 90, 160, 170], radius=18, fill="#4d5b26")
    pts = lambda L: [(80 + x * k, 90 + y * k) for x, y in L]
    d.polygon(pts([(5.5, 4.5), (12, 10.6), (14, 10.1), (18, 10.1), (20, 10.6), (26.5, 4.5), (27.4, 17.1), (22.8, 25.3), (16, 29.2), (9.2, 25.3), (4.6, 17.1)]), fill="#e2e3dd")
    d.polygon(pts([(9.2, 16.2), (13.3, 17.5), (11.7, 19.8)]), fill="#0d0e0a")
    d.polygon(pts([(22.8, 16.2), (18.7, 17.5), (20.3, 19.8)]), fill="#0d0e0a")
    d.polygon(pts([(13.6, 23.4), (18.4, 23.4), (16, 26.3)]), fill="#0d0e0a")
    d.text((80, 230), "Wolf's Landscaping Services", font=font(serif, 68), fill="#e2e3dd")
    d.text((80, 340), "Lawn care, hardscaping, retaining walls", font=font(sans, 40), fill="#c4c6b8")
    d.text((80, 400), "Royersford & Chester County, PA", font=font(sans, 40), fill="#a7b46a")
    d.rounded_rectangle([80, 500, 470, 565], radius=32, fill="#4d5b26")
    d.text((110, 513), "Free estimates", font=font(sans, 36), fill="#ffffff")
    im.save(os.path.join(ROOT, "og-image.jpg"), "JPEG", quality=86, optimize=True)
    print("og-image.jpg", os.path.getsize(os.path.join(ROOT, "og-image.jpg")) // 1024, "KB")


# ---------- WCAG contrast ----------
def lum(hexc):
    h = hexc.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def contrast():
    pairs = {
        "white on olive button (#4d5b26)": ("#ffffff", "#4d5b26"),
        "white on olive hover (#3a4420)": ("#ffffff", "#3a4420"),
        "black on off-white header button": ("#0d0e0a", "#e2e3dd"),
        "body ink on white": ("#14150f", "#ffffff"),
        "body ink on sand": ("#14150f", "#efede4"),
        "stone on sage": ("#55574b", "#e4e6d8"),
        "stone on sand": ("#55574b", "#efede4"),
        "stone on white": ("#55574b", "#ffffff"),
        "olive links on white": ("#4d5b26", "#ffffff"),
        "olive links on sand": ("#4d5b26", "#efede4"),
        "black headings on sage": ("#0d0e0a", "#e4e6d8"),
        "olive-light eyebrow on black": ("#a7b46a", "#0d0e0a"),
        "off-white nav on black": ("#e2e3dd", "#0d0e0a"),
        "footer text on black": ("#c4c6b8", "#0d0e0a"),
        "white on black": ("#ffffff", "#0d0e0a"),
        "off-white on hero olive end (#4d5b26)": ("#e2e3dd", "#4d5b26"),
    }
    for k, (a, b) in pairs.items():
        r = ratio(a, b)
        print(f"{r:5.2f}  {'PASS' if r >= 4.5 else 'FAIL'}  {k}")


if __name__ == "__main__":
    import sys
    for step in (sys.argv[1:] or ["contrast", "fonts", "images", "og"]):
        globals()[step]()

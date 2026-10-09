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
    im = Image.new("RGB", (W, H), "#1f3f28")
    d = ImageDraw.Draw(im)
    for i in range(H):  # subtle vertical gradient
        c = int(31 + (i / H) * 25)
        d.line([(0, i), (W, i)], fill=(c, 63 + int(i / H * 30), 40 + int(i / H * 20)))
    def font(names, size):
        for n in names:
            try:
                return ImageFont.truetype(n, size)
            except OSError:
                pass
        return ImageFont.load_default()
    serif = ["georgiab.ttf", "georgia.ttf", "times.ttf"]
    sans = ["segoeui.ttf", "arial.ttf"]
    d.rounded_rectangle([80, 90, 160, 170], radius=18, fill="#f4efe4")
    d.polygon([(120, 105), (145, 135), (145, 148), (120, 160), (95, 148), (95, 135)], fill="#2f5d3a")
    d.text((80, 230), "Wolf's Landscaping Services", font=font(serif, 68), fill="#ffffff")
    d.text((80, 340), "Lawn care, hardscaping, retaining walls", font=font(sans, 40), fill="#e3ead9")
    d.text((80, 400), "Royersford & Chester County, PA", font=font(sans, 40), fill="#f1d9a8")
    d.rounded_rectangle([80, 500, 470, 565], radius=32, fill="#a8651a")
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
        "white on button (old accent #c8832b)": ("#ffffff", "#c8832b"),
        "white on button (new accent #a8651a)": ("#ffffff", "#a8651a"),
        "white on hover (#8f5513)": ("#ffffff", "#8f5513"),
        "body ink on white": ("#1d241e", "#ffffff"),
        "stone on sage": ("#5b5a52", "#e7ede2"),
        "stone on sand": ("#5b5a52", "#f4efe4"),
        "stone on white": ("#5b5a52", "#ffffff"),
        "green on white (links)": ("#2f5d3a", "#ffffff"),
        "green on sand (links)": ("#2f5d3a", "#f4efe4"),
        "green-dark on sage": ("#1f3f28", "#e7ede2"),
        "gold eyebrow on dark hero": ("#f1d9a8", "#2f5d3a"),
        "light text on footer": ("#b9c7b0", "#14241a"),
        "white on green-dark": ("#ffffff", "#1f3f28"),
    }
    for k, (a, b) in pairs.items():
        r = ratio(a, b)
        print(f"{r:5.2f}  {'PASS' if r >= 4.5 else 'FAIL'}  {k}")


if __name__ == "__main__":
    import sys
    for step in (sys.argv[1:] or ["contrast", "fonts", "images", "og"]):
        globals()[step]()

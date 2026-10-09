"""Visual regression: full-page screenshots (headless Chrome/Edge) compared with a saved baseline.
  python tools/visual.py baseline   # save the current look as the reference
  python tools/visual.py compare    # re-shoot and report % of pixels that changed (diff images saved)
Screenshots live in tests/ (git-ignored). Needs Pillow and Chrome or Edge installed.
A flagged screenshot is retaken up to 2 times before it counts as a regression, because lazy-loaded
images can occasionally finish late on a busy machine.
"""
import os, sys, subprocess, threading, http.server, socketserver, shutil, functools
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(ROOT, "tests")
PAGES = ["index", "retaining-walls", "gallery", "contact", "faq"]
LANGS = ["", "es/"]
SIZES = {"mobile": (390, 3600), "desktop": (1280, 3000)}
THRESHOLD = 0.5  # percent of changed pixels that counts as a regression
RETRIES = 2
BROWSERS = [r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]


def browser():
    for b in BROWSERS:
        if os.path.exists(b): return b
    sys.exit("No Chrome/Edge found")


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass


def serve():
    srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=ROOT))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def jobs():
    for lang in LANGS:
        for page in PAGES:
            for name, size in SIZES.items():
                yield lang, page, name, size, f"{lang.rstrip('/') or 'en'}_{page}_{name}.png"


def shoot_one(port, lang, page, size, out):
    w, h = size
    url = f"http://127.0.0.1:{port}/{lang}{page}.html"
    win_w = w
    if w < 600:
        # headless Chrome will not render a window narrower than ~500px, which would crop the page.
        # Show the page inside an iframe of the true phone width instead.
        os.makedirs(TESTS, exist_ok=True)
        wrapper = os.path.join(TESTS, "_frame.html")
        with open(wrapper, "w", encoding="utf-8") as f:
            f.write(f'<!DOCTYPE html><html><body style="margin:0;background:#888"><iframe src="/{lang}{page}.html" width="{w}" height="{h}" style="border:0;display:block;background:#fff"></iframe></body></html>')
        url = f"http://127.0.0.1:{port}/tests/_frame.html"
        win_w = w + 20
    subprocess.run([browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={win_w},{h}",
                    "--virtual-time-budget=10000", f"--screenshot={out}", url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)


def shoot_all(out_dir, srv):
    os.makedirs(out_dir, exist_ok=True)
    port = srv.server_address[1]
    for lang, page, name, size, fn in jobs():
        shoot_one(port, lang, page, size, os.path.join(out_dir, fn))


def diff_pct(a, b):
    ia, ib = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    if ia.size != ib.size: return None, ia.size, ib.size
    d = ImageChops.difference(ia, ib).convert("L").point(lambda v: 255 if v > 24 else 0)
    return 100 * d.histogram()[255] / (d.width * d.height), d, None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "compare"
    base, cur, diff = (os.path.join(TESTS, d) for d in ("baseline", "current", "diff"))
    srv = serve()
    if mode == "baseline":
        if os.path.exists(base): shutil.rmtree(base)
        shoot_all(base, srv)
        print("baseline saved:", len(os.listdir(base)), "screenshots in", base)
        return 0
    if not os.path.exists(base): sys.exit("No baseline yet. Run: python tools/visual.py baseline")
    for d in (cur, diff):
        if os.path.exists(d): shutil.rmtree(d)
    os.makedirs(diff)
    shoot_all(cur, srv)
    port = srv.server_address[1]
    bad = 0
    for lang, page, name, size, fn in jobs():
        a, b = os.path.join(base, fn), os.path.join(cur, fn)
        if not os.path.exists(a): print("NEW      ", fn); bad += 1; continue
        tries = 0
        pct, d, other = diff_pct(a, b)
        while (pct is None or pct > THRESHOLD) and tries < RETRIES:
            tries += 1
            shoot_one(port, lang, page, size, b)
            pct, d, other = diff_pct(a, b)
        if pct is None:
            print(f"SIZE     {fn}: {d} -> {other}"); bad += 1
        elif pct > THRESHOLD:
            bad += 1; d.save(os.path.join(diff, fn)); print(f"CHANGED  {fn}: {pct:.2f}% pixels differ (after {tries} retake(s))")
        else:
            print(f"ok       {fn}: {pct:.2f}%" + (f" (needed {tries} retake)" if tries else ""))
    print(f"{len(list(jobs()))} screenshots compared, {bad} regression(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

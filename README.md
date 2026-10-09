# Wolf's Landscaping Services website

Owner-operated landscaping based in Royersford, PA, serving Chester County and the surrounding area. Bilingual (English and Spanish).

| | |
|---|---|
| Live website | https://sysopx786.github.io/wolfs-landscaping-redesign/ |
| Spanish version | https://sysopx786.github.io/wolfs-landscaping-redesign/es/index.html |
| Source code (GitHub) | https://github.com/sysopx786/wolfs-landscaping-redesign |

## What's in the site
14 pages in each language: home, 8 service pages, about, gallery (before/after sliders), FAQ, contact, privacy. Plus `404.html`, `sitemap.xml`, `robots.txt`, `llms.txt`.

- **Estimate form:** builds a text message on the visitor's own device (nothing is sent by the site, no email address is published). Visitors can text it to the business number, copy it, or call.
- **Gallery images** are AI-generated concept illustrations, labelled as such. They are not photos of completed projects.
- **No tracking, no cookies, no third-party requests.** Fonts and images are self-hosted.

## Editing the site
Pages are generated. Do not edit the HTML files by hand.

| To change | Edit |
|---|---|
| Any wording, English or Spanish | `tools/content.py` |
| Page layout / templates | `tools/build.py` |
| Look and feel | `styles.css` |
| Behavior (menu, sliders, form) | `script.js` |
| Business facts and brand settings | `business.json` (reference record) |
| Owner name, story and credentials on the About page | `OWNER` in `tools/content.py` (empty = not shown) |

Then rebuild and check:

```bash
python tools/build.py      # regenerates every page, sitemap, robots, llms.txt
python tools/audit.py      # links, SEO tags, hreflang, structured data, EN/ES parity
```

Commit and push. GitHub Pages publishes the `main` branch automatically.

## Tools (`tools/`)
| Script | Purpose |
|---|---|
| `build.py` | Generates all pages from `content.py` |
| `audit.py` | Static audit; exits with an error if anything is wrong |
| `crawl_live.py` | Crawls the live site (every sitemap URL, link, image, font) |
| `visual.py` | Screenshot comparison against a saved baseline (needs Pillow + Chrome) |
| `prep_assets.py` | One-time: self-hosted fonts, WebP/JPEG image sizes, social preview image, contrast check |

A GitHub Action (`.github/workflows/site-check.yml`) runs the build and audit on every push, and the live crawl every Monday. If a check fails, GitHub emails the repository owner.

## Notes
- Spanish text should be reviewed by a native speaker before relying on it.
- The privacy page is a draft and should be reviewed by the owner.
- Before adding a new image to the gallery, run `tools/prep_assets.py` to create the responsive sizes.

See `CHANGELOG.md` for the history.

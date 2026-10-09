# Wolf's Landscaping Services website

Owner-operated landscaping based in Royersford, PA, serving Chester County and the surrounding area. Bilingual (English and Spanish).

## Links

| | Public website (GitHub Pages) | Source code (GitHub) |
|---|---|---|
| **Redesign** | https://sysopx786.github.io/wolfs-landscaping-redesign/ ([Español](https://sysopx786.github.io/wolfs-landscaping-redesign/es/index.html)) | https://github.com/sysopx786/wolfs-landscaping-redesign |
| Current site | https://sysopx786.github.io/wolfs-landscaping-WEBSITE/ ([Español](https://sysopx786.github.io/wolfs-landscaping-WEBSITE/es/index.html)) | https://github.com/sysopx786/wolfs-landscaping-WEBSITE |

This repository is a copy of the current site with a new look: black, olive and off-white colors, the Wolf's logo, a banner photo and light menus.

## What's in the site
16 pages in each language: home, 8 service pages, about, reviews, gallery (before/after sliders), FAQ, contact, join the team and privacy. Plus `404.html`, `sitemap.xml`, `robots.txt` and `llms.txt`.

- **Estimate form:** builds a text message on the visitor's own device (nothing is sent by the site and no email address is published). Visitors can text it to the business number, copy it, or call.
- **No tracking, no cookies, no third-party requests.** Fonts and images are self-hosted.

## Editing the site
Pages are generated. Do not edit the HTML files by hand.

| To change | Edit |
|---|---|
| Any wording, English or Spanish | `tools/content.py` |
| Page layout / templates | `tools/build.py` |
| Look and feel | `styles.css` |
| Behavior (menu, sliders, form) | `script.js` |
| Business facts | `business.json` (reference record) |
| Owner name, story and credentials on the About page | `OWNER` in `tools/content.py` |

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
| `visual.py` | Screenshot comparison against a saved baseline (needs Pillow and Chrome) |
| `prep_assets.py` | Self-hosted fonts, WebP/JPEG image sizes, social preview image, contrast check |

A GitHub Action (`.github/workflows/site-check.yml`) runs the build and audit on every push, and the live crawl every Monday.

## Notes
- Spanish text should be reviewed by a native speaker before relying on it.
- The privacy page is a draft and should be reviewed by the owner.
- Before adding a new image to the gallery, run `tools/prep_assets.py` to create the responsive sizes.

See `CHANGELOG.md` for the history.

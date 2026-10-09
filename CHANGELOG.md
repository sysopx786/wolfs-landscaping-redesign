# Changelog

## 2026-10-09: Updated wolf artwork
- New logo (wolf emblem and full logo) replaces the previous one in the header, footer, tab and touch icons and the social preview image. The Join the team page uses the new "Join the Pack" card sheet as its poster, and the four role cards below it are text links.

## 2026-10-09: Call Now bar removed on phones
- The sticky "Call Now" bar at the bottom of phone screens is removed (markup, styles and text). The back-to-top arrow stays. Phone numbers remain as links in the header menu, home banner, Contact page, Join page and footer.

## 2026-10-09: Lighter phone banners, readable breadcrumbs
- Phone banner overlay lowered to about 36-40% (home banner 38-48%). Breadcrumbs are white and underlined on all screen sizes with a slightly darker strip across the top of each photo banner, and the home banner's small location label is lighter. Checked all 162 banner text regions on phones and desktop: lowest contrast 5.1:1 on phones, 5.5:1 on desktop, breadcrumbs at least 6.7:1.

## 2026-10-09: Phone banners show the photo
- On phones the banner overlay is about 50% instead of 75-80%, text has a soft shadow and a soft dark band behind it, and each photo is cropped so its main subject sits in the lower or right part of the banner. Every text region still passes contrast (lowest 7.1:1 on phones).

## 2026-10-09: Photo banners on inner pages
- Inner-page banners are about half as tall and have a photo behind the title under a light olive-tinted overlay. Service pages use their own gallery photo (lawn, sod, patio, garden bed, retaining wall, stone wall, perennial bed); every other page uses the sunrise photo from the home page.

## 2026-10-09: Repository cleanup
- Removed unused files and internal notes; README, changelog and business record rewritten for public viewing.

## 2026-10-09: Home banner photo
- Landscape photo behind the home headline under a dark overlay, in three sizes loaded by screen width. Inner pages keep the plain dark banner.

## 2026-10-09: Readable buttons
- Buttons inside text blocks no longer inherit the olive link color. Checked every button on every page at desktop and phone widths: all have at least 4.5:1 contrast.

## 2026-10-09: Menus
- Phone menu is a light panel with dark text, dividers and an olive estimate button; the Call Now bar hides while it is open. The desktop Services dropdown matches. The header background is solid so the logo blends in.

## 2026-10-09: New look and logo
- Colors: black `#0d0e0a`, olive `#4d5b26`, off-white `#e2e3dd` (light olive `#a7b46a` for small labels on dark). All text pairs pass WCAG AA.
- The supplied logo: round emblem in the header, full logo in the footer, wolf head as tab and touch icon, logo on the social preview image.

## 2026-10-09: Join the team
- New "Join the team" page in English and Spanish: what we look for, how to apply by call or text, and four role cards linking to the services. Linked in the menu and footer and listed in the sitemap.

## 2026-10-05: Owner, address and map
- Owner (Bryan J. Wolf) shown on the About page and home banner. Office address (429 Main St, Royersford, PA 19468) in the footer and on the Contact page with "Get directions" and "View on Google Maps" buttons. Structured data includes the address, a map link and the founder.

## 2026-10-05: Aeration, Sod & Seeding
- Service renamed "Aeration, Sod & Seeding" everywhere, including the estimate form. New page sections on why to aerate, why to overseed and after-care, plus two new FAQs.

## 2026-10-05: Gallery and home page
- Gallery has 14 before/after sliders (English and Spanish) with text descriptions for screen readers. The home page "See the difference" section shows four of them.
- Home banner: the Google rating line links to the Reviews page and sits above the buttons; the call button is a phone icon on phones.

## 2026-10-05: Reviews
- New Reviews page listing the business's Google reviews, with Google's official "G" and direct "Leave a review on Google" links on the home, About and Reviews pages.

## 2026-10-05: Location
- Business location is Royersford, PA (titles, descriptions, page text, FAQ, structured data and social image, English and Spanish). Service area is Chester County.

## 2026-10-05: Phones
- English/Spanish switch is a compact ES / EN button in the header bar on phones and tablets. The menu collapses at 1240 px so longer Spanish labels never overflow.

## 2026-10-04: First complete version
- 8 service pages, About, Gallery, FAQ, Contact and Privacy in English and Spanish (`/es/`) with language switcher and `hreflang` pairs.
- SEO: sitemap, canonical URLs, robots.txt, llms.txt, Open Graph and Twitter cards, structured data (LocalBusiness, WebSite, Service, FAQ, breadcrumbs).
- Accessibility and speed: skip link, 44 px touch targets, contrast-checked colors, self-hosted fonts, responsive WebP/JPEG images, no cookies and no third-party requests.
- Estimate form builds a text message on the visitor's device (send by text, copy, or call). No email address is published.
- Tooling: `tools/build.py` (generator), `tools/audit.py` (checks), `tools/crawl_live.py` (live-site crawl), GitHub Action on every push and weekly.

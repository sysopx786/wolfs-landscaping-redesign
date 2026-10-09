# Changelog

## 2026-10-09: Join the team in the menu
- "Join the team" (Spanish: "Únase al equipo") added to the main menu, between Contact and Free Estimate, on every page. Checked at the narrowest desktop width in both languages: fits on one line.

## 2026-10-09: Join the team is public
- The Join the team page is kept: linked in the footer of every page (English and Spanish), added to the sitemap and llms.txt, and no longer marked noindex.

## 2026-10-09: Join the team (sample page)
- New page /join-the-team.html (English and Spanish) with the "Join the pack" poster (phone number removed), what we look for, how to apply by call or text to the main number, and four role cards linking to services. Sample only: not in the menu, footer or sitemap, and marked noindex. To undo, revert this commit.

## 2026-10-05: Home page "See the difference"
- The single slider is replaced by four from the gallery: bluestone patio with fire pit, entry walkway and lighting, lawn renewal, and paver walkway.

## 2026-10-05: Six more before and after sliders
- Gallery grows from 8 to 14 pairs: bluestone patio with fire pit, paver patio and garden, curved retaining wall and lawn, new-home landscaping, entry walkway and lighting, and lawn renewal. Each has a text description in English and Spanish for screen readers.

## 2026-10-05: Owner name on the home page
- Home banner trust line now reads "Owner-operated by Bryan J. Wolf" (Spanish: "Dirigido por su dueño, Bryan J. Wolf").

## 2026-10-05: Aeration, Sod & Seeding
- Service renamed "Aeration, Sod & Seeding" (English and Spanish) everywhere it is listed, including the estimate form.
- New page sections: why aerate (with benefits list), why overseed, and an aeration and overseeding after-care guide (soil plugs, watering, traffic, mowing, fall leaves), plus two new FAQs. Wording is our own, adapted from the owner's supplied notes.

## 2026-10-05: Owner, address and Google Maps link
- Owner added: Bryan J. Wolf, Owner (About page "Meet the owner"; structured data lists him as founder).
- Principal office address added: 429 Main St, Royersford, PA 19468. Shown in the footer on every page and in a new "Our office" block on the Contact page, with "Get directions" and "View on Google Maps" buttons. Structured data has the full street address and a map link. English and Spanish.

## 2026-10-05: Phone icon button in the home banner
- On phones the call button in the home banner is a round phone-icon button on the same line as "Request a Free Estimate" (56 px touch target, spoken name "Call 610-357-1098"). On desktop it shows the icon and the number.

## 2026-10-05: Rating line is a link, shown first
- On the home page the Google rating line (stars, 5.0, "Reviews from Google (14)") is now one link to the on-site Reviews page, and the "See all reviews" buttons are removed. In the hero the link sits above "Request a Free Estimate" and the phone button so phone visitors see it on load; the "Leave a review on Google" button stays below them.

## 2026-10-05: Royersford, and reviews in the home banner
- Business location corrected: every mention of Phoenixville on the site (titles, descriptions, page text, FAQ, structured data, social preview image, English and Spanish) now says Royersford, PA. Service area still names Chester County. Structured data lists Royersford, PA as the address locality.
- Home banner: removed the repeated "5.0 Google rating / 14 customer reviews" line. The Google rating with the "Leave a review on Google" and "See all reviews" buttons now sits directly under "Request a Free Estimate" and "Call".

## 2026-10-05: Reviews bar on the home page
- Added a slim reviews bar directly under the home page hero (English and Spanish): Google G, stars, 5.0, "Reviews from Google (14)", with "Leave a review on Google" and "See all reviews" buttons. The same two buttons remain at the bottom of the reviews section.

## 2026-10-05: All 14 reviews listed
- The Reviews page now lists all 14 Google reviews, copied from the listing (pasted by the owner) with first name + last initial, time, text and stars. One review (Kate D.) has no text in the pasted copy and shows as a star rating only. The home page features Arturo V., Kathy P. and Erin S.

## 2026-10-05: Reviews page
- New Reviews page (English and Spanish) listing customer reviews from the Google listing, each with the Google "G", stars, name (first name + initial), time, text and a "View on Google" link when the review's share link is known. The menu's Reviews item now opens it. The home page shows three featured reviews and a "See all reviews" button.
- Reviews live in `tools/reviews.json`; add one and run `python tools/build.py`. The page says "Showing N of 14 reviews" until all 14 are listed.

## 2026-10-05: Leave a review button
- Added a "Leave a review on Google" button (English and Spanish) next to "Read all reviews on Google". It uses Google's direct write-a-review link built from the listing's Place ID, so it opens the review box (after Google's sign-in) on desktop and phones. The listing link alone only opens the business page.

## 2026-10-05: Reviews now come from the real Google listing
- Review quotes and the rating (5.0, 14 reviews) now match the business's own Google listing. The previous quotes and the 4.7 / 15 figures belonged to a different business and were removed, along with specific claims that came from it (reply within 1–2 days, voicemail callback, leaves collected for regular customers).
- Reviews are shown without reviewer names (the listing page did not show them), labelled "Google review".

## 2026-10-05: Real Google reviews link
- "Read all reviews on Google" now opens the business's own Google listing (Wolf’s Landscaping Services) instead of a Maps search. Link is stored once in `tools/content.py` (`google_reviews_url`).

## 2026-10-05: Google branding on reviews
- Added Google's official four-color "G" (file `brand/google-g.png`, unaltered, self-hosted) to the rating in the hero, the reviews section header, each review card, the "Read all reviews on Google" button, and the About page quotes. Rating stars use Google's yellow (#FBBC05). On the dark hero the G sits on a white circle. Decorative icons have empty alt text because "Google" is written next to them; a screen-reader line gives the rating.
- Audit now accepts intentionally empty alt text on decorative Google icons only.

## 2026-10-05: Concept labels removed
- Removed the "Concept" label from every gallery slider and the "concept" line in the home page's "See the difference" section (English and Spanish), at the owner's request. The home section now shows the instruction "Drag the handle...".

## 2026-10-05: Gallery notice removed
- Removed the one-line notice at the top of the gallery page (English and Spanish) at the owner's request. The small "Concept" label on each slider remains.

## 2026-10-05: Gallery wording
- Removed every mention of how the gallery images were made from the website (labels, notice, image descriptions, metadata, llms.txt). The badge now reads "Concept" and the notice is one short line: the images are illustrations, not photos of completed projects. Remove that line when real project photos replace them.

## 2026-10-05: Five more before/after pairs
- Gallery now has 8 before/after sliders (English and Spanish): added stone patio with seating wall, paver driveway, stone retaining wall with mulch beds, boulder and flower bed, and a new sod lawn.
- All new images are AI-generated concept illustrations (Higgsfield GPT Image 2.5), made from text prompts only, and labelled "AI concept". Each "after" was edited from its own "before" so the pairs line up.
- Fixed a stray "Call Now" link that showed in the desktop footer.
- `tools/prep_assets.py` now builds the responsive sizes for any `name-before.jpg` / `name-after.jpg` pair.

## 2026-10-05: Language button on phones
- The English/Spanish switch is now a compact **ES / EN** button in the header bar next to the menu icon on phones and tablets (it was hidden inside the menu). Fits down to 320 px screens, 44 px touch target, centered, accessible name.
- `tools/visual.py` now shoots phone-size pages inside true-width frames (headless Chrome cannot render windows narrower than ~500 px, which had been cropping the phone screenshots).

## 2026-10-04: About page
- New About page in English and Spanish, written only from confirmed facts (owner-operated, services, what customers say). Owner name, story and credentials are optional fields in `tools/content.py` and stay hidden until filled in.
- Menu: added About. Hamburger menu now starts at 1240 px so the longer Spanish labels never overflow; fixed the dropdown stacking inside the mobile menu; content width 1200 px.

## 2026-10-04: MWDS 3.0 completion pass
- **Spanish site** (`/es/`): all 13 pages translated, language switcher that keeps you on the matching page, `hreflang` pairs, Spanish FAQ and form.
- **SEO:** `sitemap.xml` (26 URLs with language alternates), canonical URLs, `robots.txt` with sitemap line and explicit search/AI crawler rules, `llms.txt`, Open Graph and Twitter cards with a preview image, richer structured data (LocalBusiness, WebSite, Service, FAQPage, BreadcrumbList). Removed star-rating markup because the Google profile identity is unconfirmed.
- **Keywords:** page titles and FAQs now use real search phrasing (for example "lawn mowing service Phoenixville", "how to fix yard drainage problems", "retaining wall cost").
- **Contact page** added; the repeated call/estimate buttons on every service page were reduced.
- **Form:** the estimate form no longer uses any email address. It now builds a text message on the visitor's device (text, copy, or call).
- **Accessibility:** fixed button contrast (white on orange was 3.1:1, now 4.6:1), larger touch targets, landmarks for floating buttons. axe-core: 0 violations on all 26 pages.
- **Performance and privacy:** self-hosted fonts (no Google Fonts request), WebP images in three sizes, content-hash cache busting.
- **Extras:** back-to-top button, print styles, custom 404 page.
- **Tooling:** generator, audit, live crawler, visual regression, weekly GitHub Action. All pages are now generated from `tools/content.py`.
- **Docs:** `README.md`, `business.json`.

## 2026-10-03/04: First release
- Home page, 8 service pages, gallery with before/after sliders (AI concept images, labelled), FAQ, privacy page.
- Published with GitHub Pages.

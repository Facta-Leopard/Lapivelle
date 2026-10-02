# Lapivelle public website

Home, support, and privacy information in Korean, English, French, Simplified Chinese, Traditional Chinese, Japanese, German, and Spanish.

Public base: https://facta-leopard.github.io/Lapivelle/

Each locale has `/{locale}/index.html`, `/{locale}/support.html`, and `/{locale}/privacy.html`. Existing `/privacy.html` and `/support.html` remain working entry points; their old English/Korean/French anchors select the corresponding language when JavaScript is available. Every localized document remains readable without JavaScript.

## Updating

Edit `_data/site.json` for reviewed translations and contact information, `assets/site.css` for styles, and `tools/render_site.py` for document structure. Then run:

```sh
python3 tools/render_site.py
python3 tools/check_site.py
node --check assets/site.js
```

These commands generate/check static documents; they do not compile the iOS app. GitHub Pages publishes committed files from the root of `main`. `.nojekyll` disables Jekyll processing. No package install, tracking service, remote font, form backend, or API key is required.

## Content and assets

- Operator name `Facta Leopard` is preserved from the earlier published policy. Support email is the contact already configured in the app: `shteosis@gmail.com`.
- Policy text describes current local-only app behavior, voluntary support messages, and GitHub Pages hosting logs separately. Planned purchases, parental gates and AI features are not presented as current behavior.
- Hosting reference: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- App submission link requirements: https://developer.apple.com/app-store/review/
- Artwork is reused from the approved Lapivelle ProductionV3 set. Only a website-sized derivative and app icon are included; the app source and full story manuscripts are not published in this repository.
- No third-party code package or design template was added. Styling follows the project-specific `DESIGN.md`.

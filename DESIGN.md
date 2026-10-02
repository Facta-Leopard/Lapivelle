# Lapivelle support website

Use the existing Lapivelle app identity as the design baseline. This is a calm, adult-operated bedtime-story product with a practical support and privacy website, not a generic software dashboard.

- Palette: midnight `#0e101b`, soft navy `#1c2031`, warm paper `#f6f1e7`, ink `#222837`, muted slate `#626979`, antique gold `#dbb86c`.
- Typography: restrained book-like display headings in Baskerville/Georgia and locale-appropriate serif fallbacks; readable body text in Avenir Next/Trebuchet and native CJK families. No remote font requests.
- Composition: a spacious navy introduction, one existing story illustration, clear support/privacy links, and warm-paper documents with narrow reading measure. Avoid repeated cards for policy paragraphs.
- Navigation: consistent logo, home/support/privacy links, explicit eight-language selector, language names in their own writing systems. Switching language keeps the page type. Canonical URLs must work without JavaScript.
- Accessibility: keyboard navigation and visible focus, skip link, 44px controls, adequate contrast, responsive layout, no essential hover interactions. Respect reduced motion. Native disclosure elements for support questions.
- Privacy: no analytics, third-party embeds, remote fonts, contact form backend, cookie banner or tracking scripts. Contact opens email; public issue reporting is clearly distinguished from private support.
- Content: use current implemented app behavior. No unverified App Store download link, release claims, response-time promises, planned IAP/AI features, or claims that hosting providers process no data.
- Images: reuse the approved generated assets from `Assets/ProductionV3`; do not invent a second character design. Keep website assets locally hosted.

This project-specific baseline was authored from the existing app/asset design while applying the design-baseline and frontend-design workflows. It introduces no third-party design-template code or package dependency.

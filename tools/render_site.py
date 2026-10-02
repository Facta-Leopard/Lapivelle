#!/usr/bin/env python3
"""Render buildless, fully readable GitHub Pages documents from reviewed locale copy."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_data/site.json").read_text(encoding="utf-8"))
PAGES = {"home": "index.html", "privacy": "privacy.html", "support": "support.html"}


def escape(value):
    return html.escape(str(value), quote=True)


def paragraph(value):
    email = DATA["email"]
    return escape(value).replace("{email}", f'<a href="mailto:{escape(email)}">{escape(email)}</a>')


def heading(value):
    return "<br>".join(escape(line) for line in value.split("\n"))


def render(locale, page, root_alias=False):
    copy = DATA["locales"][locale]
    prefix = "" if root_alias else "../"
    filename = PAGES[page]
    href = lambda lang, kind: f'{prefix}{lang}/{PAGES[kind]}'
    canonical = DATA["baseURL"] + locale + "/" + filename
    alternates = "\n".join(f'<link rel="alternate" hreflang="{code}" href="{DATA["baseURL"]}{code}/{filename}">' for code in DATA["languages"])
    title = "Lapivelle — " + copy["nav"][page]
    description = copy[page]["summary"] if page == "privacy" else copy[page]["intro"]
    nav = "".join(f'<a href="{href(locale, key)}"{chr(32) + "aria-current=\"page\"" if key == page else ""}>{escape(label)}</a>' for key, label in copy["nav"].items())
    language_links = "".join(f'<a href="{href(code, page)}" lang="{code}" hreflang="{code}"{chr(32) + "aria-current=\"page\"" if code == locale else ""}>{escape(label)}</a>' for code, label in DATA["languages"].items())
    mail = f'mailto:{DATA["email"]}?subject=Lapivelle%20Support%20%28{locale}%29'
    if page == "home":
        home = copy["home"]
        body = f'''<section class="hero wrap">
  <div class="hero-copy"><p class="eyebrow">{escape(home["eyebrow"])}</p>
  <h1>{heading(home["title"])}</h1><p class="lede">{escape(home["intro"])}</p>
  <p class="status"><span aria-hidden="true"></span>{escape(home["status"])}</p>
  <div class="actions"><a class="button primary" href="{href(locale, "support")}">{escape(copy["nav"]["support"])} <span aria-hidden="true">↗</span></a>
  <a class="text-link" href="{href(locale, "privacy")}">{escape(copy["nav"]["privacy"])}</a></div></div>
  <figure class="hero-art"><img src="{prefix}assets/story.jpg" width="1000" height="667" alt="{escape(home["imageAlt"])}" fetchpriority="high"></figure>
</section>
<section class="paper"><div class="wrap introduction">
<div class="entry-links"><a href="{href(locale, "support")}"><span class="entry-number" aria-hidden="true">01</span><div><h2>{escape(copy["nav"]["support"])}</h2><p>{escape(home["supportText"])}</p></div><span aria-hidden="true">↗</span></a>
<a href="{href(locale, "privacy")}"><span class="entry-number" aria-hidden="true">02</span><div><h2>{escape(copy["nav"]["privacy"])}</h2><p>{escape(home["privacyText"])}</p></div><span aria-hidden="true">↗</span></a></div></div></section>'''
    elif page == "support":
        support = copy["support"]
        questions = "".join(f'<details class="faq"><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>' for question, answer in support["faqs"])
        body = f'''<section class="document-heading wrap"><p class="eyebrow">Lapivelle / {escape(copy["nav"]["support"])}</p><h1>{heading(support["title"])}</h1><p class="lede">{escape(support["intro"])}</p></section>
<section class="paper"><div class="wrap support-layout"><div class="contact-panel"><p class="eyebrow">{escape(support["contactTitle"])}</p><h2><a href="{escape(mail)}">{escape(DATA["email"])}</a></h2><p>{escape(support["contactText"])}</p><a class="button ink" href="{escape(mail)}">{escape(copy["emailAction"])} <span aria-hidden="true">↗</span></a><div class="public-channel"><p>{escape(support["publicText"])}</p><a href="https://github.com/Facta-Leopard/Lapivelle/issues" rel="noreferrer">{escape(copy["publicAction"])}</a></div></div>
<div class="support-body"><h2>{escape(support["detailsTitle"])}</h2><p>{escape(support["detailsText"])}</p><h2 class="faq-title">{escape(support["faqTitle"])}</h2>{questions}</div></div></section>'''
    else:
        privacy = copy["privacy"]
        toc = "".join(f'<a href="#{escape(item[0])}">{escape(item[1])}</a>' for item in privacy["sections"])
        sections = []
        for item in privacy["sections"]:
            links = ""
            if item[0] == "website":
                links = f'<p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noreferrer">{escape(copy["providerLabel"])}</a></p>'
            elif item[0] == "sharing":
                links = f'<p><a href="https://www.apple.com/legal/privacy/" rel="noreferrer">{escape(copy["appleLabel"])}</a></p>'
            sections.append(f'<section id="{escape(item[0])}"><h2>{escape(item[1])}</h2>' + "".join(f'<p>{paragraph(text)}</p>' for text in item[2:]) + links + '</section>')
        body = f'''<section class="document-heading wrap"><p class="eyebrow">Lapivelle / {escape(copy["nav"]["privacy"])}</p><h1>{heading(privacy["title"])}</h1><p class="lede">{escape(privacy["summary"])}</p><p class="date">{escape(copy["updated"])}</p></section>
<section class="paper"><div class="wrap policy-layout"><aside><nav class="contents" aria-label="{escape(copy["contents"])}"><p class="eyebrow">{escape(copy["contents"])}</p>{toc}</nav></aside><article class="policy">{"".join(sections)}<a class="back-top" href="#top">{escape(copy["back"])} ↑</a></article></div></section>'''
    return f'''<!doctype html>
<html lang="{locale}" id="top">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description)}">
<meta name="theme-color" content="#0e101b"><meta name="referrer" content="no-referrer">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; style-src 'self'; script-src 'self'; font-src 'self'; connect-src 'none'; base-uri 'none'; form-action 'none'">
<link rel="canonical" href="{canonical}">{alternates}
<link rel="alternate" hreflang="x-default" href="{DATA["baseURL"]}{filename}">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{DATA["baseURL"]}assets/story.jpg">
<link rel="icon" href="{prefix}assets/icon.png" type="image/png"><link rel="stylesheet" href="{prefix}assets/site.css"><script src="{prefix}assets/site.js" defer></script>
</head>
<body data-page="{filename}" data-root="{str(root_alias).lower()}">
<a class="skip-link" href="#main">{escape(copy["skip"])}</a>
<header class="site-header wrap"><a class="brand" href="{href(locale, "home")}"><img src="{prefix}assets/icon.png" alt="" width="44" height="44"><span>Lapivelle</span></a>
<nav class="primary-nav" aria-label="Lapivelle">{nav}</nav><details class="languages"><summary aria-label="{escape(copy["language"])}">{escape(DATA["languages"][locale])} <span aria-hidden="true">⌄</span></summary><div class="language-menu">{language_links}</div></details></header>
<main id="main">{body}</main>
<footer class="wrap site-footer"><p>© 2026 {escape(DATA["operator"])} · Lapivelle</p><nav>{nav}</nav></footer>
</body></html>
'''


def main():
    assert set(DATA["languages"]) == set(DATA["locales"]), "Every language needs complete copy"
    for locale in DATA["languages"]:
        folder = ROOT / locale
        folder.mkdir(exist_ok=True)
        for page, filename in PAGES.items():
            (folder / filename).write_text(render(locale, page), encoding="utf-8")
    for page, filename in PAGES.items():
        (ROOT / filename).write_text(render("en", page, root_alias=True), encoding="utf-8")
    urls = [DATA["baseURL"] + locale + "/" + filename for locale in DATA["languages"] for filename in PAGES.values()]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{escape(url)}</loc><lastmod>{DATA["updated"]}</lastmod></url>' for url in urls) + '</urlset>\n'
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"Rendered {len(urls)} localized pages and three compatible root URLs.")


if __name__ == "__main__":
    main()

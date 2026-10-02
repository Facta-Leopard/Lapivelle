#!/usr/bin/env python3
"""Check the public document/link contract without a framework or app build."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "_data/site.json").read_text())


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.lang = None
        self.links = []
        self.ids = set()
        self.headers = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.headers += 1
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs["id"])
        for key in ["href", "src"]:
            if key in attrs:
                self.links.append(attrs[key])


def main():
    pages = ["index.html", "support.html", "privacy.html"]
    documents = {}
    for locale in [*DATA["languages"], ""]:
        for page in pages:
            path = ROOT / locale / page
            document = Document(path)
            assert document.lang == (locale or "en"), path
            assert document.headers == 1, path
            assert "{email}" not in path.read_text(), path
            documents[path.resolve()] = document
    for path, document in documents.items():
        for link in document.links:
            url = urlsplit(link)
            if url.scheme in {"https", "mailto"}:
                continue
            assert not url.scheme and not url.netloc, (path, link)
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            assert target.is_relative_to(ROOT), (path, link)
            assert target.is_file(), (path, link)
            if url.fragment:
                assert url.fragment in documents[target].ids, (path, link)
    ids = [section[0] for section in DATA["locales"]["en"]["privacy"]["sections"]]
    for locale in DATA["languages"]:
        copy = DATA["locales"][locale]
        assert [section[0] for section in copy["privacy"]["sections"]] == ids
        assert len(copy["support"]["faqs"]) == 5
        assert all(question and answer for question, answer in copy["support"]["faqs"])
    print(f"Checked {len(documents)} pages: languages, headings, anchors, local links, assets, privacy sections and FAQs.")


if __name__ == "__main__":
    main()

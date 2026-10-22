"""Keyword density checker for live pages AND drafts (Markdown, HTML or plain text), plus a two-page phrase comparison.

    analyze_text(text, title="", description="", headings=(), h1="", path="")   offline, no network
    analyze_file("draft.md")                                                    .md / .html / .txt
    asyncio.run(analyze_url("https://example.com/page/"))                       visible text of a live page
    asyncio.run(compare_urls(yours, theirs))                                    their top phrases that aren't among yours

Density = count × words in the phrase ÷ total words × 100, so single words and phrases share one scale.
Built on the engine behind https://www.cmoowls.com/tools/keyword-density-checker/ (https://github.com/CMO-Owls/free-seo-tools). MIT.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from cmoowls_seo_tools import core

__version__ = "1.0.0"


def analyze_text(text: str, title: str = "", description: str = "", headings=(), h1: str = "", path: str = "") -> dict:
    words = [w.lower().replace("’", "'") for w in core._WORD_RE.findall(text)]
    total = len(words)
    if total < 30:
        raise ValueError("Fewer than 30 words of text: too short to measure keyword use.")
    content = [w for w in words if w not in core._STOPWORDS and len(w) > 1]
    places = {"title": title.lower(), "description": description.lower(), "h1": h1.lower(),
              "headings": " ".join(headings).lower(), "url": path.lower().replace("-", " ").replace("_", " ")}

    def rows(counter: Counter, n: int, k: int = 15) -> list[dict]:
        out = []
        for term, cnt in counter.most_common(k):
            if cnt < 2:
                break
            out.append({"term": term, "count": cnt, "density": round(cnt * n / total * 100, 2),
                        "in": [p for p, v in places.items() if v and re.search(r"\b" + re.escape(term) + r"\b", v)]})
        return out

    singles = rows(Counter(content), 1, 20)
    two, three = rows(core._ngrams(words, 2), 2), rows(core._ngrams(words, 3), 3)
    issues = []
    heavy = [x for x in singles if x["density"] > 4 and x["count"] >= 8]
    if heavy:
        issues.append({"level": "medium", "title": f"\"{heavy[0]['term']}\" makes up {heavy[0]['density']}% of the words",
                       "detail": "That's high for natural writing. Google warns against keyword stuffing; use synonyms and related terms, and write for the reader."})
    top = (two or three or singles or [None])[0]
    if top and not top["in"] and (title or h1 or description):
        issues.append({"level": "low", "title": f"Your most-used phrase, \"{top['term']}\", isn't in the title, H1 or description",
                       "detail": "If that phrase is what the page is about, say so in the title and H1. If it isn't, the page may be drifting off topic."})
    if total < 300:
        issues.append({"level": "info", "title": f"Short text: {total} words", "detail": "Short pages can rank when they fully answer the search. Check that this one does."})
    verdict = "improve" if any(i["level"] == "medium" for i in issues) else "good"
    return {"title": title, "description": description, "h1": h1, "word_count": total, "unique_words": len(set(content)),
            "single": singles, "two": two, "three": three,
            "summary": {"verdict": verdict, "headline": "Some words are used very heavily" if verdict == "improve" else "Keyword use looks natural",
                        "issues": issues}}


def _markdown(src: str) -> dict:
    meta, body = {}, src
    fm = re.match(r"^---\n(.*?)\n---\n", src, re.S)          # front matter: title / description
    if fm:
        body = src[fm.end():]
        for k in ("title", "description"):
            m = re.search(rf"^{k}:\s*[\"']?(.*?)[\"']?\s*$", fm.group(1), re.M)
            if m:
                meta[k] = m.group(1)
    heads = re.findall(r"^(#{1,6})\s+(.*)$", body, re.M)
    h1 = " ".join(t for h, t in heads if len(h) == 1)
    text = re.sub(r"```.*?```", " ", body, flags=re.S)                # code blocks
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)                 # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)              # links → their text
    text = re.sub(r"[#>*_`|~-]+", " ", text)
    return {"text": text, "title": meta.get("title", h1), "description": meta.get("description", ""), "h1": h1,
            "headings": [t for h, t in heads if len(h) > 1]}


def _html(doc: str) -> dict:
    heads = core._headings(doc)
    body = re.sub(r"<(nav|footer|header|aside)\b.*?</\1>", " ", doc, flags=re.I | re.S)
    return {"text": core._visible_text(body), "title": core._title(doc) or "", "description": core._meta(doc, "name", "description") or "",
            "h1": " ".join(h["text"] for h in heads if h["level"] == 1), "headings": [h["text"] for h in heads if h["level"] > 1]}


def analyze_file(path: str) -> dict:
    p = Path(path)
    src = p.read_text(encoding="utf-8", errors="replace")
    parts = _html(src) if p.suffix.lower() in (".html", ".htm") else _markdown(src) if p.suffix.lower() in (".md", ".markdown", ".mdx") \
        else {"text": src, "title": "", "description": "", "h1": "", "headings": []}
    r = analyze_text(parts["text"], parts["title"], parts["description"], parts["headings"], parts["h1"], p.stem)
    return {"file": str(p), **r}


async def analyze_url(url: str) -> dict:
    return await core.check_keyword_density(url)


async def compare_urls(yours: str, theirs: str) -> dict:
    """Top 2-3 word phrases on the other page that aren't among your page's top words and phrases: topics to consider covering."""
    import asyncio
    a, b = await asyncio.gather(analyze_url(yours), analyze_url(theirs))
    return compare(a, b)


def compare(a: dict, b: dict) -> dict:
    mine = {x["term"] for k in ("single", "two", "three") for x in a[k]}
    gaps = [x for k in ("two", "three") for x in b[k] if x["term"] not in mine and not any(x["term"] in m or m in x["term"] for m in mine if " " in m)]
    shared = sorted({x["term"] for k in ("two", "three") for x in b[k]} & mine)
    return {"yours": {k: a.get(k) for k in ("url", "title", "word_count")}, "theirs": {k: b.get(k) for k in ("url", "title", "word_count")},
            "shared_phrases": shared, "their_top_phrases_not_in_yours": gaps}

"""keyword-density-checker <url-or-file> [--compare OTHER_URL] [--json] [--csv FILE]
Full visual report: https://www.cmoowls.com/tools/keyword-density-checker/
"""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import sys

from . import analyze_file, analyze_url, compare_urls


def _table(title: str, rows: list[dict]) -> None:
    print(f"\n{title}")
    if not rows:
        print("  (nothing used more than once)")
    for x in rows[:12]:
        where = ", ".join(x["in"]) if x["in"] else "-"
        print(f"  {x['term']:<34} {x['count']:>4}  {x['density']:>5.2f}%   in: {where}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="keyword-density-checker", description="Most-used words and 2-3 word phrases, their density, and where they appear.")
    p.add_argument("target", help="a page address (https://...) or a local .md, .html or .txt file")
    p.add_argument("--compare", metavar="OTHER_URL", help="compare a live page with another (e.g. a competitor's)")
    p.add_argument("--json", action="store_true", help="print the full result as JSON")
    p.add_argument("--csv", metavar="FILE", help="save every term with count, density and placement to a CSV file")
    a = p.parse_args(argv)
    try:
        if a.compare:
            r = asyncio.run(compare_urls(a.target, a.compare))
        elif os.path.isfile(a.target):
            r = analyze_file(a.target)
        else:
            r = asyncio.run(analyze_url(a.target))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False, default=str))
        return 0
    if a.compare:
        print(f"Yours:  {r['yours']['url']} ({r['yours']['word_count']} words)\nTheirs: {r['theirs']['url']} ({r['theirs']['word_count']} words)")
        print(f"\nShared top phrases: {', '.join(r['shared_phrases']) or 'none'}")
        print("\nTheir top phrases that aren't among yours (topics to consider):")
        for x in r["their_top_phrases_not_in_yours"][:15]:
            print(f"  {x['term']:<34} {x['count']:>4}  {x['density']:>5.2f}%")
        return 0
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["type", "term", "count", "density_percent", "also_in"])
            for k, label in (("single", "word"), ("two", "2-word phrase"), ("three", "3-word phrase")):
                for x in r[k]:
                    w.writerow([label, x["term"], x["count"], x["density"], ";".join(x["in"])])
    print(f"{r.get('final_url') or r.get('file')}\n{r['word_count']} words, {r['unique_words']} different  |  {r['summary']['headline']}")
    for i in r["summary"]["issues"]:
        print(f"  {i['level'].upper()}: {i['title']}")
    _table("Two-word phrases", r["two"]); _table("Three-word phrases", r["three"]); _table("Single words", r["single"])
    print("\nFull visual report: https://www.cmoowls.com/tools/keyword-density-checker/")
    return 0


if __name__ == "__main__":
    sys.exit(main())

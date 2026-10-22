import pytest

from keyword_density_checker import analyze_file, analyze_text, compare


def test_markdown_draft():
    r = analyze_file("examples/draft.md")
    assert r["title"].startswith("How to Choose Running Shoes")
    top = r["two"][0]
    assert top["term"] == "running shoes" and "title" in top["in"] and "h1" in top["in"]
    assert top["density"] == round(top["count"] * 2 / r["word_count"] * 100, 2)


def test_stuffing_flag():
    text = ("shoes " * 40) + " ".join(f"word{i}" for i in range(200))
    r = analyze_text(text, title="Shoes")
    assert r["summary"]["verdict"] == "improve"


def test_too_short():
    with pytest.raises(ValueError):
        analyze_text("just a few words here")


def test_compare_finds_their_top_phrases():
    a = {"single": [{"term": "shoes"}], "two": [{"term": "running shoes"}], "three": [], "url": "a", "title": "", "word_count": 500}
    b = {"single": [], "two": [{"term": "running shoes", "count": 5, "density": 1.0}, {"term": "trail grip", "count": 3, "density": 0.6}],
         "three": [], "url": "b", "title": "", "word_count": 600}
    r = compare(a, b)
    assert r["shared_phrases"] == ["running shoes"]
    assert [x["term"] for x in r["their_top_phrases_not_in_yours"]] == ["trail grip"]

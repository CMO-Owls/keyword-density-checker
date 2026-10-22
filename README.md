# Keyword Density Checker

**See which words and 2–3 word phrases a page really leans on, how much of the text each takes up, and whether the main ones appear in the title, H1, description and URL. Works on live pages and on drafts before you publish (Markdown, HTML or plain text), and can compare your page's phrases with a competitor's.**

```bash
pip install "git+https://github.com/CMO-Owls/keyword-density-checker.git"
keyword-density-checker drafts/new-post.md                       # a draft
keyword-density-checker https://example.com/blog/post/           # a live page
keyword-density-checker https://you.com/page/ --compare https://them.com/page/
```

No sign-up, no AI calls, MIT licensed. The same counting runs in the free [Keyword Density Checker](https://www.cmoowls.com/tools/keyword-density-checker/) on cmoowls.com, made by [CMO Owls](https://www.cmoowls.com/).

> **At a glance**
> - **Keyword density** is how often a term appears as a share of all the words on a page.
> - **There's no ideal percentage.** Google doesn't rank pages by density and warns against keyword stuffing. Use the numbers as a mirror: is the page about what its title says, and does any word sound repetitive?
> - **Two- and three-word phrases** say more about a page's topic than single words, so they're listed first.
> - **Check drafts, not just live pages:** catch a repetitive draft before it ships. Our example draft went from a flagged 5.16% to natural with a ten-minute rewrite.

## Contents

- [What keyword density is, and the formula](#what-keyword-density-is-and-the-formula)
- [Is keyword density a ranking factor?](#is-keyword-density-a-ranking-factor)
- [How to check a page or a draft](#how-to-check-a-page-or-a-draft)
- [Worked example: fixing a repetitive draft](#worked-example-fixing-a-repetitive-draft)
- [Compare two pages](#compare-two-pages)
- [How the counting works](#how-the-counting-works)
- [Use it from Python or CI](#use-it-from-python-or-ci)
- [What it can't tell you](#what-it-cant-tell-you)
- [FAQ](#faq)
- [Sources](#sources)

## What keyword density is, and the formula

**Keyword density = (times the term appears × words in the term ÷ total words) × 100.** Multiplying by the number of words in the term puts single words and phrases on one scale: it's the share of the text the term actually occupies.

| Example on a 1,200-word page | Count once | This tool |
|---|---|---|
| "shoes" used 18 times | 1.5% | 1.5% |
| "running shoes" used 9 times | 0.75% | **1.5%** |
| "trail running shoes" used 4 times | 0.33% | **1.0%** |

Many online checkers count a phrase once, which makes phrases look rarer than they are. Neither method is "right"; just compare like with like.

## Is keyword density a ranking factor?

**No, not as a number to hit.** Google's [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) says its "language matching systems are sophisticated and can understand how your page relates to many queries," and its [spam policies](https://developers.google.com/search/docs/essentials/spam-policies#keyword-stuffing) list "repeating the same words or phrases so often that it sounds unnatural" as keyword stuffing. Google answered the question directly in a 2011 Search Central video, ["What is the ideal keyword density of a page?"](https://www.youtube.com/watch?v=Rk4qgQdp2UA), and didn't give a target number. Language models such as [BERT](https://blog.google/products/search/search-language-understanding-bert/) let Google match searches worded differently from the page.

What still matters:

| Signal | What to check | Worth working on? |
|---|---|---|
| Keyword density | How much of the text one term takes up | Only to spot drift or stuffing |
| Placement | Main phrase in the title, H1, opening and URL | Yes: the page's clearest topic signals ([title links guidance](https://developers.google.com/search/docs/appearance/title-link)) |
| Topic coverage | The questions people ask about the topic are answered | Yes: what earns rankings and AI citations |

The tool flags a single word above 4% of the text (used at least 8 times) as worth a second look, and notes when your most-used phrase isn't in the title, H1 or description.

## How to check a page or a draft

1. **Install** (Python 3.10+):
   ```bash
   pip install "git+https://github.com/CMO-Owls/keyword-density-checker.git"
   ```
2. **Check a draft** before publishing. Markdown front matter (`title:`, `description:`) and `#` headings are read so placement can be checked:
   ```bash
   keyword-density-checker drafts/new-post.md
   ```
3. **Check a live page.** Menus, headers, footers, scripts and styles are left out, so you see the content:
   ```bash
   keyword-density-checker https://example.com/blog/post/
   ```
4. **Read the two-word phrases first.** The top one or two should describe the page. Then look at the `in:` column: your main phrase should appear in the title and H1.
5. **Save everything to a spreadsheet** with `--csv terms.csv`, or get the full result with `--json`.

## Worked example: fixing a repetitive draft

**[`examples/draft.md`](examples/draft.md) is a 213-word beginner's guide to running shoes, written the way first drafts often are.** The checker flags it:

```text
examples/draft.md
213 words, 78 different  |  Some words are used very heavily
  MEDIUM: "running" makes up 5.16% of the words

Two-word phrases
  running shoes                         9   8.45%   in: title, description, h1
```

"Running shoes" nine times in 213 words reads like it was written for a search engine. In [`examples/draft-revised.md`](examples/draft-revised.md) we kept the phrase in the title, H1, description and opening, and elsewhere used what a person would say: "pairs", "road shoes", "trail models", "new runners", "a model that matches your stride".

```text
examples/draft-revised.md
204 words, 86 different  |  Keyword use looks natural

Two-word phrases
  running shoes                         2   1.96%   in: title, description, h1
```

| | Draft | Revised |
|---|---:|---:|
| "running shoes" | 9 times (8.45%) | 2 times (1.96%) |
| Different words | 78 | 86 |
| Verdict | Some words used very heavily | Natural |

The topic signals didn't change: the phrase is still in every place that tells search engines what the page is about. The text just reads better, with more varied vocabulary.

## Compare two pages

**`--compare` lists the other page's top phrases that aren't among your page's top words and phrases**: topics they emphasise that you may be missing.

On 22 October 2026 we compared our [image SEO guide](https://www.cmoowls.com/blog/image-seo/) with [Google's image SEO documentation](https://developers.google.com/search/docs/appearance/google-images):

```text
Shared top phrases: alt text, google images, img element

Their top phrases that aren't among yours (topics to consider):
  search results                        9   0.87%
  img src                               7   0.68%
  structured data                       6   0.58%
  puppy jpg                             6   0.58%
  picture element                       5   0.48%
  ...
```

How to read it honestly:

- **Code samples count as text.** "img src" and "puppy jpg" come from the HTML examples in Google's page, not topics. Skip them.
- **The useful lines are topics:** "structured data" (image metadata in schema.org) and "picture element" (responsive images) are things the guide could cover in more depth.
- **It compares top phrases only**, not every word. A phrase in the list may appear on your page a few times, just not often enough to make your top list.

## How the counting works

1. **Text:** for live pages, the visible text of the HTML your server sends, with `nav`, `header`, `footer`, `aside`, scripts and styles removed. For drafts, Markdown is stripped of code blocks, images and link syntax; HTML files are read like live pages.
2. **Words:** lower-cased; numbers and common filler words (the, and, of, to, for, with…) are skipped for single words.
3. **Phrases:** every run of 2 and 3 words, skipping phrases that start or end with a filler word, so "the best" never appears.
4. **Placement:** each top term is looked up in the title, meta description (or front matter), H1, other headings and the URL path (or file name).

Live pages are fetched through the safe client in [free-seo-tools](https://github.com/CMO-Owls/free-seo-tools): public addresses only, every redirect re-checked, size and time limits.

## Use it from Python or CI

```python
import asyncio
from keyword_density_checker import analyze_file, analyze_url, compare_urls

draft = analyze_file("drafts/new-post.md")
print(draft["summary"]["headline"], draft["two"][:3])

gap = asyncio.run(compare_urls("https://you.com/page/", "https://them.com/page/"))
print([x["term"] for x in gap["their_top_phrases_not_in_yours"]])
```

In a docs or blog repository, a CI step can check every changed draft:

```yaml
- run: pip install "git+https://github.com/CMO-Owls/keyword-density-checker.git"
- run: for f in $(git diff --name-only origin/main -- '*.md'); do keyword-density-checker "$f"; done
```

## What it can't tell you

- **What people search for.** Pair it with Search Console's queries for the page (Performance → filter by page → Queries) to see what Google actually matches it to.
- **Text loaded by JavaScript** on live pages. Google can [render JavaScript](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics), but [Vercel's 2024 study](https://vercel.com/blog/the-rise-of-the-ai-crawler) found the major AI crawlers it measured don't, so text that needs scripts may be invisible to them too.
- **Word forms.** "Image" and "images" are counted separately.
- **Quality.** A page can have perfect numbers and still not answer the question. The [SEO Page Checker](https://www.cmoowls.com/tools/seo-page-checker/) covers the other on-page basics.

## FAQ

**What is a good keyword density?**
There isn't one. Make sure your main phrase is in the title, H1 and opening, write naturally, and use the checker to catch anything that sounds repetitive.

**How do I calculate keyword density?**
Divide the number of times a term appears by the total words and multiply by 100. For phrases, this tool also multiplies by the number of words in the phrase.

**Can I check a draft before I publish it?**
Yes. Point the checker at a `.md`, `.html` or `.txt` file. Markdown front matter titles and descriptions are used for the placement check.

**What is keyword stuffing?**
Repeating a word or phrase far more than natural writing would, or listing keywords out of context, to try to rank. Google's spam policies name it explicitly.

**Why doesn't my target keyword appear in the list?**
Either it's used fewer than two times, or the page uses variations instead (plurals, synonyms). If it's the page's main topic, use the exact phrase in the title, H1 and opening.

**How do I compare my page with a competitor's?**
Run `keyword-density-checker YOUR_URL --compare THEIR_URL`. It lists their top phrases that aren't among yours. Skip code fragments and look for real topics.

## Sources

- [Spam policies for Google web search: keyword stuffing](https://developers.google.com/search/docs/essentials/spam-policies#keyword-stuffing), Google Search Central, 2026
- [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide), Google Search Central, 2026
- [What is the ideal keyword density of a page?](https://www.youtube.com/watch?v=Rk4qgQdp2UA), Google Search Central on YouTube, 2011
- [Understanding searches better than ever before (BERT)](https://blog.google/products/search/search-language-understanding-bert/), Google, 2019
- [Influencing title links in Google Search](https://developers.google.com/search/docs/appearance/title-link), Google Search Central, 2026
- [Understand the JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics), Google Search Central, 2026
- [The rise of the AI crawler](https://vercel.com/blog/the-rise-of-the-ai-crawler), Vercel, 2024
- [Google image SEO best practices](https://developers.google.com/search/docs/appearance/google-images), Google Search Central, 2026

## Related

- [free-seo-tools](https://github.com/CMO-Owls/free-seo-tools): all 23 free SEO and AI-visibility tools as a Python package and CLI
- [Keyword Density Checker](https://www.cmoowls.com/tools/keyword-density-checker/), [Meta Tag Generator](https://www.cmoowls.com/tools/meta-tag-generator/) and [SEO competitor analysis](https://www.cmoowls.com/blog/seo-competitor-analysis/) on cmoowls.com

---

Made by [CMO Owls](https://www.cmoowls.com/): 21 specialized AI marketing agents that work from one shared strategy. MIT licensed.

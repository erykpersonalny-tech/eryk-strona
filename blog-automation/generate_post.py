#!/usr/bin/env python3
"""
Generator wpisów na bloga erykpersonalny.pl.

Co robi:
  1. Bierze pierwszy nieużyty temat z topics.json.
  2. Robi research na temat (web search) i pisze wpis wg style-guide.md.
  3. Wypełnia post-template.html -> zapisuje blog-<slug>.html.
  4. Wpina nową kartę na górze sekcji blog w index.html.
  5. Oznacza temat jako użyty w topics.json.

Uruchamiany przez GitHub Action co 2 tygodnie. Zmiany trafiają do
Pull Requesta, który akceptujesz (merge) albo poprawiasz. Nic nie
publikuje się bez Twojego merge'a.

Wymaga zmiennej środowiskowej ANTHROPIC_API_KEY.
Opcjonalnie UNSPLASH_ACCESS_KEY (auto-dobór zdjęcia).
"""

import os
import re
import sys
import json
import datetime
import urllib.parse
import urllib.request

import anthropic

# ---------------------------------------------------------------- Konfiguracja
MODEL = "claude-sonnet-5"  # model API; w razie potrzeby podmień na inny dostępny

REPO_ROOT = os.environ.get("REPO_ROOT", ".")
BASE = os.path.join(REPO_ROOT, "blog-automation")
STYLE_GUIDE_PATH = os.path.join(BASE, "style-guide.md")
TEMPLATE_PATH = os.path.join(BASE, "post-template.html")
TOPICS_PATH = os.path.join(BASE, "topics.json")
INDEX_PATH = os.path.join(REPO_ROOT, "index.html")

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
# Bezpieczny fallback, gdy nie ma klucza Unsplash — podmienisz przy review.
FALLBACK_HERO = "https://images.unsplash.com/photo-1517836357463-d25dfeac3438"

# Instrukcja formatu wyjścia doklejana do style guide jako system prompt.
OUTPUT_INSTRUCTIONS = """
---

# ZADANIE

Napisz jeden wpis na bloga wg powyższego przewodnika. Najpierw zrób
research (użyj web search, żeby liczby i fakty były aktualne i zgodne
z mainstreamem nauki oraz z rosterem zaufanych źródeł).

Potem zwróć odpowiedź DOKŁADNIE w tym formacie: najpierw pola metadanych
(każde w jednej linii jako "KLUCZ: wartość"), potem osobna linia
---CONTENT--- i pod nią treść artykułu jako czysty HTML. Żadnego tekstu
przed TITLE ani po treści. Bez ```-ów.

TITLE: Tytuł wpisu (bez " | Blog Eryk Jóskowski" — to dokleja szablon)
META: 1 zdanie, 140-160 znaków, z frazą kluczową, bez clickbaitu
CATEGORY: Trening | Dieta | Motywacja (dokładnie jedna z tych trzech)
READING_TIME: 9
HERO_QUERY: 2-4 angielskie słowa do wyszukania zdjęcia, np. man gym workout
HERO_ALT: krótki polski opis zdjęcia (atrybut alt)
EXCERPT: 1-2 zdania zajawki na kartę na stronie głównej, zakończone wielokropkiem...
CTA_HEADING: Nagłówek sekcji CTA
CTA_TEXT: 1 zdanie zachęty pod nagłówkiem CTA
CTA_BUTTON: Tekst na przycisku (krótki)
---CONTENT---
<p>Pierwszy akapit wpisu...</p>
... dalsza treść artykułu ...

ZASADY dla metadanych:
- Każde pole w JEDNEJ linii, dokładnie z tymi kluczami (wielkie litery).
- Nie pomijaj żadnego pola. READING_TIME to sama liczba.

ZASADY dla treści (wszystko pod ---CONTENT---):
- To ma być TYLKO wnętrze diva .article-content: znaczniki <p>, <h2>,
  <h3>, <strong>, <ul>/<ol>/<li> oraz komponenty highlight-box,
  tip-box, myth-box, reality-box (dokładnie jak w przewodniku).
- NIE dodawaj <html>, <head>, <body>, nagłówka artykułu, zdjęcia ani
  sekcji CTA — te elementy dokłada szablon automatycznie.
- Dokładnie JEDNO podsumowanie, JEDNA ściągawka, ZERO sekcji CTA w treści.
- Długość: 1500-2400 słów. Ton i struktura ściśle wg przewodnika.
- Ikony w komponentach: klasy Font Awesome (np. <i class="fas fa-fire"></i>).
"""

POLISH_MAP = str.maketrans({
    "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o",
    "ś": "s", "ź": "z", "ż": "z",
    "Ą": "a", "Ć": "c", "Ę": "e", "Ł": "l", "Ń": "n", "Ó": "o",
    "Ś": "s", "Ź": "z", "Ż": "z",
})


def slugify(text: str) -> str:
    text = text.translate(POLISH_MAP).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:60] or "wpis"


def read_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def pick_topic(topics_data: dict):
    for t in topics_data["topics"]:
        if not t.get("used"):
            return t
    return None


def fetch_hero(query: str):
    """Zwraca (url_1200, url_400). Bez klucza Unsplash -> fallback."""
    if not UNSPLASH_ACCESS_KEY:
        return FALLBACK_HERO + "?w=1200", FALLBACK_HERO + "?w=400"
    try:
        url = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode(
            {"query": query, "per_page": 1, "orientation": "landscape"}
        )
        req = urllib.request.Request(
            url, headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.load(resp)
        raw = data["results"][0]["urls"]["raw"]
        return f"{raw}&w=1200", f"{raw}&w=400"
    except Exception as e:  # degradacja do fallbacku, nie wywalaj całości
        print(f"[hero] Unsplash nie zadziałał ({e}); używam fallbacku", file=sys.stderr)
        return FALLBACK_HERO + "?w=1200", FALLBACK_HERO + "?w=400"


def generate_article(topic: dict) -> dict:
    """Woła API i zwraca sparsowany słownik z polami wpisu."""
    client = anthropic.Anthropic()  # klucz z ANTHROPIC_API_KEY
    system = read_file(STYLE_GUIDE_PATH) + "\n" + OUTPUT_INSTRUCTIONS
    user = (
        f"Temat: {topic['topic']}\n"
        f"Kategoria: {topic['category']}\n"
        f"Fraza kluczowa (ma paść w tytule, 1. akapicie, jednym <h2> i meta): "
        f"{topic['keyword']}"
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        system=system,
        messages=[{"role": "user", "content": user}],
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 5}],
    )

    # Zbierz tekst ze wszystkich bloków tekstowych (reszta to bloki web search).
    raw = "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()

    article = parse_output(raw)
    article["sources"] = extract_sources(response)
    return article


def extract_sources(response) -> list:
    """Wyciąga PRAWDZIWE źródła z cytowań web search (nie zmyślone przez model).

    Web search dokleja do bloków tekstu obiekty citation z realnym url/title
    stron, które faktycznie wyszukał. Bierzemy je, deduplikujemy po URL.
    """
    seen = {}
    for block in response.content:
        for c in getattr(block, "citations", None) or []:
            url = getattr(c, "url", None)
            if url and url not in seen:
                seen[url] = getattr(c, "title", None) or url
    return [{"url": u, "title": t} for u, t in seen.items()]


def build_sources_html(sources: list) -> str:
    """Sekcja 'Źródła' na końcu wpisu. Pusta lista -> nic nie dodaje."""
    if not sources:
        return ""
    items = "\n".join(
        f'            <li><a href="{s["url"]}" target="_blank" rel="noopener">{s["title"]}</a></li>'
        for s in sources
    )
    return "\n\n        <h2>Źródła</h2>\n        <ul>\n" + items + "\n        </ul>"


def format_sources_md(sources: list) -> str:
    """Lista źródeł do opisu PR-a (Markdown)."""
    if not sources:
        return "_Brak — model nie skorzystał z web search. Sprawdź, czy statystyki mają pokrycie._"
    return "\n".join(f"- [{s['title']}]({s['url']})" for s in sources)


META_KEYS = {
    "TITLE": "title",
    "META": "meta_description",
    "CATEGORY": "category",
    "READING_TIME": "reading_time",
    "HERO_QUERY": "hero_query",
    "HERO_ALT": "hero_alt",
    "EXCERPT": "excerpt",
    "CTA_HEADING": "cta_heading",
    "CTA_TEXT": "cta_text",
    "CTA_BUTTON": "cta_button",
}


def parse_output(raw: str) -> dict:
    """Rozbija odpowiedź na metadane (KLUCZ: wartość) + treść HTML.

    Odporne na cudzysłowy w HTML: treść bierzemy dosłownie, nic nie
    escape'ujemy (w przeciwieństwie do JSON, gdzie każdy " w HTML psuł parsowanie).
    """
    marker = "---CONTENT---"
    if marker not in raw:
        raise ValueError(f"Brak znacznika ---CONTENT--- w odpowiedzi modelu:\n{raw[:500]}")
    head, content = raw.split(marker, 1)

    article = {}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if not sep:
            continue
        mapped = META_KEYS.get(key.strip().upper())
        if mapped:
            article[mapped] = value.strip()

    missing = [v for v in META_KEYS.values() if v not in article]
    if missing:
        raise ValueError(f"Brak pól metadanych: {missing}\nGłowa odpowiedzi:\n{head[:500]}")

    # Treść: zdejmij ewentualne ```html ... ``` i białe znaki na brzegach.
    content = re.sub(r"^```(?:html)?\s*|\s*```$", "", content.strip()).strip()
    article["content_html"] = content
    return article


def fill_template(article: dict, hero_1200: str) -> str:
    tpl = read_file(TEMPLATE_PATH)
    repl = {
        "{{META_DESCRIPTION}}": article["meta_description"],
        "{{TITLE}}": article["title"],
        "{{CATEGORY}}": article["category"],
        "{{READING_TIME}}": str(article["reading_time"]),
        "{{HERO_QUERY}}": article.get("hero_query", ""),
        "{{HERO_IMAGE_URL}}": hero_1200,
        "{{HERO_ALT}}": article.get("hero_alt", article["title"]),
        "{{CONTENT}}": article["content_html"],
        "{{CTA_HEADING}}": article["cta_heading"],
        "{{CTA_TEXT}}": article["cta_text"],
        "{{CTA_BUTTON}}": article["cta_button"],
        "{{YEAR}}": str(datetime.date.today().year),
    }
    for k, v in repl.items():
        tpl = tpl.replace(k, v)
    return tpl


def insert_card(article: dict, slug: str, hero_400: str) -> None:
    """Wpina nową kartę na górze .blog-grid (najnowsze pierwsze)."""
    index = read_file(INDEX_PATH)
    anchor = '<div class="blog-grid">'
    if anchor not in index:
        raise ValueError('Nie znaleziono <div class="blog-grid"> w index.html')

    card = (
        f'\n            <a href="blog-{slug}.html" style="text-decoration: none; color: inherit;">\n'
        f'                <div class="blog-card">\n'
        f'                    <img src="{hero_400}" alt="Blog">\n'
        f'                    <div class="blog-content">\n'
        f'                        <span class="blog-tag">{article["category"]}</span>\n'
        f'                        <h3 class="blog-title">{article["title"]}</h3>\n'
        f'                        <p class="blog-excerpt">{article["excerpt"]}</p>\n'
        f'                    </div>\n'
        f'                </div>\n'
        f'            </a>'
    )
    index = index.replace(anchor, anchor + card, 1)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(index)


def mark_used(topics_data: dict, topic_id: int) -> None:
    for t in topics_data["topics"]:
        if t["id"] == topic_id:
            t["used"] = True
    with open(TOPICS_PATH, "w", encoding="utf-8") as f:
        json.dump(topics_data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> None:
    topics_data = json.loads(read_file(TOPICS_PATH))
    topic = pick_topic(topics_data)
    if topic is None:
        print("Brak nieużytych tematów w topics.json — nic do zrobienia.")
        # Sygnał dla workflow: nie otwieraj PR.
        _set_output("created", "false")
        return

    print(f"Generuję wpis: {topic['topic']}")
    article = generate_article(topic)
    slug = slugify(article["title"])
    hero_1200, hero_400 = fetch_hero(article.get("hero_query", topic["category"]))

    # Doklej sekcję "Źródła" (z prawdziwych cytowań web search) na koniec treści.
    article["content_html"] += build_sources_html(article["sources"])

    post_path = os.path.join(REPO_ROOT, f"blog-{slug}.html")
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(fill_template(article, hero_1200))

    insert_card(article, slug, hero_400)
    mark_used(topics_data, topic["id"])

    print(f"Gotowe: blog-{slug}.html + karta na index.html")
    print(f"Źródeł z web search: {len(article['sources'])}")
    _set_output("created", "true")
    _set_output("title", article["title"])
    _set_output("slug", slug)
    _set_output_multiline("sources", format_sources_md(article["sources"]))


def _set_output(key: str, value: str) -> None:
    """Przekazuje wartości do kroków GitHub Actions."""
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")


def _set_output_multiline(key: str, value: str) -> None:
    """Wieloliniowa wartość do GITHUB_OUTPUT (składnia z separatorem)."""
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        import uuid
        delim = f"EOF_{uuid.uuid4().hex}"
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"{key}<<{delim}\n{value}\n{delim}\n")


if __name__ == "__main__":
    main()

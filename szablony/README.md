# Szablony dokumentów dla klientów (PDF)

Używane przez skille `zalozenia-klienta` i `analiza-dzienniczka`.

```bash
bash szablony/setup.sh                                   # raz: fonty Inter + Roboto (npm @fontsource)
node szablony/render.js szablony/zalozenia.html dane.json Zalozenia_Imie.pdf
node szablony/render.js szablony/analiza.html  dane.json Analiza-dzienniczka-Imie.pdf
```

Struktura danych: `zalozenia.przyklad.json`, `analiza.przyklad.json` (dane fikcyjne).
Wymaga Node + Playwright (Chromium). Szablony nie zawierają danych klientów – i tak ma zostać.

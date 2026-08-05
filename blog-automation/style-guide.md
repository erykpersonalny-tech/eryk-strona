# Style Guide + Szablon — Blog erykpersonalny.pl

Przewodnik dla automatu generującego wpisy. Zakodowany głos, struktura, format i zasady, które sprawiają, że wpis brzmi jak Eryk, a nie jak dowolny trener z internetu.

---

## 1. GŁOS I TON — to jest serce marki

Zasada nadrzędna: **piszesz jak człowiek, który sam przez to przeszedł, do osób, które dopiero zaczynają i mają małe doświadczenie.** Bezpośrednio, szczerze, ciekawie, czasem anegdotycznie, czasem „trafiając w ból", ale nigdy z góry.

**Rób tak:**
- Otwieraj scenką z elementami dobrego storytellingu, nie definicją. („Styczeń. Wszyscy na siłowni." / „Pamiętam swój pierwszy raz na siłowni." / „Dieta sokowa. Keto. Paleo.")
- Mów do czytelnika przez „Ty". Zwracaj się bezpośrednio.
- Bądź szczery tam, gdzie inni owijają w bawełnę. („Spoiler: to nie takie proste.")
- Używaj własnego doświadczenia jako autorytetu — to Twoje E-E-A-T. („Popełniałem je wszystkie. Niektóre wielokrotnie.")
- Dawaj konkret: liczby, proporcje, protokoły, gotowe do wdrożenia dziś.
- Szukaj ciekawych porównań i nawiązań. („Bilans kaloryczny jest jak budżet domowy…")
- Obalaj mity — to Twój ulubiony i najmocniejszy chwyt.

**Nie rób tak:**
- Żadnego korpo-marketingu ani „eksperckiego" dystansu. Zero „Niniejszy artykuł ma na celu…".
- Nie pouczaj z góry — jesteś przewodnikiem, który sam błądził, nie belfrem.
- Nie obiecuj cudów ani szybkich efektów (to podważa wiarygodność i szkodzi SEO w kategorii zdrowotnej).
- Nie lej wody. Każdy akapit musi coś wnosić.
- Nie używaj zapożyczeń z angielskiego — WYJĄTEK: utrwalone terminy treningowe/dietetyczne bez dobrego polskiego odpowiednika (np. plank, deadlift, cardio, deficyt). Zwykłe angielskie ozdobniki („spoiler", „easy", „it's physics not magic") dalej odpadają.

---

## 2. STRUKTURA WPISU

1. **Hook (2-4 krótkie akapity)** — scenka, prowokacja albo osobiste wspomnienie. Wciąga w pierwszym zdaniu. Bez rozgrzewki.
2. **Zwrot / teza** — postaw sprawę jasno, często wbrew obiegowej opinii. („Wina braku motywacji? Nie.")
3. **Rdzeń: 5-8 ponumerowanych sekcji** (`<h2>`) — każdy punkt to jeden błąd / nawyk / strategia. W środku `<h3>` z pytaniem („Co robić zamiast tego?", „Dlaczego to ważne?") + konkret.
4. **Podsumowanie** — sekcja „Podsumowanie" z **jedną** ściągawką (lista z ✓). UWAGA: dokładnie jedno podsumowanie, jedna ściągawka, jedno CTA (patrz błąd w sekcji 7).
5. **CTA** — `cta-section` kierujące na darmowy trening / kontakt.

Długość docelowa: **8-10 min czytania (~1500-2400 słów).** Zgodna z istniejącymi wpisami.

---

## 3. SEO / META (pola do wypełnienia w `<head>`)

- **`<title>`**: `[Tytuł Wpisu] | Blog Eryk Jóskowski` — tytuł konkretny, z obietnicą albo prowokacją, zawiera frazę kluczową. (np. „Zdrowe Nawyki Żywieniowe: Bez Diety-Cud i Głupot")
- **`<meta name="description">`**: 1 zdanie, 140-160 znaków, zawiera frazę kluczową, mówi co czytelnik zyska. Bez clickbaitu.
- **`article-category`**: jedna z: `Trening`, `Dieta`, `Motywacja` (dodawaj nowe tylko świadomie — kategorie to nawigacja).
- **`article-meta`**: `[X] min czytania · Eryk Jóskowski` — czas czytania liczony realnie (~200 słów/min).
- **Fraza kluczowa** = pytanie, które klient (facet 20-30, nadwaga, wstyd, ma 3-5 h/tydzień) wpisuje w Google. Fraza pada w tytule, w pierwszym akapicie, w jednym `<h2>` i w meta description — naturalnie, bez upychania.

---

## 4. KOMPONENTY HTML — kiedy używać którego

- **`highlight-box`** (zielony pasek z boku) — kluczowy wniosek / złota zasada. Najczęstszy. 2-4 na wpis.
- **`tip-box`** (ramka z ikoną FontAwesome) — praktyczna wskazówka do wdrożenia od ręki, lista źródeł, protokół.
- **`myth-box`** (czerwony) — obalenie mitu. Format: `MIT: … / FAKT: …`. Używaj przy treściach żywieniowych/treningowych, gdzie krąży bzdura.
- **`reality-box`** (pomarańczowy) — zmiana myślenia / brutalna prawda / przeformułowanie („Nie mam motywacji" → „mam system").

Zasada: **każda dłuższa sekcja ma minimum jeden komponent.** Ściana tekstu = źle. Ale nie przesadzaj — komponent ma podkreślać puentę, nie zastępować treść.

Ikony: FontAwesome (już podpięte w `<head>`). Dobieraj sensownie (`fa-fire`, `fa-bed`, `fa-drumstick-bite`, `fa-tint`, `fa-brain`, `fa-users` itd.).

---

## 5. GUARDRAILS — dokładność i wiarygodność (kategoria zdrowotna!)

Fitness i odżywianie to dla Google kategoria YMYL — treści są oceniane surowiej. Dlatego:

- **Fakty i liczby muszą być poprawne.** Zapotrzebowanie na białko, kalorie, proporcje — trzymaj się mainstreamu nauki (np. białko 1,6-2,2 g/kg przy treningu). Żadnych zmyślonych badań ani „badania pokazują" bez pokrycia — kieruj się zdaniem uznanych fachowców i renomowanych badań, np.: Tadeusz Sowiński, Michał Wrzosek, Damian Parol, Dr Mike Israetel, Lyle McDonald, Eric Helms, Menno Henselmans, Revive Stronger, Layne Norton, Sergiusz Grzemny, Mikołaj z GainzDesire, Paweł Głuchowski, Piotr Tomaszewski, Dietetyka NieNaŻarty, Brad Schoenfeld.
- **Każda statystyka musi mieć pokrycie w web search.** Nie podawaj konkretnych liczb ani procentów bez realnie znalezionego źródła. Nie zmyślaj danych „dla efektu".
- **Preferuj naukę nad marketingiem.** Meta-analizy, badania i eksperci z rosteru > ankiety sieci fitness i portali. Jeśli już użyjesz ankiety komercyjnej, nazwij ją po imieniu („ankieta sieci X") — nie podawaj jej tonem twardego badania naukowego.
- **Źródła jawne.** Automat dołącza na końcu wpisu sekcję „Źródła" z prawdziwymi linkami (z wyników web search) i wypisuje je w opisie PR-a — po to, żebyś mógł sprawdzić każdą liczbę, zanim klikniesz merge.
- **Zero obietnic medycznych i cudów.** Nie „wyleczysz", nie „-10 kg w tydzień".
- **Twoje doświadczenie = autorytet**, ale nie udawaj lekarza. Przy tematach zdrowotnych dorzuć rozsądne zastrzeżenie (skonsultuj z lekarzem, jeśli masz schorzenia).
- **Ten guardrail jest powodem, dla którego zostaje bramka akceptacji** — automat pisze draft, ale to Ty firmujesz liczby swoim nazwiskiem.

---

## 6. SZABLON HTML — gotowy szkielet do wypełnienia

Automat wypełnia pola `{{...}}` i wstawia treść w `{{CONTENT}}` (znaczniki `<p>`, `<h2>`, `<h3>`, listy i komponenty z sekcji 4). CSS jest kompletny — zawiera wszystkie cztery typy ramek, więc każdy wpis ma czym operować.

```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{{META_DESCRIPTION}}">
    <title>{{TITLE}} | Blog Eryk Jóskowski</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" />
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --neon-green: #00ff88;
            --dark-green: #00cc6a;
            --black: #0a0a0a;
            --white: #ffffff;
            --gray: #cccccc;
        }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: var(--black); color: var(--white); overflow-x: hidden; line-height: 1.6; }

        .gradient-bg { position: fixed; width: 100%; height: 100%; background: linear-gradient(135deg, #000000 0%, #0a0a0a 50%, #1a1a1a 100%); z-index: -2; }
        .orbs { position: fixed; width: 100%; height: 100%; z-index: -1; overflow: hidden; }
        .orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.4; animation: float 20s infinite ease-in-out; }
        .orb1 { width: 600px; height: 600px; background: linear-gradient(135deg, var(--neon-green), var(--dark-green)); top: -200px; left: -200px; }
        .orb2 { width: 500px; height: 500px; background: linear-gradient(135deg, var(--neon-green), #66ffaa); bottom: -150px; right: -150px; animation-delay: 7s; }
        @keyframes float { 0%, 100% { transform: translate(0, 0) scale(1); } 33% { transform: translate(100px, -100px) scale(1.1); } 66% { transform: translate(-100px, 100px) scale(0.9); } }

        .back-button { position: fixed; top: 30px; left: 30px; z-index: 1000; display: inline-flex; align-items: center; gap: 10px; padding: 12px 24px; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 50px; color: var(--neon-green); text-decoration: none; font-weight: 600; font-size: 14px; transition: all 0.3s; box-shadow: 0 4px 20px rgba(0, 255, 136, 0.2); }
        .back-button:hover { background: rgba(0, 255, 136, 0.1); border-color: var(--neon-green); transform: translateX(-5px); box-shadow: 0 6px 30px rgba(0, 255, 136, 0.4); }
        .back-button i { font-size: 16px; }
        @media (max-width: 768px) { .back-button { top: 20px; left: 20px; padding: 10px 20px; font-size: 13px; } }

        .article-header { padding: 100px 50px 60px; text-align: center; max-width: 900px; margin: 0 auto; }
        .article-category { display: inline-block; padding: 8px 20px; background: rgba(0, 255, 136, 0.1); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 20px; color: var(--neon-green); font-size: 14px; margin-bottom: 20px; }
        .article-title { font-size: 48px; margin-bottom: 20px; background: linear-gradient(135deg, var(--white), var(--neon-green)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 900; line-height: 1.2; }
        .article-meta { color: var(--gray); font-size: 16px; }

        .article-image { max-width: 1200px; margin: 40px auto; border-radius: 20px; overflow: hidden; }
        .article-image img { width: 100%; height: auto; display: block; }

        .article-content { max-width: 800px; margin: 0 auto; padding: 40px 50px 100px; }
        .article-content p { color: var(--gray); font-size: 18px; line-height: 1.9; margin-bottom: 25px; }
        .article-content h2 { color: var(--white); font-size: 32px; margin: 50px 0 20px; background: linear-gradient(135deg, var(--neon-green), var(--white)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
        .article-content h3 { color: var(--neon-green); font-size: 24px; margin: 35px 0 15px; }
        .article-content strong { color: var(--neon-green); font-weight: 600; }
        .article-content ul, .article-content ol { margin: 20px 0 25px 30px; color: var(--gray); font-size: 18px; }
        .article-content li { margin-bottom: 12px; line-height: 1.8; }

        .highlight-box { background: rgba(0, 255, 136, 0.05); border-left: 4px solid var(--neon-green); padding: 25px 30px; margin: 35px 0; border-radius: 10px; }
        .highlight-box p { color: var(--white); margin-bottom: 0; font-size: 17px; }

        .tip-box { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(0, 255, 136, 0.2); padding: 25px 30px; margin: 35px 0; border-radius: 15px; }
        .tip-box h4 { color: var(--neon-green); margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .tip-box p { margin-bottom: 0; }

        .myth-box { background: rgba(255, 50, 50, 0.05); border: 1px solid rgba(255, 50, 50, 0.3); padding: 25px 30px; margin: 35px 0; border-radius: 15px; }
        .myth-box h4 { color: #ff3232; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .myth-box p { margin-bottom: 0; }

        .reality-box { background: rgba(255, 150, 0, 0.05); border: 1px solid rgba(255, 150, 0, 0.3); padding: 25px 30px; margin: 35px 0; border-radius: 15px; }
        .reality-box h4 { color: #ff9600; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .reality-box p { margin-bottom: 0; }

        .cta-section { text-align: center; padding: 60px 40px; background: rgba(0, 255, 136, 0.03); border-radius: 20px; margin: 60px 0; border: 1px solid rgba(0, 255, 136, 0.2); }
        .cta-section h3 { font-size: 32px; margin-bottom: 15px; color: var(--white); }
        .cta-section p { color: var(--gray); margin-bottom: 25px; font-size: 18px; }
        .cta-button { display: inline-block; padding: 18px 45px; background: linear-gradient(135deg, var(--neon-green), var(--dark-green)); color: var(--black); text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 18px; transition: all 0.3s; }
        .cta-button:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(0, 255, 136, 0.5); }

        footer { text-align: center; padding: 40px; background: rgba(0, 0, 0, 0.8); border-top: 1px solid rgba(0, 255, 136, 0.2); color: var(--gray); }

        @media (max-width: 768px) {
            .article-header { padding: 80px 20px 40px; }
            .article-title { font-size: 32px; }
            .article-content { padding: 30px 20px 60px; }
            .article-content h2 { font-size: 26px; }
            .article-content p, .article-content ul, .article-content ol { font-size: 16px; }
        }
    </style>
</head>
<body>
    <div class="gradient-bg"></div>
    <div class="orbs"><div class="orb orb1"></div><div class="orb orb2"></div></div>

    <a href="index.html#blog" class="back-button">
        <i class="fas fa-arrow-left"></i>
        Powrót
    </a>

    <div class="article-header">
        <span class="article-category">{{CATEGORY}}</span>
        <h1 class="article-title">{{TITLE}}</h1>
        <div class="article-meta">
            <i class="far fa-clock"></i> {{READING_TIME}} min czytania · Eryk Jóskowski
        </div>
    </div>

    <div class="article-image">
        <img src="{{HERO_IMAGE_URL}}" alt="{{HERO_ALT}}">
    </div>

    <div class="article-content">
        {{CONTENT}}

        <div class="cta-section">
            <h3>{{CTA_HEADING}}</h3>
            <p>{{CTA_TEXT}}</p>
            <a href="index.html#kontakt" class="cta-button">{{CTA_BUTTON}}</a>
        </div>
    </div>

    <footer>
        <p>&copy; {{YEAR}} Eryk Jóskowski - Trener Personalny</p>
    </footer>
</body>
</html>
```

---

## 7. WAŻNE: bramka akceptacji zostaje — dowód z Twojego bloga

W pliku `blog-motywacja.html` istniejąca treść ma **zdublowaną końcówkę**: po pierwszym „Podsumowanie: Sukces to System" + ściągawce + CTA cały blok podsumowania i CTA powtarza się drugi raz (jako „Podsumowanie: Motywacja Jest Dla Amatorów"), a między nimi jest urwany fragment `</div>% przypadków…`. To klasyczny błąd copy-paste, który przeszedł niezauważony do publikacji.

Wniosek dla automatu: **jeden wpis = dokładnie jedno podsumowanie, jedna ściągawka, jedno CTA.** I dlatego etap „przejrzenie → korekta → merge" nie jest formalnością — nawet ręczny proces potrafi puścić taki błąd. Automat generuje, Ty firmujesz.

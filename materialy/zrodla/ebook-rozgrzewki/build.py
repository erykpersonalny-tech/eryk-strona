"""Buduje HTML e-booka „Rozgrzewki RAMP”. Użycie: python3 build.py > rozgrzewki.html"""
import html, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from dane import EX, CHAPTERS

e = html.escape

CSS = """
@page { size: A4; margin: 0; }
:root { --black:#0a0a0a; --ink:#141614; --green:#00ff88; --green-ink:#0a9d5a; --mint:#bff5dc; --mint-bg:#ecfdf4; --grey:#5c625e; --line:#e3e7e4; --soft:#f4f6f5; --warn:#d9480f; --warn-bg:#fff3ec; }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:"Inter",Arial,sans-serif; color:var(--ink); font-size:10px; line-height:1.42; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
b { font-weight:700; } a { color:inherit; }
.page { width:210mm; height:297mm; position:relative; overflow:hidden; display:flex; flex-direction:column; break-after:page; }
.dark { background:var(--black); color:#fff; position:relative; overflow:hidden; }
.dark::after { content:""; position:absolute; right:-60px; top:-90px; width:420px; height:320px; background:radial-gradient(closest-side, rgba(0,255,136,.28), rgba(0,255,136,0)); pointer-events:none; }
.dark > * { position:relative; z-index:1; }
.brand { display:flex; align-items:center; gap:10px; font-size:8.5px; font-weight:800; letter-spacing:.3em; color:var(--green); text-transform:uppercase; }
.brand i { width:6px; height:20px; border-radius:3px; background:var(--green); display:block; }
.rule { height:1px; background:rgba(0,255,136,.45); margin:6px 0 8px; }
.eyebrow { font-size:7.5px; font-weight:800; letter-spacing:.22em; text-transform:uppercase; color:var(--green-ink); }
.foot { flex:none; height:10mm; padding:0 12mm; display:flex; align-items:center; justify-content:space-between; font-size:7px; letter-spacing:.22em; color:#8b918d; text-transform:uppercase; }
.body { flex:1; padding:7mm 11mm 0; display:flex; flex-direction:column; gap:9px; }
.card { border:1px solid var(--line); border-radius:12px; padding:11px 14px; break-inside:avoid; }
.card.mint { border-color:var(--mint); background:var(--mint-bg); }
.card.warn { background:var(--warn-bg); border-color:#f6c9b0; } .card.warn .eyebrow { color:var(--warn); }
ul.dots { list-style:none; display:grid; gap:4px; margin-top:6px; }
ul.dots li { position:relative; padding-left:12px; }
ul.dots li::before { content:""; position:absolute; left:0; top:6px; width:5px; height:5px; border-radius:50%; background:var(--green-ink); }
h2 { font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:-.01em; }
/* okładka */
.cover { flex:1; padding:22mm 16mm 16mm; display:flex; flex-direction:column; }
.cover h1 { font-size:46px; font-weight:900; line-height:1; text-transform:uppercase; margin-top:28mm; letter-spacing:-.02em; }
.cover h1 em { font-style:normal; color:var(--green); }
.cover .lead { margin-top:9mm; font-size:13px; color:#d8dcd9; max-width:150mm; line-height:1.5; }
.ramp-big { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:auto; }
.ramp-big div { border:1px solid rgba(0,255,136,.4); border-radius:12px; padding:12px; }
.ramp-big b { display:block; font-size:30px; font-weight:900; color:var(--green); line-height:1; }
.ramp-big span { font-size:10px; color:#d8dcd9; text-transform:uppercase; letter-spacing:.12em; font-weight:700; }
.chips { display:flex; gap:8px; margin-top:8mm; }
.chip { border:1px solid rgba(0,255,136,.5); border-radius:999px; padding:5px 13px; font-size:9px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; color:var(--green); }
/* intro */
.phase { display:grid; grid-template-columns:44px 1fr 70px; gap:12px; align-items:start; padding:8px 0; border-top:1px solid var(--line); }
.phase:first-of-type { border-top:0; }
.letter { width:44px; height:44px; border-radius:10px; background:var(--black); color:var(--green); font-weight:900; font-size:15px; display:flex; align-items:center; justify-content:center; }
.phase h3 { font-size:11.5px; font-weight:800; }
.phase .t { font-weight:800; color:var(--green-ink); text-align:right; font-size:10.5px; }
table { width:100%; border-collapse:collapse; font-size:9.6px; }
th { text-align:left; font-size:7.4px; letter-spacing:.18em; text-transform:uppercase; color:var(--green-ink); padding:4px 6px; border-bottom:1.5px solid var(--ink); }
td { padding:5px 6px; border-bottom:1px solid var(--line); vertical-align:top; }
td.c { font-weight:800; white-space:nowrap; }
.idx td:first-child { width:34px; }
.idx a { text-decoration:none; font-weight:700; }
/* zestaw */
.sethead { padding:9mm 12mm 7mm; }
.sethead .top { display:flex; align-items:center; justify-content:space-between; }
.setid { font-size:11px; font-weight:900; color:var(--black); background:var(--green); border-radius:6px; padding:3px 9px; letter-spacing:.06em; }
.sethead h1 { font-size:27px; font-weight:900; text-transform:uppercase; margin-top:7px; letter-spacing:-.01em; }
.sethead p { margin-top:4px; color:#d8dcd9; font-size:10.5px; }
.timechip { border:1px solid rgba(0,255,136,.5); border-radius:999px; padding:4px 12px; font-size:9px; font-weight:800; letter-spacing:.14em; color:var(--green); text-transform:uppercase; }
.ph { border:1px solid var(--line); border-radius:12px; overflow:hidden; break-inside:avoid; }
.ph-head { display:flex; align-items:center; gap:10px; padding:8px 14px; background:var(--soft); }
.ph-head .l { min-width:28px; padding:0 5px; height:28px; border-radius:7px; background:var(--black); color:var(--green); font-weight:900; font-size:11px; display:flex; align-items:center; justify-content:center; }
.ph-head h3 { font-size:11.5px; font-weight:800; text-transform:uppercase; letter-spacing:.06em; flex:1; }
.ph-head span { font-size:8.6px; color:var(--grey); }
.row { display:grid; grid-template-columns:20px 1fr 120px 86px; gap:12px; align-items:center; padding:10px 14px; border-top:1px solid var(--line); }
.row .n { font-weight:800; color:var(--green-ink); }
.row .nm { font-weight:700; font-size:12px; }
.row .cue { color:var(--grey); font-size:10px; margin-top:2px; }
.row .dose { font-weight:800; font-size:11px; text-align:right; }
a.vid { display:inline-block; text-align:center; font-size:8.8px; font-weight:800; color:var(--green-ink); text-decoration:none; border:1px solid var(--mint); background:var(--mint-bg); border-radius:999px; padding:3px 8px; }
.ramprow { padding:10px 14px; border-top:1px solid var(--line); background:var(--mint-bg); font-size:9.4px; }
.ramprow b { color:var(--green-ink); }
"""


PH = [("R", "Rozgrzanie", "2–3 min",
       "2–3 minuty na dowolnym przyrządzie do cardio: ergometr wioślarski, orbitrek, rowerek lub bieżnia – wybierasz to, co lubisz. Podnosisz tętno i temperaturę ciała – ma być Ci ciepło, a nie ciężko."),
      ("A+M", "Mobilność i przygotowanie", "4–6 min",
       "3–5 ćwiczeń dobranych do treningu: zwiększasz zakres ruchu w stawach, które zaraz będą pracować, i przygotowujesz je do obciążenia. Ruchy spokojne i kontrolowane, bez zmęczenia."),
      ("P", "Pobudzenie i serie wstępne", "3–5 min",
       "Krótkie ćwiczenie dynamiczne, a potem serie wstępne pierwszego ćwiczenia z rosnącym ciężarem. To najważniejsza część rozgrzewki – nie pomijaj jej.")]
NSETS = sum(len(c[3]) for c in CHAPTERS)
NDAY = sum(len(c[3]) for c in CHAPTERS if c[0] not in ("PROBLEMY", "EKSPRES"))


def aid(x):
    return "a-" + x.lower().replace("ó", "o").replace("ł", "l")


def foot(right="erykpersonalny.pl"):
    return f'<div class="foot"><span>Eryk Jóskowski · Trener personalny · Rumia</span><span>{right}</span></div>'


def head_html():
    fonts = "".join(f'<link rel="stylesheet" href="fonts/inter/{w}.css">' for w in (400, 500, 700, 800, 900))
    extra = """.chap-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
a.chap { display:block; text-decoration:none; border:1px solid var(--line); border-radius:12px; padding:13px 14px; }
a.chap .k { display:inline-block; font-size:10px; font-weight:900; color:var(--black); background:var(--green); border-radius:6px; padding:3px 9px; letter-spacing:.06em; }
a.chap h3 { font-size:14px; font-weight:900; text-transform:uppercase; margin-top:8px; }
a.chap p { color:var(--grey); margin-top:3px; }
a.chap .ids { margin-top:7px; font-size:9px; font-weight:700; color:var(--green-ink); }
a.chap.sos { background:var(--warn-bg); border-color:#f6c9b0; } a.chap.sos .k { background:var(--warn); color:#fff; }
.chaphead { padding:12mm 12mm 9mm; }
.chaphead h1 { font-size:34px; font-weight:900; text-transform:uppercase; margin-top:10px; letter-spacing:-.01em; }
.chaphead h1 em { font-style:normal; color:var(--green); }
.chaphead p { margin-top:6px; color:#d8dcd9; font-size:11.5px; max-width:160mm; }
.bigid { font-size:54px !important; line-height:1; margin-top:4px !important; color:var(--green); letter-spacing:.02em !important; }
.sethead .sub { font-size:13px; color:#fff; font-weight:700; margin-top:4px; }
.back { font-size:8.6px; font-weight:800; color:var(--green-ink); text-decoration:none; }"""
    return f'<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>Rozgrzewki RAMP – Eryk Jóskowski</title>{fonts}<style>{CSS}{extra}</style></head><body>'


def cover():
    tiles = "".join(f'<div><b>{l}</b><span>{t}</span></div>' for l, t, _, _ in PH)
    return f'''<div class="page"><div class="dark cover">
  <div class="brand"><i></i>Eryk Jóskowski · Trener personalny</div><div class="rule"></div>
  <h1>Rozgrzewki<br><em>przed treningiem</em><br>siłowym</h1>
  <p class="lead">{NDAY} gotowych zestawów pod Twój dzień treningowy – góra, dół, FBW, push i pull – oraz osobny rozdział na sytuacje problemowe i dni, gdy brakuje czasu. Każdy zestaw według protokołu RAMP, 8–15 minut, z filmem do każdego ćwiczenia.</p>
  <div class="chips"><span class="chip">Góra · Dół · FBW</span><span class="chip">Push · Pull</span><span class="chip">8–15 min</span></div>
  <div class="ramp-big" style="grid-template-columns:repeat(3,1fr)">{tiles}</div>
</div></div>'''


def intro():
    ph = "".join(f'''<div class="phase"><div class="letter">{l}</div><div><h3>{t}</h3><p>{d}</p></div><div class="t">{tm}</div></div>''' for l, t, tm, d in PH)
    return f'''<div class="page"><div class="body" style="padding-top:12mm">
  <div><div class="eyebrow">Jak korzystać z e-booka</div><h2 style="margin-top:4px">Protokół RAMP w praktyce</h2></div>
  <div class="card">{ph}</div>
  <div class="card mint"><div class="eyebrow">Serie wstępne – faza P</div>
    <p style="margin-top:6px">Ostatni krok każdej rozgrzewki to kilka serii pierwszego ćwiczenia z treningu, z rosnącym ciężarem. Liczba powtórzeń spada, ciężar rośnie – żadna seria nie męczy. Przerwy 60–90 s.</p>
    <table style="margin-top:8px"><tr><th>Seria</th><th>Gdy pracujesz na 1–6 powt.</th><th>Gdy pracujesz na 6–12 powt.</th></tr>
      <tr><td class="c">1</td><td>pusty gryf / bardzo lekko × 8–10</td><td>ok. 50% ciężaru roboczego × 8</td></tr>
      <tr><td class="c">2</td><td>ok. 40% × 6–8</td><td>ok. 70% × 4–5</td></tr>
      <tr><td class="c">3</td><td>ok. 60% × 4–5</td><td>–</td></tr>
      <tr><td class="c">4</td><td>ok. 75% × 2–3</td><td>–</td></tr>
      <tr><td class="c">5</td><td>ok. 85–90% × 1–2</td><td>–</td></tr></table>
    <p style="margin-top:6px;color:var(--grey)">„Wersja rozszerzona” (ciężkie dni siły) = wszystkie 5 serii z lewej kolumny, przed bardzo ciężkimi seriami jeszcze 1 × 1 na ok. 90–95%.</p></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:9px">
    <div class="card"><div class="eyebrow">Jak wybrać zestaw</div><ul class="dots"><li>Numer rozgrzewki (np. <b>FB3</b>) znajdziesz w swoim planie treningowym w HubFit.</li><li>Kliknij rozdział w spisie treści i przejdź do zestawu o tym numerze.</li><li>Zestawy <b>Problemy</b> i <b>Ekspres</b> stosujesz tylko wtedy, gdy wpiszę je w plan.</li></ul></div>
    <div class="card"><div class="eyebrow">Zasady</div><ul class="dots">
      <li>Ćwiczenia robisz po kolei, bez długich przerw.</li>
      <li>Kolejność jest ułożona tak, żeby nie wstawać i kłaść się co chwilę.</li>
      <li>Filmy otwierasz, klikając <b>▶ Wideo</b>.</li>
      <li>Rozgrzewka ma rozgrzać, a nie zmęczyć.</li></ul></div>
  </div>
  <div class="card warn"><div class="eyebrow">Uwaga</div><p style="margin-top:5px">Ćwiczenia mają być bez bólu. Kłucie, drętwienie lub ból w stawie – przerwij i daj mi znać. Sprzęt: wolne ciężary, guma oporowa, mini-band, wałek i własna masa ciała.</p></div>
</div>{foot("2")}</div>'''


def index():
    tiles = ""
    for code, name, desc, sets in CHAPTERS:
        ids = " · ".join(s["id"] for s in sets)
        tiles += f'<a class="chap{" sos" if code in ("PROBLEMY", "EKSPRES") else ""}" href="#{aid('ch-' + code)}"><span class="k">{code}</span><h3>{e(name)}</h3><p>{e(desc)}</p><div class="ids">{len(sets)} {"zestawy" if len(sets) in (2,3,4) else "zestawów"}: {ids}</div></a>'
    return f'''<div class="page"><div class="body" style="padding-top:12mm">
  <div><div class="eyebrow">Spis treści</div><h2 style="margin-top:4px">Jaki masz dzisiaj trening?</h2>
  <p style="margin-top:4px;color:var(--grey)">Kliknij rozdział – przeniesie Cię do listy zestawów.</p></div>
  <div class="chap-grid">{tiles}</div>
</div>{foot("3")}</div>'''


def chapter_page(code, name, desc, sets, pages, pageno):
    named = code in ("PROBLEMY", "EKSPRES")
    rows = "".join(f'<tr><td class="c"><a href="#{aid(s['id'])}">{s["id"]}</a></td>{(f'<td><a href="#{aid(s["id"])}"><b>{e(s["title"])}</b></a></td>' if named else "")}<td class="c">{s["time"]}</td><td class="c">str. {pages[s["id"]]}</td></tr>' for s in sets)
    return f'''<div class="page" id="{aid('ch-' + code)}">
  <div class="dark chaphead"><div class="brand"><i></i>Rozdział · {code}</div><div class="rule"></div>
    <h1>{e(name.split(" (")[0]).replace("Dzień ", "Dzień <em>", 1) + ("</em>" if name.startswith("Dzień ") else "")}</h1><p>{e(desc)}</p></div>
  <div class="body"><div class="card"><table class="idx"><tr><th>Zestaw</th>{"<th></th>" if named else ""}<th>Czas</th><th></th></tr>{rows}</table></div>
  <a class="back" href="#spis">‹ wróć do spisu treści</a></div>{foot(str(pageno))}</div>'''


def set_page(s, chap, pageno, named=False):
    def rows(items, start):
        out = ""
        for i, (k, dose) in enumerate(items, start):
            name, url, cue = EX[k]
            out += f'<div class="row"><span class="n">{i}</span><div><div class="nm">{e(name)}</div><div class="cue">{e(cue)}</div></div><div class="dose">{e(dose)}</div>{(f'<a class="vid" href="{url}">▶ Wideo</a>' if url else "<span></span>")}</div>'
        return out
    n_r, n_am = len(s["R"]), len(s["AM"])
    (l1, t1, m1, _), (l2, t2, m2, _), (l3, t3, m3, _) = PH
    return f'''<div class="page" id="{aid(s['id'])}">
  <div class="dark sethead"><div class="top"><div class="brand"><i></i>Rozgrzewka · {e(chap)}</div><span class="timechip">{s["time"]}</span></div>
    <div class="rule"></div>
    <h1 class="bigid">{s["id"]}</h1>{(f'<p class="sub">{e(s["title"])}</p>' if named else "")}</div>
  <div class="body">
    <div class="ph"><div class="ph-head"><div class="l">{l1}</div><h3>{t1}</h3><span>{m1}</span></div>{rows(s["R"], 1)}</div>
    <div class="ph"><div class="ph-head"><div class="l">{l2}</div><h3>{t2}</h3><span>{m2}</span></div>{rows(s["AM"], n_r + 1)}</div>
    <div class="ph"><div class="ph-head"><div class="l">{l3}</div><h3>{t3}</h3><span>{m3}</span></div>{rows(s["P"], n_r + n_am + 1)}
      <div class="ramprow"><b>Serie wstępne:</b> {e(s["ramp"])} – według tabeli ze strony 2.</div></div>
    <a class="back" style="margin-top:auto;margin-bottom:3mm" href="#spis">‹ wróć do spisu treści</a>
  </div>{foot(str(pageno))}</div>'''


def build():
    pages, p = {}, 4
    for code, name, desc, sets in CHAPTERS:
        pages["ch-" + code] = p; p += 1
        for s in sets:
            pages[s["id"]] = p; p += 1
    out = [head_html(), cover(), intro(), index().replace('<div class="page">', '<div class="page" id="spis">', 1)]
    for code, name, desc, sets in CHAPTERS:
        out.append(chapter_page(code, name, desc, sets, pages, pages["ch-" + code]))
        chap = name.split(" (")[0].replace("Dzień ", "dzień ").replace("Problemy", "problemy")
        for s in sets:
            out.append(set_page(s, chap, pages[s["id"]], code in ("PROBLEMY", "EKSPRES")))
    out.append("</body></html>")
    return "".join(out)


if __name__ == "__main__":
    sys.stdout.write(build())

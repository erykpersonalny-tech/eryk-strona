"""Buduje jadłospisy 1800 i 2500 kcal (HTML -> PDF) z data.py."""
import html
from pathlib import Path
from playwright.sync_api import sync_playwright
from data import PLANS

OUT = Path(__file__).parent
e = html.escape

CSS = """
@page { size: A4; margin: 0; }
:root { --black:#0a0a0a; --green:#00ff88; --green-ink:#0a9d5a; --mint:#bff5dc; --mint-bg:#ecfdf4; --grey:#5c625e; --line:#e3e7e4; }
* { box-sizing:border-box; margin:0; padding:0; }
body { font-family:"Inter",-apple-system,"Helvetica Neue",Arial,sans-serif; color:#121412; font-size:10.5px; line-height:1.45;
       -webkit-print-color-adjust:exact; print-color-adjust:exact; }
b { font-weight:700; }
.page { width:210mm; height:297mm; position:relative; overflow:hidden; page-break-after:always; display:flex; flex-direction:column; }
.page:last-child { page-break-after:auto; }
.hero { background:var(--black); color:#fff; position:relative; overflow:hidden; padding:11mm 12mm 9mm; }
.hero::after { content:""; position:absolute; right:-60px; top:-90px; width:420px; height:320px; background:radial-gradient(closest-side, rgba(0,255,136,.28), rgba(0,255,136,0)); }
.hero > * { position:relative; z-index:1; }
.brand { display:flex; align-items:center; gap:10px; font-size:8.5px; font-weight:800; letter-spacing:.3em; color:var(--green); text-transform:uppercase; }
.brand i { width:6px; height:20px; border-radius:3px; background:var(--green); display:block; }
.rule { height:1px; background:rgba(0,255,136,.45); margin:6px 0 8px; }
h1 { font-size:30px; font-weight:900; line-height:1.05; text-transform:uppercase; letter-spacing:-.01em; }
.chips { display:flex; gap:8px; margin-top:10px; flex-wrap:wrap; }
.chip { border:1px solid rgba(0,255,136,.5); border-radius:999px; padding:4px 12px; font-size:8.5px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; color:var(--green); }
.chip.grey { border-color:rgba(255,255,255,.25); color:#d8dcd9; }
.tiles { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-top:12px; }
.tile { border:1px solid rgba(255,255,255,.14); background:rgba(255,255,255,.04); border-radius:10px; padding:8px; text-align:center; }
.tile small { display:block; font-size:7px; letter-spacing:.14em; text-transform:uppercase; color:#b9bfbb; font-weight:800; }
.tile b { display:block; font-size:21px; font-weight:900; line-height:1.15; }
.tile span { font-size:7.5px; color:var(--green); font-weight:700; }
.tile.on { background:linear-gradient(135deg,var(--green),#00cc6a); border:0; color:var(--black); }
.tile.on small, .tile.on span { color:var(--black); }
.body { zoom:var(--z,1); flex:1; padding:7mm 9.5mm 0; display:flex; flex-direction:column; gap:9px; }
.card { border:1.2px solid var(--mint); border-radius:13px; padding:12px 14px; }
.card.dark { background:var(--black); color:#fff; border:0; position:relative; overflow:hidden; }
.card.dark::after { content:""; position:absolute; right:-30px; top:-50px; width:240px; height:180px; background:radial-gradient(closest-side, rgba(0,255,136,.22), rgba(0,255,136,0)); }
.card.dark > * { position:relative; z-index:1; }
.card.mint { background:var(--mint-bg); }
.ch { display:flex; align-items:center; gap:10px; margin-bottom:7px; }
.ico { width:26px; height:26px; border-radius:7px; background:var(--black); display:flex; align-items:center; justify-content:center; flex:none; }
.ico svg { width:14px; height:14px; stroke:var(--green); fill:none; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }
.card.dark .ico { background:var(--green); } .card.dark .ico svg { stroke:var(--black); }
.ch h2 { font-size:13.5px; font-weight:900; text-transform:uppercase; letter-spacing:.02em; }
.blocks { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-top:8px; }
.blocks div { background:var(--mint-bg); border:1px solid var(--mint); border-radius:9px; padding:6px; text-align:center; }
.blocks small { display:block; font-size:7.5px; letter-spacing:.14em; color:var(--green-ink); font-weight:800; text-transform:uppercase; }
ul.dots { list-style:none; display:grid; gap:4px; }
ul.dots li { position:relative; padding-left:11px; }
ul.dots li::before { content:""; position:absolute; left:0; top:5.5px; width:5px; height:5px; border-radius:50%; background:var(--green); }
.card:not(.dark) ul.dots li::before { background:var(--green-ink); }
table { width:100%; border-collapse:collapse; }
th { font-size:7.5px; letter-spacing:.14em; text-transform:uppercase; text-align:left; padding:4px 0; border-bottom:2px solid var(--black); color:#333; }
td { padding:6px 0; border-bottom:1px solid var(--line); }
td.p { color:var(--green-ink); font-weight:800; }
.foot-note { font-size:8.5px; color:var(--grey); margin-top:7px; }
.swap { display:flex; gap:10px; align-items:flex-start; }
.footer { height:12mm; background:var(--black); color:#fff; display:flex; align-items:center; justify-content:space-between; padding:0 12mm; margin-top:8px; }
.footer .who { display:flex; align-items:center; gap:10px; font-weight:900; font-size:11px; letter-spacing:.06em; }
.footer .who i { width:5px; height:18px; border-radius:3px; background:var(--green); display:block; }
.footer .meta { font-size:7.5px; letter-spacing:.2em; color:#a9aea9; font-weight:700; }
/* strony dni */
.dayhero { padding:8mm 12mm 7mm; }
.dayhero .top { display:flex; justify-content:space-between; align-items:center; }
.dayhero .blk { color:#9aa09c; font-weight:800; font-size:12px; }
.dayhero h1 { font-size:26px; }
.meal { border:1.2px solid var(--mint); border-radius:12px; padding:9px 13px 10px; }
.mh { display:flex; align-items:center; gap:9px; }
.tag { border:1px solid var(--mint); background:var(--mint-bg); color:var(--green-ink); border-radius:999px; padding:2px 9px; font-size:7.5px; font-weight:800; letter-spacing:.14em; text-transform:uppercase; }
.mh h3 { flex:1; font-size:12px; font-weight:800; }
.kc { background:var(--green); color:var(--black); border-radius:5px; padding:2px 7px; font-weight:900; font-size:8.5px; }
.mac { background:var(--black); color:#fff; border-radius:5px; padding:2px 7px; font-weight:800; font-size:8.5px; }
.mb { display:grid; grid-template-columns:1fr 1.15fr; gap:16px; margin-top:6px; }
.eb { font-size:7.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--green-ink); font-weight:800; margin-bottom:3px; }
ol.steps { list-style:none; display:grid; gap:4px; counter-reset:s; }
ol.steps li { counter-increment:s; display:flex; gap:8px; align-items:flex-start; }
ol.steps li::before { content:counter(s); flex:none; width:15px; height:15px; border-radius:4px; border:1px solid var(--mint); background:var(--mint-bg); color:var(--green-ink); font-weight:800; font-size:8px; display:flex; align-items:center; justify-content:center; margin-top:1px; }
.shake { border:1.2px dashed var(--mint); background:var(--mint-bg); border-radius:12px; padding:9px 13px; }
.shake .row { display:flex; gap:10px; align-items:center; }
.shake .row p { flex:1; }
.shake .alt { margin-top:6px; padding-top:6px; border-top:1px dashed var(--mint); font-size:9.5px; color:#2f3431; }
.total { display:flex; justify-content:space-between; align-items:center; background:var(--black); color:#fff; border-radius:10px; padding:8px 14px; font-weight:800; }
.total span { color:var(--green); }
/* co dalej */
.big { font-size:15px; font-weight:900; }
a { color:inherit; }
.cta { display:inline-block; margin-top:8px; background:var(--green); color:var(--black); border-radius:8px; padding:6px 12px; font-weight:900; text-decoration:none; font-size:10px; }
"""

ICON = {
 "clock": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "fork": '<svg viewBox="0 0 24 24"><path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M16 3c-2 2-2 6 0 8v10"/></svg>',
 "chart": '<svg viewBox="0 0 24 24"><path d="M5 20V10M12 20V4M19 20v-7"/></svg>',
 "swap": '<svg viewBox="0 0 24 24"><path d="M7 7h12l-3-3M17 17H5l3 3"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}

def footer():
    return ('<div class="footer"><div class="who"><i></i>ERYK JÓSKOWSKI</div>'
            '<div class="meta">TRENER PERSONALNY · RUMIA · ERYKPERSONALNY.PL</div></div>')

def card_head(icon, title):
    return f'<div class="ch"><div class="ico">{ICON[icon]}</div><h2>{e(title)}</h2></div>'

def swap_line(text, grams):
    has_water = "wody" in text
    skyr = int(round(grams * 7.5 / 10.0) * 10)
    water = " – i daj ok. połowę wody" if has_water else ""
    if grams <= 25:
        kefir = grams * 20
        return f'<b>Bez odżywki?</b> Zamiast {grams} g odżywki dodaj {skyr} g skyra naturalnego albo {kefir} ml kefiru{water}.'
    return f'<b>Bez odżywki?</b> Zamiast {grams} g odżywki dodaj {skyr} g skyra naturalnego{water}.'

def cover(k, p):  # strona 1
    t = p["targets"]
    rows = "".join(f'<tr><td><b>{e(d)}</b></td><td>{kc}</td><td class="p">{b} g</td><td>{w} g</td><td>{tt} g</td></tr>'
                   for d, kc, b, w, tt in p["summary"])
    return f'''
<section class="page" style="--z:1.07">
  <div class="hero">
    <div class="brand"><i></i>Eryk Jóskowski · Trener personalny</div>
    <div class="rule"></div>
    <h1>Jadłospis 7-dniowy<br>{p["kcal"]} kcal</h1>
    <div class="chips"><span class="chip">25 % B · 30 % T · 45 % W</span><span class="chip grey">Proste przepisy · gotowanie raz na 2 dni</span></div>
    <div class="tiles">
      <div class="tile on"><small>Kalorie</small><b>{p["kcal"]}</b><span>kcal / dzień</span></div>
      <div class="tile"><small>Białko 25 %</small><b>{t["B"][0]}</b><span>g · {t["B"][1]} kcal</span></div>
      <div class="tile"><small>Tłuszcz 30 %</small><b>{t["T"][0]}</b><span>g · {t["T"][1]} kcal</span></div>
      <div class="tile"><small>Węglow. 45 %</small><b>{t["W"][0]}</b><span>g · {t["W"][1]} kcal</span></div>
    </div>
  </div>
  <div class="body">
    <div class="card">{card_head("clock", "Jak zbudowany jest ten jadłospis")}
      <p>Tydzień podzielony jest na <b>3 bloki po 2 dni</b> + 1 dzień samodzielny. W ramach bloku gotujesz raz — wieczorem przed pierwszym dniem bloku — i jesz to samo przez 2 dni. Każdy dzień to <b>3 posiłki + szejk</b>.</p>
      <div class="blocks"><div><small>Blok A</small><b>Dzień 1–2</b></div><div><small>Blok B</small><b>Dzień 3–4</b></div><div><small>Blok C</small><b>Dzień 5–6</b></div><div><small>Dzień 7</small><b>Samodzielny</b></div></div>
    </div>
    <div class="card dark">{card_head("fork", "Zasady przygotowania")}
      <ul class="dots">
        <li>Mięso, ryby, kasze, ryż, makaron i ziemniaki gotuj w podwójnej ilości — starczy na 2 dni, przechowuj w lodówce w zamkniętych pojemnikach.</li>
        <li>Jajka, kanapki, tortille i owsiankę składaj na świeżo — każde z nich to maksymalnie 10 minut.</li>
        <li>Gramatury podane są dla produktów surowych/sypkich przed ugotowaniem. Przyprawy dobieraj według własnego uznania.</li>
        <li>Owoce w szejkach możesz swobodnie wymieniać między sobą (maliny, borówki, mango, truskawki) — kaloryka pozostaje zbliżona.</li>
      </ul>
    </div>
    <div class="card mint">{card_head("swap", "Nie masz odżywki białkowej?")}
      <p>Szejk zrobisz bez niej. <b>Zamiast każdych 10 g odżywki dodaj 75 g skyra naturalnego</b> – białko i kaloryka zostają praktycznie bez zmian. Możesz też użyć <b>200 ml kefiru</b> zamiast każdych 10 g odżywki – białka będzie odrobinę mniej, a kaloryka wzrośnie o ok. 60 kcal. W szejkach na wodzie daj wtedy ok. połowę wody. Dokładne ilości znajdziesz pod każdym szejkiem.</p>
    </div>
    <div class="card">{card_head("chart", "Podsumowanie tygodnia")}
      <table><tr><th>Dzień</th><th>Kcal</th><th>Białko</th><th>Węglow.</th><th>Tłuszcz</th></tr>{rows}</table>
      <p class="foot-note">Wartości kaloryczne i makroskładniki są orientacyjne – ten sam produkt u różnych producentów może różnić się o kilka–kilkanaście procent. Jeśli liczysz dokładnie, sprawdzaj etykiety produktów, które kupujesz.</p>
    </div>
  </div>
  {footer()}
</section>'''

def day_page(k, d):
    meals = ""
    for typ, name, kcal, (b, w, t), ing, steps in d["meals"]:
        meals += f'''
    <div class="meal"><div class="mh"><span class="tag">{e(typ)}</span><h3>{e(name)}</h3><span class="kc">{kcal} kcal</span><span class="mac">B {b} · W {w} · T {t}</span></div>
      <div class="mb"><div><div class="eb">Składniki (1 porcja)</div><ul class="dots">{"".join(f"<li>{e(x)}</li>" for x in ing)}</ul></div>
      <div><div class="eb">Przygotowanie</div><ol class="steps">{"".join(f"<li>{e(x)}</li>" for x in steps)}</ol></div></div></div>'''
    s_txt, s_kcal, (sb, sw, st), s_g = d["shake"]
    tk, tb, tw, tt = d["total"]
    return f'''
<section class="page" style="--z:1.2">
  <div class="hero dayhero">
    <div class="top"><div class="brand"><i></i>Jadłospis {k} kcal</div><div class="blk">{e(d["block"])}</div></div>
    <div class="rule"></div>
    <h1>{e(d["title"])}</h1>
    <div class="chips"><span class="chip">{e(d["note"])}</span></div>
  </div>
  <div class="body">{meals}
    <div class="shake"><div class="row"><span class="tag" style="background:#fff">Szejk</span><p>{e(s_txt)}</p><span class="kc">{s_kcal} kcal</span><span class="mac">B {sb} · W {sw} · T {st}</span></div>
      <div class="alt">{swap_line(s_txt, s_g)}</div></div>
    <div class="total">Razem / dzień<div><span>{tk} kcal</span> · B {tb} g · W {tw} g · T {tt} g</div></div>
  </div>
  {footer()}
</section>'''

def next_page(k):
    return f'''
<section class="page">
  <div class="hero">
    <div class="brand"><i></i>Eryk Jóskowski · Trener personalny</div>
    <div class="rule"></div>
    <h1>Co dalej?</h1>
    <p style="margin-top:8px; color:#dfe3e0; font-size:12px; max-width:150mm">Masz za sobą tydzień konkretnego jedzenia. Najważniejsze teraz: nie wracać do starych nawyków od poniedziałku – tylko zrobić z tego stały rytm.</p>
  </div>
  <div class="body">
    <div class="card">{card_head("arrow", "Jak wykorzystać ten jadłospis dalej")}
      <ul class="dots">
        <li><b>Powtarzaj bloki.</b> Masz 4 gotowe zestawy dni – możesz je układać w kolejnych tygodniach w dowolnej kolejności.</li>
        <li><b>Wymieniaj posiłki w obrębie tej samej pory dnia.</b> Śniadanie z bloku A zamiast śniadania z bloku C – kaloryka zostaje podobna.</li>
        <li><b>Obserwuj masę ciała przez 2–3 tygodnie</b>, ważąc się kilka razy w tygodniu rano. Liczy się średnia, nie pojedynczy pomiar.</li>
        <li><b>Głód, brak energii albo waga stoi w miejscu?</b> To sygnał, że kaloryczność trzeba dopasować do Ciebie – i tu mogę pomóc.</li>
      </ul>
    </div>
    <div class="grid" style="display:grid; grid-template-columns:1fr 1fr; gap:9px">
      <div class="card dark"><div class="eb" style="color:var(--green)">Rumia i okolice</div><p class="big">Pierwszy trening gratis</p>
        <p style="margin-top:5px; color:#dfe3e0">Poznajmy się na sali. Sprawdzimy technikę, porozmawiamy o celu i ułożymy plan – treningowy i żywieniowy.</p>
        <a class="cta" href="https://erykpersonalny.pl/#kontakt">Umów trening</a></div>
      <div class="card dark"><div class="eb" style="color:var(--green)">Cała Polska</div><p class="big">Współpraca online</p>
        <p style="margin-top:5px; color:#dfe3e0">Indywidualny plan treningowy i żywieniowy dopasowany do Twojego dnia, stały kontakt i cotygodniowe podsumowania w aplikacji.</p>
        <a class="cta" href="https://erykpersonalny.pl/#kontakt">Napisz do mnie</a></div>
    </div>
    <div class="card mint">{card_head("arrow", "Zaczynasz z siłownią?")}
      <p>Pobierz mój darmowy plan <b>„Pierwsze 4 tygodnie na siłowni”</b> – checklista pierwszej wizyty, 2 treningi całego ciała z wideo i rozpiska tydzień po tygodniu.</p>
      <a class="cta" href="https://erykpersonalny.pl/4-tygodnie/">erykpersonalny.pl/4-tygodnie</a>
    </div>
    <div class="card">{card_head("arrow", "Masz pytanie?")}
      <p>Odpisz na dowolnego maila ode mnie – czytam i odpowiadam osobiście. Możesz też napisać na <b>kontakt@erykpersonalny.pl</b> lub zadzwonić: <b>+48 577 243 692</b>.</p>
    </div>
    <p class="foot-note" style="margin-top:auto">Jadłospis ma charakter ogólny i edukacyjny. Nie zastępuje indywidualnej porady dietetyka ani lekarza – w przypadku chorób, ciąży, alergii lub nietolerancji pokarmowych skonsultuj zmiany ze specjalistą. © Eryk Jóskowski.</p>
  </div>
  {footer()}
</section>'''

def build(k):
    p = PLANS[k]
    title = f"Jadłospis 7-dniowy {k} kcal – Eryk Jóskowski"
    doc = (f'<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>{e(title)}</title>'
           f'<meta name="author" content="Eryk Jóskowski"><style>{CSS}</style></head><body>'
           + cover(k, p) + "".join(day_page(k, d) for d in p["days"]) + next_page(k) + '</body></html>')
    hp = OUT / f"jadlospis-{k}.html"; hp.write_text(doc, encoding="utf-8")
    pdf = OUT / f"Jadlospis-7-dni-{k}-kcal.pdf"
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(); pg.goto(hp.as_uri()); pg.wait_for_load_state("networkidle")
        over = pg.evaluate("""[...document.querySelectorAll('.page')].map((p,i)=>{const b=p.querySelector('.body'),f=p.querySelector('.footer');
            const last=[...b.children].pop(); return Math.round(f.getBoundingClientRect().top-last.getBoundingClientRect().bottom)})""")
        pg.pdf(path=str(pdf), format="A4", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        b.close()
    # metadane PDF
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(str(pdf)); w = PdfWriter(clone_from=r)
    w.add_metadata({"/Title": title, "/Author": "Eryk Jóskowski", "/Subject": "Jadłospis 7-dniowy z przepisami"})
    with open(pdf, "wb") as f: w.write(f)
    print(k, "wolne px na stronach:", over)
    return pdf

if __name__ == "__main__":
    for k in PLANS: build(k)

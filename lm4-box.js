/*
 * Okienko „Pierwsze 4 tygodnie na siłowni” na końcu wpisów blogowych.
 * Użycie we wpisie (przed .cta-section):
 *   <div id="lm4-box"></div><script src="/lm4-box.js" defer></script>
 * Treść i wygląd zmieniasz tylko tutaj – działa we wszystkich wpisach naraz.
 */
(function () {
  'use strict';
  var box = document.getElementById('lm4-box');
  if (!box) return;

  var css = '' +
    '#lm4-box{margin:60px 0 0}' +
    '.lm4b{display:grid;grid-template-columns:1fr 190px;gap:28px;align-items:center;padding:36px;border-radius:20px;' +
    'background:linear-gradient(135deg,rgba(0,255,136,.08),rgba(0,255,136,.02));border:1px solid rgba(0,255,136,.35);position:relative;overflow:hidden}' +
    '.lm4b-tag{display:inline-block;padding:5px 14px;border-radius:20px;border:1px solid rgba(0,255,136,.35);background:rgba(0,255,136,.1);' +
    'color:#00ff88;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase}' +
    '.lm4b h3{margin:14px 0 8px !important;font-size:28px !important;line-height:1.15;color:#fff !important;text-transform:uppercase;font-weight:900;' +
    '-webkit-text-fill-color:#fff !important;background:none !important}' +
    '.lm4b h3 span{color:#00ff88;-webkit-text-fill-color:#00ff88}' +
    '.lm4b p.lm4b-sub{color:#ccc;font-size:16px !important;line-height:1.6 !important;margin:0 0 16px !important}' +
    '.lm4b-form{display:grid;grid-template-columns:1fr 1fr;gap:10px}' +
    '.lm4b-form input[type=text],.lm4b-form input[type=email]{width:100%;box-sizing:border-box;padding:14px 18px;border-radius:50px;font-size:16px;' +
    'background:rgba(255,255,255,.06);border:1px solid rgba(0,255,136,.25);color:#fff;outline:none;font-family:inherit}' +
    '.lm4b-form input:focus{border-color:rgba(0,255,136,.6)}' +
    '.lm4b-consent{grid-column:1/-1;display:flex;gap:10px;align-items:flex-start;font-size:12.5px;line-height:1.5;color:rgba(255,255,255,.55);text-align:left}' +
    '.lm4b-consent input{width:18px;height:18px;margin-top:1px;accent-color:#00ff88;flex:none}' +
    '.lm4b-consent a{color:#00ff88}' +
    '.lm4b-form button{grid-column:1/-1;border:0;border-radius:50px;padding:15px 24px;font-weight:800;font-size:16px;cursor:pointer;color:#0a0a0a;' +
    'background:linear-gradient(135deg,#00ff88,#00cc6a);font-family:inherit;transition:transform .2s,box-shadow .2s}' +
    '.lm4b-form button:hover{transform:translateY(-2px);box-shadow:0 10px 30px rgba(0,255,136,.45)}' +
    '.lm4b-form button:disabled{opacity:.6;transform:none;cursor:default}' +
    '.lm4b-err{grid-column:1/-1;color:#ff9a7a;font-size:13px}' +
    '.lm4b-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}' +
    '.lm4b-ok{display:none;padding:18px;border-radius:14px;background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.3);color:#ccc;font-size:15px}' +
    '.lm4b-ok strong{color:#00ff88}' +
    '.lm4b-img img{width:100%;border-radius:8px;box-shadow:0 20px 50px rgba(0,0,0,.6);transform:rotate(3deg);border:1px solid rgba(255,255,255,.08)}' +
    '.lm4b-more{margin:12px 0 0 !important;font-size:13px !important;color:rgba(255,255,255,.45) !important}' +
    '.lm4b-more a{color:#00ff88}' +
    '@media (max-width:700px){.lm4b{grid-template-columns:1fr;padding:26px 20px}.lm4b-img{display:none}.lm4b-form{grid-template-columns:1fr}.lm4b h3{font-size:24px !important}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  box.innerHTML =
    '<div class="lm4b">' +
      '<div>' +
        '<span class="lm4b-tag">Darmowy plan PDF</span>' +
        '<h3>Pierwsze 4 tygodnie <span>na siłowni</span></h3>' +
        '<p class="lm4b-sub">Gotowy plan dla początkujących: checklista pierwszej wizyty, 2 treningi całego ciała z wideo, rozpiska tydzień po tygodniu i dziennik do wydruku. Wyślę Ci go na maila.</p>' +
        '<form class="lm4b-form" novalidate>' +
          '<input type="text" name="name" placeholder="Imię" autocomplete="given-name">' +
          '<input type="email" name="email" placeholder="Twój e-mail" autocomplete="email" inputmode="email">' +
          '<input type="text" name="hp" class="lm4b-hp" tabindex="-1" autocomplete="off" aria-hidden="true">' +
          '<label class="lm4b-consent"><input type="checkbox" name="consent"><span>Chcę otrzymać plan i zapisuję się do newslettera (porady treningowe i żywieniowe, max. kilka maili w miesiącu). Możesz wypisać się w każdej chwili. <a href="/polityka-prywatnosci.html" target="_blank">Polityka prywatności</a>.</span></label>' +
          '<div class="lm4b-err"></div>' +
          '<button type="submit">Wyślij mi plan</button>' +
        '</form>' +
        '<div class="lm4b-ok"><strong>Gotowe! Sprawdź skrzynkę 📬</strong> Plan wyślę w ciągu kilku minut. Nie widzisz maila? Zajrzyj do zakładek Oferty lub Spam.</div>' +
        '<p class="lm4b-more">Zobacz, co jest w środku: <a href="/4-tygodnie/">szczegóły planu</a></p>' +
      '</div>' +
      '<div class="lm4b-img" aria-hidden="true"><img src="/images/lm-4tyg-cover.jpg" alt="" loading="lazy"></div>' +
    '</div>';

  var f = box.querySelector('form'), err = box.querySelector('.lm4b-err'), btn = f.querySelector('button');
  var slug = (location.pathname.split('/').pop() || '').replace(/\.html$/, '').replace(/^blog-/, '');
  var source = ('blog-' + slug).slice(0, 40);

  f.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = f.name.value.trim(), email = f.email.value.trim();
    err.textContent = '';
    if (!name) { err.textContent = 'Wpisz imię.'; return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { err.textContent = 'Wpisz poprawny adres e-mail.'; return; }
    if (!f.consent.checked) { err.textContent = 'Zaznacz zgodę, żebym mógł wysłać Ci plan.'; return; }
    btn.disabled = true; btn.textContent = 'Wysyłam…';
    fetch('/.netlify/functions/subscribe', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name, email: email, list: '4tygodnie', source: source, hp: f.hp.value })
    }).then(function (r) {
      if (!r.ok) throw new Error();
      f.style.display = 'none'; box.querySelector('.lm4b-ok').style.display = 'block';
      if (window.gtag) window.gtag('event', 'generate_lead', { lead_magnet: '4tygodnie', source: source });
    }).catch(function () {
      err.textContent = 'Coś poszło nie tak. Spróbuj ponownie za chwilę albo napisz na kontakt@erykpersonalny.pl.';
      btn.disabled = false; btn.textContent = 'Wyślij mi plan';
    });
  });
})();

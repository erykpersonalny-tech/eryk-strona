// Przyjmuje jeden dzień dzienniczka z /dzienniczek/ i przekazuje go do n8n.
// Zmienne środowiskowe (Netlify → Site configuration → Environment variables):
//   N8N_DIARY_WEBHOOK_URL – produkcyjny adres webhooka z workflow n8n
//   N8N_DIARY_SECRET      – dowolny długi losowy ciąg; ten sam wpisujesz w n8n
// Bez nich funkcja odpowiada 503, a strona trzyma dane na urządzeniu klienta.

const MAX_BYTES = 5.5 * 1024 * 1024;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const reply = (statusCode, body) => ({
  statusCode,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return reply(405, { error: 'Method Not Allowed' });
  if ((event.body || '').length > MAX_BYTES) return reply(413, { error: 'Za dużo zdjęć w jednym dniu – usuń kilka i spróbuj ponownie.' });

  let d;
  try {
    d = JSON.parse(event.body);
  } catch (e) {
    return reply(400, { error: 'Nieprawidłowe dane.' });
  }

  // honeypot – boty wypełniają ukryte pole
  if (d.hp) return reply(200, { ok: true });

  const name = String(d.name || '').trim().slice(0, 80);
  const email = String(d.email || '').trim().toLowerCase().slice(0, 120);
  if (!name) return reply(400, { error: 'Brak imienia.' });
  if (!EMAIL_RE.test(email)) return reply(400, { error: 'Nieprawidłowy e-mail.' });
  if (d.consent !== true) return reply(400, { error: 'Brak zgody na przetwarzanie danych.' });
  if (!Number.isInteger(d.dayIndex) || d.dayIndex < 0 || d.dayIndex > 6) return reply(400, { error: 'Nieprawidłowy dzień.' });
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(d.date || ''))) return reply(400, { error: 'Brak daty – wybierz początek tygodnia.' });

  const meals = (Array.isArray(d.meals) ? d.meals : []).slice(0, 6).map((m) => ({
    id: String(m.id || '').slice(0, 4),
    label: String(m.label || '').slice(0, 40),
    time: String(m.time || '').slice(0, 5),
    text: String(m.text || '').slice(0, 2000),
    photos: (Array.isArray(m.photos) ? m.photos : [])
      .filter((p) => typeof p === 'string' && p.startsWith('data:image/'))
      .slice(0, 6),
  }));

  const url = process.env.N8N_DIARY_WEBHOOK_URL;
  const secret = process.env.N8N_DIARY_SECRET;
  if (!url || !secret) {
    console.log('submit-diary: brak konfiguracji N8N_DIARY_WEBHOOK_URL / N8N_DIARY_SECRET');
    return reply(503, { error: 'Wysyłka jest chwilowo niedostępna.' });
  }

  const payload = {
    clientId: String(d.clientId || '').slice(0, 64),
    name, email,
    start: String(d.start || '').slice(0, 10),
    dayIndex: d.dayIndex,
    dayName: String(d.dayName || '').slice(0, 20),
    date: d.date,
    water_l: Number(d.water_l) || 0,
    glasses: Number(d.glasses) || 0,
    sleep_h: Number(d.sleep_h) || 0,
    meals,
    complete: d.complete === true,
    filledDays: Number(d.filledDays) || 0,
    sentAt: new Date().toISOString(),
  };

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Diary-Secret': secret },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      console.log('submit-diary: n8n odpowiedział', res.status, await res.text().catch(() => ''));
      return reply(502, { error: 'Serwer nie przyjął danych.' });
    }
    return reply(200, { ok: true });
  } catch (e) {
    console.log('submit-diary: błąd połączenia z n8n', e.message);
    return reply(502, { error: 'Brak połączenia z serwerem.' });
  }
};

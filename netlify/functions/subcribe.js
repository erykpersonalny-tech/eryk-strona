const https = require('https');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  let email, name;
  try {
    const body = JSON.parse(event.body);
    email = body.email;
    name = body.name;
  } catch (e) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Nieprawidłowe dane' }) };
  }

  if (!email || !email.includes('@')) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Nieprawidłowy email' }) };
  }

  const payload = JSON.stringify({
    email: email,
    fields: { name: name },
    groups: ['198572466364220944']
  });

  return new Promise((resolve) => {
    const options = {
      hostname: 'connect.mailerlite.com',
      path: '/api/subscribers',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.MAILERLITE_API_KEY}`,
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          resolve({ statusCode: 200, body: JSON.stringify({ success: true }) });
        } else {
          console.log('MailerLite error:', res.statusCode, data);
          resolve({ statusCode: 500, body: JSON.stringify({ error: 'Błąd MailerLite', details: data }) });
        }
      });
    });

    req.on('error', (e) => {
      console.log('Request error:', e.message);
      resolve({ statusCode: 500, body: JSON.stringify({ error: e.message }) });
    });

    req.write(payload);
    req.end();
  });
};

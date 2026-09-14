exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const { email } = JSON.parse(event.body);

  if (!email || !email.includes('@')) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Nieprawidłowy email' }) };
  }

  const response = await fetch('https://connect.mailerlite.com/api/subscribers', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MAILERLITE_API_KEY}`
    },
    body: JSON.stringify({
      email: email,
      groups: ['198572466364220944']
    })
  });

  if (!response.ok) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Błąd zapisu' }) };
  }

  return {
    statusCode: 200,
    body: JSON.stringify({ success: true })
  };
};

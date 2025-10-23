const nodemailer = require('nodemailer');

exports.handler = async (event, context) => {
  try {
    if (event.httpMethod !== 'POST') {
      return { statusCode: 405, body: JSON.stringify({ error: 'Method not allowed' }) };
    }

    const data = JSON.parse(event.body || '{}');

    // Expect data to include a `type` field (contact | booking) and form fields
    const type = data.type || 'contact';

    // Read SMTP config from environment variables
    const SMTP_HOST = process.env.SMTP_HOST || 'smtp.gmail.com';
    const SMTP_PORT = process.env.SMTP_PORT ? parseInt(process.env.SMTP_PORT, 10) : 587;
    const SMTP_USER = process.env.SMTP_USER;
    const SMTP_PASS = process.env.SMTP_PASS;
    const TO_EMAIL = process.env.TO_EMAIL || SMTP_USER;

    if (!SMTP_USER || !SMTP_PASS) {
      return { statusCode: 500, body: JSON.stringify({ error: 'SMTP credentials not configured' }) };
    }

    const transporter = nodemailer.createTransport({
      host: SMTP_HOST,
      port: SMTP_PORT,
      secure: SMTP_PORT === 465, // true for 465, false for other ports
      auth: {
        user: SMTP_USER,
        pass: SMTP_PASS,
      },
    });

    let subject = 'Website Contact';
    let text = '';

    if (type === 'booking') {
      subject = `Booking Request from ${data.name || 'Unknown'}`;
      text = `Booking Request:\n\nName: ${data.name}\nEmail: ${data.email}\nType: ${data.type}\nDate: ${data.date}\nTime: ${data.time}\nNotes: ${data.notes || ''}`;
    } else {
      subject = `Contact Form Submission from ${data.name || 'Unknown'}`;
      text = `Name: ${data.name}\nEmail: ${data.email}\n\nMessage:\n${data.message || ''}`;
    }

    const mailOptions = {
      from: SMTP_USER,
      to: TO_EMAIL,
      subject,
      text,
    };

    await transporter.sendMail(mailOptions);

    return {
      statusCode: 200,
      body: JSON.stringify({ success: true, message: 'Email sent' }),
    };
  } catch (err) {
    console.error('Forward-email error:', err);
    return {
      statusCode: 500,
      body: JSON.stringify({ success: false, error: err.message }),
    };
  }
};

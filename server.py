from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from logging.handlers import RotatingFileHandler
import traceback
from time import strftime
import json

app = Flask(__name__)

# Configure logging
if not os.path.exists('logs'):
    os.mkdir('logs')

# Set up file logging
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# Set up console logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
app.logger.addHandler(console_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('UP Website backend startup')

# Enable CORS for specific origin
CORS(app)  # CORS will be configured with the ALLOWED_ORIGIN

# Email configuration
import os
from dotenv import load_dotenv

# Load environment variables from .env file in development
if os.path.exists('.env'):
    load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "diamondminddynasty@gmail.com"
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Get the allowed origin from environment variable or default to localhost
ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', 'http://localhost:8000')

# Configure CORS for the specific origin
CORS(app, resources={
    r"/*": {
        "origins": [ALLOWED_ORIGIN],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = SENDER_EMAIL  # Sending to yourself
        msg['Subject'] = f"Contact Form Submission from {name}"

        body = f"""
        Name: {name}
        Email: {email}

        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({"success": True, "message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/send-booking', methods=['POST'])
def send_booking():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        date = data.get('date')
        time = data.get('time')
        session_type = data.get('type')
        notes = data.get('notes', '')

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = SENDER_EMAIL
        msg['Subject'] = f"Booking Request from {name} - {session_type}"

        body = f"""
        Booking Request Details:
        
        Name: {name}
        Email: {email}
        Session Type: {session_type}
        Preferred Date: {date}
        Preferred Time: {time}

        Additional Notes:
        {notes}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({"success": True, "message": "Booking request sent successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

        body = f"""
        Name: {name}
        Email: {email}

        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)

        # Send email
        server.send_message(msg)
        server.quit()

        return jsonify({"success": True, "message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    if not EMAIL_PASSWORD:
        print("Warning: EMAIL_PASSWORD environment variable not set!")
    app.run(port=5000)
from flask import Blueprint, request, jsonify
import smtplib
import ssl
from email.message import EmailMessage
import re
import os

bp = Blueprint('contact', __name__, url_prefix='/api/v1/contact')


# Simple email validator
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

# Your receiver email
ADMIN_EMAIL = 'kewan.rashed@gmail.com'

# Your SMTP configuration (Yandex example)
SMTP_SERVER = 'smtp.yandex.com'
SMTP_PORT = 465
SMTP_USERNAME = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASS')


@bp.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or len(name) < 2:
        return jsonify({"error": "Invalid name"}), 400

    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email"}), 400

    if not message or len(message) < 10:
        return jsonify({"error": "Message too short"}), 400

    try:
        # Build email
        email_message = EmailMessage()
        email_message['Subject'] = f"New Contact Form Message from {name}"
        email_message['From'] = SMTP_USERNAME
        email_message['To'] = ADMIN_EMAIL
        email_message.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

        # Send email securely
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(email_message)

        return jsonify({"message": "Message sent successfully."}), 200

    except Exception as e:
        print(f"Email sending failed: {e}")
        return jsonify({"error": "Failed to send message."}), 500

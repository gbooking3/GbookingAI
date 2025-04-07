from flask import jsonify
from app.extensions import mongo
from app.utils.jwt_utils import create_access_token, create_refresh_token,decode_token
from app.models.user import User

#email
import smtplib
import random
from email.message import EmailMessage
def register_user(data):
    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400
    User.create_user(data)
    return jsonify({"message": "User registered successfully"}), 201

def login_user(data):
    user = mongo.db.users.find_one({
        "phone": data["phone"],
        "ownid": data["ownid"]
    })
    if not user:
        return jsonify({"error": "User Not Found"}), 404

    payload = {"ownid": user["ownid"]}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_details": User.to_json(user)
    }), 200


def refresh_token(data):
    
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "Missing refresh token"}), 400

    decoded = decode_token(refresh_token, is_refresh=True)
    if not decoded:
        return jsonify({"error": "Invalid or expired refresh token"}), 403

    ownid = decoded["ownid"]
    
    
  
    user = User.find_by_ownid(ownid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    
    new_access_token = create_access_token({"ownid": ownid})
    new_refresh_token = refresh_token 

    
    return jsonify({
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "user_details": User.to_json(user)

    }), 200



def generate_otp(length=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def send_otp_yandex(sender_email, sender_password, recipient_email):
    otp = generate_otp()
    
    msg = EmailMessage()
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(f'Your OTP code is: {otp}')

    try:
        with smtplib.SMTP_SSL('smtp.yandex.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print(f"OTP sent to {recipient_email}: {otp}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    return otp    




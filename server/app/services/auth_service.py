from flask import jsonify
from app.utils.jwt_utils import create_access_token, create_refresh_token, decode_token
from app.models.user import User
import smtplib
import random
from email.message import EmailMessage
def register_user(data):
    """
    Register a new user if email, phone, and ownid are not already taken.
    If an inactive user matches all three, reactivate the account.
    """
    email = data.get("email")
    phone = data.get("phone")
    ownid = data.get("ownid")

    existing_user = User.find_by_ownid(ownid)

    if existing_user:
        if not existing_user.get("is_active", True):
            # Account is inactive (soft-deleted)
            if (existing_user.get("email") == email and existing_user.get("phone") == phone):
                # ✅ Safe to reactivate — all credentials match
                User.reactivate_user(ownid)
                return jsonify({"message": "Account reactivated. Please log in."}), 200
            else:
                # ⚠️ Credentials don't match — potential impersonation
                return jsonify({
                    "error": "This ID was previously deleted. Please contact support to recover the account."
                }), 403
        else:
            # Active account already exists
            return jsonify({"error": "ID already exists"}), 400

    # No user with this ID exists — check email & phone globally
    if User.find_by_email(email):
        return jsonify({"error": "Email already exists"}), 400

    if User.find_by_phone(phone):
        return jsonify({"error": "Phone number already exists"}), 400

    # ✅ All checks passed — create new user
    data["is_active"] = True
    User.create_user(data)
    return jsonify({"message": "User registered successfully"}), 201




def login_user_by_ownid(ownid):
    """
    Login a user using their ownid by issuing JWT tokens.
    """
    user = User.find_by_ownid(ownid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    payload = {"ownid": user["ownid"]}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_details": User.to_json(user)
    }), 200


def refresh_user_token(data):
    """
    Validate refresh token and issue a new access token.
    """
    token = data.get("refresh_token")
    if not token:
        return jsonify({"error": "Missing refresh token"}), 400

    decoded = decode_token(token, is_refresh=True)
    if not decoded:
        return jsonify({"error": "Invalid or expired refresh token"}), 403

    ownid = decoded["ownid"]
    user = User.find_by_ownid(ownid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_access_token = create_access_token({"ownid": ownid})

    return jsonify({
        "access_token": new_access_token,
        "refresh_token": token,  # Reusing the same refresh token
        "user_details": User.to_json(user)
    }), 200


def generate_otp(length=6):
    """
    Generate a random numeric OTP of specified length.
    """
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def send_otp_via_yandex(sender_email, sender_password, recipient_email):
    """
    Send OTP to user's email using Yandex SMTP.
    """
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

def delete_user_by_id(user_id):
    return User.delete_by_ownid(user_id)

def update_user_name(data):
    return User.update_user_name(data)

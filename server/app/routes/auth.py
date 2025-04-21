from flask import Blueprint, request, jsonify
from app.services.auth_service import (
    register_user, login_user_by_ownid, refresh_user_token,
    send_otp_via_yandex, generate_otp
)
from app.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
generated_otp = None


@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400
    required_fields = ["email", "phone", "ownid"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"Missing field: {field}"}), 400
    return register_user(data)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    ownid = data.get("ownid")
    method = data.get("method")
    contact_value = User.find_by_ownid(ownid)
    email = contact_value["email"]
    print("The email is : ",email)
    global generated_otp
    user = User.find_by_ownid(ownid)
    if not user:
        return jsonify({ "error": "Invalid credentials" }), 404

 
    if method == "email":
       
        otp = send_otp_via_yandex(
            sender_email='mohamedabohamad@yandex.com',
            sender_password='qoebhhdmafgowgjn',
            recipient_email=email
        )
    elif method == "phone":
        otp = generate_otp()
        print(f"Simulated SMS to {contact_value}: OTP = {otp}")
    else:
        return jsonify({"error": "Invalid contact method"}), 400

    generated_otp = otp
    return login_user_by_ownid(ownid)


@bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    ownid = data.get("ownid")
    otp = data.get("otp")
    stored_otp = generated_otp 
    print("                ",stored_otp)
    print(type(otp))
    print(type(stored_otp))

    if stored_otp != otp:
        return jsonify({"error": "OTP is wrong"}), 400

    return jsonify({"message": "OTP verified successfully"}), 200



@bp.route('/refresh-token', methods=['POST'])
def refresh():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    return refresh_user_token(data)

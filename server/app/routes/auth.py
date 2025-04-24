from flask import Blueprint, request, jsonify
from app.services.auth_service import (
    register_user, login_user_by_ownid, refresh_user_token,
    send_otp_via_yandex, generate_otp, delete_user_by_id
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

    # 🔐 Find user by ownid and ensure they are active
    user = User.find_by_ownid(ownid)
    if not user or not user.get("is_active", True):
        return jsonify({ "error": "User not found or inactive" }), 404

    global generated_otp

    # ✅ Proceed with OTP logic
    if method == "email":
        otp = send_otp_via_yandex(
            sender_email='mohamedabohamad@yandex.com',
            sender_password='qoebhhdmafgowgjn',
            recipient_email=user["email"]
        )
    elif method == "phone":
        otp = generate_otp()
        print(f"Simulated SMS to {user['phone']}: OTP = {otp}")
    else:
        return jsonify({"error": "Invalid contact method"}), 400

    generated_otp = otp
    return login_user_by_ownid(ownid)


@bp.route("/delete-account", methods=["DELETE"])
def delete_account():
    data = request.get_json()
    user_id = data.get("ownid")

    if not user_id:
        return jsonify({"error": "Missing 'ownid'"}), 400

    if delete_user_by_id(user_id):
        return jsonify({"message": "User deleted successfully."}), 200
    else:
        return jsonify({"error": "User not found or could not be deleted."}), 404


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

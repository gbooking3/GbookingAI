from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user
from app.services.auth_service import login_user
from app.services.auth_service import refresh_token
from app.utils.jwt_utils import decode_token, create_access_token
from app.services.auth_service import generate_otp
from app.services.auth_service import send_otp_yandex
from app.extensions import mongo


bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
generated_otp = None
@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return register_user(data)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    method = data.get("method")  # "email" or "phone"
    ownid = data.get("ownid")

    if not ownid or not method:
        return jsonify({"error": "Missing ownid or method"}), 400

    # Fetch user
    user = mongo.db.users.find_one({"ownid": ownid})
    if not user:
        return jsonify({"error": "User not found"}), 404

    contact_value = user.get(method)
    if not contact_value:
        return jsonify({"error": f"User has no {method} on file"}), 400

    # Send OTP
    global generated_otp
    if method == "email":
        generated_otp = send_otp_yandex(
            sender_email='mohamedabohamad@yandex.com',
            sender_password='qoebhhdmafgowgjn',
            recipient_email=contact_value
        )
    elif method == "phone":
        generated_otp = generate_otp()
        print(f"Simulated SMS to {contact_value}: OTP = {generated_otp}")
        # Replace with real SMS logic if needed
    else:
        return jsonify({"error": "Invalid contact method"}), 400

    # Call separate logic to build response
    return login_user(user)

@bp.route('/refresh-token', methods=['POST'])
def refresh():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    return refresh_token(data)


@bp.route('/verify-otp', methods=['POST'])
def verify_otp():

     if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
     data = request.get_json()
     otp = data.get("otp")
     print(otp)
     print(generated_otp)

    # Compare provided OTP with the global OTP
     if str(otp) != generated_otp:
        return jsonify({"error": "OTP is wrong"}), 400

     return jsonify({"message": "OTP verified successfully"}), 200
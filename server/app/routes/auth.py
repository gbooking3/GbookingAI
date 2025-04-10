from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user
from app.services.auth_service import login_user
from app.services.auth_service import refresh_token
from app.utils.jwt_utils import decode_token, create_access_token
from app.services.auth_service import generate_otp
from app.services.auth_service import send_otp_yandex

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
generated_otp = None
@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return register_user(data)

@bp.route('/login', methods=['POST'])
def login():
     data = request.get_json()
     # Generate OTP
     global generated_otp
     mail=data.get("email")
     
     generated_otp=send_otp_yandex('mohamedabohamad@yandex.com','qoebhhdmafgowgjn',mail)

     return login_user(data)

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
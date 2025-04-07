from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user
from app.services.auth_service import login_user
from app.services.auth_service import refresh_token
from app.utils.jwt_utils import decode_token, create_access_token

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return register_user(data)

@bp.route('/login', methods=['POST'])
def login():
     data = request.get_json()
     return login_user(data)

@bp.route('/refresh', methods=['POST'])
def refresh():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json()
    return refresh_token(data)


@bp.route('/verifyotp', methods=['POST'])
def verify_otp():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    otp = data.get("otp")
    
    print(otp)
    if otp != "123456":
      return jsonify({"error": "otp is wrong"}), 400


    return jsonify({"message": "OTP verified successfully"}), 200
from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user
from app.services.auth_service import login_user
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
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "Missing refresh token"}), 400

    decoded = decode_token(refresh_token, is_refresh=True)
    if not decoded:
        return jsonify({"error": "Invalid or expired refresh token"}), 403

    ownid = decoded["ownid"]
    
    
    from app.models.user import get_user_by_ownid
    user = get_user_by_ownid(ownid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    
    new_access_token = create_access_token({"ownid": ownid})
    new_refresh_token = refresh_token 

    
    return jsonify({
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "user_details": {
            "ownid": user.ownid,
        }
    }), 200

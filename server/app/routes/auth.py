from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user
from app.services.auth_service import login_user
from app.services.auth_service import refresh_token
from app.utils.jwt_utils import decode_token, create_access_token

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaa",data)
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

from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user
from app.services.auth_service import login_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    return register_user(data)

@bp.route('/login', methods=['POST'])
def login():
     data = request.get_json()
     return login_user(data)

from flask import jsonify
from app.extensions import mongo
from app.utils.jwt_utils import create_access_token, create_refresh_token
from app.models.user import User

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

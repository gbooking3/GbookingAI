from flask import jsonify
from app.extensions import mongo
from app.models.user import User
from flask import request, jsonify

def register_user(data):
    users_collection = mongo.db.users

    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"error": "Email already exists"}), 400

    User.create_user(data)
    
    return jsonify({"message": "User registered successfully"}), 201

def login_user(data):
    data = request.get_json()  # Parse the JSON data from the request body
    # Print the received JSON data for debugging
    print("Received data:", data)    
    return jsonify({"message": "User registered successfully"}), 201


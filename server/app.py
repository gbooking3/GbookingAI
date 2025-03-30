import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask_cors import CORS
# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5173", "http://localhost:5173"])


# Configure MongoDB
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongo_client = PyMongo(app)
db = mongo_client.db  # Get the database

if db is None:
    print("Database connection failed!")
else:
    print("Database connected successfully!")

# Collection for products
user_collection= db.Gbooking

@app.route('/')    # http://127.0.0.1/:5000/
def home():
    return "<h1>Hello, Flask!</h1>"


@app.route('/Gbooking', methods=['POST'])
def add_product():
    data = request.json  # Get JSON data from request
    if not data or "name" not in data or "email" not in data or "id" not in data or "phone" not in data or "ownid" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_user = {
        "id": data["id"],
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "ownid": data["ownid"],
        "password":data["password"]

    }
    result = user_collection.insert_one(new_user)  # Insert into MongoDB

    return jsonify({"message": "Product added", "id": str(result.inserted_id)}), 201



if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from .routes import auth
from app.extensions import mongo
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)
    # CORS(app, origins=["http://127.0.0.1:5173", "http://localhost:5173"])

    # Configure MongoDB
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    mongo.init_app(app)

    app.register_blueprint(auth.bp)

    return app

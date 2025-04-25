from flask import Flask
from .routes import auth
from .routes import chat
from .routes import contact
from app.extensions import mongo
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5173", "http://localhost:5173","http://10.0.0.21:5173"])

    # Configure MongoDB
    app.config["SECRET_KEY"]         = os.getenv('SECRET_KEY')
    app.config["MONGO_URI"]          = os.getenv("MONGO_URI")
    app.config["REFRESH_SECRET_KEY"] = os.getenv("REFRESH_SECRET_KEY")
    mongo.init_app(app)
    
    app.register_blueprint(contact.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(chat.bp)

    return app

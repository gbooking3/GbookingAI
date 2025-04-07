import jwt 
from datetime import datetime, timedelta
from flask import current_app

def create_token(data: dict, secret_key: str, expires_minutes: int):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    return jwt.encode(payload, secret_key, algorithm="HS256")

def create_access_token(data: dict):
    secret = current_app.config["SECRET_KEY"]
    return create_token(data, secret, expires_minutes=15)

def create_refresh_token(payload):
    secret = current_app.config["SECRET_KEY"]
    payload["type"] = "refresh"
    payload["exp"] = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token, is_refresh=False):
    try:
        SECRET_KEY = current_app.config["SECRET_KEY"]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if is_refresh and payload.get("type") != "refresh":
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


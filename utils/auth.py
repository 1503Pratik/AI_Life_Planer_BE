import jwt
from datetime import datetime, timedelta
from flask import request, jsonify, g
from functools import wraps
from config import settings

SECRET = settings.SECRET_KEY

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        return None

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].replace("Bearer ", "")

        if not token:
            return jsonify({"error": "Missing token"}), 401

        decoded = decode_token(token)
        if not decoded:
            return jsonify({"error": "Invalid or expired token"}), 401

        g.user_id = decoded["user_id"]  # 🔥 store user id globally
        return fn(*args, **kwargs)

    return wrapper

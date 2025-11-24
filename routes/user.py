from flask import Blueprint, request, jsonify
from database.models import create_user, db

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    result = create_user(data["name"], data["email"])
    return jsonify({"message": "User created", "id": str(result.inserted_id)})

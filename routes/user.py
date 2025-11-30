# from flask import Blueprint, request, jsonify
# from database.models import create_user, db

# user_bp = Blueprint("user", __name__)

# @user_bp.route("/register", methods=["POST"])
# def register():
#     data = request.json
#     result = create_user(data["name"], data["email"])
#     return jsonify({"message": "User created", "id": str(result.inserted_id)})




# from flask import Blueprint, request, jsonify
# from werkzeug.security import check_password_hash
# from database.models import create_user, find_user_by_email, find_user_by_id
# from utils.auth import generate_token, auth_required
# import re

# user_bp = Blueprint("user", __name__)

# # ---------------- SIGNUP ----------------
# @user_bp.route("/register", methods=["POST"])
# def register():
#     data = request.json

#     if not data.get("name") or not data.get("email") or not data.get("password"):
#         return jsonify({"error": "name, email, password required"}), 400

#     if find_user_by_email(data["email"]):
#         return jsonify({"error": "Email already registered"}), 400

#     res = create_user(data["name"], data["email"], data["password"])

#     token = generate_token(str(res.inserted_id))

#     return jsonify({
#         "message": "User created",
#         "token": token
#     }), 201

# # ---------------- LOGIN ----------------
# @user_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json

#     user = find_user_by_email(data.get("email"))
#     if not user:
#         return jsonify({"error": "Invalid email"}), 400

#     if not check_password_hash(user["password"], data.get("password", "")):
#         return jsonify({"error": "Invalid password"}), 400

#     token = generate_token(str(user["_id"]))

#     return jsonify({
#         "message": "Login successful",
#         "token": token
#     })

# # ---------------- PROFILE ----------------
# @user_bp.route("/me", methods=["GET"])
# @auth_required
# def profile():
#     user = find_user_by_id(g.user_id)
#     user["_id"] = str(user["_id"])
#     del user["password"]
#     return jsonify({"user": user})





from flask import Blueprint, request, jsonify, g
from werkzeug.security import check_password_hash
from database.models import create_user, find_user_by_email, find_user_by_id
from utils.auth import generate_token, auth_required

user_bp = Blueprint("user", __name__)

# ---------------- SIGNUP ----------------
@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "name, email, password required"}), 400

    if find_user_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 400

    res = create_user(data["name"], data["email"], data["password"])

    token = generate_token(str(res.inserted_id))

    return jsonify({
        "message": "User created",
        "token": token
    }), 201


# ---------------- LOGIN ----------------
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = find_user_by_email(data.get("email"))
    if not user:
        return jsonify({"error": "Invalid email"}), 400

    if not check_password_hash(user["password"], data.get("password", "")):
        return jsonify({"error": "Invalid password"}), 400

    token = generate_token(str(user["_id"]))

    return jsonify({
        "message": "Login successful",
        "token": token
    })


# ---------------- PROFILE ----------------
@user_bp.route("/me", methods=["GET"])
@auth_required
def profile():
    user = find_user_by_id(g.user_id)
    user["_id"] = str(user["_id"])
    del user["password"]
    return jsonify({"user": user})

# from flask import Blueprint, request, jsonify
# from database.connection import db
# from datetime import datetime

# budget_bp = Blueprint("budget", __name__)

# @budget_bp.route("/add", methods=["POST"])
# def add_transaction():
#     data = request.json
#     trans = {
#         "user_id": data["user_id"],
#         "amount": data["amount"],
#         "type": data["type"],  # income / expense
#         "category": data.get("category"),
#         "date": datetime.utcnow()
#     }
#     result = db.budget.insert_one(trans)
#     return jsonify({"message": "Transaction added"})

# @budget_bp.route("/summary/<user_id>", methods=["GET"])
# def budget_summary(user_id):
#     expenses = sum([t["amount"] for t in db.budget.find({"user_id": user_id, "type": "expense"})])
#     income = sum([t["amount"] for t in db.budget.find({"user_id": user_id, "type": "income"})])
#     return jsonify({"income": income, "expenses": expenses, "balance": income-expenses})




from flask import Blueprint, request, jsonify, g
from database.connection import db
from datetime import datetime
from utils.auth import auth_required

budget_bp = Blueprint("budget", __name__)


# ---------------- ADD TRANSACTION ----------------
@budget_bp.route("/add", methods=["POST"])
@auth_required
def add_transaction():
    data = request.json

    if not data.get("amount") or not data.get("type"):
        return jsonify({"error": "amount and type required"}), 400

    trans = {
        "user_id": g.user_id,
        "amount": float(data["amount"]),
        "type": data["type"],          # income / expense
        "category": data.get("category"),
        "date": datetime.utcnow()
    }

    db.budget.insert_one(trans)

    return jsonify({"message": "Transaction added"}), 201


# ---------------- SUMMARY ----------------
@budget_bp.route("/summary", methods=["GET"])
@auth_required
def budget_summary():
    user_id = g.user_id

    expenses = sum(t["amount"] for t in db.budget.find({"user_id": user_id, "type": "expense"}))
    income = sum(t["amount"] for t in db.budget.find({"user_id": user_id, "type": "income"}))

    return jsonify({
        "income": income,
        "expenses": expenses,
        "balance": income - expenses
    }), 200

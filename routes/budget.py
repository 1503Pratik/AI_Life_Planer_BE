from flask import Blueprint, request, jsonify
from database.connection import db
from datetime import datetime

budget_bp = Blueprint("budget", __name__)

@budget_bp.route("/add", methods=["POST"])
def add_transaction():
    data = request.json
    trans = {
        "user_id": data["user_id"],
        "amount": data["amount"],
        "type": data["type"],  # income / expense
        "category": data.get("category"),
        "date": datetime.utcnow()
    }
    result = db.budget.insert_one(trans)
    return jsonify({"message": "Transaction added"})

@budget_bp.route("/summary/<user_id>", methods=["GET"])
def budget_summary(user_id):
    expenses = sum([t["amount"] for t in db.budget.find({"user_id": user_id, "type": "expense"})])
    income = sum([t["amount"] for t in db.budget.find({"user_id": user_id, "type": "income"})])
    return jsonify({"income": income, "expenses": expenses, "balance": income-expenses})

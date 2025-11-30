# from flask import Blueprint, request, jsonify
# from database.models import create_habit, get_habits_for_user, update_habit, mark_habit_done, get_habit_by_id
# from database.connection import db
# from utils.helpers import serialize_list, serialize_doc
# from bson import ObjectId

# habit_bp = Blueprint("habit", __name__)

# # ---------------- CREATE HABIT ----------------
# @habit_bp.route("/add", methods=["POST"])
# def add_habit():
#     data = request.get_json(silent=True) or {}
#     if not data.get("user_id") or not data.get("habit_name"):
#         return jsonify({"error": "user_id and habit_name required"}), 400

#     frequency = data.get("frequency", "daily")
#     doc = create_habit(data["user_id"], data["habit_name"], frequency)
#     return jsonify({"message": "habit created", "id": str(doc.inserted_id)}), 201


# # ---------------- GET ALL HABITS ----------------
# @habit_bp.route("/all/<user_id>", methods=["GET"])
# def all_habits(user_id):
#     return jsonify(serialize_list(get_habits_for_user(user_id))), 200


# # ---------------- MARK HABIT COMPLETE ----------------
# @habit_bp.route("/complete/<habit_id>", methods=["POST"])
# def complete_habit(habit_id):
#     data = request.get_json(silent=True) or {}
#     date = data.get("date")
#     res = mark_habit_done(habit_id, date)
#     if res.modified_count:
#         updated = get_habit_by_id(habit_id)
#         return jsonify(serialize_doc(updated)), 200
#     return jsonify({"error": "habit not found or not updated"}), 404


# # ---------------- UPDATE HABIT ----------------
# @habit_bp.route("/update/<habit_id>", methods=["PUT"])
# def edit_habit(habit_id):
#     data = request.get_json(silent=True) or {}
#     allowed = {k: v for k, v in data.items() if k in ["habit_name", "frequency", "streak"]}
#     if not allowed:
#         return jsonify({"error": "no updatable fields provided"}), 400
#     update_habit(habit_id, allowed)
#     return jsonify({"message": "habit updated"}), 200


# # ✅ -------- FITNESS UPDATE (UI REQUIREMENT) --------
# @habit_bp.route("/fitness/update/<habit_id>", methods=["POST"])
# def update_fitness(habit_id):
#     data = request.get_json(silent=True) or {}

#     db.habits.update_one(
#         {"_id": ObjectId(habit_id)},
#         {
#             "$set": {
#                 "steps": data.get("steps", 0),
#                 "calories": data.get("calories", 0)
#             }
#         }
#     )
#     # return jsonify({"message": "Fitness data updated successfully"}), 200
#     updated = get_habit_by_id(habit_id)
#     return jsonify(serialize_doc(updated)), 200





from flask import Blueprint, request, jsonify, g
from database.models import (
    create_habit, get_habits_for_user, update_habit,
    mark_habit_done, get_habit_by_id
)
from database.connection import db
from utils.helpers import serialize_list, serialize_doc
from utils.auth import auth_required
from bson import ObjectId

habit_bp = Blueprint("habit", __name__)


# ---------------- CREATE HABIT ----------------
@habit_bp.route("/add", methods=["POST"])
@auth_required
def add_habit():
    data = request.get_json(silent=True) or {}

    if not data.get("habit_name"):
        return jsonify({"error": "habit_name required"}), 400

    frequency = data.get("frequency", "daily")

    doc = create_habit(g.user_id, data["habit_name"], frequency)
    return jsonify({"message": "habit created", "id": str(doc.inserted_id)}), 201


# ---------------- GET ALL HABITS ----------------
@habit_bp.route("/all", methods=["GET"])
@auth_required
def all_habits():
    habits = get_habits_for_user(g.user_id)
    return jsonify(serialize_list(habits)), 200


# ---------------- MARK HABIT COMPLETE ----------------
@habit_bp.route("/complete/<habit_id>", methods=["POST"])
@auth_required
def complete_habit(habit_id):
    data = request.get_json(silent=True) or {}
    date = data.get("date")

    res = mark_habit_done(habit_id, date)

    if res.modified_count:
        updated = get_habit_by_id(habit_id)
        return jsonify(serialize_doc(updated)), 200

    return jsonify({"error": "habit not found or not updated"}), 404


# ---------------- UPDATE HABIT ----------------
@habit_bp.route("/update/<habit_id>", methods=["PUT"])
@auth_required
def edit_habit(habit_id):
    data = request.get_json(silent=True) or {}

    allowed = {k: v for k, v in data.items() if k in ["habit_name", "frequency", "streak"]}

    if not allowed:
        return jsonify({"error": "no updatable fields provided"}), 400

    update_habit(habit_id, allowed)

    return jsonify({"message": "habit updated"}), 200


# -------- FITNESS UPDATE (UI REQUIREMENT) --------
@habit_bp.route("/fitness/update/<habit_id>", methods=["POST"])
@auth_required
def update_fitness(habit_id):
    data = request.get_json(silent=True) or {}

    db.habits.update_one(
        {"_id": ObjectId(habit_id)},
        {
            "$set": {
                "steps": data.get("steps", 0),
                "calories": data.get("calories", 0)
            }
        }
    )

    updated = get_habit_by_id(habit_id)

    return jsonify(serialize_doc(updated)), 200

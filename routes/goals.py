# # routes/goals.py
# from flask import Blueprint, request, jsonify
# from database.models import create_goal, get_goals_for_user, update_goal, find_goal_by_id, update_goal_progress
# from utils.helpers import serialize_list, serialize_doc

# goal_bp = Blueprint("goal", __name__)

# @goal_bp.route("/add", methods=["POST"])
# def add_goal():
#     data = request.get_json() or {}
#     if not data.get("user_id") or not data.get("goal_title"):
#         return jsonify({"error": "user_id and goal_title required"}), 400
#     res = create_goal(data["user_id"], data["goal_title"], data.get("deadline"))
#     return jsonify({"message": "goal created", "id": str(res.inserted_id)}), 201

# @goal_bp.route("/all/<user_id>", methods=["GET"])
# def all_goals(user_id):
#     return jsonify(serialize_list(get_goals_for_user(user_id))), 200

# @goal_bp.route("/update/<goal_id>", methods=["PUT"])
# def edit_goal(goal_id):
#     data = request.get_json() or {}
#     allowed = {k: v for k, v in data.items() if k in ["goal_title", "deadline", "progress", "description"]}
#     if not allowed:
#         return jsonify({"error": "no updatable fields provided"}), 400
#     update_goal(goal_id, allowed)
#     return jsonify({"message": "goal updated"}), 200

# @goal_bp.route("/progress/<goal_id>", methods=["POST"])
# def progress_goal(goal_id):
#     data = request.get_json() or {}
#     delta = data.get("delta")
#     set_progress = data.get("set")
#     update_goal_progress(goal_id, progress_delta=delta or 0, set_progress=set_progress)
#     updated = find_goal_by_id(goal_id)
#     return jsonify(serialize_doc(updated)), 200




from flask import Blueprint, request, jsonify, g
from database.models import (
    create_goal, get_goals_for_user, update_goal,
    find_goal_by_id, update_goal_progress
)
from utils.helpers import serialize_list, serialize_doc
from utils.auth import auth_required

goal_bp = Blueprint("goal", __name__)


# ---------------- CREATE GOAL ----------------
@goal_bp.route("/add", methods=["POST"])
@auth_required
def add_goal():
    data = request.get_json() or {}

    if not data.get("goal_title"):
        return jsonify({"error": "goal_title required"}), 400

    res = create_goal(
        g.user_id,
        data["goal_title"],
        data.get("deadline")
    )

    return jsonify({"message": "goal created", "id": str(res.inserted_id)}), 201


# ---------------- GET ALL GOALS ----------------
@goal_bp.route("/all", methods=["GET"])
@auth_required
def all_goals():
    goals = get_goals_for_user(g.user_id)
    return jsonify(serialize_list(goals)), 200


# ---------------- UPDATE GOAL ----------------
@goal_bp.route("/update/<goal_id>", methods=["PUT"])
@auth_required
def edit_goal(goal_id):
    data = request.get_json() or {}

    allowed = {k: v for k, v in data.items()
               if k in ["goal_title", "deadline", "progress", "description"]}

    if not allowed:
        return jsonify({"error": "no updatable fields provided"}), 400

    update_goal(goal_id, allowed)

    return jsonify({"message": "goal updated"}), 200


# ---------------- UPDATE PROGRESS ----------------
@goal_bp.route("/progress/<goal_id>", methods=["POST"])
@auth_required
def progress_goal(goal_id):
    data = request.get_json() or {}

    delta = data.get("delta")
    set_progress = data.get("set")

    update_goal_progress(
        goal_id,
        progress_delta=delta or 0,
        set_progress=set_progress
    )

    updated = find_goal_by_id(goal_id)

    return jsonify(serialize_doc(updated)), 200

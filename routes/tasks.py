# from flask import Blueprint, request, jsonify
# from database.connection import db
# from database.models import create_task

# task_bp = Blueprint("task", __name__)

# @task_bp.route("/add", methods=["POST"])
# def add_task():
#     data = request.json
#     result = create_task(data["user_id"], data["title"], data["description"], data["due_date"])
#     return jsonify({"message": "Task added", "id": str(result.inserted_id)})

# @task_bp.route("/all/<user_id>")
# def get_tasks(user_id):
#     tasks = list(db.tasks.find({"user_id": user_id}))
#     for t in tasks:
#         t["_id"] = str(t["_id"])
#     return jsonify(tasks)



from flask import Blueprint, request, jsonify, g
from utils.auth import auth_required
from database.models import create_task
from database.connection import db

task_bp = Blueprint("task", __name__)

@task_bp.route("/add", methods=["POST"])
@auth_required
def add_task():
    data = request.json
    result = create_task(
        g.user_id,                 # 🔥 auto from token
        data["title"],
        data.get("description"),
        data.get("due_date")
    )
    return jsonify({"message": "Task added", "id": str(result.inserted_id)})

@task_bp.route("/all", methods=["GET"])
@auth_required
def get_tasks():
    tasks = list(db.tasks.find({"user_id": g.user_id}))
    for t in tasks:
        t["_id"] = str(t["_id"])
    return jsonify(tasks)

# from flask import Blueprint, request, jsonify
# from database.connection import db
# from datetime import datetime

# calendar_bp = Blueprint("calendar", __name__)

# @calendar_bp.route("/add", methods=["POST"])
# def add_event():
#     data = request.json
#     event = {
#         "user_id": data["user_id"],
#         "title": data["title"],
#         "date": data["date"],
#         "time": data.get("time"),
#         "created_at": datetime.utcnow()
#     }
#     result = db.calendar.insert_one(event)
#     return jsonify({"message": "Event added", "id": str(result.inserted_id)})

# @calendar_bp.route("/all/<user_id>", methods=["GET"])
# def get_events(user_id):
#     events = list(db.calendar.find({"user_id": user_id}))
#     for e in events:
#         e["_id"] = str(e["_id"])
#     return jsonify(events)




from flask import Blueprint, request, jsonify, g
from database.connection import db
from datetime import datetime
from utils.auth import auth_required

calendar_bp = Blueprint("calendar", __name__)


# ---------------- ADD EVENT ----------------
@calendar_bp.route("/add", methods=["POST"])
@auth_required
def add_event():
    data = request.json

    if not data.get("title") or not data.get("date"):
        return jsonify({"error": "title and date are required"}), 400

    event = {
        "user_id": g.user_id,
        "title": data["title"],
        "date": data["date"],
        "time": data.get("time"),
        "created_at": datetime.utcnow()
    }

    result = db.calendar.insert_one(event)

    return jsonify({"message": "Event added", "id": str(result.inserted_id)}), 201


# ---------------- GET ALL EVENTS ----------------
@calendar_bp.route("/all", methods=["GET"])
@auth_required
def get_events():
    events = list(db.calendar.find({"user_id": g.user_id}))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events), 200

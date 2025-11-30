# from flask import Blueprint, jsonify

# integration_bp = Blueprint("integration", __name__)

# @integration_bp.route("/google/sync")
# def google_sync():
#     return jsonify({"status": "Google Calendar sync initialized"})

# @integration_bp.route("/apple/sync")
# def apple_sync():
#     return jsonify({"status": "Apple Health sync initialized"})




from flask import Blueprint, jsonify, g
from utils.auth import auth_required

integration_bp = Blueprint("integration", __name__)

# ---------------- GOOGLE CALENDAR SYNC ----------------
@integration_bp.route("/google/sync", methods=["GET"])
@auth_required
def google_sync():
    return jsonify({
        "status": "success",
        "message": "Google Calendar sync initialized",
        "user_id": g.user_id
    })


# ---------------- APPLE HEALTH SYNC ----------------
@integration_bp.route("/apple/sync", methods=["GET"])
@auth_required
def apple_sync():
    return jsonify({
        "status": "success",
        "message": "Apple Health sync initialized",
        "user_id": g.user_id
    })

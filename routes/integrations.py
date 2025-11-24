from flask import Blueprint, jsonify

integration_bp = Blueprint("integration", __name__)

@integration_bp.route("/google/sync")
def google_sync():
    return jsonify({"status": "Google Calendar sync initialized"})

@integration_bp.route("/apple/sync")
def apple_sync():
    return jsonify({"status": "Apple Health sync initialized"})

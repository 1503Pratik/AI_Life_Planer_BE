# # routes/calendar.py
# import json
# from flask import Blueprint, redirect, request, url_for, jsonify
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from database.connection import db
# import config
# import os

# calendar_bp = Blueprint("calendar", __name__)

# # NOTE: you need client_secret.json downloaded from Google Cloud Console
# # Put it at project root as client_secret.json or adjust path.
# CLIENT_SECRETS_FILE = os.path.join(os.getcwd(), "client_secret.json")
# SCOPES = ["https://www.googleapis.com/auth/calendar.events", "https://www.googleapis.com/auth/userinfo.email"]

# @calendar_bp.route("/auth_url", methods=["GET"])
# def get_auth_url():
#     flow = Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE,
#         scopes=SCOPES,
#         redirect_uri=config.settings.OAUTH_REDIRECT_URI
#     )
#     auth_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
#     # Save state temporarily if needed. For simplicity return url to client
#     return jsonify({"auth_url": auth_url})

# @calendar_bp.route("/oauth2callback", methods=["GET"])
# def oauth2callback():
#     state = request.args.get("state")
#     flow = Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE,
#         scopes=SCOPES,
#         redirect_uri=config.settings.OAUTH_REDIRECT_URI
#     )
#     flow.fetch_token(authorization_response=request.url)
#     credentials = flow.credentials
#     token_doc = {
#         "token": credentials.to_json(),
#         "created_at": credentials.expiry.isoformat()
#     }
#     res = db.calendar_tokens.insert_one(token_doc)
#     return jsonify({"message": "Google Calendar connected", "token_id": str(res.inserted_id)})

# def _get_service_from_token_doc(token_doc):
#     creds_json = token_doc["token"]
#     from google.oauth2.credentials import Credentials
#     creds = Credentials.from_authorized_user_info(json.loads(creds_json), SCOPES)
#     service = build("calendar", "v3", credentials=creds)
#     return service

# @calendar_bp.route("/events/create/<token_id>", methods=["POST"])
# def create_event(token_id):
#     data = request.get_json() or {}
#     token_doc = db.calendar_tokens.find_one({"_id": ObjectId(token_id)})
#     if not token_doc:
#         return jsonify({"error": "token not found"}), 404
#     service = _get_service_from_token_doc(token_doc)
#     event = {
#         "summary": data.get("summary", "AI Planner Event"),
#         "description": data.get("description", ""),
#         "start": {"dateTime": data["start"], "timeZone": data.get("timeZone", "UTC")},
#         "end": {"dateTime": data["end"], "timeZone": data.get("timeZone", "UTC")},
#     }
#     created = service.events().insert(calendarId="primary", body=event).execute()
#     return jsonify(created), 201




from flask import Blueprint, request, jsonify
from database.connection import db
from datetime import datetime

calendar_bp = Blueprint("calendar", __name__)

@calendar_bp.route("/add", methods=["POST"])
def add_event():
    data = request.json
    event = {
        "user_id": data["user_id"],
        "title": data["title"],
        "date": data["date"],
        "time": data.get("time"),
        "created_at": datetime.utcnow()
    }
    result = db.calendar.insert_one(event)
    return jsonify({"message": "Event added", "id": str(result.inserted_id)})

@calendar_bp.route("/all/<user_id>", methods=["GET"])
def get_events(user_id):
    events = list(db.calendar.find({"user_id": user_id}))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events)

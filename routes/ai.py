# from flask import Blueprint, request, jsonify
# from services.ai_engine import process_user_query

# ai_bp = Blueprint("ai", __name__)

# @ai_bp.route("/process", methods=["POST"])
# def ai_process():
#     query = request.json["query"]
#     response = process_user_query(query)
#     return jsonify({"ai_output": response})
# @ai_bp.route("/recommend/tasks/<user_id>", methods=["GET"])
# def recommend_tasks(user_id):
#     recommendations = recommend_tasks_for_user(user_id)
#     return jsonify({
#         "user_id": user_id,
#         "recommended_tasks": recommendations
#     })

# from flask import Blueprint, request, jsonify
# from services.ai_engine import process_user_query
# from services.recommendation import RecommendationService 
# from services.utils import serialize_doc 

# ai_bp = Blueprint("ai", __name__)

# rec_service = RecommendationService()  

# @ai_bp.route("/process", methods=["POST"])
# def ai_process():
#     query = request.json["query"]
#     response = process_user_query(query)
#     return jsonify({"ai_output": response})

# # # ✅ NEW ENDPOINT (Fixes your 404)
# # @ai_bp.route("/recommend/tasks/<user_id>", methods=["GET"])
# # def recommend_tasks(user_id):
# #     result = rec_service.recommend_next_tasks(user_id)
# #     return jsonify(result)

# @ai_bp.route("/recommend/tasks/<user_id>", methods=["GET"])
# def recommend_tasks(user_id):
#     service = RecommendationService()
#     result = service.recommend_next_tasks(user_id)

#     # Convert ObjectId in tasks list
#     result["chosen"] = [serialize_doc(t) for t in result["chosen"]]

#     return jsonify(result)


# from flask import Blueprint, request, jsonify
# from services.ai_engine import process_user_query
# from services.recommendation import RecommendationService
# from utils.helpers import serialize_doc
# from database.models import get_tasks_for_user

# ai_bp = Blueprint("ai", __name__)
# rec_service = RecommendationService()

# # ---------------- AI CHAT ----------------
# @ai_bp.route("/process", methods=["POST"])
# def ai_process():
#     data = request.get_json(silent=True) or {}
#     query = data.get("query", "")

#     if not query:
#         return jsonify({"error": "query is required"}), 400

#     response = process_user_query(query)
#     return jsonify({"ai_output": response})


# # ---------------- TASK RECOMMENDATION ----------------
# @ai_bp.route("/recommend/tasks/<user_id>", methods=["GET"])
# def recommend_tasks(user_id):
#     result = rec_service.recommend_next_tasks(user_id)
#     result["chosen"] = [serialize_doc(t) for t in result["chosen"]]
#     return jsonify(result)


# # ✅ PRODUCTIVITY (ONLY ONE ROUTE + UNIQUE FUNCTION NAME)
# @ai_bp.route("/productivity/<user_id>", methods=["GET"])
# def generate_productivity_plan(user_id):
#     tasks = get_tasks_for_user(user_id)
#     titles = [t.get("title") for t in tasks if "title" in t]

#     tips = rec_service.ai.suggest_daily_plan(titles) if titles else "No tasks available for planning."
#     return jsonify({"productivity_plan": tips})




from flask import Blueprint, request, jsonify, g
from services.ai_engine import process_user_query
from services.recommendation import RecommendationService
from utils.helpers import serialize_doc
from database.models import get_tasks_for_user
from utils.auth import auth_required

ai_bp = Blueprint("ai", __name__)
rec_service = RecommendationService()

# ---------------- AI CHAT ----------------
@ai_bp.route("/process", methods=["POST"])
@auth_required
def ai_process():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "query is required"}), 400

    response = process_user_query(query)
    return jsonify({"ai_output": response})


# ---------------- TASK RECOMMENDATION ----------------
@ai_bp.route("/recommend/tasks", methods=["GET"])
@auth_required
def recommend_tasks():
    result = rec_service.recommend_next_tasks(g.user_id)
    result["chosen"] = [serialize_doc(t) for t in result["chosen"]]
    return jsonify(result)


# ---------------- PRODUCTIVITY PLAN ----------------
@ai_bp.route("/productivity", methods=["GET"])
@auth_required
def generate_productivity_plan():
    tasks = get_tasks_for_user(g.user_id)
    titles = [t.get("title") for t in tasks if "title" in t]

    tips = rec_service.ai.suggest_daily_plan(titles) if titles else "No tasks available for planning."
    return jsonify({"productivity_plan": tips})

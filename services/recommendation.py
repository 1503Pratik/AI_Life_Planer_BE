# services/recommendation.py
from .ai_engine import AIEngine
from database.models import get_tasks_for_user, get_habits_for_user, get_goals_for_user

class RecommendationService:
    def __init__(self):
        self.ai = AIEngine()

    def recommend_next_tasks(self, user_id: str, limit: int = 5):
        tasks = get_tasks_for_user(user_id)
        pending = [t for t in tasks if t.get("status") == "pending"]
        # Basic heuristic: sort by due_date if exists, else created_at
        def key_fn(t):
            return (t.get("due_date") or "", t.get("created_at") or "")
        pending_sorted = sorted(pending, key=key_fn)
        chosen = pending_sorted[:limit]
        titles = [t.get("title") for t in chosen]
        ai_plan = self.ai.suggest_daily_plan(titles) if titles else "No tasks for today"
        return {"chosen": chosen, "ai_plan": ai_plan}

    def habit_suggestions(self, user_id: str):
        habits = get_habits_for_user(user_id)
        prompt = f"User habits: {habits}. Suggest 5 complementary habits and a short reason each."
        return self.ai.generate_response(prompt)

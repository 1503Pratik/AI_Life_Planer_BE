# services/recommendation.py

from datetime import datetime
from database.models import User, Habit, Goal
from .ai_engine import AIEngine

class RecommendationService:
    """
    Handles AI-powered recommendations for tasks,
    habits, goals, and life planning.
    """

    def __init__(self):
        self.ai = AIEngine()

    # -----------------------------------------------
    # 1. Personalized Habit Recommendations
    # -----------------------------------------------
    def recommend_habits(self, user: User) -> str:
        prompt = f"""
        The user has the following lifestyle details:
        - Age: {user.age}
        - Work type: {user.work_type}
        - Current habits: {user.habits}

        Suggest 5 new healthy habits the user can adopt.
        """

        return self.ai.generate_response(prompt)

    # -----------------------------------------------
    # 2. Personalized Goal Breakdown
    # -----------------------------------------------
    def break_down_goal(self, goal: Goal) -> str:
        prompt = f"""
        Break down this goal into small, achievable weekly steps:

        Goal Title: {goal.title}
        Description: {goal.description}

        Provide an action plan.
        """

        return self.ai.generate_response(prompt)

    # -----------------------------------------------
    # 3. Daily Task Suggestions
    # -----------------------------------------------
    def suggest_daily_tasks(self, user: User, habits: list[Habit], goals: list[Goal]) -> str:
        prompt = f"""
        Based on the user's profile and goals, prepare a list of suggested tasks.

        User:
        {user}

        Habits:
        {habits}

        Goals:
        {goals}

        Return in bullet points.
        """

        return self.ai.generate_response(prompt)

    # -----------------------------------------------
    # 4. Productivity Tips
    # -----------------------------------------------
    def productivity_tips(self, profession: str) -> str:
        prompt = f"""
        Provide 10 productivity tips for someone working as:
        {profession}
        """

        return self.ai.generate_response(prompt)

    # -----------------------------------------------
    # 5. Mood-based Recommendations
    # -----------------------------------------------
    def mood_recommendation(self, mood: str) -> str:
        prompt = f"""
        The user feels {mood}. Suggest:
        - An appropriate task
        - A relaxation activity
        - A short motivational quote
        """

        return self.ai.generate_response(prompt)

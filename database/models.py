# from database.connection import db
# from datetime import datetime

# # USER Document
# def create_user(name, email):
#     user = {
#         "name": name,
#         "email": email,
#         "created_at": datetime.utcnow()
#     }
#     return db.users.insert_one(user)

# # TASK Document
# def create_task(user_id, title, description, due_date):
#     task = {
#         "user_id": user_id,
#         "title": title,
#         "description": description,
#         "due_date": due_date,
#         "status": "pending",
#         "created_at": datetime.utcnow()
#     }
#     return db.tasks.insert_one(task)

# # HABIT Document
# def create_habit(user_id, habit_name, frequency):
#     habit = {
#         "user_id": user_id,
#         "habit_name": habit_name,
#         "frequency": frequency,
#         "streak": 0,
#         "created_at": datetime.utcnow()
#     }
#     return db.habits.insert_one(habit)

# # GOAL Document
# def create_goal(user_id, goal_title, deadline):
#     goal = {
#         "user_id": user_id,
#         "goal_title": goal_title,
#         "deadline": deadline,
#         "progress": 0,
#         "created_at": datetime.utcnow()
#     }
#     return db.goals.insert_one(goal)

# # ACTIVITY LOG
# def log_activity(user_id, activity_type):
#     log_entry = {
#         "user_id": user_id,
#         "activity_type": activity_type,
#         "timestamp": datetime.utcnow()
#     }
#     return db.activity_logs.insert_one(log_entry)



from database.connection import db
from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash

# -----------------------------------
# USER Document
# -----------------------------------
# def create_user(name, email):
#     user = {
#         "name": name,
#         "email": email,
#         "created_at": datetime.utcnow()
#     }
#     return db.users.insert_one(user)


def create_user(name, email, password):
    user = {
        "name": name,
        "email": email,
        "password": generate_password_hash(password),  # 🔥 HASHED PASSWORD
        "created_at": datetime.utcnow()
    }
    return db.users.insert_one(user)

def find_user_by_email(email):
    return db.users.find_one({"email": email})

def find_user_by_id(user_id):
    return db.users.find_one({"_id": ObjectId(user_id)})

# -----------------------------------
# TASK Document
# -----------------------------------
def create_task(user_id, title, description, due_date):
    task = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    return db.tasks.insert_one(task)

# -----------------------------------
# HABIT Document
# -----------------------------------
# def create_habit(user_id, habit_name, frequency):
#     habit = {
#         "user_id": user_id,
#         "habit_name": habit_name,
#         "frequency": frequency,
#         "streak": 0,
#         "completions": [],         # NEW FIELD ADDED
#         "created_at": datetime.utcnow()
#     }
#     return db.habits.insert_one(habit)

def create_habit(user_id, habit_name, frequency):
    habit = {
        "user_id": user_id,
        "habit_name": habit_name,
        "frequency": frequency,
        "streak": 0,
        "completions": [],
        "steps": 0,          
        "calories": 0,      
        "created_at": datetime.utcnow()
    }
    return db.habits.insert_one(habit)


# --- NEW: Habit helpers ---
def get_habit_by_id(habit_id: str):
    return db.habits.find_one({"_id": ObjectId(habit_id)})

def mark_habit_done(habit_id: str, date_str: str = None):
    """
    Increment streak + add completion date.
    """
    date_iso = date_str or datetime.utcnow().isoformat()
    return db.habits.update_one(
        {"_id": ObjectId(habit_id)},
        {
            "$push": {"completions": date_iso},
            "$inc": {"streak": 1}
        }
    )

# -----------------------------------
# GOAL Document
# -----------------------------------
def create_goal(user_id, goal_title, deadline):
    goal = {
        "user_id": user_id,
        "goal_title": goal_title,
        "deadline": deadline,
        "progress": 0,
        "created_at": datetime.utcnow()
    }
    return db.goals.insert_one(goal)

# --- NEW: Goal helpers ---
def find_goal_by_id(goal_id: str):
    return db.goals.find_one({"_id": ObjectId(goal_id)})

def update_goal_progress(goal_id: str, progress_delta: int = 0, set_progress: int = None):
    """
    Either increment progress OR set a new progress value.
    """
    if set_progress is not None:
        return db.goals.update_one(
            {"_id": ObjectId(goal_id)},
            {"$set": {"progress": set_progress}}
        )
    else:
        return db.goals.update_one(
            {"_id": ObjectId(goal_id)},
            {"$inc": {"progress": progress_delta}}
        )

# -----------------------------------
# ACTIVITY LOG
# -----------------------------------
def log_activity(user_id, activity_type):
    log_entry = {
        "user_id": user_id,
        "activity_type": activity_type,
        "timestamp": datetime.utcnow()
    }
    return db.activity_logs.insert_one(log_entry)


# -----------------------------------
# ADD THESE MISSING HABIT FUNCTIONS
# -----------------------------------

def get_habits_for_user(user_id: str):
    """Return all habits for a user."""
    return list(db.habits.find({"user_id": user_id}))

def update_habit(habit_id: str, update_data: dict):
    """Update habit fields: name, frequency, etc."""
    return db.habits.update_one(
        {"_id": ObjectId(habit_id)},
        {"$set": update_data}
    )
def get_goals_for_user(user_id: str):
    return list(db.goals.find({"user_id": user_id}))

def update_goal(goal_id: str, update_data: dict):
    return db.goals.update_one(
        {"_id": ObjectId(goal_id)},
        {"$set": update_data}
    )
def get_tasks_for_user(user_id: str):
    """Return all tasks for a user."""
    return list(db.tasks.find({"user_id": user_id}))

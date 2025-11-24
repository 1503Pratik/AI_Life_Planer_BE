from flask import Flask
from flask_cors import CORS
import config

app = Flask(__name__)
# app.secret_key = config.SECRET_KEY
app.secret_key = config.settings.SECRET_KEY
CORS(app)

# Register Blueprints
from routes.user import user_bp
from routes.tasks import task_bp
from routes.habits import habit_bp
from routes.goals import goal_bp
from routes.ai import ai_bp
from routes.calendar import calendar_bp
from routes.budget import budget_bp
from routes.integrations import integration_bp

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(task_bp, url_prefix='/tasks')
app.register_blueprint(habit_bp, url_prefix='/habits')
app.register_blueprint(goal_bp, url_prefix='/goals')
app.register_blueprint(ai_bp, url_prefix='/ai')
app.register_blueprint(calendar_bp, url_prefix="/calendar")
app.register_blueprint(budget_bp, url_prefix="/budget")
app.register_blueprint(integration_bp, url_prefix="/integrations")

if __name__ == "__main__":
    app.run(debug=True)

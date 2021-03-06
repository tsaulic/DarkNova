from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from configuration import game_db_path, secret_key

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = game_db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = secret_key
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)

from core.routes import login
from core.routes import logout
from core.routes import play
from core.routes import populate
from core.routes import schedule

app.register_blueprint(login.bp)
app.register_blueprint(logout.bp)
app.register_blueprint(play.bp)
app.register_blueprint(populate.bp)
app.register_blueprint(schedule.bp)

from core.scheduler import scheduler_start_on_bg_thread

# always start the scheduler with the app, as gunicorn will re-start the app if no requests are made to it within a
# specified timeout
scheduler_start_on_bg_thread()

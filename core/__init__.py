from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data/game.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from core.models import Player


def init_db():
    """For use on command line for setting up
    the database.
    """

    db.drop_all()
    db.create_all()

def populate_mock_db():
    db.session.add(Player(username="Rincewind", email="example@example.com"))
    db.session.add(Player(username="Unknown", email="unknown@unknown.com"))
    db.session.add(Player(username="Test", email="test@test.com"))
    db.session.commit()


import core.routes

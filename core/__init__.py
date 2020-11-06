from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data/game.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from core.models import Player, Sector


def init_db():
    """For use on command line for setting up
    the database.
    """

    db.drop_all()
    db.create_all()


def populate_mock_db():
    sol = Sector(id=0, name='Sol')
    sector_1 = Sector(id=1, name="")
    db.session.add(Player(
        username="Rincewind",
        email="example@example.com",
        ship_name="The Luggage",
        sector=sector_1
    ))
    db.session.add(Player(
        username="Unknown",
        email="unknown@unknown.com",
        ship_name="Unknown ship",
        sector=sol
    ))
    db.session.add(Player(
        username="Test",
        email="test@test.com",
        ship_name="Test ship",
        sector=sol
    ))
    db.session.commit()


import core.routes

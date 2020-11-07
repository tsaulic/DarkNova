from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from core.models import Player, Sector


def init_db():
    """For use on command line for setting up
    the database.
    """

    db.drop_all()
    db.create_all()


def populate_mock_db(sectors_value):
    db.drop_all()
    db.create_all()
    sol = Sector(id=0, name='Sol')
    db.session.add(Player(
        username="Rincewind",
        email="example@example.com",
        ship_name="The Luggage",
        sector=sol
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

    for sector in range(1, sectors_value):
        db.session.add(Sector(id=sector, name=""))
    db.session.commit()


import core.routes

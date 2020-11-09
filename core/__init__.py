from datetime import timedelta
from random import randrange

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import game_db_path, secret_key

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = game_db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = secret_key
app.permanent_session_lifetime = timedelta(minutes=5)
db = SQLAlchemy(app)

from core.models import Player, Sector, Planet


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
        db.session.add(Sector(id=sector, name=''))
        if has_planet(8) and sector != 0: db.session.add(Planet(name='Unknown planet', sector_id=sector))
        if has_planet(8) and sector != 0: db.session.add(Planet(name='Unknown planet', sector_id=sector))
        if has_planet(8) and sector != 0: db.session.add(Planet(name='Unknown planet', sector_id=sector))
        if has_planet(8) and sector != 0: db.session.add(Planet(name='Unknown planet', sector_id=sector))
        if has_planet(8) and sector != 0: db.session.add(Planet(name='Unknown planet', sector_id=sector))
    db.session.commit()


def has_planet(cutoff):
    rand_num = randrange(9)
    return False if rand_num > cutoff else True

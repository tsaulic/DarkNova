import sqlite3
from random import randrange

import flask
from flask import request, Blueprint, redirect, url_for
from sqlalchemy import exc

from configuration import sectors_default_amount
from core import db
from core.models import Planet
from core.models import Player
from core.models import Sector

bp = Blueprint('populate', __name__)

sol = Sector(id=0, name='Sol')


def populate_mock_db(sectors_value):
    db.session.expire_all()
    db.drop_all()
    db.create_all()
    db.session.expire_all()

    db.session.add(Player(
        username="Admin",
        email='admin@example.com',
        ship_name="Admin's ship",
        sector=sol
    ))

    for sector in range(1, sectors_value):
        db.session.add(Sector(id=sector, name=''))
        if has_planet(4) and sector != 0: db.session.add(Planet(name='Unowned', sector_id=sector))
        if has_planet(2) and sector != 0: db.session.add(Planet(name='Unowned', sector_id=sector))
        if has_planet(0) and sector != 0: db.session.add(Planet(name='Unowned', sector_id=sector))

    try:
        db.session.commit()
    except AssertionError as err:
        db.session.rollback()
        flask.abort(409, err)
    except (exc.IntegrityError, sqlite3.IntegrityError) as err:
        db.session.rollback()
        flask.abort(409, err.orig)
    except Exception as err:
        db.session.rollback()
        flask.abort(500, err)
    finally:
        db.session.close()


def has_planet(cutoff):
    rand_num = randrange(9)
    return False if rand_num > cutoff else True


def insert_player(player_name, ship_name):
    email_seed = randrange(1, 999) * randrange(1, 999)
    db.session.add(Player(
        username=player_name,
        email='{}@example.com'.format(email_seed),
        ship_name=ship_name,
        sector=sol
    ))

    try:
        db.session.commit()
    except AssertionError as err:
        db.session.rollback()
        flask.abort(409, err)
    except (exc.IntegrityError, sqlite3.IntegrityError) as err:
        db.session.rollback()
        flask.abort(409, err.orig)
    except Exception as err:
        db.session.rollback()
        flask.abort(500, err)
    finally:
        db.session.close()
        return redirect(url_for('play.play'))


@bp.route('/populate', methods=['GET'])
def populate():
    sector_value = request.args.get('sectors')
    sol_exists = False

    try:
        sector_value = int(sector_value)
    except ValueError:
        flask.abort(400, 'Parameter sector must be of type int')
    except TypeError:
        sector_value = sectors_default_amount

    try:
        sol_exists = Sector.query.filter_by(id=0).scalar() is not None
    except exc.OperationalError:
        pass

    if sector_value is not None and not sol_exists:
        populate_mock_db(sector_value)
    elif not sol_exists:
        populate_mock_db(sectors_default_amount)
    else:
        flask.abort(400, 'DB already created')

    return 'success'

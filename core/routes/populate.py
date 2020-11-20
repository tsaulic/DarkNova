from random import randrange

import flask
from flask import request, Blueprint
from sqlalchemy import exc

from configuration import sectors_default_amount, turns_start_amount
from core import db
from core.models import Player, Planet, Sector, Port
from core.updater import start_scheduler
from core.util import commit_try

bp = Blueprint('populate', __name__)


def populate_mock_db(sectors_value):
    db.drop_all()
    db.create_all()

    db.session.expire_on_commit = False
    commit_try()

    db.session.add(Sector(
        id=0,
        name='Sol',
        beacon='The hub of the universe!'
    ))

    db.session.add(Player(
        username='Admin',
        email='admin@example.com',
        ship_name='Admin\'s ship',
        turns=999999,
        sector_key=0  # Sol
    ))

    db.session.add(Port(
        type=0,
        sector_key=0  # Sol
    ))

    commit_try()

    for sector in range(1, sectors_value):
        db.session.add(Sector(id=sector, name=''))

        if has_feature(4) and sector != 0: db.session.add(Planet(name='Unowned', sector_key=sector))
        if has_feature(2) and sector != 0: db.session.add(Planet(name='Unowned', sector_key=sector))
        if has_feature(0) and sector != 0: db.session.add(Planet(name='Unowned', sector_key=sector))
        if has_feature(5) and sector != 0: db.session.add(Port(type=randrange(0, 5), sector_key=sector))

    if commit_try(): start_scheduler()


def has_feature(cutoff):
    rand_num = randrange(9)
    return False if rand_num > cutoff else True


def insert_player(player_name, ship_name):
    email_seed = randrange(1, 999) * randrange(1, 999)
    db.session.add(Player(
        username=player_name,
        email='{}@example.com'.format(email_seed),
        ship_name=ship_name,
        turns=turns_start_amount,
        sector_key=0  # Sol
    ))

    commit_try()


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
    except exc.ProgrammingError:
        pass

    if sector_value is not None and not sol_exists:
        populate_mock_db(sector_value)
    elif not sol_exists:
        populate_mock_db(sectors_default_amount)
    else:
        flask.abort(400, 'DB already created')

    return 'success'

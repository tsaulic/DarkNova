from random import randrange

import flask
from flask import request, Blueprint
from sqlalchemy import exc

from configuration import sectors_default_amount, turns_start_amount
from core import db
from core.models import Player, Planet, Sector, Port, Link
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

    db.session.add(Link(to=1, sector_key=0))
    for sector in range(1, sectors_value):
        # create each sector
        db.session.add(Sector(id=sector, name=''))

        # add sector mandatory initial warp links
        db.session.add(Link(to=sector - 1, sector_key=sector))
        if sector != sectors_value: db.session.add(Link(to=sector + 1, sector_key=sector))

        # add up to 10 more random links
        for link_to in range(0, 9):
            link = randrange(0, sectors_value)
            if has_feature(33) and sector != link:
                db.session.add(Link(to=link, sector_key=sector))

        # add planets
        if has_feature(33) and sector != 0:
            db.session.add(Planet(name='Unowned', sector_key=sector))
        if has_feature(11) and sector != 0:
            db.session.add(Planet(name='Unowned', sector_key=sector))
        if has_feature(1) and sector != 0:
            db.session.add(Planet(name='Unowned', sector_key=sector))

        # add ports
        if has_feature(66) and sector != 0:
            if has_feature(1) and sector in range(1, 5):
                db.session.add(Port(type=0, sector_key=sector))
            elif has_feature(66):
                db.session.add(Port(type=randrange(1, 3), sector_key=sector))
            else:
                db.session.add(Port(type=randrange(3, 5), sector_key=sector))

    commit_try()


def has_feature(cutoff):
    rand_num = randrange(99)
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

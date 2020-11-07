from flask import render_template, request

from core import app, populate_mock_db, db
from core.models import Player, Sector


@app.route('/')
def game_route():
    from sqlalchemy import exc
    player_name = request.args.get('player')
    move = request.args.get('move')
    active_player = None
    players_in_sector = ''

    if player_name is not None:
        active_player = Player.query.filter_by(username=player_name).first()

    if active_player is not None:
        for player in active_player.sector.players:
            if player.username != player_name:
                players_in_sector += "{} ,".format(player.username).strip().rstrip(',')

        if players_in_sector == "": players_in_sector = "None"
    else:
        return render_error("Invalid player")

    if move is not None:
        active_player.sector = Sector.query.filter_by(id=move).first()
        try:
            db.session.commit()
        except AttributeError:
            return render_error("Invalid sector")
        except exc.IntegrityError:
            return render_error("Invalid sector")

    sector_name = active_player.sector.name

    return render_template(
        'index.html',
        title="Test",
        content='Playing as {} aboard {} in sector {} {}; Other ships here: {}'.format(
            active_player.username,
            active_player.ship_name,
            active_player.sector.id,
            '({})'.format(sector_name) if sector_name != "" else '{}'.format(sector_name),
            players_in_sector)
    )


@app.route('/populate')
def populate_mock_db_route():
    sector_value = request.args.get('sectors')

    try:
        sector_value = int(sector_value)
    except ValueError:
        return 'Parameter must be of type int'

    if sector_value is not None:
        populate_mock_db(sector_value)
    else:
        populate_mock_db(5)

    return 'success'


def render_error(message):
    return render_template(
        'index.html',
        title='Error',
        content=message
    )

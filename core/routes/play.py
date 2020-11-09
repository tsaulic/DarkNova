from flask import render_template, request, session, redirect, url_for, Blueprint
from sqlalchemy import exc

from configuration import version
from core.actions.capture import capture
from core.actions.move import move
from core.models import Player, Sector
from core.render_static import render_error
from core.routes.populate import insert_player

bp = Blueprint('play', __name__)


@bp.route('/play')
def play():
    active_player = None
    players_in_sector = None
    player_name = None
    ship_name = None

    if 'player_name' in session:
        player_name = session['player_name']
        player_exists = Player.query.filter_by(username=player_name).scalar() is not None
    else:
        return redirect(url_for('login.login'))

    if 'ship_name' in session:
        ship_name = session['ship_name']

    if not player_exists and player_name is not None and ship_name is not None:
        insert_player(player_name, ship_name)

    actions = {}

    if request.args.get('move') is not None:
        actions['move'] = request.args.get('move')
    if request.args.get('capture') is not None:
        actions['capture'] = request.args.get('capture')

    if player_name is not None:
        # noinspection PyBroadException
        try:
            active_player = Player.query.filter_by(username=player_name).first()
        except exc.OperationalError:
            return render_error('Please create the DB first')
        except Exception:
            return render_error('Failed to fetch player')

    if active_player is not None:
        planets = Sector.query.filter_by(id=active_player.sector.id).first().planets
        if len(active_player.sector.players) > 1:
            players_in_sector = ', '.join(player.username for player in active_player.sector.players
                                          if player.username != active_player.username)
    else:
        return render_error("Invalid player")

    for action in actions:
        if action == 'move':
            return move(actions['move'], active_player)
        if action == 'capture':
            return capture(actions['capture'], planets, active_player)

    sector_name = active_player.sector.name
    sector_info = '{} ({})'.format(active_player.sector.id, sector_name) if sector_name != "" \
        else active_player.sector.id

    if len(planets) > 0:
        planets_in_sector = ', '.join('{} id={}'.format(planet.name, planet.id) for planet in planets)
    else:
        planets_in_sector = None

    return render_template(
        'play.html',
        title='DarkNova version: {}'.format(version),
        content='Playing as {} aboard {} in sector {}; Other ships here: {}; Planets: {}'.format(
            active_player.username,
            active_player.ship_name,
            sector_info,
            players_in_sector,
            planets_in_sector),
        player=active_player,
        sector=active_player.sector.id,
        planets=planets
    )

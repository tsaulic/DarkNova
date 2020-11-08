from flask import render_template, request, session, redirect, url_for
from sqlalchemy import exc

from config import version
from core import app
from core.actions.move import move
from core.actions.take import take
from core.models import Player, Sector
from core.render_static import render_error


@app.route('/play')
def play():
    if 'player' in session:
        player_name = session['player']
    else:
        return redirect(url_for('login'))

    actions = {}

    if request.args.get('move') is not None:
        actions['move'] = request.args.get('move')
    if request.args.get('take') is not None:
        actions['take'] = request.args.get('take')

    active_player = None
    players_in_sector = None

    if player_name is not None:
        # noinspection PyBroadException
        try:
            active_player = Player.query.filter_by(username=player_name).first()
        except exc.OperationalError:
            return redirect(url_for('populate'))
        except Exception:
            return render_error("Failed to fetch player")

    if active_player is not None:
        planets = Sector.query.filter_by(id=active_player.sector.id).first().planets
        if len(active_player.sector.players) > 1:
            players_in_sector = ', '.join(player.username for player in active_player.sector.players
                                          if player.username != active_player.username)
    else:
        return render_error("Invalid player")

    for action in actions:
        if action is 'move': return move(actions['move'], active_player)
        if action is 'take': return take(actions['take'], planets, active_player)

    sector_name = active_player.sector.name
    sector_info = '{} ({})'.format(active_player.sector.id, sector_name) if sector_name != "" \
        else active_player.sector.id

    if len(planets) > 0:
        planets_in_sector = ', '.join('{} id={}'.format(planet.name, planet.id) for planet in planets)
    else:
        planets_in_sector = None

    return render_template(
        'game.html',
        title='DarkNova version: {}'.format(version),
        content='Playing as {} aboard {} in sector {}; Other ships here: {}; Planets: {}'.format(
            active_player.username,
            active_player.ship_name,
            sector_info,
            players_in_sector,
            planets_in_sector)
    )

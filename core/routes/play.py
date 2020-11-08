from flask import render_template, request, session, redirect, url_for

from config import version
from core import app, db
from core.models import Player, Sector
from core.render_static import render_error


@app.route('/play')
def play():
    if 'player' in session:
        player_name = session['player']
    else:
        return redirect(url_for('login'))

    from sqlalchemy import exc
    move = request.args.get('move')
    take = request.args.get('take')
    active_player = None
    players_in_sector = None

    if player_name is not None:
        try:
            active_player = Player.query.filter_by(username=player_name).first()
        except exc.OperationalError:
            return redirect(url_for('populate'))

    if move is not None:
        active_player.sector = Sector.query.filter_by(id=move).first()

        try:
            db.session.commit()
            return redirect(url_for('play'))
        except AttributeError:
            return render_error("Invalid sector")
        except exc.IntegrityError:
            return render_error("Invalid sector")

    if active_player is not None:
        if len(active_player.sector.players) > 1:
            players_in_sector = ', '.join(player.username for player in active_player.sector.players
                                          if player.username != active_player.username)
    else:
        return render_error("Invalid player")

    sector_name = active_player.sector.name
    sector_info = '{} ({})'.format(active_player.sector.id, sector_name) if sector_name != "" \
        else active_player.sector.id

    planets = Sector.query.filter_by(id=active_player.sector.id).first().planets
    if len(planets) > 0:
        planets_in_sector = ', '.join('{} id={}'.format(planet.name, planet.id) for planet in planets)
    else:
        planets_in_sector = None

    for planet in planets:
        if take is not None:
            try:
                take = int(take)
            except ValueError:
                return 'Parameter take must be of type int'

            if take == planet.id and planet.owner == []:
                planet.name = '{}-{}'.format(active_player.username[0] + active_player.ship_name[0],
                                             active_player.sector.id)
                planet.owner.append(active_player)

                try:
                    db.session.commit()
                    return redirect(url_for('play'))
                except AttributeError:
                    return render_error("Invalid planet")
                except exc.IntegrityError:
                    return render_error("Invalid planet")

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

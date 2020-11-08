from flask import render_template, request, session, redirect, url_for

from config import version
from core import app, populate_mock_db, db
from core.models import Player, Sector


@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        player = request.form['player']
        session['player'] = player
        return redirect(url_for('game_route'))
    else:
        if 'player' in session:
            return redirect(url_for('game_route'))

        return render_template(
            'login.html',
            title="Login"
        )


@app.route('/logout')
def logout():
    session.pop('player', None)
    return redirect(url_for('login'))


@app.route('/game')
def game_route():
    if 'player' in session:
        player_name = session['player']
    else:
        return redirect(url_for("login"))

    from sqlalchemy import exc
    move = request.args.get('move')
    take = request.args.get('take')
    active_player = None
    players_in_sector = ''
    planets_in_sector = ''

    if player_name is not None:
        active_player = Player.query.filter_by(username=player_name).first()

    if move is not None:
        active_player.sector = Sector.query.filter_by(id=move).first()

        try:
            db.session.commit()
        except AttributeError:
            return render_error("Invalid sector")
        except exc.IntegrityError:
            return render_error("Invalid sector")

    if active_player is not None:
        for player in active_player.sector.players:
            if player.username != player_name:
                players_in_sector += "{} ,".format(player.username).rstrip(',').strip()

        if players_in_sector == "": players_in_sector = "None"
    else:
        return render_error("Invalid player")

    sector_name = active_player.sector.name
    sector_info = '{} ({})'.format(active_player.sector.id, sector_name) if sector_name != "" \
        else active_player.sector.id

    planets = Sector.query.filter_by(id=active_player.sector.id).first().planets
    for planet in planets:
        planets_in_sector += "{} {},".format(planet.name, planet.id).rstrip(',').strip()

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


@app.route('/populate')
def populate_mock_db_route():
    sectors_default = 5
    sector_value = request.args.get('sectors')

    try:
        sector_value = int(sector_value)
    except ValueError:
        return 'Parameter sector must be of type int'
    except TypeError:
        sector_value = sectors_default

    if sector_value is not None:
        populate_mock_db(sector_value)
    else:
        populate_mock_db(sectors_default)

    return 'success'


def render_error(message):
    return render_template(
        'game.html',
        title='Error',
        content=message
    )

import flask
from flask import url_for, redirect, flash

from core.strings import not_enough_turns
from core.util import commit_try


def capture(planet_id, planets, active_player):
    if active_player.turns > 0:
        pass
    else:
        flash(not_enough_turns)
        return redirect(url_for('play.play'))

    try:
        planet_id = int(planet_id)
    except ValueError:
        flask.abort(500, 'Parameter capture must be of type int')

    for planet in planets:
        sector_planets = len([planet for planet in active_player.sector.planets if planet.owner is not None])
        if planet_id == planet.id and planet.owner is None:
            planet.name = '{}-{}-{}'.format(active_player.username[0] + active_player.ship_name[0],
                                            active_player.sector.id,
                                            sector_planets + 1)
            planet.owner = active_player.id
            active_player.turns = active_player.turns - 1

            if commit_try(expunge=False): return redirect(url_for('play.play'))
    else:
        return redirect(url_for('play.play'))

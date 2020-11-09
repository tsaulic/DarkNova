from flask import url_for, redirect
from sqlalchemy import exc

from core import db
from core.render_static import render_error


def capture(planet_id, planets, active_player):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return render_error('Parameter capture must be of type int')

    for planet in planets:
        sector_planets = len([planet for planet in active_player.sector.planets if planet.owner is not None])
        if planet_id == planet.id and planet.owner is None:
            planet.name = '{}-{}-{}'.format(active_player.username[0] + active_player.ship_name[0],
                                            active_player.sector.id,
                                            sector_planets + 1)
            planet.owner = active_player.id

            try:
                db.session.commit()
                return redirect(url_for('play'))
            except AttributeError:
                return render_error("Invalid planet")
            except exc.IntegrityError:
                return render_error("Invalid planet")
    else:
        return redirect(url_for('play'))

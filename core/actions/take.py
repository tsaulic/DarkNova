from flask import url_for
from sqlalchemy import exc
from werkzeug.utils import redirect

from core import db
from core.render_static import render_error


def take(planet_id, planets, active_player):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return 'Parameter take must be of type int'

    for planet in planets:
        if planet_id == planet.id and planet.owner == []:
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

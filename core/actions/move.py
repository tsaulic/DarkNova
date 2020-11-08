from flask import url_for, redirect
from sqlalchemy import exc

from core import Sector, db
from core.render_static import render_error


def move(sector, active_player):
    if sector is not None:
        active_player.sector = Sector.query.filter_by(id=sector).first()

        try:
            db.session.commit()
            return redirect(url_for('play'))
        except AttributeError:
            return render_error("Invalid sector")
        except exc.IntegrityError:
            return render_error("Invalid sector")
    else:
        return render_error("Sector must not be None")

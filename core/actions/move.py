import flask
from flask import url_for, redirect, flash
from sqlalchemy import exc

from core import db
from core.models import Sector
from core.strings import not_enough_turns, sector_must_be_int


def move(sector, active_player):
    if sector is not None:
        if active_player.turns > 0:
            pass
        else:
            flash(not_enough_turns)
            return redirect(url_for('play.play'))

        try:
            sector = int(sector)
        except ValueError:
            flash(sector_must_be_int)
            return redirect(url_for('play.play'))

        active_player.sector = Sector.query.filter_by(id=sector).first()
        active_player.turns -= 1

        try:
            db.session.commit()
        except AssertionError as err:
            db.session.rollback()
            flask.abort(409, err)
        except exc.IntegrityError as err:
            db.session.rollback()
            flask.abort(409, err.orig)
        except Exception as err:
            db.session.rollback()
            flask.abort(500, err)
        finally:
            db.session.close()
            return redirect(url_for('play.play'))
    else:
        flask.abort(500, 'Sector must not be None')

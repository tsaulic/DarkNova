import flask
from flask import url_for, redirect, flash
from sqlalchemy import exc

from core import db
from core.models import Sector


def move(sector, active_player):
    if sector is not None:
        try:
            sector = int(sector)
        except ValueError:
            flash("Please enter a sector number")
            return redirect(url_for('play.play'))

        active_player.sector = Sector.query.filter_by(id=sector).first()

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

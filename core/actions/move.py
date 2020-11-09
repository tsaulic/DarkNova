import sqlite3

import flask
from flask import url_for, redirect
from sqlalchemy import exc

from core import Sector, db


def move(sector, active_player):
    if sector is not None:
        active_player.sector = Sector.query.filter_by(id=sector).first()

        try:
            db.session.commit()
        except AssertionError as err:
            db.session.rollback()
            flask.abort(409, err)
        except (exc.IntegrityError, sqlite3.IntegrityError) as err:
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

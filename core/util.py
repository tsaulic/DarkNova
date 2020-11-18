import flask
from sqlalchemy import exc

from core import db


def commit_try(expunge = True):
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
        if expunge: db.session.expunge_all()
        db.session.close()
        return True

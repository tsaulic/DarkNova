from flask import session, redirect, url_for, Blueprint

bp = Blueprint('logout', __name__)


@bp.route('/logout', methods=['GET'])
def logout():
    session.pop('player_name', None)
    session.pop('ship_name', None)
    return redirect(url_for('login.login'))

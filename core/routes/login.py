from flask import request, session, redirect, url_for, render_template, Blueprint

bp = Blueprint('login', __name__)


@bp.route("/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        player_name = request.form['player_name']
        ship_name = request.form['ship_name']
        session['player_name'] = player_name
        session['ship_name'] = ship_name
        return redirect(url_for('play.play'))
    else:
        if 'player_name' in session:
            return redirect(url_for('play.play'))

        return render_template(
            'login.html',
            title="Login"
        )

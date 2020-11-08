from flask import request, session, redirect, url_for, render_template

from core import app


@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        player = request.form['player']
        session['player'] = player
        return redirect(url_for('play'))
    else:
        if 'player' in session:
            return redirect(url_for('play'))

        return render_template(
            'login.html',
            title="Login"
        )


@app.route('/logout')
def logout():
    session.pop('player', None)
    return redirect(url_for('login'))

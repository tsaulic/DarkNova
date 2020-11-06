from flask import jsonify

from core import app, init_db, Player, populate_mock_db


@app.route("/")
def game_route():
    from sqlalchemy import exc
    try:
        Player.query.all()
    except exc.OperationalError:
        init_db()

    players = Player.query.all()
    players_json = {}
    for player in players:
        players_json[player.id] = player.serialize()

    return jsonify(players_json)


@app.route("/reset_db")
def reset_db_route():
    init_db()
    return "success"


@app.route("/populate_mock_db")
def populate_mock_db_route():
    populate_mock_db()
    return "success"

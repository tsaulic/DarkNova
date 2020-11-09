import core.routes.login
import core.routes.play
import core.routes.populate
from core import app

if __name__ == '__main__':
    # do this until I fix my app :( or use Blueprints?
    print(core.routes.login)
    print(core.routes.populate)
    print(core.routes.play)
    # app.run(port=9909, debug=False)

    # does not work on Windows, use:
    # $env:FLASK_APP="game.py"
    # flask run --host=0.0.0.0 --port=9909
    # and turn off debug (debug=False)
    app.run(host='0.0.0.0')

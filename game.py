import core.routes.login
import core.routes.play
import core.routes.populate
from core import app

if __name__ == '__main__':
    # do this until I fix my app :( or use Blueprints?
    print(core.routes.login)
    print(core.routes.populate)
    print(core.routes.play)
    app.run(debug=True)

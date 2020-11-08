from core import app
import core.routes

if __name__ == '__main__':
    print('Running game version: {}'.format(core.routes.version))
    app.run(debug=True)

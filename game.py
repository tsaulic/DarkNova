from flask import Flask

app = Flask(__name__)


@app.route('/')
def run():
    from core.db import get_db
    get_db()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

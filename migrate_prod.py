from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

# set up connection to your Google Cloud SQL DB instance
# python migrate_prod.py db upgrade; after you've created your migration files
from configuration import system

if system == 'Linux':
    game_db_path = '' # fix prod path and certs
else:
    game_db_path = 'postgres+psycopg2://postgres:password@localhost:5432/darknova' # use local DB

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = game_db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
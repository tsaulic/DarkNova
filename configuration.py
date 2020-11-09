import os

import semver

version = semver.VersionInfo.parse('0.2.4-alpha+build.12')
# game_db_path = 'sqlite:///../game.sqlite'
game_db_path = 'sqlite:///:memory:'
secret_key = os.environ.get("DARKNOVA_SECRET_KEY") or "test"

# game related stuff
sectors_default_amount = 500

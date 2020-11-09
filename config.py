import os
import semver

version = semver.VersionInfo.parse('0.2.2-alpha+build.10')
game_db_path = 'sqlite:///../game.sqlite'
secret_key = os.environ.get("DARKNOVA_SECRET_KEY") or "test"

# game related stuff
sectors_default_amount = 100

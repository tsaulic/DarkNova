import os, semver

version = semver.VersionInfo.parse('0.2.0-alpha+build.7')
game_db_path = 'sqlite:///../game.sqlite'
secret_key = os.environ.get("DARKNOVA_SECRET_KEY") or "test"

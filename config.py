import os, semver

version = semver.VersionInfo.parse('0.1.1-pre.2+build.6')
game_db_path = 'sqlite:///../game.sqlite'
secret_key = os.environ.get("DARKNOVA_SECRET_KEY") or "test"

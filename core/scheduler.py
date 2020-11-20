import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from configuration import update_interval_seconds, turns_limit_amount, turns_tick_amount, factor
from core.models import Player
from core.util import commit_try

scheduler = BackgroundScheduler()


def update():
    players = Player.query.all()
    turns_to_add = round(turns_tick_amount * factor)
    for player in players:
        if player.turns < turns_limit_amount:
            if player.turns >= turns_limit_amount:
                break
            elif player.turns + turns_to_add > turns_limit_amount:
                player.turns = turns_limit_amount
            else:
                player.turns += round(turns_tick_amount * factor)

    commit_try()


def start_scheduler():
    scheduler.add_job(func=update, trigger="interval", seconds=update_interval_seconds)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())

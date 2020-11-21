import time
from datetime import datetime

import schedule

from configuration import turns_limit_amount, turns_tick_amount, factor, scheduler_interval_seconds
from core.models import Player
from core.util import commit_try


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
                if turns_to_add < 1:
                    turns_to_add = 1
                player.turns += turns_to_add

    commit_try()


scheduler = schedule.every(scheduler_interval_seconds).seconds.do(update)


def scheduler_start():
    while True:
        schedule.run_pending()
        time.sleep(1)


def scheduler_get_remaining_time():
    time_of_next_run = schedule.next_run()
    time_now = datetime.now()

    return (time_of_next_run - time_now).seconds

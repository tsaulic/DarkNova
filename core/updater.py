import atexit
import time

from apscheduler.schedulers.background import BackgroundScheduler

from configuration import update_interval_seconds
from core.models import Player


def update():
    print(Player.query.all())


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update, trigger="interval", seconds=update_interval_seconds)
    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())

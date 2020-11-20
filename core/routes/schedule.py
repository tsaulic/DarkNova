from threading import Thread

from flask import Blueprint

from core.scheduler import scheduler_start

bp = Blueprint('schedule', __name__)


@bp.route('/schedule', methods=['GET'])
def logout():
    background_thread = Thread(target=scheduler_start)
    background_thread.start()

    return 'success'

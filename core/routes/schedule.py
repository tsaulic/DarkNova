from flask import Blueprint

from core.scheduler import start_scheduler, scheduler

bp = Blueprint('schedule', __name__)


@bp.route('/schedule', methods=['GET'])
def logout():
    if not scheduler.running: start_scheduler()
    return 'success'

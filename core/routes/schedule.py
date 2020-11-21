from flask import Blueprint

from core.scheduler import scheduler_start_on_bg_thread

bp = Blueprint('schedule', __name__)


@bp.route('/schedule', methods=['GET'])
def logout():
    scheduler_start_on_bg_thread()

    return 'success'

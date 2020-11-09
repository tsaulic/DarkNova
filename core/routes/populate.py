from flask import request, redirect, url_for

from configuration import sectors_default_amount
from core import app, populate_mock_db
from core.render_static import render_error


@app.route('/populate')
def populate():
    sector_value = request.args.get('sectors')

    try:
        sector_value = int(sector_value)
    except ValueError:
        return render_error('Parameter sector must be of type int')
    except TypeError:
        sector_value = sectors_default_amount

    if sector_value is not None:
        populate_mock_db(sector_value)
    else:
        populate_mock_db(sectors_default_amount)

    return redirect(url_for('play'))

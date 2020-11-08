from flask import render_template


def render_error(message):
    return render_template(
        'game.html',
        title='Error',
        content=message
    )

from flask import render_template


def render_error(message):
    return render_template(
        'play.html',
        title='Error',
        content=message
    )

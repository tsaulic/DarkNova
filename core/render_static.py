from flask import render_template


def render_error(message):
    # TODO: add an error.html!!!
    return render_template(
        'play.html',
        title='Error',
        content=message,
        sector=None
    )

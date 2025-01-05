from flask import render_template, session
from app.errors import bp

@bp.route('/quandary')
def quandary():
    error_message = 'Something unexpected occurred.'
    if 'error_message' in session:
        error_message = session.pop('error_message')
    return render_template("errors/quandary.html", error_message=error_message)

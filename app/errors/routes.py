from flask import render_template, session
from app.errors import bp

@bp.route('/quandary')
def quandary():
    error_message = 'Something went wrong, if this continues please contact support.'
    if 'error_message' in session:
        error_message = session.pop('error_message')
    return render_template("errors/quandary.html", error_message=error_message)

@bp.route('/no_permission')
def no_permission():
    error_message = 'You do not have the required permission to view this page.'
    return render_template("errors/quandary.html", error_message=error_message)

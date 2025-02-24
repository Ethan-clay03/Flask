from flask import render_template, session, g, current_app
from app.errors import bp
from app.logger import error_logger

@bp.route('/error')
def error():
    error_message = 'Something went wrong, if this continues please contact support.'
    if g.is_admin: # Only display error if admin is logged in, otherwise throw generic error to user
        error_message = session.get('error_message')
    error_logger.error(f"Error: {error_message} \nAction performed by UserID: {session['_user_id']}")
    return render_template("errors/error.html", error_message=error_message)

@bp.route('/no_permission')
def no_permission():
    error_message = 'You do not have the required permission to view this page.'
    return render_template("errors/error.html", error_message=error_message)

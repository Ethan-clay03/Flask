from flask import render_template, session, g, current_app
from app.errors import bp
from app.logger import error_logger

@bp.route('/error')
def error():
    error_header = session['error_header']
    error_message = session['generic_error_message']
    user_id = 'User Not Logged In'
    if g.is_admin: # Only display error if admin is logged in, otherwise throw generic error to user
        error_message = session.get('error_message')
    if '_user_id' in session:
        user_id =  session['_user_id']
    error_logger.error(f"Error: {error_message} \nAction performed by UserID: {user_id}")
    return render_template("errors/error.html", error_header=error_header, error_message=error_message)

@bp.route('/no_permission')
def no_permission():
    error_header = session['error_header']
    error_message = session['generic_error_message']
    return render_template("errors/error.html", error_header=error_header, error_message=error_message)

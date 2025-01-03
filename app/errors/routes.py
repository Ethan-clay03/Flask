#https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-1-installing-packages
from flask import render_template, session
from app.errors import bp

@bp.route('/quandary')
def quandary():
    error_message = session.pop('error_message')
    return render_template("errors/quandary.html", error_message=error_message)

#https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-1-installing-packages
from flask import Blueprint, render_template, redirect, url_for, request
from app.auth import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from flask_login import login_user

@bp.route('/signup')
def signup():
    return render_template(url_for('profile.signup'))

@bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        return redirect(url_for('profile.signup'))

    new_user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), role_id=2)  # Assuming role_id is required and you have a default value or retrieve it from elsewhere

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('profile.login'))

@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False # If checkbox for user is ticked

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('profile.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))
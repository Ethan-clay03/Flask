#https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-1-installing-packages
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.profile import bp
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from app.logger import app_logger

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

    new_user = User.create_user(username=username, email=email, password=password)

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
    return redirect(url_for('profile.index'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/login')
def login():
    return render_template('profile/login.html')

@login_required
@bp.route('/home')
def index():
    app_logger.error("Logger accessed on profile page")
    if current_user.is_authenticated:
        return render_template('profile/index.html', username=current_user.username)
    
    return redirect(url_for('profile.login'))
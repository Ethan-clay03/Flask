#https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-1-installing-packages
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.profile import bp
from werkzeug.security import check_password_hash
from app.models import User
from app import db
from flask_login import login_user, logout_user, login_required, current_user
from app.logger import auth_logger

@bp.route('/signup')
def signup():
    return render_template('profile/signup.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    form_data = {
        'email': request.form.get('email'),
        'username': request.form.get('username'),
        'password': request.form.get('password')
    }

    user = User.query.filter_by(email=form_data['email']).first()

    if user:
        return redirect(url_for('profile.signup'))

    try:
        if not form_data['username'] or not form_data['email'] or not form_data['password']:
            raise ValueError("Missing required fields: Email, Username, Password")
        new_user = User.create_user(username=form_data['username'], email=form_data['email'], password=form_data['password'])
    except ValueError as e:
        auth_logger.error("Unable to create user, full error was: " + str(e))
        flash('Missing required fields')
        return redirect(url_for('profile.signup'))

    db.session.add(new_user)
    db.session.commit()

    # Log the user in automatically 
    login_user(new_user) 

    return redirect(url_for('profile.index'))

@bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False # Change to boolean value depending if tickbox is selected

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
    if current_user.is_authenticated:
        return render_template('profile/index.html', username=current_user.username)
    
    return redirect(url_for('profile.login'))

@login_required
@bp.route('/manage_bookings')
def manage_bookings():
    if current_user.is_authenticated:
        return render_template('profile/manage_bookings.html', username=current_user.username)
    
    return redirect(url_for('profile.login'))
from flask import render_template, redirect, url_for
from app.profile import bp
from app.models import User 

@bp.route('/')
def index():
    return render_template('profile/index.html')

@bp.route('/login')
def login():
    return 'Login'

@bp.route('/signup')
def signup():
    return render_template('profile/signup.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    if User.search_user_by_email(email):
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth.login'))

@bp.route('/logout')
def logout():
    return 'Logout'
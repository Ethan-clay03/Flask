from flask import render_template, redirect, url_for
from app.profile import bp
from app.models import User 
from flask_login import current_user, login_required

@bp.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        return render_template('profile/index.html', username=current_user.username)
    else:
        return redirect(url_for('profile.login'))

@bp.route('/login')
def login():
    return render_template('profile/login.html')

@bp.route('/signup', methods=['POST'])
def signup_post():
    return 'hit POST'
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    if User.search_user_by_email(email):
        return redirect('signup.html')

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    
    return redirect('profile/login.html')

@bp.route('/signup')
def signup():
    return render_template('profile/signup.html')

@bp.route('/logout')
def logout():
    return 'Logout'

#https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-1-installing-packages
from flask import render_template, redirect, url_for, request, flash, jsonify, session, current_app
from flask_principal import Identity, identity_changed
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.profile import bp
from app.models import User, Bookings, Listings
from app.logger import auth_logger
from app import db, permission_required, user_permission

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    #If a callback URL has been sent in any request add it to the session, once user signed up it will be handled and return
    #the user to the previous page they were browsing (does not currently hold a full page cache)
    if request.args.get('callback'):
        session['callback'] = request.args.get('callback')

    if request.method == 'POST':
        form_data = {
            'email': request.form.get('email'),
            'username': request.form.get('username'),
            'password': request.form.get('password')
        }

        # Validate form data
        error = validate_signup_form(form_data)
        if error:
            flash(error, 'error')
            return redirect(url_for('profile.signup'))

        # Create new user and log in automatically
        try:
            new_user = User.create_user(
                username=form_data['username'],
                email=form_data['email'],
                password=form_data['password']
            )
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            if 'callback' in session.keys():
                callback = session.pop('callback')
                flash("Account successfully created. Please review your booking before continuing", 'success')
                return redirect(callback)
            
            flash('Successfully created your account. You have been logged in automatically', 'success')
            return redirect(url_for('profile.index'))
        except Exception as e:
            auth_logger.error(f"Unable to create user: {e}")
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('profile.signup'))

    return render_template('profile/signup.html')

def validate_signup_form(form_data):
    if not all(form_data.values()):
        return 'Missing required fields: Email, Username, Password'

    if not is_valid_username(form_data['username']):
        return "You are only allowed to use the following special characters in usernames: - _ +"

    if User.search_user_by_email(form_data['email']):
            return'Email address already exists'

    if User.search_user_by_username(form_data['username']):
        return 'Username already exists'
    
    return None

def is_valid_username(username):
    allowed_special_chars = "-_+"
    return all(c.isalnum() or c in allowed_special_chars for c in username)


@bp.route('/login', methods=['POST'])
def login_post():
    username_field = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False # Change to boolean value depending if tickbox is selected

    if '@' in username_field:
        user = User.search_user_by_email(username_field)
    else:
        user = User.search_user_by_username(username_field)

    if not user or not check_password_hash(user.password, password):
        flash('Invalid username/email and or password. Please try again or <a href="' + url_for('profile.password_reset') + '">reset your password here</a>.', 'danger')
        return redirect(url_for('profile.login'))

    login_user(user, remember=remember)

    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

    if 'callback' in session.keys():
        callback = session.pop('callback')
        flash("You have been successfully logged in. Please review your booking before continuing", 'success')
        return redirect(callback)
    
    return redirect(url_for('profile.index'))


@bp.route('/check-username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data.get('username', '').strip()
    if username is None:
        return jsonify({'error': 'Username is required'}), 400
    
    if not is_valid_username(username):
        return jsonify({'error': "Username contains invalid special characters. You may only use: - _ +"}), 400
    #Search to see if username already exists
    user_exist = User.search_user_by_username(username)
    if user_exist is not None:
        return jsonify({'error': 'Username already exists'}), 400

    return jsonify({'available': True, 'success': username + ' is available.'})


@bp.route('/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get('email', '').strip()

    if email is None:
        return jsonify({'error': 'Email is required'}), 400
    
    email_exist = User.search_user_by_email(email)

    if email_exist:
        return jsonify({'error': 'Email already registered'}), 400

    return jsonify({'available': True, 'success': 'Email is available'})


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/login')
def login():
    #If a callback URL has been sent in any request add it to the session, once user logged in it will be handled and return
    #the user to the previous page they were browsing (does not currently hold a full page cache)
    if request.args.get('callback'):
        session['callback'] = request.args.get('callback')
    if current_user.is_authenticated:
        return redirect(url_for('profile.index'))

    return render_template('profile/login.html')


@bp.route('/password-reset')
def password_reset():
    return render_template('profile/password-reset.html')


@bp.route('/password-reset', methods=['POST'])
def check_password_reset_1():
    username = request.form.get('username')
    email = request.form.get('email')
    
    #Search to see if username already exists
    user_exist = User.search_user_by_username(username)
    if user_exist is None:
        return flash('Username does not exist', 'error')
    
    email_exist = User.search_user_by_email(email)
    if email_exist is None:
        return flash('Email does not exist', 'error')

    session['password-reset-email'] = email
    return redirect(url_for('profile.password_reset_2'))


@bp.route('/password-reset/2FA')
def password_reset_2():
    return render_template('profile/password-reset-2.html')


@bp.route('/password-reset/2FA', methods=['POST'])
def check_password_reset_2():
    code =  request.form.get('2fa-code')
    
    #Simulate 2FA code being entered
    if code == '123456' or code == '234567':
        return redirect(url_for('profile.password_reset_3'))
    
    return flash('Invalid 2FA Code', 'error')


@bp.route('/password-reset/reset-password')
@permission_required(user_permission)
def password_reset_3():
    return render_template('profile/password-reset-3.html')


@bp.route('password-reset/from-profile')
@permission_required(user_permission)
def password_reset_from_profile():
    email = current_user.email


@bp.route('/password-reset/reset-password', methods=['POST'])
def password_reset_process():
    email = session.get('password-reset-email')
    
    if email == None:
        email = current_user.email
        
    password1 = request.form.get('password-1')
    password2 = request.form.get('password-2')
    
    #Simulate 2FA code being entered
    if password1 == password2:
        User.change_user_password(email, password1)
        flash('Password was updated successfully', 'success')
        return redirect(url_for('profile.login'))
    flash('Passwords must match', 'error')
    return redirect(url_for('profile.password_reset_3'))

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
        bookings = Bookings.get_user_bookings(current_user.id)
        locations = Listings.get_all_locations(True)
        return render_template('profile/manage_bookings.html', username=current_user.username, bookings=bookings, locations=locations)
    
    flash('You must be logged in to view your current bookings', 'error')
    return redirect(url_for('profile.login'))

@bp.route('/manage_profile', methods=['GET', 'POST'])
def manage_profile():
    user = User.search_user_id(current_user.id)

    if user == None:
        flash('You must be logged in to update your profile','error')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        
        User.update_user_details(user.id, username, email)
        
        flash('Successfully updated profile details', 'success')
        return redirect(url_for('profile.manage_profile'))
    return render_template('profile/manage_profile.html', user=user)


@bp.route('/cancel_booking', methods=['POST'])
@permission_required(user_permission)
def cancel_booking():
    data = request.get_json()
    booking_id = data.get('booking_id')
    if not booking_id:
        return jsonify({'error': 'Missing booking_id'}), 400
    
    success = Bookings.cancel_booking(booking_id)
    if success:
        return jsonify({'message': 'Booking cancelled successfully'}), 200
    else:
        return jsonify({'error': 'Failed to cancel booking'}), 400


@bp.route('/manage_bookings/view/<int:id>')
def manage_profile_view_booking(id):

    return render_template('profile/view_booking.html')

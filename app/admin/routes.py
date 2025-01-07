from flask import render_template, redirect, url_for
from app import admin_permission, permission_required, super_admin_permission
from app.admin import bp


@bp.route('/home')
@permission_required(admin_permission)
def index():
    return render_template('admin/index.html')

@bp.route('/')
@permission_required(admin_permission)
def home():
    return redirect(url_for('admin.home'))

@bp.route('/manage_bookings')
@permission_required(admin_permission)
def manage_bookings():
    return render_template('admin/index.html')

@bp.route('/manage_users')
@permission_required(super_admin_permission)
def manage_users():
    return render_template('admin/index.html')

@bp.route('/manage_user_bookings')
@permission_required(admin_permission)
def manage_user_bookings():
    return render_template('admin/index.html')
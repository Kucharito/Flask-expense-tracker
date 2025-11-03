from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.forms import RegisterForm, LoginForm
from app.models import User
from app.notifications_utils import create_notification

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            create_notification(user.id, 'You have successfully logged in.', 'info')
            return redirect(url_for('index'))

        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print("submitted",form.validate_on_submit())
    print("errors",form.errors)
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = generate_password_hash(form.password.data)
        )

        db.session.add(new_user)
        db.session.commit()
        print(">>> User uložený:", new_user.username)
        create_notification(new_user.id, 'Welcome to the Expense App!', 'info')

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
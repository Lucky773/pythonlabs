from flask import render_template, url_for, flash, redirect
from . import auth_bp
from ..forms import RegistrationForm, LoginForm 
from flask_login import login_user, current_user, logout_user, login_required
from ..models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Обробка реєстрації та створення нового користувача
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', title='Register', form=form)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Обробка логіну користувача
        return redirect(url_for('index'))

    return render_template('login.html', title='Login', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

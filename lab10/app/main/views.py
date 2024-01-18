from flask import render_template, url_for, flash, redirect, abort
from . import main_bp
from flask_login import login_required
from ..models import db, User

@main_bp.route("/")
@login_required
def index():
    # Опис логіки для головної сторінки
    pass

@main_bp.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    # Опис логіки для сторінки профілю користувача
    pass

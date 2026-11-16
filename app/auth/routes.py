from urllib.parse import urlsplit

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from ..extensions import db
from ..models import User
from . import bp
from .forms import LoginForm, RegisterForm


def _is_safe_next(target):
    """Pozwala przekierować tylko na lokalne adresy (ochrona przed open redirect)."""
    if not target:
        return False
    parts = urlsplit(target)
    return not parts.netloc and not parts.scheme and target.startswith("/")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Konto utworzone. Możesz się zalogować.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.email == form.email.data.strip().lower())
        )
        if user is None or not user.check_password(form.password.data):
            flash("Nieprawidłowy e-mail lub hasło.", "danger")
            return render_template("auth/login.html", form=form), 401

        login_user(user, remember=form.remember.data)
        next_page = request.args.get("next")
        if not _is_safe_next(next_page):
            next_page = url_for("main.dashboard")
        return redirect(next_page)

    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("Wylogowano pomyślnie.", "info")
    return redirect(url_for("main.index"))
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from . import db
from .forms import SigninForm, SignupForm
from .models import User

auth = Blueprint("auth", __name__)


def configure(app):
    app.register_blueprint(auth)


@auth.route("/signin", methods=["GET", "POST"])
def signin_page():
    if current_user.is_authenticated:
        return redirect(url_for("views.home_page"))

    form = SigninForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash("You are logged", category="success")
            return redirect(url_for("views.home_page"))
        else:
            flash("Email or password is invalid, please, try again", category="warning")

    if form.errors != {}:
        for errors in form.errors.values():
            for msg in errors:
                flash(msg, category="danger")

    return render_template("auth/signin.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for("views.home_page"))
        
    form = SignupForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data, phone=form.phone.data, gender=form.gender.data)
        db.session.add(new_user)
        db.session.commit()
        flash("You are registred now", category="success")
        return redirect(url_for("auth.signin_page"))

    if form.errors != {}:
        for errors in form.errors.values():
            for msg in errors:
                flash(msg, category="danger")

    return render_template("auth/signup.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out", category="success")
    return redirect(url_for("views.home_page"))
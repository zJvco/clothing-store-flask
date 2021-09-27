from flask import Blueprint, flash, abort
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from sqlalchemy.exc import IntegrityError

from . import db
from .models import User, Product
from .forms import ProfileForm, AddressForm

views = Blueprint("views", __name__)


def configure(app):
    app.register_blueprint(views)


@views.route("/")
def home_page():
    return render_template("index.html")


@views.route("/store")
def store_page():
    products = Product.query.all()
    return render_template("store.html", products=products)


@views.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():
    profile_form = ProfileForm()
    address_form = AddressForm()

    if profile_form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()

        try:
            user.username = profile_form.username.data
            user.phone = profile_form.phone.data
            user.gender = profile_form.gender.data

            if profile_form.current_password.data:
                if user.verify_password(profile_form.current_password.data):
                    if profile_form.password_new.data:
                        print(profile_form.password_new.data)
                        user.password = profile_form.password_new.data
                    else:
                        flash("You need to fill the new password field", category="warning")
                        return redirect(url_for("views.profile_page"))
                else:
                    flash("Wrong password, type you current password", category="warning")
                    return redirect(url_for("views.profile_page"))

            db.session.commit()
        except IntegrityError:
            abort(404)
        else:
            flash("Changes were made sucefully", category="success")

    if address_form.validate_on_submit():
        pass

    if profile_form.errors != {}:
        for errors in profile_form.errors.values():
            for msg in errors:
                flash(msg, category="danger")

    return render_template("profile.html", profile_form=profile_form, address_form=address_form)


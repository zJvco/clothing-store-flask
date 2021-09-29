from flask import Blueprint, flash, abort, request
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import db
from .models import User, Product, Address
from .forms import ProfileForm, AddressForm, EditAddressForm

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

    if profile_form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()

        user.username = profile_form.username.data
        user.phone = profile_form.phone.data
        user.gender = profile_form.gender.data

        if profile_form.current_password.data:
            if user.verify_password(profile_form.current_password.data):
                if profile_form.password_new.data:
                    user.password = profile_form.password_new.data
                else:
                    flash("You need to fill the new password field", category="warning")
                    return redirect(url_for("views.profile_page"))
            else:
                flash("Wrong password, type you current password", category="warning")
                return redirect(url_for("views.profile_page"))

        db.session.commit()
        flash("Changes were made successfully", category="success")
        return redirect(url_for('views.profile_page'))

    if profile_form.errors != {}:
        for errors in profile_form.errors.values():
            for msg in errors:
                flash(msg, category="danger")

    return render_template("profile/profile.html", profile_form=profile_form)


@views.route("/profile/address", methods=["GET", "POST"])
@login_required
def profile_address_page():
    address_form = AddressForm()
    edit_address_form = EditAddressForm()

    if address_form.validate_on_submit():
        new_address = Address(cep=address_form.cep.data, street=address_form.street.data,
                            number=address_form.number.data, city=address_form.city.data,
                            complement=address_form.complement.data, user_id=current_user.id)
        db.session.add(new_address)
        db.session.commit()
        flash("Address were created successfully", category="success")
        return redirect(url_for('views.profile_address_page'))

    if address_form.errors != {}:
        for errors in address_form.errors.values():
            for msg in errors:
                flash(msg, category="danger")

    return render_template("profile/address.html", address_form=address_form, edit_address_form=edit_address_form)


@views.route("/profile/address/edit/<id>", methods=["GET", "POST"])
@login_required
def profile_address_edit_page(id):
    edit_address_form = EditAddressForm()
    address = Address.query.filter_by(id=id).first()

    if edit_address_form.validate_on_submit():
        address.cep = request.form.get("cep")
        address.street = request.form.get("street")
        address.number = request.form.get("number")
        address.city = request.form.get("city")
        address.complement = request.form.get("complement")
        db.session.commit()
        flash("Address changed successfully", category="success")
        return redirect(url_for("views.profile_address_page"))

    if edit_address_form.errors != {}:
        for errors in edit_address_form.errors.values():
            for msg in errors:
                flash(msg, category="danger")

    return redirect(url_for("views.profile_address_page"))

@views.route("/profile/address/remove/<id>")
@login_required
def profile_address_remove_page(id):
    address = Address.query.filter_by(id=id).first()
    db.session.delete(address)
    db.session.commit()

from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import login_required

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


@views.route("/profile")
@login_required
def profile_page():
    profile_form = ProfileForm()
    address_form = AddressForm()
    return render_template("profile.html", profile_form=profile_form)


from flask import Blueprint
from flask import render_template, redirect, url_for

from .models import Product

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
def profile_page():
    return render_template("profile.html")
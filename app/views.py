from flask import Blueprint
from flask import render_template, redirect, url_for

views = Blueprint("views", __name__)


def configure(app):
    app.register_blueprint(views)


@views.route("/")
def home_page():
    return render_template("index.html")


@views.route("/products")
def products_page():
    return render_template("products.html")
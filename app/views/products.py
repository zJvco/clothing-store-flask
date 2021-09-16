from flask import Blueprint
from flask import render_template, redirect, url_for

products = Blueprint("products", __name__, url_prefix="/products")

@products.route("/")
def products_page():
    return render_template("products.html")
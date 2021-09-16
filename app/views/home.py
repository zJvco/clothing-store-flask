from flask import Blueprint
from flask import render_template, redirect, url_for

views = Blueprint("views", __name__)

@views.route("/")
def home_page():
    return render_template("index.html")
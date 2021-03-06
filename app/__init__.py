import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
adm = Admin(name="Clothing Store Administration", template_mode="bootstrap4")
migrate = Migrate(compare_type=True)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_CONNECTION")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FLASK_ADMIN_SWATCH"] = "cosmo"

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.signin_page"

    from .admin import IndexAdmin

    adm.init_app(app, index_view=IndexAdmin())
    migrate.init_app(app, db)

    from . import admin
    from . import auth, views

    views.configure(app)
    auth.configure(app)
    admin.configure()

    from . import cli

    cli.configure(app)

    return app

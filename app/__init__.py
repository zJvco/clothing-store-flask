import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
adm = Admin(name="Clothing Store", template_mode="bootstrap3")
migrate = Migrate(compare_type=True)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_CONNECTION")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FLASK_ADMIN_SWATCH"] = "flatly"

    db.init_app(app)
    login_manager.init_app(app)

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

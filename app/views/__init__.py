from app.views.home import views
from app.views.admin import admin
from app.views.auth import auth
from app.views.restapi import restapi
from app.views.products import products


def init_app(app):
    app.register_blueprint(views)
    app.register_blueprint(products)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(restapi)
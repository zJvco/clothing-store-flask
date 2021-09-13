from flask import Blueprint

bp_home = Blueprint("home", __name__)
bp_auth = Blueprint("auth", __name__)
bp_admin = Blueprint("admin", __name__, url_prefix="/admin")
bp_restapi = Blueprint("restapi", __name__, url_prefix="/api")

def init_app(app):
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_restapi)
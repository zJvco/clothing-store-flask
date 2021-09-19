from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from . import adm, db
from .models import User, Product


def configure():
    adm.add_view(StoreAdmin(User, db.session))
    adm.add_view(StoreAdmin(Product, db.session))


class StoreAdmin(ModelView):
    form_excluded_columns=("created_date", "updated_date")

    def is_accessible(self):
        return current_user.is_authenticated
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from wtforms.fields import FileField
from wtforms.validators import DataRequired

from . import adm, db
from .models import User, Product


def configure():
    adm.add_view(UserAdmin(User, db.session))
    adm.add_view(ProductsAdmin(Product, db.session))


class UserAdmin(ModelView):
    form_excluded_columns = ["created_date", "updated_date", "products", "adresses"]
    column_exclude_list = ["password", "phone", "money"]
    column_searchable_list = ["email"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin


class ProductsAdmin(ModelView):
    form_excluded_columns = ["created_date", "updated_date", "user_products"]
    column_exclude_list = ["image"]

    column_type_formatters = {"image": FileField(label="Image", validators=[DataRequired()])}

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin
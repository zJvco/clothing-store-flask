from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_wtf.file import FileField, FileRequired, FileAllowed

from . import adm, db
from .models import User, Product


def configure():
    adm.index_view = IndexAdmin()

    adm.add_view(UserAdmin(User, db.session))
    adm.add_view(ProductsAdmin(Product, db.session))


class IndexAdmin(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("views.home_page"))


class UserAdmin(ModelView):
    form_excluded_columns = ["created_date", "updated_date", "products", "adresses"]
    column_exclude_list = ["password", "phone", "money"]
    column_searchable_list = ["email"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.index"))


class ProductsAdmin(ModelView):
    form_excluded_columns = ["created_date", "updated_date", "owner_users"]
    column_exclude_list = ["image", "description"]

    def on_model_change(self, form, model, is_created):
        model.image = form.image.data.filename

    def scaffold_form(self):
        form = super().scaffold_form()
        form.image = FileField(label="Image", validators=[FileRequired(), FileAllowed(["jpg", "png"], "You can upload only images")])
        return form

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.index"))
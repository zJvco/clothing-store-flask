from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import RadioField, PasswordField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed

from . import adm, db
from .models import User, Product


def configure():
    adm.add_view(UserAdmin(User, db.session))
    adm.add_view(ProductsAdmin(Product, db.session))


class IndexAdmin(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("views.home_page"))


class UserAdmin(ModelView):
    form_excluded_columns = ["created_date", "updated_date", "products", "adresses"]
    column_exclude_list = ["password_hash", "phone", "money", "image"]
    column_searchable_list = ["email"]

    form_widget_args = {
        "gender": {
            "style": "display: flex; list-style-type: none;",
        }
    }

    def on_model_change(self, form, model, is_created):
        if type(form.image.data) is str or form.image.data is None:
            return

        model.image = form.image.data.filename

    def scaffold_form(self):
        form = super().scaffold_form()
        form.password_hash = PasswordField(label="Password", validators=[Length(min=6, max=128), DataRequired()])
        form.gender = RadioField(label="Gender", validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female'), ('undefined', 'Undefined')])
        form.image = FileField(label="Image", validators=[FileAllowed(["jpg", "png"], "You can upload only images")])
        return form

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.index"))


class ProductsAdmin(ModelView):
    form_excluded_columns = ["created_date", "updated_date", "owner_users"]
    column_exclude_list = ["image", "description"]

    def on_model_change(self, form, model, is_created):
        path = "/img"
        model.image = f"{path}/{form.image.data.filename}"

    def scaffold_form(self):
        form = super().scaffold_form()
        form.image = FileField(label="Image", validators=[FileRequired(), FileAllowed(["jpg", "png"], "You can upload only images")])
        return form

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.index"))
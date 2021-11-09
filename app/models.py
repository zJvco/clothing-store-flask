from flask_login import UserMixin
from sqlalchemy.sql import func

from .utils import random_choice_image
from . import db, bcrypt, login_manager

# orders_details = db.Table("orders_details",
#     db.Column("order_id", db.Integer, db.ForeignKey("orders.id")),
#     db.Column("product_id", db.Integer, db.ForeignKey("products.id")),
#     db.Column("quantity", db.Integer, nullable=False),
#     db.Column("unit_price", db.Integer, nullable=False)
# )

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(50), nullable=False)
    email = db.Column("email", db.String(50), nullable=False, unique=True)
    password_hash = db.Column("password", db.String(128), nullable=False)
    phone = db.Column("phone", db.Integer, unique=True)
    money = db.Column("money", db.Float, nullable=False, default=0)
    admin = db.Column("admin", db.Boolean, default=False)
    image = db.Column("image", db.String(240), default=random_choice_image("./app/static/img/profile/default"))
    gender = db.Column("gender", db.String(20), default="undefined".title(), nullable=False)
    created_date = db.Column("created_date", db.DateTime(timezone=True), default=func.now())
    updated_date = db.Column("updated_date", db.DateTime(timezone=True), onupdate=func.now())

    adresses = db.relationship("Address", backref=db.backref("owner_user"))
    orders = db.relationship("Order", backref=db.backref("owner_user"))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, pwd):
        self.password_hash = bcrypt.generate_password_hash(pwd).decode("utf-8")

    def verify_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)

    def __repr__(self):
        return "<User %r>" % self.id


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column("id", db.Integer, primary_key=True)
    category_id = db.Column("category_id", db.Integer, db.ForeignKey("categories.id"), nullable=False)
    name = db.Column("name", db.String(45), unique=True, nullable=False)
    price = db.Column("price", db.Float, nullable=False)
    description = db.Column("description", db.Text(1000))
    image = db.Column("image", db.String(240))
    quantity = db.Column("quantity", db.Integer)
    created_date = db.Column("created_date", db.DateTime(timezone=True), default=func.now())
    updated_date = db.Column("updated_date", db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Product %r>" % self.id


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(50), nullable=False)

    products = db.relationship("Product", backref=db.backref("category"))

    def __repr__(self):
        return "<Category %r>" % self.name


class Address(db.Model):
    __tablename__ = "adresses"

    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
    cep = db.Column("cep", db.Integer, nullable=False)
    street = db.Column("street", db.String(200), nullable=False)
    number = db.Column("number", db.Integer, nullable=False)
    city = db.Column("city", db.String(100), nullable=False)
    complement = db.Column("complement", db.String(140))

    def __repr__(self):
        return "<Address %r>" % self.id


class OrderDetail(db.Model):
    __tablename__ = "orders_details"

    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    order_id = db.Column("order_id", db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column("product_id", db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column("quantity", db.Integer, nullable=False)
    unit_price = db.Column("unit_price", db.Float, nullable=False)

    def __repr__(self):
        return "<OrderDetail %r>" % self.id


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column("id", db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
    order_date = db.Column("order_date", db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return "<Order %r>" % self.id

from random import choice
from os import listdir
from os.path import isfile, join
from flask_login import UserMixin
from sqlalchemy.sql import func

from . import db, bcrypt, login_manager

users_has_products = db.Table("users_has_products",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"))
)


def random_choice_image(path):
    file_list = []
    pi = path.find("static")

    for file in listdir(path):
        if isfile(join(path, file)):
            file_list.append(file)
    return f"{path[pi:]}/{choice(file_list)}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(50), nullable=False)
    email = db.Column("email", db.String(50), nullable=False, unique=True)
    __password = db.Column("password", db.String(128), nullable=False)
    phone = db.Column("phone", db.Integer, unique=True)
    __money = db.Column("money", db.Float, nullable=False, default=0)
    admin = db.Column("admin", db.Boolean, default=False)
    image = db.Column("image", db.String(240), default=random_choice_image("./app/static/img/profile/default"))
    gender = db.Column("gender", db.String(20), default="undefined".title(), nullable=False)
    created_date = db.Column("created_date", db.DateTime(timezone=True), default=func.now())
    updated_date = db.Column("updated_date", db.DateTime(timezone=True), onupdate=func.now())

    products = db.relationship("Product", secondary=users_has_products, backref=db.backref("owner_users", lazy="dynamic"))
    adresses = db.relationship("Address", backref=db.backref("owner_user"))

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, pwd):
        self.__password = bcrypt.generate_password_hash(pwd).decode("utf-8")

    @property
    def money(self):
        return self.__money

    @money.setter
    def money(self, value):
        self.__money = value

    def verify_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)

    def __repr__(self):
        return "<User %r>" % self.id


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(45), unique=True, nullable=False)
    price = db.Column("price", db.Float, nullable=False)
    description = db.Column("description", db.Text(1000))
    image = db.Column("image", db.String(240))
    created_date = db.Column("created_date", db.DateTime(timezone=True), default=func.now())
    updated_date = db.Column("updated_date", db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return "<Product %r>" % self.id


class Address(db.Model):
    __tablename__ = "adresses"

    id = db.Column("id", db.Integer, primary_key=True)
    cep = db.Column("cep", db.Integer, nullable=False)
    street = db.Column("street", db.String(200), nullable=False)
    number = db.Column("number", db.Integer, nullable=False)
    city = db.Column("city", db.String(100), nullable=False)
    complement = db.Column("complement", db.Text(500))

    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return "<Address %r>" % self.id

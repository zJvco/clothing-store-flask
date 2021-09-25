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
    for file in listdir(path):
        if isfile(join(path, file)):
            file_list.append(file)
    return f"{path}/{choice(file_list)}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.Integer, unique=True)
    money = db.Column(db.Float, nullable=False, default=0)
    admin = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(240), default=random_choice_image("./app/static/img/profile/default"))
    gender = db.Column(db.String(20), default="undefined".title(), nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    products = db.relationship("Product", secondary=users_has_products, backref=db.backref("owner_users", lazy="dynamic"))
    adresses = db.relationship("Address", backref=db.backref("owner_user"))

    def __init__(self, username, email, password, phone=None, gender="undefined"):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.phone = phone
        self.gender = gender

    def verify_password(self, pwd):
        return bcrypt.check_password_hash(self.password, pwd)

    def __repr__(self):
        return "<User %r>" % self.id


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text(1000))
    image = db.Column(db.String(240))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, name, price, description, image):
        self.name = name
        self.price = price
        self.description = description
        self.image = image

    def __repr__(self):
        return "<Product %r>" % self.id


class Address(db.Model):
    __tablename__ = "adresses"

    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String(200), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    complement = db.Column(db.Text(500))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, cep, street, number, city, complement, user_id):
        self.cep = cep
        self.street = street
        self.number = number
        self.city = city
        self.complement = complement
        self.user_id = user_id

    def __repr__(self):
        return "<Address %r>" % self.id

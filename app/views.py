from flask import Blueprint, flash, abort, request, json
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import db
from .models import User, Product, Address, Order, OrderDetail, Category
from .forms import ProfileForm, AddressForm, EditAddressForm, DepositForm

views = Blueprint("views", __name__)


def configure(app):
    app.register_blueprint(views)


@views.route("/")
def home_page():
    return render_template("index.html")


@views.route("/store/")
def store_page():
    products = Product.query.filter(Product.quantity > 0).all()
    categories = Category.query.all()
    return render_template("store.html", products=products, categories=categories)


@views.route("/store/<category>/")
def store_category_page(category):
    products = db.session.query(Product).join(Category).filter(Category.name == category.lower(), Product.quantity > 0).all()
    categories = Category.query.all()
    return render_template("store.html", products=products, categories=categories)


@views.route("/store/<category>/<product_name>/")
def store_product_page(category, product_name):
    product = db.session.query(Product).join(Category).filter(Category.name == category.lower(), Product.name == product_name.lower(), Product.quantity > 0).first()
    if not product:
        flash("Product not found", "warning")
        return redirect(url_for("views.store_page"))

    products_by_category = db.session.query(Product).join(Category).filter(Category.name == category.lower()).limit(20).all()
    other_category_products = db.session.query(Product).join(Category).filter(Category.name != category.lower()).limit(20).all()
    return render_template("product.html", product=product,
                                           products_by_category=products_by_category,
                                           other_category_products=other_category_products)


@views.route("/cart/")
@login_required
def cart_page():
    return render_template("cart.html")


@views.route("/buy/", methods=["POST"])
@login_required
def buy_page():
    params = json.loads(request.get_data())
    user = User.query.filter_by(id=current_user.id).first()
    order = Order(user_id=current_user.id)
    db.session.add(order)

    for param in params:
        product_id = param["id"]
        quantity = int(param["quantity"])
        product = Product.query.filter_by(id=product_id).first()

        if not product:
            flash("Product not found", category="warning")
            return abort(400)
        elif user.money < product.price:
            flash("You don't have money to buy this product", category="danger")
            return abort(400)
        elif product.quantity < quantity:
            flash("We no longer have this product in stock", category="warning")
            return abort(400)

        user.money -= product.price
        product.quantity -= quantity
        order_details = OrderDetail(order_id=order.id, product_id=product.id, quantity=quantity, unit_price=product.price)
        db.session.add(order_details)

    db.session.commit()
    flash("Successful purchase", category="success")
    return "success", 201


@views.route("/profile/", methods=["GET", "POST"])
@login_required
def profile_page():
    profile_form = ProfileForm()

    if profile_form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()

        user.username = profile_form.username.data
        user.phone = profile_form.phone.data
        user.gender = profile_form.gender.data

        if profile_form.current_password.data:
            if user.verify_password(profile_form.current_password.data):
                if profile_form.password_new.data:
                    user.password = profile_form.password_new.data
                else:
                    flash("You need to fill the new password field", category="warning")
                    return redirect(url_for("views.profile_page"))
            else:
                flash("Wrong password, type you current password", category="warning")
                return redirect(url_for("views.profile_page"))

        db.session.commit()
        flash("Changes were made successfully", category="success")
        return redirect(url_for('views.profile_page'))

    if profile_form.errors != {}:
        for errors in profile_form.errors.values():
            for msg in errors:
                flash(msg, category="danger")

    return render_template("profile/profile.html", profile_form=profile_form)


@views.route("/profile/address/", methods=["GET", "POST"])
@login_required
def profile_address_page():
    address_form = AddressForm()
    edit_address_form = EditAddressForm()

    if address_form.validate_on_submit():
        new_address = Address(cep=address_form.cep.data, street=address_form.street.data,
                            number=address_form.number.data, city=address_form.city.data,
                            complement=address_form.complement.data, user_id=current_user.id)
        db.session.add(new_address)
        db.session.commit()
        flash("Address were created successfully", category="success")
        return redirect(url_for('views.profile_address_page'))

    if address_form.errors != {}:
        for errors in address_form.errors.values():
            for msg in errors:
                flash(msg, category="danger")

    return render_template("profile/address.html", address_form=address_form, edit_address_form=edit_address_form)


@views.route("/profile/address/edit/<id>/", methods=["GET", "POST"])
@login_required
def profile_address_edit_page(id):
    edit_address_form = EditAddressForm()
    address = Address.query.filter_by(id=id).first()

    if edit_address_form.validate_on_submit():
        address.cep = edit_address_form.cep.data
        address.street = edit_address_form.street.data
        address.number = edit_address_form.number.data
        address.city = edit_address_form.city.data
        address.complement = edit_address_form.complement.data
        db.session.commit()
        flash("Address changed successfully", category="success")
        return redirect(url_for("views.profile_address_page"))

    if edit_address_form.errors != {}:
        for errors in edit_address_form.errors.values():
            for msg in errors:
                flash(msg, category="danger")

    return redirect(url_for("views.profile_address_page"))


@views.route("/profile/address/remove/<id>/")
@login_required
def profile_address_remove_page(id):
    address = Address.query.filter_by(id=id).first()
    db.session.delete(address)
    db.session.commit()


@views.route("/profile/deposit/", methods=["GET", "POST"])
@login_required
def profile_deposit_page():
    deposit_form = DepositForm()

    if request.method == "POST":
        user = User.query.filter_by(id=current_user.id).first()
        if deposit_form.validate_on_submit():
            user.money += deposit_form.value.data
            db.session.commit()
            flash("Amount successfully deposited", category="success")

        if deposit_form.errors != {}:
            for errors in deposit_form.errors.values():
                for msg in errors:
                    flash(msg, category="danger")
                    
        return redirect(request.url)
    else:
        return render_template("profile/deposit.html", deposit_form=deposit_form)


@views.route("/purchases/")
@login_required
def purchases_page():
    purchases = db.session.query(OrderDetail, Product, Order.order_date).join(Order).join(Product).filter(Order.user_id == current_user.id, OrderDetail.order_id == Order.id, OrderDetail.product_id == Product.id).all()
    return render_template("purchases.html", purchases=purchases)
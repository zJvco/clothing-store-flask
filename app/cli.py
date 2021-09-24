import click, sys
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .models import User


@click.command("create_db")
@with_appcontext
def create_db():
    db.create_all()


@click.command("drop_db")
def drop_db():
    db.drop_all()


@click.command("create_user")
@click.option("--username", "-u")
@click.option("--email", "-e")
@click.option("--password", "-p")
@click.option("--phone", "-t", type=int)
@with_appcontext
def create_user(username, email, password, phone):
    try:
        user = User(username, email, password, phone)
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError:
        raise "An error was found, please, try again"
    else:
        print(f"User {username} created successfully!")


@click.command("delete_user")
@click.option("-id", type=int)
@with_appcontext
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
    except SQLAlchemyError:
        raise "An error was found, please, try again"
    else:
        print(f"User {user.username} deleted successfully!")


def configure(app):
    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(create_user)
    app.cli.add_command(delete_user)

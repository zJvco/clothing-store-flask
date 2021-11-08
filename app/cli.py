import click
from time import sleep
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .models import User


@click.command("create_db")
@with_appcontext
def create_db():
    db.create_all()


@click.command("drop_db")
@with_appcontext
def drop_db():
    db.drop_all()


@click.command("create_user")
@click.option("--username", "-u")
@click.option("--email", "-e")
@click.option("--password", "-p")
@with_appcontext
def create_user(username, email, password):
    if not username or not email or not password:
        print("Usage: -u [username] -e [email] -p [password]")
        return

    try:
        user = User(username=username, email=email, password=password)
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
    if not id:
        print("Usage: -id [user id]")
        return

    user = User.query.filter_by(id=id).first()
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            raise "An error was found, please, try again"
        else:
            print(f"User {user.username} deleted successfully!")
    else:
        print("User not found, please, check the id again")


@click.command("make_admin")
@click.option("--email", "-e")
@with_appcontext
def make_admin(email):
    if not email:
        print("Usage: --email / -e [user email]")
        return

    user = User.query.filter_by(email=email).first()
    if user:
        if user.admin:
            print(f"User {user.username} is already admin")
            return
            
        answer = str(input(f"You have sure to give admin to {user.username}? [Y / N]: "))
        if answer.upper() == "Y" or answer.upper() == "YES":
            try:
                user.admin = True
                db.session.commit()
            except SQLAlchemyError:
                raise "An error was found, please, try again"
            else:
                print(f"User {user.username} has admin now")
        elif answer.upper() == "N" or answer.upper() == "NO":
            print("Leaving...")
            sleep(2)
        else:
            print("The options not correspond, try again")
    else:
        print("User not found, please, check the email again")


def configure(app):
    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(create_user)
    app.cli.add_command(delete_user)
    app.cli.add_command(make_admin)

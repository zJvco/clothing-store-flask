import click, sys
from flask.cli import with_appcontext
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .models import User


@click.command("create_db")
@with_appcontext
def create_db():
    db.create_all()


@click.command("create_user")
@click.option("-u")
@click.option("-e")
@click.option("-p")
@click.option("-t", type=int)
@with_appcontext
def create_user(username, email, password, phone):
    try:
        user = User(username, email, password, phone)
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError:
        sys.exit("An error was found, please, try again")
    else:
        print(f"Usuário {username} criado com sucesso!")


def configure(app):
    app.cli.add_command(create_db)
    app.cli.add_command(create_user)

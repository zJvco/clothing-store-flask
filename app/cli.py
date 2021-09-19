import click
from flask.cli import with_appcontext

from . import db


@click.command("create_db")
@with_appcontext
def create_db():
    db.create_all()


def configure(app):
    app.cli.add_command(create_db)

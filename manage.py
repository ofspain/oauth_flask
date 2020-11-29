import os

from flask.cli import FlaskGroup

from flaskapp.app.app import create_app
from flaskapp.app.app.extensions import db
from flaskapp.app.app.main import app
from flaskapp.app.app.modules.users.models import User

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(last="FEMIFEYISHARA", email="michael@mherman.org"))
    db.session.commit()


if __name__ == "__main__":
    cli()

# encoding: utf-8
# pylint: disable=invalid-name,wrong-import-position,wrong-import-order
"""
Extensions setup
================

Extensions provide access to common resources of the application.

Please, put new extension instantiations and initializations here.
"""

from flask_moment import Moment

from .logging import Logging

logging = Logging(None)

from flask_cors import CORS

cross_origin_resource_sharing = CORS()

from .flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from sqlalchemy_utils import force_auto_coercion, force_instant_defaults

force_auto_coercion()
force_instant_defaults()

from flask_login import LoginManager

login_manager = LoginManager()

from flask_marshmallow import Marshmallow

marshmallow = Marshmallow()

from .auth import OAuth2Provider

oauth2 = OAuth2Provider()

from flaskapp.app.app.extensions import api
from .swagger import init_app as init_swagger
from flask_bootstrap import Bootstrap


def init_app(app):
    """
    Application extensions initialization.
    """
    bootstrap = Bootstrap()


    moment = Moment()
    for extension in (
            logging,
            cross_origin_resource_sharing,
            db,
            login_manager,
            marshmallow,
            oauth2,
            api,
            bootstrap,
            moment

    ):
        extension.init_app(app)
    init_swagger(app)


def insertRole():
    pass




def setup_db(app):

    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables():
        from ..modules.permissions.dao import RoleDao
        db.create_all()

        list_roles = RoleDao.startup_insertion()
        print(list_roles)
        with db.session.begin():
            for role in list_roles:
                db.session.add(role)

        print(RoleDao.find_by_name('User'))

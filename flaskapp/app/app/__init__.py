# encoding: utf-8
"""
Example RESTful API Server.
"""

from .config import config
from flask import Flask

# from .extensions import register_api

# import models here explicitly to force their mapped tables to be created if need be


def create_app(flask_config_name=None):
    """
    Entry point to the Flask RESTful Server application.
    """
    flask_config_name = flask_config_name or 'default'
    app = Flask(__name__)

    app.config.from_object(config[flask_config_name])

    from . import extensions
    extensions.init_app(app)
    from . import modules
    modules.init_app(app)

    extensions.setup_db(app)
    return app



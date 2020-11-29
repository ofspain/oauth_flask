import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

from flaskapp.app.app.extensions import logging
from .http_exceptions import abort
from flask_restplus._http import HTTPStatus

from flaskapp.app.app.modules.users.resources import ns
from flaskapp.app.app.modules.oauth.resources import api as oat

#log = logging.Logging

# api_blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api()

api.add_namespace(ns)
api.add_namespace(oat)

# Note Error handler can also be registered with namespace where it
# will override that registered with namespace


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    #log.exception(message)

    abort(HTTPStatus.INTERNAL_SERVER_ERROR, message)


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    #log.warning(traceback.format_exc())

    abort(HTTPStatus.NOT_FOUND, 'A database result was required but none was found.')


def init_app(app):
    api.init_app(app)
    # app.register_blueprint(api_blueprint)

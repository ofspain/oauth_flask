# encoding: utf-8
"""
Extended Api Namespace implementation with an application-specific helpers
--------------------------------------------------------------------------
"""
from contextlib import contextmanager
from functools import wraps
import logging

import sqlalchemy

from flask_restplus import Namespace as BaseNamespace
from flask_restplus._http import HTTPStatus

from . import http_exceptions
from flask import jsonify
from flask_login import current_user

#from ... import Role
from ...modules.permissions.dao import RoleDao

log = logging.getLogger(__name__)


class Namespace(BaseNamespace):
    """
    Having app-specific handlers here.
    """

    def permissions_required(self, allowable_permissions):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not (current_user and current_user.role_id):
                    resp = jsonify({{"message": "You are not authorized to view resource"}})
                    code = HTTPStatus.FORBIDDEN
                    return resp, code
                role_id = current_user.role_id
                role = RoleDao.load_entity_by_id(Role, role_id)
                if (role.permission & allowable_permissions) != allowable_permissions:
                    resp = jsonify({{"message": "You are not authorized to view resource"}})
                    code = HTTPStatus.FORBIDDEN
                    return resp, code
                return f(*args, **kwargs)

            return decorated_function

        return decorator

    @contextmanager
    def commit_or_abort(self, session, default_error_message="The operation failed to complete"):
        """
        Context manager to simplify a workflow in resources

        Args:
            session: db.session instance
            default_error_message: Custom error message

        Exampple:
        >>> with api.commit_or_abort(db.session):
        ...     team = Team(**args)
        ...     db.session.add(team)
        ...     return team
        """
        try:
            with session.begin():
                yield
        except ValueError as exception:
            log.info("Database transaction was rolled back due to: %r", exception)
            http_exceptions.abort(code=HTTPStatus.CONFLICT, message=str(exception))
        except sqlalchemy.exc.IntegrityError as exception:
            log.info("Database transaction was rolled back due to: %r", exception)
            http_exceptions.abort(
                code=HTTPStatus.CONFLICT,
                message=default_error_message
            )

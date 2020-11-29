# encoding: utf-8
# pylint: disable=too-few-public-methods,invalid-name,bad-continuation
"""
RESTful API Auth resources
--------------------------
"""

import logging

from flask_restplus import Resource
from flask_restplus._http import HTTPStatus
from werkzeug import security

from . import schemas
from .dao import ClientDao
from .schemas import DetailedOAuth2ClientSchema
from ...extensions.api import abort
from ...extensions.api.namespace import Namespace
from ...extensions.api.query_params import pagination_param, PaginationHelper
from flask import request

from .models import db, OAuth2Client

log = logging.getLogger(__name__)
api = Namespace('clients', description="Authentication")


@api.route('/')
class Oauth2Clients(Resource):
    """
    Manipulations with OAuth2 clients.
    """

    #    @api.permission_required(permissions.AdminRolePermission())
    #    @api.response(schemas.DetailedOAuth2ClientSchema(many=True))
    @api.expect(pagination_param)
    # @api.response(HTTPStatus.FORBIDDEN, 'No authority to visit this resource')
    def get(self, args):
        """
        List of OAuth2 Clients.

        Returns a list of OAuth2 Clients starting from ``offset`` limited by
        ``limit`` parameter.
        tags:
          - oauths
        """
        clients_query = ClientDao.load_all_client_query()
        args = pagination_param.parse_args(request)
        offset = args.get('offset', 1)
        limit = args.get('limit', 10)

        paginator = PaginationHelper(clients_query, "clients", schemas.DetailedOAuth2ClientSchema, limit, offset)

        return paginator.paginate_query()

    def post(self):
        with api.commit_or_abort(
                db.session,
                default_error_message="Failed to create a new OAuth2 client."
        ):
            data = api.payload
            oauth_schema = DetailedOAuth2ClientSchema()
            errors = oauth_schema.validate(data)
            if errors:
                return errors, HTTPStatus.BAD_REQUEST.value

            user_id = data.get('user_id')
            name = data.get('name')
            _redirect_uris = data.get('redirect_uris')
            _default_scope = data.get('default_scopes')

            # TODO: reconsider using gen_salt
            new_oauth2_client = OAuth2Client(
                user_id=user_id,
                name=name,
                client_id=security.gen_salt(40),
                client_secret=security.gen_salt(50),
                _redirect_uris=_redirect_uris,
                _default_scopes=_default_scope
            )
            ClientDao.add(new_oauth2_client, db.session)
            return oauth_schema.dump(new_oauth2_client), HTTPStatus.CREATED.value


@api.route('/<client_id>')
class ClientUnit(Resource):
    """
    Manipulations with a specific user.
    """

    def abort_if_client_not_found(self, clt_id):
        clt = ClientDao.load_entity_by_id(clt_id)
        if not clt:
            abort(HTTPStatus.NOT_FOUND.value, message="USER {0} doesn't exist".format(clt_id))

    def get(self, entity_id):

        self.abort_if_client_not_found(entity_id)

        return ClientDao.load_entity_by_id(entity_id)

    def put(self, entity_id):

        self.abort_if_client_not_found(entity_id)
        data = api.payload
        clt = ClientDao.load_entity_by_id(entity_id)

        pass

    def delete(self, clt_id):

        self.abort_if_client_not_found(clt_id)
        user = ClientDao.load_entity_by_id(clt_id)
        ClientDao.delete(user)

        return None, 204

# encoding: utf-8
# pylint: disable=too-few-public-methods
"""
RESTful ns User resources
--------------------------
"""

import logging

from flask_restplus import Resource
from flask_restplus._http import HTTPStatus

from .dao import UserDao
from .models import db, User
from .parameters import user_add
from .schema import UserSchema
from ..permissions.dao import RoleDao
from ...extensions.api import abort
from ...extensions.api.namespace import Namespace
from ...extensions.api.query_params import pagination_param, PaginationHelper
from flask import request

# from flask_restplus import Namespace

log = logging.getLogger(__name__)
ns = Namespace('users', description='Operations related to users')
ns.model("user_add", user_add)


@ns.route("/")
class UserList(Resource):
    """
    Manipulations with users.
    """

    #    @ns.permission_required(permissions.AdminRolePermission())
    @ns.expect(pagination_param, validate=True)
    def get(self):

        users = UserDao.load_all_users_query()
        args = pagination_param.parse_args(request)
        offset = args.get('offset', 0)
        limit = args.get('limit', 2)
        schema = UserSchema()

        paginator = PaginationHelper(UserDao.load_all_users_query(), users,
                                     "UserList.get", schema, limit, offset)

        return paginator.paginate_query()

    @ns.expect(user_add, validate=True)
    def post(self):

        with ns.commit_or_abort(
                db.session,
                default_error_message="Failed to create a new user."
        ):
            data = ns.payload
            user_schema = UserSchema()
            errors = user_schema.validate(data)
            if errors:
                return errors, HTTPStatus.BAD_REQUEST.value

            first = data.get('first')
            last = data.get('last')
            email = data.get('email')
            role = data.get('role')
            Role = RoleDao.find_by_name(role)
            print(Role)
            user = User(last=last, email=email)
            user.role_id = Role.id
            if first:
                user.first = first
            message, result = user.check_password_strength_and_hash_if_ok(data.get('password'))
            if not result:
                return {"error": message},

            UserDao.add(user, db.session)
            # db.session.add(new_user)
        return user_schema.dump(user), HTTPStatus.CREATED.value


@ns.route('/<int:user_id>')
class UserUnit(Resource):
    """
    Manipulations with a specific user.
    """

    def abort_if_user_not_found(self, user_id):
        user = UserDao.load_entity_by_id(User, user_id)
        if not user:
            abort(HTTPStatus.NOT_FOUND.value, message="USER {0} doesn't exist".format(user_id))

    @ns.marshal_with(UserSchema)
    def get(self, entity_id):

        self.abort_if_user_not_found(entity_id)

        return UserDao.load_entity_by_id(entity_id)

    # @ns.response(HTTPStatus.OK, 'User successfully updated.')
    @ns.expect(UserSchema)
    @ns.marshal_with(UserSchema)
    def put(self, entity_id):

        self.abort_if_user_not_found(entity_id)
        data = ns.payload
        user = UserDao.load_entity_by_id(entity_id)

        first = data.get('first')
        last = data.get('last')
        email = data.get('email')
        creation_date = data.get('date')
        active = data.get('active')

        if first:
            user.first = first
        if last:
            user.last = last
        if email:
            user.email = email
        if creation_date:
            user.creation_date = creation_date
        if active:
            user.active = active

        return UserDao.update(user)

    # @ns.response(204, 'Category successfully deleted.')
    def delete(self, user_id):

        self.abort_if_user_not_found(user_id)
        user = UserDao.load_entity_by_id(user_id)
        UserDao.delete(user)

        return None, 204

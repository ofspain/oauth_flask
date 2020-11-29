
from flask_restplus import fields, Model

user_add = Model('Add User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog post'),
    'email': fields.String(required=True, description='Users Email'),
    'last': fields.String(required=True, description='User last name'),
    'first': fields.String(description='User first name'),
    'password': fields.String(required=True, description='User password'),
    'role': fields.String(required=True, description="User's permission within the system",
                          enum=("User", "Moderator", "Administrator"))
})

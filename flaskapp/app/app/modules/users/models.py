from flaskapp.app.app.extensions import db, login_manager
from passlib.apps import custom_app_context as password_context
import re
from flask_login import UserMixin, AnonymousUserMixin


# on diff between server_default and default is that during creation of a new column e.g during migration
# server_default will add the default value to existing column. This is handy for NOT NULL new column
# default do not do this and will not work in this respect


class User(db.Model, UserMixin):
    __tablename__ = 'USERS'
    id = db.Column('ID', db.Integer, primary_key=True)
    first = db.Column('NAME', db.String(50))
    password_hash = db.Column('PASSWORD', db.String(256), nullable=False)
    email = db.Column('EMAIL', db.String(64), unique=True, index=True)
    creation_date = db.Column('CREATED', db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    active = db.Column('ACTIVE', db.Boolean, default=False)
    last = db.Column("LASTNAME", db.String(50), nullable=False)
    role_id = db.Column('ROLE_ID', db.Integer, db.ForeignKey('ROLES.ID'))

    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)

    def check_password_strength_and_hash_if_ok(self, password):
        if len(password) < 8:
            return 'The password is too short. Please, specify a password with at least 8 characters.', False
        if len(password) > 32:
            return 'The password is too long. Please, specify a password with no more than 32 characters.', False
        if re.search(r'[A-Z]', password) is None:
            return 'The password must include at least one uppercase letter.', False
        if re.search(r'[a-z]', password) is None:
            return 'The password must include at least one lowercase letter. ', False
        if re.search(r'\d', password) is None:
            return 'The password must include at least one number.', False
        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None:
            return 'The password must include at least one symbol. ', False
        self.password_hash = password_context.hash(password)
        return '', True

    def has_a_permission(self, permission):
        role = self.role
        return role.permission == permission

    def __init__(self, last="", email=""):
        self.last = last
        self.email = email

    @property
    def is_active(self):
        return self.active


class AnonymousUser(AnonymousUserMixin):
    """Representing an unauthenticated user in the system

        Encapsulates a dummy user who is never entitled to more
        than an ordinary role on our system
    """


login_manager.anonymous_user = AnonymousUser

import time

from sqlalchemy_utils import ScalarListType

from flaskapp.app.app.extensions import db
"""
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
"""


class OAuth2Client(db.Model):
    __tablename__ = 'oauth2_client'

    # public or confidential
    is_confidential = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('USERS.ID', ondelete='CASCADE'))

    # The first argument to db.relationship() indicates whatmodel is on the other side
    # of the relationship. This model can be provided as a string if the class is not yet defined.
    # The backref argument to db.relationship() defines the reverse direction of the relationship
    # by adding a role attribute to the User model. This attribute can be used
    # instead of role_id to access the Role model as an object instead of as a foreign key.

    user = db.relationship('User', backref='client')


    name = db.Column(db.String(40))
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)
    _redirect_uris = db.Column(ScalarListType(separator=' '), nullable=False)
    _default_scopes = db.Column(ScalarListType(separator=' '), nullable=False)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'

        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris  # .split()

        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes  # .split()

        return []


class OAuth2Grant(db.Model):
    """
    Intermediate temporary helper for OAuth2 Grants.
    """

    __tablename__ = 'oauth2_grant'

    id = db.Column(db.Integer, primary_key=True)  # pylint: disable=invalid-name

    user_id = db.Column(db.ForeignKey('USERS.ID', ondelete='CASCADE'), index=True, nullable=False)
    user = db.relationship('User')

    client_id = db.Column(
        db.String(length=40),
        db.ForeignKey('oauth2_client.client_id'),
        index=True,
        nullable=False,
    )
    client = db.relationship('OAuth2Client')

    code = db.Column(db.String(length=255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(length=255), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    scopes = db.Column(ScalarListType(separator=' '), nullable=False)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self.scopes   #.split()
        return []


class OAuth2Token(db.Model):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('USERS.ID', ondelete='CASCADE'))
    user = db.relationship('User')

    client_id = db.Column(
        db.String(128), db.ForeignKey('oauth2_client.client_id'),
        nullable=False,
    )
    client = db.relationship('OAuth2Client')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    scopes = db.Column(ScalarListType(separator=' '), nullable=False)

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()

    def delete(self):
        db.session.delete(self)

        db.session.commit()
        return self


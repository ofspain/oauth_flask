# encoding: utf-8
# pylint: disable=no-self-use
"""
OAuth2 provider setup.

It is based on the code from the example:
https://github.com/lepture/example-oauth2-server

More details are available here:
* http://flask-oauthlib.readthedocs.org/en/latest/oauth2.html
* http://lepture.com/en/2013/create-oauth-server
"""

from datetime import datetime, timedelta
import logging

from flask_login import current_user
from flask_oauthlib import provider
from flask_restplus._http import HTTPStatus
import sqlalchemy

from flaskapp.app.app.extensions import db

log = logging.getLogger(__name__)


class OAuth2RequestValidator(provider.OAuth2RequestValidator):
    # pylint: disable=abstract-method
    """
    A project-specific implementation of OAuth2RequestValidator, which connects
    our User and OAuth2* implementations together.
    """

    def __init__(self, app):
        from flaskapp.app.app.modules.oauth.models import OAuth2Client, OAuth2Grant, OAuth2Token
        self._client_class = OAuth2Client
        self._grant_class = OAuth2Grant
        self._token_class = OAuth2Token
        self.app = app
        from flaskapp.app.app.modules.oauth.dao import ClientDao, GrantDao, TokenDao
        super(OAuth2RequestValidator, self).__init__(
            usergetter=self._usergetter,
            clientgetter=ClientDao.load_client_by_id,
            tokengetter=TokenDao.load_token,
            grantgetter=GrantDao.load_grant_by_client_and_code,
            tokensetter=self._tokensetter,
            grantsetter=self._grantsetter,
        )

    def _usergetter(self, username, password, client, request):
        # pylint: disable=method-hidden,unused-argument
        # Avoid circular dependencies
        # for password credential authorization
        from flaskapp.app.app.modules.users.dao import UserDao
        return UserDao.authenticate_user(username, password)

    def _tokensetter(self, token, request, *args, **kwargs):
        # pylint: disable=method-hidden,unused-argument
        # TODO: review expiration time
        from flaskapp.app.app.modules.oauth.dao import TokenDao
        expires_in = token['expires_in']
        expires = datetime.utcnow() + timedelta(seconds=expires_in)

        try:
            with db.session.begin():
                token_instance = self._token_class(
                    access_token=token['access_token'],
                    refresh_token=token.get('refresh_token'),
                    token_type=token['token_type'],
                    scopes=[scope for scope in token['scope'].split(' ') if scope],
                    expires=expires,
                    client_id=request.client.client_id,
                    user_id=request.user.id,
                )
                TokenDao.add(token_instance, db.session)
                # db.session.add(token_instance)
        except sqlalchemy.exc.IntegrityError:
            log.exception("Token-setter has failed.")
            return None
        return token_instance

    def _grantsetter(self, client_id, code, request, *args, **kwargs):
        # pylint: disable=method-hidden,unused-argument
        # TODO: review expiration time
        from flaskapp.app.app.modules.oauth.dao import GrantDao
        # decide the expires time yourself consider retrieving from app config
        app_expire_grant = int(self.app.config.get('OAUTH2_PROVIDER_TOKEN_EXPIRES_IN') / 10)
        expires = datetime.utcnow() + timedelta(seconds=app_expire_grant)
        try:
            with db.session.begin():

                grant_instance = self._grant_class(
                    client_id=client_id,
                    code=code['code'],
                    redirect_uri=request.redirect_uri,
                    #scopes=request.scopes,
                    user_id=current_user.id,
                    expires=expires
                )
                # db.session.add(grant_instance)
                GrantDao.add(grant_instance, db.session)
        except sqlalchemy.exc.IntegrityError:
            log.exception("Grant-setter has failed.")
            return None
        return grant_instance


def api_invalid_response(req):
    """
    This is a default handler for OAuth2Provider, which raises abort exception
    with error message in JSON format.
    """
    # pylint: disable=unused-argument
    from flaskapp.app.app.extensions import api
    api.abort(code=HTTPStatus.UNAUTHORIZED.value)


class OAuth2Provider(provider.OAuth2Provider):
    """
    A helper class which connects OAuth2RequestValidator with OAuth2Provider.
    All auth decorator will be implemented on this object too
    """

    def __init__(self, *args, **kwargs):
        super(OAuth2Provider, self).__init__(*args, **kwargs)
        self.invalid_response(api_invalid_response)

    def init_app(self, app):
        from flaskapp.app.app.modules.oauth.views import auth_blueprint
        assert app.config['SECRET_KEY'], "SECRET_KEY must be configured!"
        super(OAuth2Provider, self).init_app(app)
        self._validator = OAuth2RequestValidator(app)
        app.register_blueprint(auth_blueprint)

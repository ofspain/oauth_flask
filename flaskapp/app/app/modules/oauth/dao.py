from flaskapp.app.app.extensions.flask_sqlalchemy.db import SuperDao
from .models import OAuth2Client, OAuth2Grant, OAuth2Token


class ClientDao(SuperDao):

    @staticmethod
    def load_client_by_id(client_id):
        return OAuth2Client.query.filter_by(client_id=client_id).first()

    @staticmethod
    def load_all_client_query():
        return OAuth2Client.query

    @staticmethod
    def load_client_from_user(user):
        return OAuth2Client.query.filter_by(user_id=user.id).first()


class GrantDao(SuperDao):

    @staticmethod
    def load_grant_by_client_and_code(client_id, code):
        return OAuth2Grant.query.filter_by(client_id=client_id, code=code).first()


class TokenDao(SuperDao):

    @staticmethod
    def load_token(access_token=None, refresh_token=None):
        if access_token:
            return OAuth2Token.query.filter_by(access_token=access_token).first()
        if refresh_token:
            return OAuth2Token.query.filter_by(refresh_token=refresh_token).first()
        return None

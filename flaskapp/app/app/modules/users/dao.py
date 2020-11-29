from flaskapp.app.app.extensions.flask_sqlalchemy.db import SuperDao
from .models import User


class UserDao(SuperDao):

    @staticmethod
    def load_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def load_all_users_query():
        return User.query

    @staticmethod
    def load_user_by_username(username):
        return User.query.filter_by(email=username).first()

    @staticmethod
    def authenticate_user(email, plain_password_entered):
        """This afford us to affirm both incorrect IDs(username/email)
            and password independently
        """
        user_to_auth = UserDao.load_user_by_username(email)
        if user_to_auth is not None:
            is_auth = user_to_auth.verify_password(plain_password_entered)
            if is_auth:
                return user_to_auth
            else:
                return None

        return user_to_auth



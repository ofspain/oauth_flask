# encoding: utf-8
"""
Auth module
===========
"""
# from flaskapp.app.app.extensions.api import api
from flask import session

from flaskapp.app.app.extensions import login_manager, oauth2
from flaskapp.app.app.modules.users.dao import UserDao
from flaskapp.app.app.modules.users.models import User


def load_user_from_request(request):
    print('LOADER FROM REQUEST CALLED')
    """
    Load user from OAuth2 Authentication header.
    """
    user = None
    if hasattr(request, 'oauth'):
        user = request.oauth.user
    else:
        for k, v in request.args.items():
            print(k, v)
        is_valid, oauth = oauth2.verify_request(scopes=[])
        if '_user_id' in session.keys():
            user = UserDao.load_entity_by_id(User, session['_user_id'])
    return user


def init_app(app, **kwargs):
    # pylint: disable=unused-argument
    """
    Init auth module.
    """
    # Bind Flask-Login for current_user
    login_manager.request_loader(load_user_from_request)

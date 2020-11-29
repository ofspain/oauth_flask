# coding: utf-8
"""
OAuth2 provider setup.

It is based on the code from the example:
https://github.com/lepture/example-oauth2-server

More details are available here:
* http://flask-oauthlib.readthedocs.org/en/latest/oauth2.html
* http://lepture.com/en/2013/create-oauth-server
"""

from flask import Blueprint, request, render_template, url_for, flash, session
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect

from flaskapp.app.app.extensions import oauth2
from .dao import ClientDao

from .models import OAuth2Client
from ..users.dao import UserDao

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')  # pylint: disable=invalid-name


@auth_blueprint.route('/oauth2/token', methods=['GET', 'POST'])
@oauth2.token_handler
def access_token(*args, **kwargs):
    # pylint: disable=unused-argument
    """
    This endpoint is for exchanging/refreshing an access token.

    Returns:
        response (dict): a dictionary or None as the extra credentials for
        creating the token response.
    """
    return None


@auth_blueprint.route('/oauth2/revoke', methods=['POST'])
@oauth2.revoke_handler
def revoke_token():
    """
    This endpoint allows a user to revoke their access token.
    """
    pass


@auth_blueprint.route('/oauth2/authorize', methods=['GET', 'POST'])
@oauth2.authorize_handler
def authorize(*args, **kwargs):

    # pylint: disable=unused-argument
    """
    This endpoint asks user if he grants access to his data to the requesting
    application.
    """
    # TODO: improve implementation. This implementation is broken because we
    # don't use cookies, so there is no session which client could carry on.
    # OAuth2 server should probably be deployed on a separate domain, so we
    # can implement a login page and store cookies with a session id.
    # ALTERNATIVELY, authorize page can be implemented as SPA (single page
    # application)
    if not (current_user and current_user.is_authenticated):
        print('<><><><> ADDING FROM OAUTH')
        session['FROM_OAUTH'] = True
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        oauth2_client = OAuth2Client.query.get_or_404(client_id)
        kwargs['client'] = oauth2_client
        kwargs['user'] = current_user
        # scoped = kwargs["scopes"].split(' ')
        return render_template('authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, DataRequired


class LoginForm(Form):
    identity = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        passord_entered = form.password.data
        identity_entered = form.identity.data
        attempting_user = UserDao.authenticate_user(identity_entered, passord_entered)
        if attempting_user is None:
            flash('Invalid password or email.')
            return render_template('login.html', form=form)
        else:
            login_user(attempting_user, form.remember_me.data, force=True)

            if 'FROM_OAUTH' in session and session['FROM_OAUTH']:
                clt_id = ClientDao.load_client_from_user(current_user).client_id
                return redirect(url_for('auth.authorize', client_id=clt_id,
                                        scope='write:user', response_type='code'))
            return redirect(url_for('auth.logout'))

    return render_template('login.html', form=form)


#ns = Namespace()
#@ns.permissions_required(Permission.DEFAULT)

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('auth.login'))

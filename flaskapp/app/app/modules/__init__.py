# encoding: utf-8
"""
Modules
=======

Modules enable logical resource separation.

You may control enabled modules by modifying ``ENABLED_MODULES`` config
variable.
"""

from flaskapp.app.app.modules.users import init_app as user_init
from flaskapp.app.app.modules.oauth import init_app as oauth_init
from flaskapp.app.app.modules.permissions import init_app as role_init


def init_app(app, **kwargs):
    """
        Application extensions initialization.
        """
    for mod in (
            role_init,
            user_init,
            oauth_init,
    ):
        mod(app)

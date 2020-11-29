from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from flaskapp.app.app.modules.users.schema import UserSchema

spec = APISpec(
    title="My App",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("Users", schema=UserSchema)

# add swagger tags that are used for endpoint annotation
"""
tags = [
    {'name': 'users',
     'description': 'For users'
     },
    {'name': 'oauths',
     'description': 'For authentication/authorization'
     },
]

for tag in tags:
    print("Adding tag: {}".format(tag['name']))
    spec.tag(tag)

"""

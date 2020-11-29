from flaskapp.app.app.extensions import marshmallow as ma
from marshmallow import fields as flds

from .models import OAuth2Client
from ..users.schema import UserSchema


class BaseOAuth2ClientSchema(ma.Schema):
    """
    Base OAuth2 client schema exposes only the most general fields.
    """
    default_scopes = flds.List(flds.String, required=True)
    redirect_uris = flds.List(flds.String, required=True)
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("clients_client_unit", values=dict(client_id="<client_id>")),
            "collection": ma.URLFor("clients_oauth2_clients"),
            "backlink": ma.URLFor("users_user_unit", values=dict(user_id="<user_id>"))
        }
    )
    user_id = flds.Integer(description="Unique ID of user")
    client_id = flds.String(description="Unique ID of client", dump_only=True)
    client_type = flds.String(description="Client type")
    name = flds.String(description="Name")

    class Meta:
        """
            By this, this schema inherited all properties of the type declared as model
            to inherit all its method however, we will proceed thus

            class Meta:
               model = OAuth2Client
        """
        model = OAuth2Client
        fields = ("user_id", "client_id", "name", "client_type", "default_scopes", "redirect_uris", "_links")


class DetailedOAuth2ClientSchema(BaseOAuth2ClientSchema):
    """
        Detailed OAuth2 client schema exposes all useful fields.
        """
    user = flds.Nested(UserSchema, only=('id', 'email', 'first', 'last', 'url'))
    client_secret = flds.String(description="Client Secret")

    class Meta(BaseOAuth2ClientSchema.Meta):

        fields = BaseOAuth2ClientSchema.Meta.fields + (
            "client_secret", "user"
        )
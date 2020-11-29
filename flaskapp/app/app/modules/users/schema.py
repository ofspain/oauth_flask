from flaskapp.app.app.extensions import marshmallow as ma
from marshmallow import fields as flds, validates as val, ValidationError


# validation occurs only when we try to convert input e.g form data to model in our program
# THus it occurs when we load()[deserialized/download] and not when we dump()


def validate_first(first_value):
    if first_value and len(first_value) not in range(8, 32):
        raise ValidationError("First name must be between 8 and 32")



class UserSchema(ma.Schema):
    name = flds.Method('format_name')
    id = flds.Integer(description="Unique ID of user", dump_only=True)
    email = flds.Email(description="User's unique email", required=True)
    last = flds.String(description="User's last name")
    first = flds.String(description="User's first name", validate=validate_first)
    creation_date = flds.DateTime(description="Sign up date, defaults to today")
    active = flds.Boolean(description="Active or not")
    password = flds.String(description="dummy password")
    url = ma.URLFor("users_user_unit", user_id='<id>', _external=True)
    role = flds.String(description="User Role", required=True)


    @val("last")
    def validate_last(self, value):
        if not value or len(value) not in range(8, 32):
            raise ValidationError("Last name must be between 8 and 32")

    def format_name(self, user):
        return "{}, {}".format(user.last, user.first)

    class Meta:
        fields = ("id", "first", "last", "creation_date", "url",
                  "email", "active", "name", "password", "role"
                  )

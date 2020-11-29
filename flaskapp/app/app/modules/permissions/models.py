from flaskapp.app.app.extensions import db


class Role(db.Model):
    __tablename__ = 'ROLES'

    id = db.Column("ID", db.Integer, primary_key=True)
    name = db.Column("NAME", db.String(64), unique=True)
    permission = db.Column("PERMISSION", db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')


class Permission:
    DEFAULT = 0x00
    PUBLIC_ACTIVITIES = 0x02
    INTERNAL_ACTIVITIES = 0x04
    ADMINISTER = 0x80


ROLES = {
    'User': Permission.DEFAULT | Permission.PUBLIC_ACTIVITIES,
    'Moderator': Permission.DEFAULT | Permission.PUBLIC_ACTIVITIES | Permission.INTERNAL_ACTIVITIES,
    'Administrator': (0xff, False)
}

from flaskapp.app.app.extensions.flask_sqlalchemy.db import SuperDao
from .models import Role, ROLES


class RoleDao(SuperDao):

    @staticmethod
    def startup_insertion():
        to_insert_role = list()
        for r in ROLES:
            role = RoleDao.find_by_name(r)
            if role is None:
                role = Role(name=r)
                role.permissions = ROLES[r]
                to_insert_role.append(role)

        return to_insert_role

    @staticmethod
    def find_by_name(name):
        return Role.query.filter_by(name=name).first()

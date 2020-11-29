from flaskapp.app.app.extensions import db


class SuperDao(object):
    """To implement all crud operation generic to all models"""

    @classmethod
    def add(cls, model, ssn):
        ssn.add(model)
        return model

    @classmethod
    def update(cls, model):
        db.session.commit()
        return model

    @classmethod
    def delete(cls, model):
        db.delete(model)
        return db.session.commit()

    @staticmethod
    def load_entity_by_id(cls, entity_id):
        return cls.query.get(entity_id)

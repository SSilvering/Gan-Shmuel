from sqlalchemy import inspect
from app.server.db.models import *
from sqlalchemy.exc import IntegrityError


class DbHelper:
    """
    This is an helper class for interacting with the SQL database.
    It helps the code be more DRY.
    """

    def __init__(self, db):
        self.db = db

    @staticmethod
    def get_all(model):
        return model.query.all()

    @staticmethod
    def get_all_with_filter(model, **kwargs):
        return model.query.filter_by(**kwargs).all()

    @staticmethod
    def get_one(model, **kwargs):
        return model.query.filter_by(**kwargs).first()

    def add_instance(self, model, **kwargs):
        try:
            instance = model(**kwargs)
            self.db.session.add(instance)
            self.commit_changes()
            return instance

        except IntegrityError:
            """IntegrityError will raise when trying to add an 
            item with a unique constrain that already exists."""
            return False

    def commit_changes(self):
        self.db.session.commit()

    def health_check(self, model, **kwargs):
        instance = model(**kwargs)
        inspection = inspect(instance)

        if not inspection.pending:
            self.db.session.add(instance)

        if inspection.pending:
            self.db.session.commit()

        if not inspection.pending:
            self.db.session.delete(instance)
            return True

        return False

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.base.domain.unit_of_work import UnitOfWork
from app.config import settings

DB_URL = str(settings.DATABASE_URL)
assert DB_URL is not None, "DB_URL environment variable needed."


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self):
        self.session_maker = sessionmaker(bind=create_engine(DB_URL))

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, _exc_val, _traceback):
        if exc_type is not None:
            self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

import contextlib
from typing import Annotated, Any, Iterator

from fastapi import Depends
from sqlalchemy import (
    JSON,
    Connection,
    MetaData,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import settings
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = str(settings.DATABASE_URL)

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


class Base(DeclarativeBase):
    metadata = metadata
    type_annotation_map = {dict[str, Any]: JSON}


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_engine(
            DATABASE_URL,
            pool_size=settings.DATABASE_POOL_SIZE,
            pool_recycle=settings.DATABASE_POOL_TTL,
            pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
        )
        self._sessionmaker = sessionmaker(autocommit=False, bind=self._engine)

    def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.contextmanager
    def connect(self) -> Iterator[Connection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                connection.rollback()
                raise

    @contextlib.contextmanager
    def session(self) -> Iterator[Session]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            # rollback session and raise again for fastapi handler
            session.rollback()
            raise
        else:
            # commit only if no exception occurred
            # TODO: write tests to check for execption leaking when commiting
            session.commit()
        finally:
            session.close()


DB_URL = str(settings.DATABASE_URL)
assert DB_URL is not None, "DB_URL environment variable needed."

sessionmanager = DatabaseSessionManager(DB_URL, {"echo": True})  # make configurable


def get_db_session():
    with sessionmanager.session() as session:
        yield session


DBSessionDep = Annotated[Session, Depends(get_db_session)]

from contextlib import ExitStack
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db_session
from src.main import app
from tests.integration.user.fixtures import *
from tests.integration.schedule.fixtures import *

# create objects in memory for fast tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
        # commit for the values to persist in same default scope = 'function'
        db.commit()
    finally:
        db.close()


app.dependency_overrides[get_db_session] = override_get_db


@pytest.fixture(autouse=True)
def actual_app():
    with ExitStack():
        yield app


# recreate tables after each test runs
# this is little slow; but ensures data isn't persisted across tests
@pytest.fixture
def client(actual_app):
    with TestClient(app) as c:
        Base.metadata.create_all(bind=engine)
        yield c
    Base.metadata.drop_all(bind=engine)

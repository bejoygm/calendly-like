from contextlib import ExitStack
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db_session
from src.user.data.models.user import User
from src.main import app

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
    finally:
        print("here")
        db.commit()
        db.close()


app.dependency_overrides[get_db_session] = override_get_db


@pytest.fixture(autouse=True)
def actual_app():
    with ExitStack():
        yield app


# recreate tables after each test runs
# this is a little; but ensures data isn't persisted across tests
# A better way should exist
@pytest.fixture
def client(actual_app):
    with TestClient(app) as c:
        Base.metadata.create_all(bind=engine)
        yield c
    Base.metadata.drop_all(bind=engine)

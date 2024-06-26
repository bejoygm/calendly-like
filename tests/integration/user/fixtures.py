from collections import namedtuple
import pytest


User = namedtuple("User", ["id", "name", "email"])


@pytest.fixture
def user(client) -> User:
    email = "abc@example.com"
    response = client.post(
        "/users/",
        json={"email": email, "name": "abc"},
    )
    return User(**response.json())


@pytest.fixture
def booking_user(client) -> User:
    email = "booking_user@example.com"
    response = client.post(
        "/users/",
        json={"email": email, "name": "booking_user"},
    )
    return User(**response.json())

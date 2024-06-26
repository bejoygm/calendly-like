from collections import namedtuple
import pytest


User = namedtuple("User", ["id", "name", "email"])


@pytest.fixture
def user(client) -> User:
    email = "bejoygm@gmail.com"
    response = client.post(
        "/users/",
        json={"email": email, "name": "Event creator"},
    )
    return User(**response.json())


@pytest.fixture
def booking_user(client) -> User:
    email = "bejoyrock@gmail.com"
    response = client.post(
        "/users/",
        json={"email": email, "name": "Booking user"},
    )
    return User(**response.json())

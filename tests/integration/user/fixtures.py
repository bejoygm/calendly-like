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

import pytest
from pydantic import ValidationError

from app.user.domain.models.user import User


def test_user_create():
    name = "test"
    email = "abc@example.com"
    user = User(
        name=name,
        email=email,
    )

    assert user
    assert user.name == name
    assert user.email == email


def test_customer_create_throws_invalid_email_exception():

    with pytest.raises(ValidationError) as exc:
        User(
            name="test",
            email="abc@exampl",
        )
    assert exc.value.errors()[0]["loc"][0] == "email"
    assert exc.value.errors()[0]["msg"].startswith("value is not a valid email address")

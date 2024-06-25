from collections import namedtuple
import pytest

from tests.integration.user.fixtures import User


Availability = namedtuple(
    "Availability", ["id", "name", "user_id", "rules", "timezone"]
)


@pytest.fixture
def availability(client, user: User) -> Availability:
    name = "custom"
    payload = {
        "name": name,
        "rules": [
            {
                "day": "sun",
                "intervals": [{"from": "12:00", "to": "17:00"}],
            },
        ],
        "timezone": "Antarctica/Palmer",
        "email": user.email,
    }

    response = client.post(
        "/availability/",
        json=payload,
    )
    return Availability(**response.json())


Event = namedtuple(
    "Event", ["id", "name", "starts_from", "ends_at", "duration", "availability_id"]
)
EventCalendar = namedtuple("EventCalendar", ["timezone", "days"])


@pytest.fixture
def event(client, availability: Availability) -> Event:
    payload = {
        "name": "Catchup over coffee ☕",
        "starts_from": "2024-06-15",
        "ends_at": "2024-06-21",
        "duration": 30,
        "availability_id": availability.id,
    }

    response = client.post(
        "/events/",
        json=payload,
    )
    return Event(**response.json())

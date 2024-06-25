from datetime import datetime
import uuid
from tests.integration.schedule.fixtures import Availability, Event
from fastapi import status


def _payload(availability_id):
    return {
        "name": "Catchup over coffee ☕",
        "starts_from": "2024-06-24",
        "ends_at": "2024-06-24",
        "duration": 30,
        "availability_id": availability_id,
    }


def test_create_event(client, availability: Availability):
    payload = _payload(availability.id)

    response = client.post(
        "/events/",
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]


def test_invalid_duration(client, availability: Availability):
    payload = _payload(availability)

    # minimum event duration must be 15
    payload["duration"] = 14

    response = client.post(
        "/events/",
        json=payload,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_invalid_start_time(client, availability: Availability):
    payload = _payload(availability)

    # starts_from should be less than ends_at
    payload["starts_from"] = "2024-06-25"
    payload["ends_at"] = "2024-06-24"

    response = client.post(
        "/events/",
        json=payload,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_invalid_availablility(client):
    payload = _payload(str(uuid.uuid4()))

    response = client.post(
        "/events/",
        json=payload,
    )
    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == "Availability not found"


def test_event_calendar(client, event: Event):
    response = client.get(
        f"/events/{event.id}/calendar",
        params={
            "start_date": event.starts_from,
            "end_date": event.ends_at,
            "timezone": "Antarctica/Palmer",
        },
    )

    data = response.json()

    days = [day for day in data["days"] if len(day["spots"]) > 0]

    # days with spot available should be 1
    assert len(days) == 1

    # no. of spots available should be 10
    # because duration is 30 mins and availability 12-5
    assert len(days[0]["spots"]) == 10


def test_event_calendar_for_different_timezones(client, user):
    availability_payload = {
        "name": "custom",
        "rules": [
            {
                "day": "sat",
                "intervals": [{"from": "14:30", "to": "17:00"}],
            },
        ],
        "timezone": "Asia/Kolkata",
        "email": user.email,
    }

    availability = client.post(
        "/availability/",
        json=availability_payload,
    ).json()

    event_payload = {
        "name": "Catchup over coffee ☕",
        "starts_from": "2024-06-24",
        "ends_at": "2024-06-30",
        "duration": 30,
        "availability_id": availability["id"],
    }

    event = client.post(
        "/events/",
        json=event_payload,
    ).json()
    
    calendar = client.get(
        f"/events/{event["id"]}/calendar",
        params={
            "start_date": "2024-06-23",
            "end_date": "2024-06-30",
            "timezone": "America/New_York",
        },
    ).json()
    
    days_without_spots = [d for d in calendar["days"] if len(d['spots']) == 0]
    assert days_without_spots

    # the result should have 10 spots for 29th (monday)
    spots = [d for d in calendar["days"] if d["date"] == "2024-06-29"][0]["spots"]
    
    assert len(spots) == 5
    
    # and it should start at from 5:00
    start_time = datetime.strptime(spots[0]["start_time"], '%Y-%m-%dT%H:%M:%S%z')
    assert (start_time.hour, start_time.minute) == (5, 0)
    
def test_event_calendar_when_there_is_no_overlap(client, event: Event):
    calendar = client.get(
        f"/events/{event.id}/calendar",
        params={
            "start_date": "2100-06-23",
            "end_date": "2100-06-30",
            "timezone": "America/New_York",
        },
    ).json()
    
    assert len(calendar["days"]) == 0

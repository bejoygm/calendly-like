from tests.integration.user.fixtures import User
from uuid import uuid4
from fastapi import status


def test_create_availability(client, user: User):
    name = "custom"
    payload = {
        "name": name,
        "rules": [
            {
                "day": "sun",
                "intervals": [{"from": "15:00", "to": "15:30"}],
            },
        ],
        "timezone": "America/Nome",
        "email": user.email,
    }

    response = client.post(
        "/availability/",
        json=payload,
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert "id" in data

    get_response = client.get(
        f"/availability/{data["id"]}",
    )

    assert get_response.status_code == status.HTTP_200_OK
    get_data = get_response.json()

    assert get_data["name"] == name

def test_get_non_existent_availability(client):
    uuid = uuid4()
    response = client.get(
        f"/availability/{uuid}",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    
    assert data['detail'] == 'Availability not found'


def test_invalid_interval_availability(client, user: User):
    # create an invalid interval where start time is greater than end time
    payload = {
        "name": 'custom',
        "rules": [
            {
                "day": "sun",
                "intervals": [{"from": "16:00", "to": "15:30"}],
            },
        ],
        "timezone": "America/Nome",
        "email": user.email,
    }
    
    response = client.post(
        "/availability/",
        json=payload,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    

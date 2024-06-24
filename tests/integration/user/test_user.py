def test_create_user(client):
    email = "abc@example.com"
    response = client.post(
        "/users/",
        json={"email": email, "name": "abc"},
    )
    assert response.status_code == 201
    data = response.json()

    user_id = data["id"]
    get_response = client.get(
        f"/users/{user_id}",
    )

    assert get_response.status_code == 200
    get_data = get_response.json()

    assert get_data["email"] == email

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_items_empty_then_create(client):
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)

    response = client.post("/items", params={"name": "test-item"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test-item"
    assert "id" in data


def test_events_create_and_list(client):
    response = client.post("/events", params={"message": "hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "hello"
    assert "id" in data

    response = client.get("/events")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)

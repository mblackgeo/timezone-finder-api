def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert "healthy" in response.text


def test_tz_at(client):
    response = client.post("/tz-at", json={"lat": 51.5, "lng": -0.11})
    assert response.status_code == 200
    assert response.json() == {"timezone_id": "Europe/London"}


def test_tz(client):
    response = client.post("/tz-at", json={"lat": 51.5, "lng": -0.11})
    assert response.status_code == 200
    assert response.json() == {"timezone_id": "Europe/London"}

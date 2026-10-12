from app import models
from tests.conftest import TestingSessionLocal

def test_get_classes(client):
    response = client.get("/classes/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_existing_class(client):
    db = TestingSessionLocal()
    try:
        new_class = models.Class(
            name = "No-Gi Intermediate",
            instructor = "Charles Oliveira",
            start_time="2026-10-12T18:00:00",
            end_time="2026-10-12T19:30:00",
            capacity=20 # remove capacity later
        )
        db.add(new_class)
        db.commit()
        db.refresh(new_class)

        response = client.get(f"/classes/{new_class.id}")
        assert response.status_code == 200
        assert response.json()["name"] == "No-Gi Intermediate"
        assert response.json()["instructor"] == "Charles Oliveira"
    finally:
        db.close()
def test_get_nonexistent_class(client):
    response = client.get("/classes/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Class not found"}



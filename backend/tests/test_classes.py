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
def test_create_class_admin(client):
    db = TestingSessionLocal()
    admin = models.User(
        name="John Doe",
        email="johndoeadmin@gmail.com",
        password_hash="hash",
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    class_data = {
        "name": "No-Gi Kids",
        "instructor": "John Doe",
        "start_time": "2026-10-12T18:00:00",
        "end_time": "2026-10-12T19:30:00",
    }
    response = client.post(f"/classes/?user_id={admin.id}", json=class_data)
    assert response.status_code == 200
    assert response.json()["name"] == "No-Gi Kids"
    assert response.json()["instructor"] == "John Doe"
    db.close()
def test_create_class_no_permission(client):
    db = TestingSessionLocal()
    member = models.User(
        name="Jane Doe",
        email="janedoeadmin@gmail.com",
        password_hash="hash",
        role="member"
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    class_data = {
        "name": "No-Gi Kids",
        "instructor": "John Doe",
        "start_time": "2026-10-12T18:00:00",
        "end_time": "2026-10-12T19:30:00",
    }
    response = client.post(f"/classes/?user_id={member.id}", json=class_data)
    assert response.status_code == 403
    assert response.json() == {"detail" : "Admin access required"}
    db.close()
def test_update_class(client):
    db = TestingSessionLocal()
    admin = models.User(
        name="John Doe",
        email="johndoeadmin@gmail.com",
        password_hash="hash",
        role="admin"
    )
    class_ = models.Class(
        name="Gi Fundamentals",
        instructor="John Doe",
        start_time="2026-10-12T18:00:00",
        end_time="2026-10-12T19:30:00",
    )
    db.add(admin)
    db.add(class_)
    db.commit()
    db.refresh(admin)
    db.refresh(class_)
    response = client.patch(f"/classes/{class_.id}?user_id={admin.id}", json={"name": "Gi Intermediate"})
    assert response.status_code == 200
    assert response.json()["name"] == "Gi Intermediate"
    assert response.json()["instructor"] == "John Doe"
    db.close()
def test_put_class(client):
    db = TestingSessionLocal()
    admin = models.User(
        name="John Doe",
        email="johndoeadmin@gmail.com",
        password_hash="hash",
        role="admin"
    )
    class_ = models.Class(
        name="Gi Fundamentals",
        instructor="John Doe",
        start_time="2026-10-12T18:00:00",
        end_time="2026-10-12T19:30:00",
    )
    db.add(admin)
    db.add(class_)
    db.commit()
    db.refresh(admin)
    db.refresh(class_)
    new_class = {
        "name": "Gi Intermediate",
        "instructor": "John Danaher",
        "start_time": "2026-10-14T18:00:00",
        "end_time": "2026-10-14T19:30:00",
    }
    response = client.put(f"/classes/{class_.id}?user_id={admin.id}", json=new_class)
    assert response.status_code == 200
    assert response.json()["name"] == "Gi Intermediate"
    assert response.json()["instructor"] == "John Danaher"
    db.close()
def test_delete_class(client):
    db = TestingSessionLocal()
    admin = models.User(
        name="John Doe",
        email="johndoeadmin@gmail.com",
        password_hash="hash",
        role="admin"
    )
    class_ = models.Class(
        name="Gi Fundamentals",
        instructor="John Doe",
        start_time="2026-10-12T18:00:00",
        end_time="2026-10-12T19:30:00",
    )
    db.add(admin)
    db.add(class_)
    db.commit()
    db.refresh(admin)
    db.refresh(class_)
    response = client.delete(f"/classes/{class_.id}?user_id={admin.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "class deleted"
    response = client.get(f"/classes/{class_.id}")
    assert response.status_code == 404
    db.close()








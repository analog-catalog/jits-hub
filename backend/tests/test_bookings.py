from app import models
import pytest
from tests.conftest import TestingSessionLocal
from app.auth import hash_password

def test_create_booking(client):
    db = TestingSessionLocal()
    user = models.User(
        name="John Doe",
        email="jdoe@gmail.com",
        password_hash="password",
        role="member"
    )
    class_ = models.Class(
        name="No-Gi Fundamentals",
        instructor="Marcelo Garcia",
        start_time="2026-10-15T18:00:00",
        end_time="2026-10-15T19:30:00"
    )
    db.add(user)
    db.add(class_)
    db.commit()
    db.refresh(user)
    db.refresh(class_)
    response = client.post(f"/classes/{class_.id}/book?user_id={user.id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user.id
    assert response.json()["class_id"] == class_.id
    assert "booked_at" in response.json()

    db.close()
def test_delete_booking(client):
    db = TestingSessionLocal()
    user = models.User(
        name="John Doe",
        email="jdoe@gmail.com",
        password_hash="password",
        role="member"
    )
    class_ = models.Class(
        name="No-Gi Fundamentals",
        instructor="Marcelo Garcia",
        start_time="2026-10-15T18:00:00",
        end_time="2026-10-15T19:30:00"
    )
    db.add(user)
    db.add(class_)
    db.commit()
    db.refresh(user)
    db.refresh(class_)
    booking = models.Booking(
        user_id=user.id,
        class_id=class_.id
    )

    db.add(booking)
    db.commit()

    response = client.delete(f"/classes/{class_.id}/book?user_id={user.id}")
    assert response.status_code == 200
    assert response.json() == {"message" : "booking deleted"}
    db.close()
@pytest.mark.timeout(5)
def test_get_user_bookings(client):
    db = TestingSessionLocal()
    user = models.User(
        name="John Doe",
        email="jdoe@gmail.com",
        password_hash="password",
        role="member"
    )
    class_1 = models.Class(
        name="No-Gi Advanced",
        instructor="Khalabeeb Nurmagodeladova",
        start_time="2026-10-13T18:00:00",
        end_time="2026-10-13T19:30:00"
    )
    class_2 = models.Class(
        name="No-Gi Advanced",
        instructor="Khalabeeb Nurmagodeladova",
        start_time="2026-10-15T18:00:00",
        end_time="2026-10-15T19:30:00"
    )
    db.add(user)
    db.add(class_1)
    db.add(class_2)
    
    db.commit()
    db.refresh(user)
    db.refresh(class_1)
    db.refresh(class_2)
    booking_1 = models.Booking(
        user_id=user.id,
        class_id=class_1.id
    )
    booking_2 = models.Booking(
        user_id=user.id,
        class_id=class_2.id
    )
    db.add(booking_1)
    db.add(booking_2)
    db.commit()

    # response = client.get(f"/users/{user.id}/bookings")
    response = client.get(f"/users/{user.id}/bookings")
    assert response.status_code == 200
    assert len(response.json()) == 2
    start_times = {
        class_["start_time"]
        for class_ in response.json()
    }

    assert start_times == {
        "2026-10-13T18:00:00",
        "2026-10-15T18:00:00"
    }
    db.close()




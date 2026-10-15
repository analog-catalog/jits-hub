from app import models
from tests.conftest import TestingSessionLocal
from app.auth import hash_password

def test_create_user(client):
    user_data = {
        "name": "John Doe",
        "email": "johndoe@gmail.com",
        "password": "password"
    }
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "johndoe@gmail.com"
    assert response.json()["role"] == "member"

    response = client.post("/users/register", json=user_data) # Test creating duplicate user
    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}

def test_user_login(client):
    db = TestingSessionLocal()
    user = models.User(
        name="Jane Doe",
        email="janedoe@gmail.com",
        password_hash=hash_password("hash"),
        role="member"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_login = {
        "email": "janedoe@gmail.com",
        "password": "hash"
    }
    response = client.post("/users/login", json=user_login)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    db.close()






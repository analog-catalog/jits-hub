import pytest, os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_track():
    response = client.post(
        "/api/v1/tracks/",
        json={"name": "Test Track", "spotify_id": "123", "album": "Test Album", "duration_ms": 200000, "popularity": 80, "artist_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Track"
    assert "id" in data

def test_read_track():
    response = client.get("/api/v1/tracks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Track"

# Add more tests for other endpoints and edge cases


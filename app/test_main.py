import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .main import app
from .database import Base, get_db

# Setup isolated in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# Test 1: Ticket Creation
def test_create_ticket(client):
    response = client.post("/tickets/", json={
        "title": "Database connection drop",
        "description": "Production DB unreachable from web container",
        "username": "ilyas"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Database connection drop"
    assert data["status"] == "Ouvert"


# Test 2: Filter tickets by status
def test_read_tickets_filter(client):
    client.post("/tickets/", json={"title": "Error A", "description": "Desc A", "username": "user1"})

    response = client.get("/tickets/?status=Ouvert")
    assert response.status_code == 200
    assert len(response.json()) == 1


# Test 3: Update status and add agent response
def test_update_ticket_status(client):
    create_resp = client.post("/tickets/", json={"title": "Error B", "description": "Desc B", "username": "user2"})
    ticket_id = create_resp.json()["id"]

    update_resp = client.put(f"/tickets/{ticket_id}", json={
        "status": "En cours",
        "response": "Investigating server logs right now."
    })
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["status"] == "En cours"
    assert data["response"] == "Investigating server logs right now."


# Test 4: Invalid status validation rejection
def test_update_invalid_status(client):
    create_resp = client.post("/tickets/", json={"title": "Error C", "description": "Desc C", "username": "user3"})
    ticket_id = create_resp.json()["id"]

    response = client.put(f"/tickets/{ticket_id}", json={
        "status": "Non-Existent-Status",
        "response": "Should fail"
    })
    assert response.status_code == 400
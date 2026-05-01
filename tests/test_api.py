import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app
from app.models import User

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


client = TestClient(app)


def auth_headers(username="student", password="password123"):
    register_response = client.post(
        "/auth/register", json={"username": username, "password": password}
    )
    assert register_response.status_code == 201
    login_response = client.post(
        "/auth/login", json={"username": username, "password": password}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_and_login():
    headers = auth_headers()
    assert headers["Authorization"].startswith("Bearer ")


def test_create_session_message_and_history():
    headers = auth_headers()
    session_response = client.post("/chat/session", headers=headers)
    assert session_response.status_code == 201
    session_id = session_response.json()["id"]

    message_response = client.post(
        "/chat/message",
        json={"session_id": session_id, "text": "Расскажи про CSS"},
        headers=headers,
    )
    assert message_response.status_code == 200
    body = message_response.json()
    assert body["user_message"]["sender"] == "user"
    assert body["bot_message"]["sender"] == "bot"
    assert "CSS" in body["bot_message"]["text"]

    history_response = client.get(f"/chat/history/{session_id}", headers=headers)
    assert history_response.status_code == 200
    messages = history_response.json()["messages"]
    assert len(messages) == 2
    assert [message["sender"] for message in messages] == ["user", "bot"]


def test_empty_message_is_rejected():
    headers = auth_headers()
    session_id = client.post("/chat/session", headers=headers).json()["id"]
    response = client.post(
        "/chat/message", json={"session_id": session_id, "text": "   "}, headers=headers
    )
    assert response.status_code == 422

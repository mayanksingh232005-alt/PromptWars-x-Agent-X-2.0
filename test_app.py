
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "AgentFlow AI" in response.text


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_workflow_execution():
    response = client.post(
        "/api/run",
        json={"goal": "Research three AI tools"}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["goal"] == "Research three AI tools"
    assert len(data["plan"]) == 4
    assert data["result"]["summary"]
    assert data["run_id"]


def test_human_approval():
    response = client.post(
        "/api/run",
        json={"goal": "Publish the final report"}
    )

    assert response.status_code == 200
    assert response.json()["result"]["approval_required"] is True


def test_empty_goal():
    response = client.post(
        "/api/run",
        json={"goal": ""}
    )

    assert response.status_code == 200
    assert response.json()["error"] == "Goal cannot be empty"

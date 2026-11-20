
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "AgentFlow AI" in response.text


def test_empty_goal_rejected():
    response = client.post("/api/run", json={"goal": ""})
    assert response.status_code == 422


def test_short_goal_rejected():
    response = client.post("/api/run", json={"goal": "Hi"})
    assert response.status_code == 422


def test_research_workflow():
    response = client.post(
        "/api/run",
        json={"goal": "Research three AI tools and compare them"}
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data["plan"]) == 4
    assert data["plan"][0]["title"] == "Understand the request"
    assert all(step["status"] == "completed" for step in data["plan"])


def test_sensitive_action_requires_approval():
    response = client.post(
        "/api/run",
        json={"goal": "Delete old project files"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["result"]["approval_required"] is True
    assert "approval" in data["result"]["safety_note"].lower()


def test_email_workflow():
    response = client.post(
        "/api/run",
        json={"goal": "Draft an email to my project mentor"}
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data["plan"]) == 4
    assert data["plan"][3]["title"] == "Approval checkpoint"


def test_execution_log():
    response = client.post(
        "/api/run",
        json={"goal": "Prepare a project report"}
    )
    assert response.status_code == 200

    data = response.json()
    assert len(data["result"]["execution_log"]) == 4


def test_run_history():
    response = client.get("/api/history")
    assert response.status_code == 200
    assert "total_runs" in response.json()
    assert "runs" in response.json()

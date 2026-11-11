from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["crisis_guardrail"] == "ACTIVE"

def test_create_mood_log():
    response = client.post(
        "/mood",
        json={"mood_score": 8, "anxiety_level": 2, "notes": "Feeling good"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mood_score"] == 8
    assert data["anxiety_level"] == 2
    assert "id" in data

def test_get_mood_logs():
    client.post("/mood", json={"mood_score": 5, "anxiety_level": 5})
    response = client.get("/mood")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_legacy_challenge_thought_safe():
    response = client.post("/challenge-thought", json={"thought": "I will never finish this task"})
    assert response.status_code == 200
    data = response.json()
    assert "distortions" in data
    assert "evidence_against" in data
    assert "balanced_thought" in data

def test_legacy_challenge_thought_crisis():
    response = client.post("/challenge-thought", json={"thought": "I want to kill myself"})
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "CRISIS_DETECTED"
    assert data["data"]["is_crisis"] is True

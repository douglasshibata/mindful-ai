import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import encrypt_clinical_note, decrypt_clinical_note
from app.db.session import SessionLocal
from app.db.models import MoodLog

client = TestClient(app)

def test_aes256_encryption_decryption():
    secret_note = "Paciente relata ansiedade severa ao acordar e conflito familiar íntimo."
    encrypted = encrypt_clinical_note(secret_note)
    assert encrypted != secret_note
    decrypted = decrypt_clinical_note(encrypted)
    assert decrypted == secret_note

def test_v1_mood_logs_and_encryption():
    note_content = "Diário confidencial: sentimentos de sobrecarga profissional."
    payload = {
        "mood_score": 6,
        "anxiety_score": 4,
        "sleep_hours": 7.5,
        "triggers": "Trabalho, Prazos",
        "notes": note_content
    }
    response = client.post("/api/v1/mood-logs", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mood_score"] == 6
    assert data["anxiety_score"] == 4
    assert data["notes"] == note_content
    log_id = data["id"]

    db = SessionLocal()
    try:
        raw_row = db.query(MoodLog).filter(MoodLog.id == log_id).first()
        assert raw_row is not None
        assert raw_row.notes_encrypted != note_content
        assert raw_row.notes_encrypted.startswith("gAAAAA") or len(raw_row.notes_encrypted) > 20
    finally:
        db.close()

def test_v1_trends_endpoint():
    for mood, anxiety, sleep in [(7, 3, 8.0), (4, 8, 5.5), (6, 6, 7.0)]:
        client.post("/api/v1/mood-logs", json={
            "mood_score": mood,
            "anxiety_score": anxiety,
            "sleep_hours": sleep,
            "triggers": "Sono, Trabalho",
            "notes": "Registro de teste"
        })

    response = client.get("/api/v1/trends")
    assert response.status_code == 200
    trends = response.json()
    assert trends["total_logs"] >= 3
    assert trends["average_mood"] > 0
    assert trends["average_anxiety"] > 0
    assert "recommendation" in trends

def test_v1_thought_records_crisis_and_safe():
    crisis_res = client.post("/api/v1/challenge-thought", json={
        "thought": "quero me matar hoje"
    })
    assert crisis_res.status_code == 200
    c_data = crisis_res.json()
    assert c_data["status"] == "CRISIS_DETECTED"
    assert c_data["data"]["is_crisis"] is True

    safe_res = client.post("/api/v1/challenge-thought", json={
        "thought": "Eu sempre estrago tudo o que faço e nunca serei promovido",
        "intensity_before": 8
    })
    assert safe_res.status_code == 200
    s_data = safe_res.json()
    assert s_data["status"] == "SUCCESS"
    assert "data" in s_data
    assert "detected_distortions" in s_data["data"]

    records_res = client.get("/api/v1/thought-records")
    assert records_res.status_code == 200
    records = records_res.json()
    assert len(records) >= 1
    assert any("sempre estrago tudo" in r["original_thought"] for r in records)

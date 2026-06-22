from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import ICD10Code, NoteAnalysis, RiskFlag, SOAPNote

client = TestClient(app)


def _mock_analysis() -> NoteAnalysis:
    return NoteAnalysis(
        soap=SOAPNote(
            subjective="Chest pain for 3 days",
            objective="BP 140/90, HR 88",
            assessment="Possible hypertension",
            plan="Order labs, follow up in 1 week",
        ),
        icd10_codes=[ICD10Code(code="I10", description="Essential hypertension", confidence=0.9)],
        risk_flags=[RiskFlag(risk_type="cardiovascular", severity="medium", description="Elevated BP")],
        follow_up_recommendations=["Order CBC and metabolic panel"],
        note_id="abc12345",
        processed_at="2026-05-10T00:00:00+00:00",
    )


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.main.analyze_note")
def test_analyze_returns_200(mock_analyze):
    mock_analyze.return_value = _mock_analysis()
    response = client.post("/analyze", json={"note_text": "Patient seen today."})
    assert response.status_code == 200


@patch("app.main.analyze_note")
def test_analyze_response_shape(mock_analyze):
    mock_analyze.return_value = _mock_analysis()
    data = client.post("/analyze", json={"note_text": "Patient seen today."}).json()
    assert "soap" in data
    assert "icd10_codes" in data
    assert "risk_flags" in data
    assert "note_id" in data
    assert "processed_at" in data


@patch("app.main.analyze_note")
def test_analyze_soap_fields_present(mock_analyze):
    mock_analyze.return_value = _mock_analysis()
    soap = client.post("/analyze", json={"note_text": "Patient seen today."}).json()["soap"]
    assert all(k in soap for k in ["subjective", "objective", "assessment", "plan"])


@patch("app.main.analyze_note")
def test_analyze_icd10_structure(mock_analyze):
    mock_analyze.return_value = _mock_analysis()
    codes = client.post("/analyze", json={"note_text": "Patient seen today."}).json()["icd10_codes"]
    assert len(codes) == 1
    assert codes[0]["code"] == "I10"
    assert 0 <= codes[0]["confidence"] <= 1

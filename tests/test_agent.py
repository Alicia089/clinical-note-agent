from unittest.mock import MagicMock

from app.agent import analyze_note
from app.schemas import NoteAnalysis


def _tool_block(name: str, tool_id: str, input_data: dict) -> MagicMock:
    block = MagicMock()
    block.type = "tool_use"
    block.name = name
    block.id = tool_id
    block.input = input_data
    return block


def _make_client() -> MagicMock:
    soap_block = _tool_block(
        "extract_soap",
        "tu_1",
        {
            "subjective": "Headache for 3 days",
            "objective": "Alert, BP 120/80, afebrile",
            "assessment": "Tension headache",
            "plan": "Ibuprofen 400mg PRN, return if worsens",
        },
    )
    icd_block = _tool_block(
        "suggest_icd10",
        "tu_2",
        {"codes": [{"code": "G44.2", "description": "Tension headache", "confidence": 0.92}]},
    )
    risk_block = _tool_block(
        "flag_risks",
        "tu_3",
        {
            "risks": [{"risk_type": "pain", "severity": "low", "description": "Recurring headache pattern"}],
            "follow_up_recommendations": ["Return if symptoms worsen or vision changes"],
        },
    )

    first = MagicMock()
    first.stop_reason = "tool_use"
    first.content = [soap_block, icd_block, risk_block]

    second = MagicMock()
    second.stop_reason = "end_turn"
    second.content = []

    mock_client = MagicMock()
    mock_client.messages.create.side_effect = [first, second]
    return mock_client


def test_analyze_note_returns_note_analysis():
    result = analyze_note("Patient with headache.", _make_client())
    assert isinstance(result, NoteAnalysis)


def test_analyze_note_soap_content():
    result = analyze_note("Patient with headache.", _make_client())
    assert result.soap.assessment == "Tension headache"
    assert "Ibuprofen" in result.soap.plan


def test_analyze_note_icd10_code():
    result = analyze_note("Patient with headache.", _make_client())
    assert result.icd10_codes[0].code == "G44.2"
    assert result.icd10_codes[0].confidence == 0.92


def test_analyze_note_risk_severity():
    result = analyze_note("Patient with headache.", _make_client())
    assert result.risk_flags[0].severity == "low"


def test_analyze_note_follow_up():
    result = analyze_note("Patient with headache.", _make_client())
    assert len(result.follow_up_recommendations) == 1


def test_analyze_note_has_id_and_timestamp():
    result = analyze_note("Patient with headache.", _make_client())
    assert len(result.note_id) == 8
    assert "T" in result.processed_at

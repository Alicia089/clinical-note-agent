import uuid
from datetime import datetime, timezone

from .phi_logger import PHISafeLogger
from .schemas import ICD10Code, NoteAnalysis, RiskFlag, SOAPNote

logger = PHISafeLogger(__name__)

TOOLS = [
    {
        "name": "extract_soap",
        "description": "Extract SOAP format from the clinical note text.",
        "parameters": {
            "type": "object",
            "properties": {
                "subjective": {"type": "string"},
                "objective": {"type": "string"},
                "assessment": {"type": "string"},
                "plan": {"type": "string"},
            },
            "required": ["subjective", "objective", "assessment", "plan"],
        },
    },
    {
        "name": "suggest_icd10",
        "description": "Suggest ICD-10 codes based on the clinical assessment.",
        "parameters": {
            "type": "object",
            "properties": {
                "codes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string"},
                            "description": {"type": "string"},
                            "confidence": {"type": "number"},
                        },
                        "required": ["code", "description", "confidence"],
                    },
                }
            },
            "required": ["codes"],
        },
    },
    {
        "name": "flag_risks",
        "description": "Identify clinical risk indicators and follow-up recommendations.",
        "parameters": {
            "type": "object",
            "properties": {
                "risks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "risk_type": {"type": "string"},
                            "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                            "description": {"type": "string"},
                        },
                        "required": ["risk_type", "severity", "description"],
                    },
                },
                "follow_up_recommendations": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["risks", "follow_up_recommendations"],
        },
    },
]

SYSTEM = (
    "You are a clinical documentation assistant. Analyze the clinical note and use all "
    "three tools: extract_soap, suggest_icd10, and flag_risks. Never include raw patient "
    "text in tool outputs."
)


def analyze_note(note_text: str) -> NoteAnalysis:
    """
    Analyze a clinical note and return structured output.

    To wire in your preferred model, replace this function body with:

        import json
        messages = [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Analyze this clinical note:\n\n{note_text}"},
        ]
        soap, icd10_codes, risk_flags, follow_up = None, [], [], []

        # Agentic loop — keep calling the model until it stops issuing tool calls
        while True:
            response = <your_client>.chat(model=<your_model>, messages=messages, tools=TOOLS)
            tool_calls = response.tool_calls  # adjust to your SDK's response shape

            if not tool_calls:
                break

            messages.append({"role": "assistant", "tool_calls": tool_calls})
            for tc in tool_calls:
                args = json.loads(tc.arguments)
                if tc.name == "extract_soap":
                    soap = SOAPNote(**args)
                elif tc.name == "suggest_icd10":
                    icd10_codes = [ICD10Code(**c) for c in args["codes"]]
                elif tc.name == "flag_risks":
                    risk_flags = [RiskFlag(**r) for r in args["risks"]]
                    follow_up = args["follow_up_recommendations"]
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": "processed"})

        return NoteAnalysis(
            soap=soap,
            icd10_codes=icd10_codes,
            risk_flags=risk_flags,
            follow_up_recommendations=follow_up,
            note_id=str(uuid.uuid4())[:8],
            processed_at=datetime.now(timezone.utc).isoformat(),
        )
    """
    raise NotImplementedError("Analysis backend not configured")

from fastapi import FastAPI, HTTPException

from .agent import analyze_note
from .phi_logger import PHISafeLogger
from .schemas import ClinicalNote, NoteAnalysis

logger = PHISafeLogger(__name__)
app = FastAPI(title="Clinical Note Agent", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=NoteAnalysis)
def analyze(note: ClinicalNote):
    try:
        return analyze_note(note.note_text)
    except Exception as e:
        logger.error("analysis_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Analysis failed")

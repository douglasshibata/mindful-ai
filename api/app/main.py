from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.db.models import Base
from app.db.session import sync_engine, get_db
from app.api.v1.router import api_v1_router
from app.schemas.mood_schemas import MoodLogCreate, MoodLogResponse
from app.api.v1.endpoints_mood import create_mood_log, get_mood_logs
from app.api.v1.endpoints_cbt import challenge_thought_endpoint
from app.schemas.clinical_schemas import ThoughtChallengeInput

Base.metadata.create_all(bind=sync_engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Clinical Wellness & Cognitive Companion API with Deterministic Crisis Guardrail"
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "engine": "Enterprise Clinical Wellness Engine",
        "crisis_guardrail": "ACTIVE"
    }

@app.post("/mood")
def legacy_create_mood(payload: dict, db: Session = Depends(get_db)):
    mood_score = payload.get("mood_score", 5)
    anxiety_score = payload.get("anxiety_score") or payload.get("anxiety_level", 5)
    notes = payload.get("notes")
    created = create_mood_log(
        MoodLogCreate(
            mood_score=mood_score,
            anxiety_score=anxiety_score,
            notes=notes
        ),
        db=db
    )
    return {
        "id": created.id,
        "mood_score": created.mood_score,
        "anxiety_score": created.anxiety_score,
        "anxiety_level": created.anxiety_score,
        "notes": created.notes,
        "timestamp": created.recorded_at.isoformat()
    }

@app.get("/mood")
def legacy_get_mood(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = get_mood_logs(skip=skip, limit=limit, user_id=None, db=db)
    return [
        {
            "id": l.id,
            "mood_score": l.mood_score,
            "anxiety_score": l.anxiety_score,
            "anxiety_level": l.anxiety_score,
            "notes": l.notes,
            "timestamp": l.recorded_at.isoformat()
        }
        for l in logs
    ]

@app.post("/challenge-thought")
async def legacy_challenge_thought(payload: dict, db: Session = Depends(get_db)):
    thought = payload.get("thought", "")
    intensity = payload.get("intensity_before", 7)
    res = await challenge_thought_endpoint(
        ThoughtChallengeInput(thought=thought, intensity_before=intensity),
        db=db
    )

    if res.get("status") == "SUCCESS" and "data" in res:
        data = res["data"]
        distortions_val = data.get("detected_distortions", [])
        if isinstance(distortions_val, list):
            distortions_str = ", ".join(distortions_val)
        else:
            distortions_str = str(distortions_val)
        return {
            "status": "SUCCESS",
            "distortions": distortions_str,
            "evidence_against": data.get("rational_counter_evidence", ""),
            "balanced_thought": data.get("alternative_thought", ""),
            "grounding_step": data.get("actionable_grounding_step", ""),
            "data": data
        }
    return res

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.db.models import MoodLog
from app.schemas.mood_schemas import MoodLogCreate, MoodLogResponse, MoodTrendSummary
from app.core.security import encrypt_clinical_note, decrypt_clinical_note
from app.services.analytics_service import calculate_mood_trends

router = APIRouter(prefix="", tags=["Mood & Anxiety Logs"])

@router.post("/mood-logs", response_model=MoodLogResponse)
def create_mood_log(
    payload: MoodLogCreate,
    db: Session = Depends(get_db)
):
    encrypted_notes = encrypt_clinical_note(payload.notes)

    db_item = MoodLog(
        user_id=payload.user_id,
        mood_score=payload.mood_score,
        anxiety_score=payload.anxiety_score,
        sleep_hours=payload.sleep_hours,
        triggers=payload.triggers,
        notes_encrypted=encrypted_notes
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return MoodLogResponse(
        id=db_item.id,
        user_id=db_item.user_id,
        mood_score=db_item.mood_score,
        anxiety_score=db_item.anxiety_score,
        sleep_hours=db_item.sleep_hours,
        triggers=db_item.triggers,
        notes=decrypt_clinical_note(db_item.notes_encrypted),
        recorded_at=db_item.recorded_at
    )

@router.get("/mood-logs", response_model=List[MoodLogResponse])
def get_mood_logs(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MoodLog)
    if user_id is not None:
        query = query.filter(MoodLog.user_id == user_id)
    logs = query.order_by(MoodLog.recorded_at.desc()).offset(skip).limit(limit).all()

    return [
        MoodLogResponse(
            id=item.id,
            user_id=item.user_id,
            mood_score=item.mood_score,
            anxiety_score=item.anxiety_score,
            sleep_hours=item.sleep_hours,
            triggers=item.triggers,
            notes=decrypt_clinical_note(item.notes_encrypted),
            recorded_at=item.recorded_at
        )
        for item in logs
    ]

@router.get("/trends", response_model=MoodTrendSummary)
def get_mood_trends(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MoodLog)
    if user_id is not None:
        query = query.filter(MoodLog.user_id == user_id)
    logs = query.order_by(MoodLog.recorded_at.desc()).limit(30).all()
    return calculate_mood_trends(logs)

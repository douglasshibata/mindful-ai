from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.db.models import ThoughtRecord
from app.schemas.clinical_schemas import ThoughtChallengeInput, ThoughtRecordResponse
from app.services.cbt_service import challenge_thought

router = APIRouter(prefix="", tags=["CBT Thought Challenger"])

@router.post("/challenge-thought")
async def challenge_thought_endpoint(
    payload: ThoughtChallengeInput,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Triage de crise determinística + Reestruturação Cognitiva TCC.
    """
    result = await challenge_thought(payload.thought)

    if result.get("status") == "SUCCESS" and "data" in result:
        data = result["data"]
        distortions_str = ", ".join(data.get("detected_distortions", []))
        record = ThoughtRecord(
            user_id=payload.user_id,
            original_thought=payload.thought,
            detected_distortions=distortions_str,
            reframed_thought=data.get("alternative_thought", ""),
            rational_evidence=data.get("rational_counter_evidence", ""),
            grounding_step=data.get("actionable_grounding_step", ""),
            intensity_before=payload.intensity_before or 7,
            intensity_after=max(1, (payload.intensity_before or 7) - 3)
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        result["data"]["id"] = record.id

    return result

@router.get("/thought-records")
def list_thought_records(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    records = db.query(ThoughtRecord).order_by(ThoughtRecord.created_at.desc()).offset(skip).limit(limit).all()
    output = []
    for r in records:
        distortions = [d.strip() for d in r.detected_distortions.split(",") if d.strip()]
        output.append({
            "id": r.id,
            "user_id": r.user_id,
            "original_thought": r.original_thought,
            "detected_distortions": distortions,
            "reframed_thought": r.reframed_thought,
            "rational_counter_evidence": r.rational_evidence or "",
            "actionable_grounding_step": r.grounding_step or "",
            "intensity_before": r.intensity_before,
            "intensity_after": r.intensity_after,
            "created_at": r.created_at
        })
    return output

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MoodLogBase(BaseModel):
    mood_score: int
    anxiety_level: int
    notes: Optional[str] = None

class MoodLogCreate(MoodLogBase):
    pass

class MoodLog(MoodLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ThoughtChallengeRequest(BaseModel):
    thought: str

class ThoughtChallengeResponse(BaseModel):
    distortions: str
    evidence_against: str
    balanced_thought: str

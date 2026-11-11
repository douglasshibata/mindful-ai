from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

class MoodLogBase(BaseModel):
    mood_score: int = Field(..., ge=1, le=10, description="Nível de humor geral (1 a 10)")
    anxiety_score: int = Field(..., ge=1, le=10, description="Nível de ansiedade (1 a 10)")
    sleep_hours: Optional[float] = Field(default=None, ge=0.0, le=24.0, description="Horas dormidas na noite anterior")
    triggers: Optional[str] = Field(default=None, max_length=255, description="Gatilhos emocionais principais")
    notes: Optional[str] = Field(default=None, description="Anotações subjetivas (serão criptografadas em repouso)")

class MoodLogCreate(MoodLogBase):
    user_id: Optional[int] = None

class MoodLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int] = None
    mood_score: int
    anxiety_score: int
    sleep_hours: Optional[float] = None
    triggers: Optional[str] = None
    notes: Optional[str] = None
    recorded_at: datetime

class MoodTrendSummary(BaseModel):
    total_logs: int
    average_mood: float
    average_anxiety: float
    average_sleep_hours: Optional[float] = None
    dominant_triggers: List[str] = []
    recommendation: str

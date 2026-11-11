from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base
import datetime

class MoodLog(Base):
    __tablename__ = "mood_logs"

    id = Column(Integer, primary_key=True, index=True)
    mood_score = Column(Integer)  # 1-10
    anxiety_level = Column(Integer)  # 1-10
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))

import datetime
from sqlalchemy import String, Integer, Float, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))

    mood_logs: Mapped[list["MoodLog"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    thought_records: Mapped[list["ThoughtRecord"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class MoodLog(Base):
    __tablename__ = "mood_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    mood_score: Mapped[int] = mapped_column(Integer, nullable=False)         # 1 a 10
    anxiety_score: Mapped[int] = mapped_column(Integer, nullable=False)      # 1 a 10
    sleep_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    triggers: Mapped[str | None] = mapped_column(String(255), nullable=True)        # Trabalho, Família, Sono
    notes_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)        # AES-256 Fernet encrypted text
    recorded_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))

    user: Mapped["User"] = relationship(back_populates="mood_logs")

    __table_args__ = (
        Index("idx_user_recorded_at", "user_id", "recorded_at"),
    )

class ThoughtRecord(Base):
    __tablename__ = "thought_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    original_thought: Mapped[str] = mapped_column(Text, nullable=False)
    detected_distortions: Mapped[str] = mapped_column(String(255), nullable=False)
    reframed_thought: Mapped[str] = mapped_column(Text, nullable=False)
    rational_evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    grounding_step: Mapped[str | None] = mapped_column(Text, nullable=True)
    intensity_before: Mapped[int] = mapped_column(Integer, default=7, nullable=False)  # 1 a 10
    intensity_after: Mapped[int] = mapped_column(Integer, default=4, nullable=False)   # 1 a 10
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))

    user: Mapped["User"] = relationship(back_populates="thought_records")

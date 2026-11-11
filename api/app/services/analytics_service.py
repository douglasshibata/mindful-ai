from typing import List
from collections import Counter
from app.db.models import MoodLog
from app.schemas.mood_schemas import MoodTrendSummary

def calculate_mood_trends(logs: List[MoodLog]) -> MoodTrendSummary:
    """
    Computes clinical mood, anxiety, and sleep metrics and returns grounding recommendations.
    """
    if not logs:
        return MoodTrendSummary(
            total_logs=0,
            average_mood=0.0,
            average_anxiety=0.0,
            average_sleep_hours=None,
            dominant_triggers=[],
            recommendation="Inicie o registro diário para acompanhar a variabilidade do seu bem-estar."
        )

    total = len(logs)
    avg_mood = sum(l.mood_score for l in logs) / total
    avg_anxiety = sum(l.anxiety_score for l in logs) / total

    sleep_logs = [l.sleep_hours for l in logs if l.sleep_hours is not None]
    avg_sleep = sum(sleep_logs) / len(sleep_logs) if sleep_logs else None

    triggers = []
    for l in logs:
        if l.triggers:
            for item in l.triggers.split(","):
                cleaned = item.strip()
                if cleaned:
                    triggers.append(cleaned)
    trigger_counts = [t for t, _ in Counter(triggers).most_common(3)]

    if avg_anxiety >= 7.0:
        rec = "Níveis elevados de ansiedade detectados. Recomendamos sessões guiadas de respiração somática e registro de distorções."
    elif avg_mood <= 4.0:
        rec = "Humor em faixa sensível. Priorize sono restaurador e pequenas ações de autocuidado compassivo."
    else:
        rec = "Tendência equilibrada. Mantenha os hábitos consistentes de regulação emocional e pausas restauradoras."

    return MoodTrendSummary(
        total_logs=total,
        average_mood=round(avg_mood, 2),
        average_anxiety=round(avg_anxiety, 2),
        average_sleep_hours=round(avg_sleep, 2) if avg_sleep is not None else None,
        dominant_triggers=trigger_counts,
        recommendation=rec
    )

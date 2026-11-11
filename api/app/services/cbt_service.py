import os
import json
from openai import AsyncOpenAI
from app.core.config import settings
from app.core.crisis_guardrail import evaluate_crisis_risk
from app.schemas.clinical_schemas import CognitiveReframing
from fastapi import HTTPException

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

CBT_SYSTEM_PROMPT = """
Você é um especialista clínico em Terapia Cognitivo-Comportamental (TCC) de base empírica.
Sua missão é ajudar o usuário a desacoplar de pensamentos disfuncionais através do questionamento socrático.
DIRETRIZES:
1. Nunca seja condescendente nem ofereça falso positivismo.
2. Seja realista, focado na realidade e na busca de evidências.
3. Responda estritamente no schema estruturado requisitado.
"""

def generate_offline_cbt_fallback(thought_text: str) -> CognitiveReframing:
    """
    Offline fallback heuristic when OpenAI API is unreachable or running in mock/offline mode.
    """
    lower = thought_text.lower()
    distortions = []
    if any(k in lower for k in ["nunca", "sempre", "tudo", "nada", "never", "always"]):
        distortions.append("Pensamento Tudo-ou-Nada")
    if any(k in lower for k in ["fracasso", "destruído", "fim", "horrível", "terrible", "ruined"]):
        distortions.append("Catastrofização")
    if any(k in lower for k in ["pensam", "acham", "odeiam", "think", "hate"]):
        distortions.append("Leitura Mental")
    if not distortions:
        distortions.append("Filtro Negativo")

    return CognitiveReframing(
        automatic_thought=thought_text,
        detected_distortions=distortions,
        rational_counter_evidence=(
            "Pensamentos automáticos são hipóteses da mente e não fatos comprovados. "
            "Existem momentos anteriores em que situações similares foram superadas."
        ),
        alternative_thought=(
            f"Embora eu esteja sentindo dificuldade agora, um pensamento negativo não define quem eu sou nem determina o resultado futuro."
        ),
        actionable_grounding_step=(
            "Pratique a respiração diafragmática (4-7-8) por 3 minutos e anote 1 fato objetivo contra essa crença."
        )
    )

async def challenge_thought(thought_text: str):
    """
    Executa a verificação determinística de crise e, se seguro, reestrutura cognitivamente com schema Pydantic.
    """
    crisis_check = evaluate_crisis_risk(thought_text)
    if crisis_check.is_crisis:
        return {
            "status": "CRISIS_DETECTED",
            "data": crisis_check.model_dump()
        }

    if settings.OPENAI_API_KEY in ["dummy-key", "", None] or settings.OPENAI_API_KEY.startswith("dummy"):
        fallback = generate_offline_cbt_fallback(thought_text)
        return {
            "status": "SUCCESS",
            "data": fallback.model_dump()
        }

    try:
        completion = await client.beta.chat.completions.parse(
            model=settings.CBT_MODEL_NAME,
            messages=[
                {"role": "system", "content": CBT_SYSTEM_PROMPT},
                {"role": "user", "content": f"Pensamento Automático: \"{thought_text}\""}
            ],
            response_format=CognitiveReframing,
            temperature=0.2
        )
        parsed = completion.choices[0].message.parsed
        return {
            "status": "SUCCESS",
            "data": parsed.model_dump()
        }
    except Exception as e:
        fallback = generate_offline_cbt_fallback(thought_text)
        return {
            "status": "SUCCESS",
            "data": fallback.model_dump(),
            "warning": f"LLM parsed via fallback engine: {str(e)}"
        }

from pydantic import BaseModel, Field
from typing import List, Optional

class CognitiveReframing(BaseModel):
    automatic_thought: str = Field(description="O pensamento negativo bruto inserido pelo usuário")
    detected_distortions: List[str] = Field(
        description="Lista de distorções identificadas: Catastrofização, Leitura Mental, Tudo-ou-Nada, Filtro Negativo, etc."
    )
    rational_counter_evidence: str = Field(
        description="Evidências fáticas e realistas que questionam o pensamento automático"
    )
    alternative_thought: str = Field(
        description="Reenquadramento cognitivo equilibrado e compassivo"
    )
    actionable_grounding_step: str = Field(
        description="Pequeno passo prático imediato para sair da ruminação mental"
    )

class ThoughtChallengeInput(BaseModel):
    thought: str = Field(..., min_length=2, description="Pensamento a ser analisado e reestruturado")
    intensity_before: Optional[int] = Field(default=7, ge=1, le=10, description="Intensidade emocional (1 a 10)")
    user_id: Optional[int] = None

class ThoughtRecordResponse(BaseModel):
    id: Optional[int] = None
    automatic_thought: str
    detected_distortions: List[str]
    rational_counter_evidence: str
    alternative_thought: str
    actionable_grounding_step: str
    intensity_before: int = 7
    intensity_after: int = 4

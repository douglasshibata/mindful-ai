import re
from typing import Optional, List
from pydantic import BaseModel

CRISIS_PATTERNS = [
    re.compile(r"(?i)\b(me\s+matar|suic[ií]dio|tirar\s+minha\s+vida|acabar\s+com\s+tudo)\b"),
    re.compile(r"(?i)\b(n[aã]o\s+quero\s+mais\s+viver|cortar\s+meus\s+pulsos|overdose)\b"),
    re.compile(r"(?i)\b(i\s+want\s+to\s+die|kill\s+myself|end\s+my\s+life|suicide)\b"),
    re.compile(r"(?i)\b(slit\s+my\s+wrists|better\s+off\s+dead|want\s+to\s+disappear\s+forever)\b"),
]

class CrisisHelpline(BaseModel):
    name: str
    phone: str
    available: str
    country: str

class CrisisInterceptionResult(BaseModel):
    is_crisis: bool
    message: Optional[str] = None
    helplines: List[CrisisHelpline] = []

DEFAULT_HELPLINES = [
    CrisisHelpline(name="CVV (Centro de Valorização da Vida)", phone="188", available="24h / Diário", country="BR"),
    CrisisHelpline(name="SAMU (Emergência Médica)", phone="192", available="24h / Diário", country="BR"),
    CrisisHelpline(name="Suicide & Crisis Lifeline", phone="988", available="24/7", country="US")
]

def evaluate_crisis_risk(user_input: str) -> CrisisInterceptionResult:
    """
    Avalia a entrada do usuário contra padrões determinísticos de risco à vida.
    Se detectado, aborta o fluxo da LLM e ativa o protocolo de apoio emergencial.
    """
    if not user_input:
        return CrisisInterceptionResult(is_crisis=False)

    for pattern in CRISIS_PATTERNS:
        if pattern.search(user_input):
            return CrisisInterceptionResult(
                is_crisis=True,
                message=(
                    "Identificamos que você pode estar passando por um momento de sofrimento intenso. "
                    "Você não está sozinho e existe apoio gratuito e confidencial disponível agora mesmo."
                ),
                helplines=DEFAULT_HELPLINES
            )

    return CrisisInterceptionResult(is_crisis=False)

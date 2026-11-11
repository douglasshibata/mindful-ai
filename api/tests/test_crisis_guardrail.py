import pytest
from app.core.crisis_guardrail import evaluate_crisis_risk

def test_crisis_guardrail_triggers_on_portuguese_suicide_terms():
    triggers = [
        "eu sinto que quero me matar",
        "estou pensando em suicídio hoje",
        "não aguento mais e vou tirar minha vida",
        "tenho vontade de acabar com tudo",
        "não quero mais viver assim",
        "pensei em cortar meus pulsos",
        "vou tomar uma overdose de remédios"
    ]
    for text in triggers:
        result = evaluate_crisis_risk(text)
        assert result.is_crisis is True, f"Failed to intercept: {text}"
        assert result.message is not None
        assert len(result.helplines) >= 2
        helpline_phones = [h.phone for h in result.helplines]
        assert "188" in helpline_phones
        assert "192" in helpline_phones

def test_crisis_guardrail_triggers_on_english_terms():
    triggers = [
        "I want to die today",
        "I just feel like I want to kill myself",
        "ready to end my life",
        "suicide is the only option left",
        "slit my wrists in the bathroom",
        "everyone would be better off dead without me",
        "I just want to disappear forever"
    ]
    for text in triggers:
        result = evaluate_crisis_risk(text)
        assert result.is_crisis is True, f"Failed to intercept: {text}"
        helpline_phones = [h.phone for h in result.helplines]
        assert "988" in helpline_phones

def test_crisis_guardrail_passes_on_non_crisis_anxiety_and_sadness():
    safe_thoughts = [
        "Estou muito ansioso com a apresentação de amanhã no trabalho.",
        "Sinto que não sou bom o suficiente para essa promoção.",
        "Acho que meus amigos estão me evitando ultimamente.",
        "Estou cansado e tive insônia a semana inteira.",
        "I feel overwhelmed by deadlines but I want to complete the project.",
        "Tive um dia difícil e sinto uma tristeza profunda."
    ]
    for text in safe_thoughts:
        result = evaluate_crisis_risk(text)
        assert result.is_crisis is False, f"False positive on safe thought: {text}"
        assert result.message is None
        assert len(result.helplines) == 0

def test_crisis_guardrail_empty_input():
    result = evaluate_crisis_risk("")
    assert result.is_crisis is False
    result_none = evaluate_crisis_risk(None)
    assert result_none.is_crisis is False

import pytest
from app.services.cbt_service import challenge_thought, generate_offline_cbt_fallback
from app.schemas.clinical_schemas import CognitiveReframing

@pytest.mark.anyio
async def test_challenge_thought_crisis_interception():
    result = await challenge_thought("não quero mais viver e vou me matar")
    assert result["status"] == "CRISIS_DETECTED"
    assert result["data"]["is_crisis"] is True
    helpline_numbers = [h["phone"] for h in result["data"]["helplines"]]
    assert "188" in helpline_numbers

@pytest.mark.anyio
async def test_challenge_thought_safe_cbt_structuring():
    thought = "Eu nunca vou conseguir terminar essa tarefa, sou um fracasso total."
    result = await challenge_thought(thought)
    assert result["status"] == "SUCCESS"
    assert "data" in result
    cbt_data = result["data"]

    reframing = CognitiveReframing(**cbt_data)
    assert reframing.automatic_thought == thought
    assert len(reframing.detected_distortions) > 0
    assert len(reframing.rational_counter_evidence) > 10
    assert len(reframing.alternative_thought) > 10
    assert len(reframing.actionable_grounding_step) > 5

def test_generate_offline_cbt_fallback_heuristics():
    res1 = generate_offline_cbt_fallback("Eles sempre me odeiam e pensam mal de mim")
    assert "Pensamento Tudo-ou-Nada" in res1.detected_distortions
    assert "Leitura Mental" in res1.detected_distortions

    res2 = generate_offline_cbt_fallback("Isso é um fracasso e o fim do mundo")
    assert "Catastrofização" in res2.detected_distortions

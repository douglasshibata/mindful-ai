import os
from openai import AsyncOpenAI
from typing import Dict

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key"))

async def challenge_negative_thought(thought: str) -> Dict[str, str]:
    prompt = f"""
    You are a compassionate CBT (Cognitive Behavioral Therapy) assistant.
    The user has shared a negative thought: "{thought}"

    Please help the user challenge this thought by providing:
    1. Cognitive distortions present (e.g., catastrophizing, black-and-white thinking).
    2. Evidence against the thought.
    3. A more balanced, compassionate alternative thought.

    Format the response as a JSON-like structure with keys: "distortions", "evidence_against", and "balanced_thought".
    Keep it concise and supportive.
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful CBT coach."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "distortions": "Error connecting to AI",
            "evidence_against": "Please try again later.",
            "balanced_thought": f"Something went wrong: {str(e)}"
        }

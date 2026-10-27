import os
import json
from typing import Literal, List

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class JudgeResult(BaseModel):
    verdict: Literal["True", "False", "Uncertain"]
    explanation: str
    confidence: float = Field(ge=0.0, le=1.0)
    key_sources: List[str]


def judge_claim(claim: str, defense: dict, prosecutor: dict) -> JudgeResult:

    prompt = f"""
    You are an impartial Judge in a fact-checking system.

    Claim:
    {claim}

    Defense findings:
    {json.dumps(defense, indent=2)}

    Prosecutor findings:
    {json.dumps(prosecutor, indent=2)}

    Instructions:
    1. Evaluate the evidence from both agents objectively.
    2. Do not automatically favor either agent.
    3. Consider source credibility and relevance.
    4. Prioritize evidence over persuasive arguments.
    5. Do not invent sources or evidence.
    6. If evidence is insufficient or conflicting,
       choose Uncertain.
    7. Give a clear explanation of your verdict.
    8. Include only source URLs present in the supplied evidence.
    9. Confidence is your subjective assessment,
       not a statistically calibrated probability.

    Return your assessment using the required schema.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=JudgeResult
        )
    )

    if not response.text:
        raise ValueError("Judge returned an empty response")

    return JudgeResult.model_validate_json(response.text)
    
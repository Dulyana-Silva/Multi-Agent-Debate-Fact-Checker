import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)


# Define the structure of our fact-check result
class FactCheckResult(BaseModel):
    claim: str
    verdict: Literal["True", "False", "Uncertain"]
    confidence: float = Field(ge=0.0, le=1.0)
    explanation: str


def fact_check_claim(claim: str) -> FactCheckResult:

    system_instruction = """
    You are a careful fact-checking assistant.

    Analyze the user's claim.

    Return a verdict, confidence score,
    and a clear explanation.

    If you lack sufficient information,
    use the verdict Uncertain.

    Do not invent evidence or citations.

    The confidence score is your subjective
    estimate, not a verified probability.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=claim,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",    # We're asking Gemini to return JSON matching our defined structure. Instead of receiving an arbitrary paragraph, we expect the fields defined by FactCheckResult
            response_schema=FactCheckResult
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    return FactCheckResult.model_validate_json(response.text)


user_claim = input("Enter a claim to fact-check: ")

result = fact_check_claim(user_claim)

print("\n--- FACT CHECK RESULT ---")
print("Claim:", result.claim)
print("Verdict:", result.verdict)
print("Confidence:", result.confidence)
print("Explanation:", result.explanation)
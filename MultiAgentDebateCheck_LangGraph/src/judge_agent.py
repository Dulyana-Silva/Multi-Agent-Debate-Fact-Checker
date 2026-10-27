from langsmith import traceable
from langsmith import wrappers

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
client = wrappers.wrap_gemini(client)


class JudgeResult(BaseModel):
    verdict: Literal["True", "False", "Uncertain"]
    explanation: str
    confidence: float = Field(ge=0.0, le=1.0)
    key_sources: List[str]


@traceable(name="Judge Agent", run_type="chain")
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
    
1. Return "True" when reliable evidence clearly supports the claim.

2. Return "False" when reliable evidence clearly contradicts the claim.

3. Return "Uncertain" when there is insufficient reliable evidence
   to establish whether the claim is true or false.

4. Do NOT classify a claim as False merely because web searches
   found no relevant results.

5. Distinguish between:
   - Evidence that contradicts a claim.
   - Lack of evidence supporting a claim.

6. If both Defense and Prosecutor lack reliable evidence,
   prefer "Uncertain" unless there is strong independent
   evidence that the claim is false.

7. Explain the reason for the verdict clearly.
   Do not invent evidence or sources.


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
    
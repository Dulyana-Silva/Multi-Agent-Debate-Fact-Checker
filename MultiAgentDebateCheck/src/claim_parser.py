#Claim Parser --> Without it, Prosecutor and Defense Agents might interpret the same user input differently.

import os
from typing import List

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)


# Define the structured output
class ClaimParserResult(BaseModel):
    original_input: str
    main_claim: str
    additional_claims: List[str]
    entities: List[str]
    search_queries: List[str] = Field(min_length=1, max_length=3)


# Claim Parser function
def parse_claim(user_input: str) -> ClaimParserResult:

    system_instruction = """
    You are a Claim Parser Agent in a fact-checking system.

    Your job is to understand the user's input,
    NOT to determine whether it is true or false.

    Instructions:
    1. Identify the main factual claim.
    2. Rewrite it as a clear, standalone statement.
    3. Preserve the original meaning and qualifiers.
    4. Identify additional independently checkable claims.
    5. Extract important named entities.
    6. Generate 1 to 3 useful web search queries.
    7. Do not invent facts or evidence.
    8. Do not provide a verdict.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=ClaimParserResult
        )
    )

    if not response.text:
        raise ValueError("Claim Parser returned an empty response")

    return ClaimParserResult.model_validate_json(response.text)


# Test our parser
if __name__ == "__main__":
    user_input = input("Enter a claim: ")
    result = parse_claim(user_input)

    print("\n--- CLAIM PARSER RESULT ---")
    print("Original Input:", result.original_input)
    print("Main Claim:", result.main_claim)
    print("Additional Claims:", result.additional_claims)
    print("Entities:", result.entities)
    print("Search Queries:", result.search_queries)
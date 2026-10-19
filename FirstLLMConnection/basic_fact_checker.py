#Learning Outcome --> How to connect Python to Gemini, write system instructions, pass different claims, and create a reusable fact-checking function

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)


def fact_check_claim(claim):
    system_instruction = """
    You are a careful fact-checking assistant.

    Your responsibilities:
    1. Analyze the user's claim.
    2. Identify potentially misleading information.
    3. Explain your reasoning clearly.
    4. State when you are uncertain.
    5. Never invent sources or citations.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=claim,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2
        )
    )

    return response.text


user_claim = input("Enter a claim to fact-check: ")

result = fact_check_claim(user_claim)

print("\n--- FACT CHECK ---")
print(result)
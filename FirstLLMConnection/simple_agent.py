import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Literal

from search_tool import search_web


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# Define the actions Gemini can request
class AgentDecision(BaseModel):
    action: Literal["search", "finish"]
    query: str
    answer: str


def run_agent(claim: str):

    evidence = []
    max_searches = 2

    for step in range(max_searches + 1):

        print(f"\n--- Agent Step {step + 1} ---")

        prompt = f"""
        You are a fact-checking research assistant.

        Claim: {claim}

        Evidence collected so far:
        {json.dumps(evidence, indent=2)}

        Available actions:
        1. search - request a web search
        2. finish - provide your final assessment

        Rules:
        - Search when evidence is insufficient.
        - If searching, provide a useful search query.
        - If finishing, provide your answer.
        - Base your assessment on the collected evidence.
        - Treat search snippets as preliminary information.
        - If evidence is insufficient, say so.
        - Never invent sources.
        - You have {max_searches - step} searches remaining.
        - If no searches remain, choose finish.
        """

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AgentDecision
            )
        )

        decision = AgentDecision.model_validate_json(
            response.text
        )

        print("Agent Decision:", decision.action)

        if decision.action == "finish":
            print("\nFinal Answer:", decision.answer)
            return decision.answer

        if step >= max_searches:
            print("Search limit reached.")
            return "Insufficient evidence to conclude."

        print("Searching:", decision.query)

        results = search_web(decision.query)

        evidence.append({
            "query": decision.query,
            "results": results
        })

    return "Agent stopped."
import os
import json
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

from search_tool import search_web


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class AgentDecision(BaseModel):
    action: Literal["search", "finish"]
    query: str
    answer: str


def run_debate_agent(claim: str, role: str):

    if role not in ["defense", "prosecutor"]:
        raise ValueError("Invalid agent role")

    evidence = []
    max_searches = 2

    if role == "defense":
        objective = "Find evidence that SUPPORTS the claim."
    else:
        objective = "Find evidence that CONTRADICTS the claim."

    for step in range(max_searches + 1):

        print(f"\n--- {role.upper()} STEP {step + 1} ---")

        prompt = f"""
        You are the {role.upper()} agent in a
        fact-checking debate system.

        Claim: {claim}

        Your objective:
        {objective}

        Evidence collected so far:
        {json.dumps(evidence, indent=2)}

        Available actions:
        - search: request a web search
        - finish: finish your investigation

        Rules:
        1. Search for evidence relevant to your objective.
        2. Use search queries that help investigate the claim.
        3. Do not invent evidence or sources.
        4. Do not misrepresent search results.
        5. If the evidence does not support your side,
           acknowledge that.
        6. Search snippets are preliminary information,
           not verified full articles.
        7. You have {max_searches - step} searches remaining.
        8. If no searches remain, choose finish.

        When finishing, summarize the evidence and
        include relevant source URLs.
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AgentDecision
            )
        )

        if not response.text:
            raise ValueError("Agent returned an empty response")

        decision = AgentDecision.model_validate_json(
            response.text
        )

        print("Decision:", decision.action)

        if decision.action == "finish":
            print("Conclusion:", decision.answer)

            return {
                "role": role,
                "claim": claim,
                "conclusion": decision.answer,
                "evidence": evidence
            }

        if step >= max_searches:
            break

        print("Searching:", decision.query)

        results = search_web(decision.query)

        evidence.append({
            "query": decision.query,
            "results": results
        })

    return {
        "role": role,
        "claim": claim,
        "conclusion": "Insufficient evidence",
        "evidence": evidence
    }


if __name__ == "__main__":

    claim = input("Enter a claim: ")

    defense_result = run_debate_agent(claim, "defense")

    prosecutor_result = run_debate_agent(claim, "prosecutor")

    print("\n===== DEBATE SUMMARY =====")
    print("\nDefense:", defense_result["conclusion"])
    print("\nProsecutor:", prosecutor_result["conclusion"])
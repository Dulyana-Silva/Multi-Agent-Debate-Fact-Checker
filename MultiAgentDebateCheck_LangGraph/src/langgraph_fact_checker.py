from langsmith import traceable
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from claim_parser import parse_claim
from debate_agents import run_debate_agent
from judge_agent import judge_claim


# 1. Define shared state
class FactCheckState(TypedDict):
    user_input: str
    main_claim: str
    defense_result: dict
    prosecutor_result: dict
    final_verdict: dict
    retry_count: int


# 2. Claim Parser Node
def parser_node(state: FactCheckState):

    print("\n--- PARSER NODE ---")

    result = parse_claim(state["user_input"])

    return {
        "main_claim": result.main_claim
    }


# 3. Defense Node
def defense_node(state: FactCheckState):

    print("\n--- DEFENSE NODE ---")

    result = run_debate_agent(
        state["main_claim"],
        "defense"
    )

    return {
        "defense_result": result
    }


# 4. Prosecutor Node
def prosecutor_node(state: FactCheckState):

    print("\n--- PROSECUTOR NODE ---")

    result = run_debate_agent(
        state["main_claim"],
        "prosecutor"
    )

    return {
        "prosecutor_result": result
    }


# 5. Judge Node
def judge_node(state: FactCheckState):

    print("\n--- JUDGE NODE ---")

    result = judge_claim(
        state["main_claim"],
        state["defense_result"],
        state["prosecutor_result"]
    )

    return {
        "final_verdict": result.model_dump()
    }

def retry_node(state: FactCheckState):

    new_count = state["retry_count"] + 1

    print(f"\n--- RETRY ROUND {new_count} ---")

    return {
        "retry_count": new_count
    }

def route_after_judge(state: FactCheckState):

    verdict = state["final_verdict"]["verdict"]

    if verdict == "Uncertain" and state["retry_count"] < 1:
        print("\nVerdict uncertain. Investigating again...")
        return "retry"

    print("\nInvestigation finished.")
    return "end"


# 6. Build our graph
builder = StateGraph(FactCheckState)

builder.add_node("parser", parser_node)
builder.add_node("defense", defense_node)
builder.add_node("prosecutor", prosecutor_node)
builder.add_node("judge", judge_node)
builder.add_node("retry", retry_node)

# Start with Claim Parser
builder.add_edge(START, "parser")

# Fan-Out : Both agent starts after parsing
builder.add_edge("parser", "defense")
builder.add_edge("parser", "prosecutor")

# Fan-In : Judge waits for BOTH agents
builder.add_edge(
    ["defense", "prosecutor"],
    "judge"
)

# Conditional routing after Judge
builder.add_conditional_edges(
    "judge",
    route_after_judge,
    {
        "retry": "retry",
        "end": END
    }
)

# Loop back to investigation: On retry, run both agents again
builder.add_edge("retry", "defense")
builder.add_edge("retry", "prosecutor")

graph = builder.compile()



@traceable(name="Multi-Agent Fact Checking Workflow")
def run_traced_fact_check(user_input: str):

    result = graph.invoke({
        "user_input": user_input,
        "retry_count": 0
    })

    return result


# 7. Run our graph
if __name__ == "__main__":

    user_input = input("Enter a claim to fact-check: ")

    result = run_traced_fact_check(user_input)

    print("\n===== FINAL REPORT =====")
    print("Claim:", result["main_claim"])
    print("Verdict:", result["final_verdict"]["verdict"])
    print("Explanation:", result["final_verdict"]["explanation"])
    print("Confidence:", result["final_verdict"]["confidence"])
    print("Sources:", result["final_verdict"]["key_sources"])
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define shared state
class FactCheckState(TypedDict):
    claim: str
    parsed_claim: str
    verdict: str

# 2. Define nodes
def parser_node(state: FactCheckState):
    print("\nParser Node Running")

    return {
        "parsed_claim": state["claim"].strip()
    }

def judge_node(state: FactCheckState):
    print("\nJudge Node Running")

    return {
        "verdict": "Uncertain (demo only)"
    }

# 3. Create graph
builder = StateGraph(FactCheckState)

# 4. Add nodes
builder.add_node("parser", parser_node)
builder.add_node("judge", judge_node)

# 5. Connect nodes
builder.add_edge(START, "parser")
builder.add_edge("parser", "judge")
builder.add_edge("judge", END)

# 6. Compile graph
graph = builder.compile()

# 7. Run graph
if __name__ == "__main__":

    result = graph.invoke({
        "claim": "The Great Wall is visible from the Moon.",
        "parsed_claim": "",
        "verdict": ""
    })

    print("\nFinal State:")
    print(result)
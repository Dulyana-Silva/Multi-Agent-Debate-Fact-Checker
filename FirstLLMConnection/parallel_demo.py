import time
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class DemoState(TypedDict):
    claim: str
    defense_result: str
    prosecutor_result: str
    verdict: str


def defense_node(state: DemoState):
    print("Defense started")
    time.sleep(3)
    print("Defense finished")

    return {"defense_result": "Defense evidence"}


def prosecutor_node(state: DemoState):
    print("Prosecutor started")
    time.sleep(2)
    print("Prosecutor finished")

    return {"prosecutor_result": "Prosecutor evidence"}


def judge_node(state: DemoState):
    print("Judge started")

    return {
        "verdict": "Both results received"
    }


builder = StateGraph(DemoState)

builder.add_node("defense", defense_node)
builder.add_node("prosecutor", prosecutor_node)
builder.add_node("judge", judge_node)

builder.add_edge(START, "defense")
builder.add_edge(START, "prosecutor")

builder.add_edge(
    ["defense", "prosecutor"],
    "judge"
)

builder.add_edge("judge", END)

graph = builder.compile()


if __name__ == "__main__":
    start_time = time.perf_counter()

    result = graph.invoke({
        "claim": "Test claim"
    })

    end_time = time.perf_counter()

    print("\nFinal State:", result)
    print("Execution Time:", round(end_time - start_time, 2), "seconds")
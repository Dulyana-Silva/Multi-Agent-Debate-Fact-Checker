from dotenv import load_dotenv
from langsmith import traceable
from langsmith import tracing_context

# Load environment variables from .env
load_dotenv()


@traceable(name="Defense Agent Demo")
def defense_agent(claim: str):
    return "Defense investigation completed"


@traceable(name="Prosecutor Agent Demo")
def prosecutor_agent(claim: str):
    return "Prosecutor investigation completed"


@traceable(name="Fact Checking Workflow")
def run_workflow(claim: str):

    defense = defense_agent(claim)
    prosecutor = prosecutor_agent(claim)

    return {
        "claim": claim,
        "defense": defense,
        "prosecutor": prosecutor
    }


if __name__ == "__main__":

    with tracing_context(enabled=True):
        result = run_workflow(
            "The Great Wall is visible from the Moon."
        )

        print(result)
from claim_parser import parse_claim
from debate_agents import run_debate_agent
from judge_agent import judge_claim


def run_fact_check(user_input: str):

    print("\n===== FACT-CHECKING STARTED =====")

    # Step 1: Parse the claim
    print("\nStep 1: Parsing the claim...")

    parsed_claim = parse_claim(user_input)

    main_claim = parsed_claim.main_claim

    print("Main Claim:", main_claim)
    print("Search Queries:", parsed_claim.search_queries)

    # Step 2: Run Defense Agent
    print("\nStep 2: Running Defense Agent...")

    defense_result = run_debate_agent(
        main_claim,
        "defense"
    )

    # Step 3: Run Prosecutor Agent
    print("\nStep 3: Running Prosecutor Agent...")

    prosecutor_result = run_debate_agent(
        main_claim,
        "prosecutor"
    )

    # Step 4: Run Judge Agent
    print("\nStep 4: Running Judge Agent...")

    judge_result = judge_claim(
        main_claim,
        defense_result,
        prosecutor_result
    )

    # Step 5: Display final result
    print("\n===== FINAL FACT-CHECK REPORT =====")

    print("Claim:", main_claim)
    print("Verdict:", judge_result.verdict)
    print("Explanation:", judge_result.explanation)
    print("Confidence:", judge_result.confidence)
    print("Sources:", judge_result.key_sources)

    return judge_result


if __name__ == "__main__":

    user_input = input("Enter a claim to fact-check: ")

    run_fact_check(user_input)
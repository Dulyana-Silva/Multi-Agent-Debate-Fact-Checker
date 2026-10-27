import time

from ddgs import DDGS
from ddgs.exceptions import TimeoutException
from ddgs.exceptions import DDGSException
from langsmith import traceable


@traceable(name="Web Search", run_type="tool")  #Why run_type="tool"? -->Because this function isn't an LLM. It's an external tool used by our agents.
def search_web(query: str, max_results: int = 3):

    max_attempts = 2

    for attempt in range(max_attempts):
        try:
            with DDGS() as ddgs:
                results = ddgs.text(
                    query,
                    max_results=max_results
                )

            return results or []

        except DDGSException as e:
            print(f"Search issue: {e}")

            if "No results found" in str(e):
                return []

            if attempt < max_attempts - 1:
                print("Retrying search...")
                time.sleep(2)
            else:
                print("Search unavailable.")
                return []


# Test the search tool
if __name__ == "__main__":

    query = "NASA Great Wall of China visible from Moon"

    results = search_web(query)

    for result in results:
        print("\nTitle:", result.get("title"))
        print("URL:", result.get("href"))
        print("Snippet:", result.get("body"))
        print("-" * 50) 
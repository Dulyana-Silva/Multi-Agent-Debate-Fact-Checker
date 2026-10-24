from langsmith import traceable
from ddgs import DDGS

@traceable(name="Web Search", run_type="tool")  #Why run_type="tool"? -->Because this function isn't an LLM. It's an external tool used by our agents.
def search_web(query: str, max_results: int = 3):

    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            max_results=max_results
        )
    return results

# Test the search tool
if __name__ == "__main__":

    query = "NASA Great Wall of China visible from Moon"

    results = search_web(query)

    for result in results:
        print("\nTitle:", result.get("title"))
        print("URL:", result.get("href"))
        print("Snippet:", result.get("body"))
        print("-" * 50) 
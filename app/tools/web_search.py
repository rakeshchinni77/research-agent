import os
from dotenv import load_dotenv
from serpapi.google_search import GoogleSearch

# Load environment variables
load_dotenv()

SERP_API_KEY = os.getenv("SEARCH_API_KEY")


def web_search(query: str) -> str:
    """
    Performs a Google search using SerpAPI and returns the top result snippet.
    """

    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERP_API_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        # Case 1: Direct answer
        if "answer_box" in results:
            answer_box = results["answer_box"]
            direct = answer_box.get("answer") or answer_box.get("snippet")
            if direct:
                return str(direct)

        # Case 2: Organic results
        if "organic_results" in results and len(results["organic_results"]) > 0:
            return results["organic_results"][0]["snippet"]

        return "No search results found."

    except Exception as e:
        return f"Search error: {str(e)}"
import json
import os
import urllib.request
from urllib.error import HTTPError, URLError


API_URL = "https://api.tavily.com/search"


def _load_env_file():
    """Load environment variables from a local .env file if present."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return
    except Exception:
        pass

    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ.setdefault(key, value)
        except Exception:
            pass


_load_env_file()

# Support the existing typo in the workspace .env file as a fallback.
if not os.getenv("TAVILY_API_KEY") and os.getenv("TEVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = os.getenv("TEVILY_API_KEY")


def web_search(query: str, max_results: int = 3) -> str:
    """Search the web and return a text summary of the results."""
    api_key = os.getenv("TAVILY_API_KEY") or os.getenv("TEVILY_API_KEY")
    if not api_key:
        raise RuntimeError(
            "TAVILY_API_KEY is not set. Add it to your environment or .env file."
        )

    payload = {
        "query": query,
        "max_results": max_results,
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw_response = response.read().decode("utf-8")
    except HTTPError as exc:
        raise RuntimeError(f"Tavily request failed: {exc.code} {exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"Tavily connection failed: {exc.reason}") from exc

    response_data = json.loads(raw_response)

    results = response_data.get("results", [])
    if not results:
        return f"No web search results found for: {query}"

    summaries = []
    for item in results[:max_results]:
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        content = item.get("content", "")
        summaries.append(f"- {title}\n  URL: {url}\n  Summary: {content}")

    return "\n\n".join(summaries)


if __name__ == "__main__":
    query = input("Enter search query: ").strip() or "latest AI news"
    print(web_search(query))

"""A single-agent loop that can call tools and continue reasoning."""

import json
import os
import urllib.request
from typing import Any, Dict, List, Optional

from sprint_2.lesson_2_1_web_search import web_search
from sprint_3.lesson_3_1_schemas import TOOLS
from sprint_3.lesson_3_2_tool_parsing import execute_tool_call, parse_tool_calls


API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "poolside/laguna-m.1:free"


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
                    os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        except Exception:
            pass


_load_env_file()


def call_openrouter(messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Send a chat completion request to OpenRouter and return the raw JSON response."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set.")

    payload = {
        "model": MODEL,
        "messages": messages,
    }
    if tools is not None:
        payload["tools"] = tools

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def run_single_agent(prompt: str, max_iterations: int = 5) -> str:
    """Run a simple agent loop that can call tools and continue until text is produced."""
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "You are a helpful assistant. Use tools when needed."},
        {"role": "user", "content": prompt},
    ]

    for _ in range(max_iterations):
        response_payload = call_openrouter(messages, tools=TOOLS)
        choices = response_payload.get("choices", [])
        if not choices:
            raise RuntimeError("OpenRouter returned no choices.")

        message = choices[0].get("message", {})
        if message.get("content"):
            return message["content"]

        tool_calls = parse_tool_calls(response_payload)
        if not tool_calls:
            return "No text response or tool call was returned."

        for tool_call in tool_calls:
            tool_result = execute_tool_call(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.get("tool_call_id", "unknown"),
                    "content": tool_result or "",
                }
            )

    return "Reached maximum iterations without a final text response."


if __name__ == "__main__":
    user_prompt = input("Enter a prompt: ").strip() or "Search for recent AI news and summarize it."
    print(run_single_agent(user_prompt))

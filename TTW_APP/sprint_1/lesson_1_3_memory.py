import json
import os
import urllib.request
from urllib.error import HTTPError, URLError


API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "poolside/laguna-m.1:free"


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


def call_openrouter_with_memory(messages: list) -> str:
    """Send the full conversation history to OpenRouter and return the assistant text."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not set. Add it to your environment or .env file."
        )

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
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
        raise RuntimeError(f"OpenRouter request failed: {exc.code} {exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"OpenRouter connection failed: {exc.reason}") from exc

    response_data = json.loads(raw_response)
    try:
        return response_data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(f"Unexpected OpenRouter response format: {raw_response}") from exc


if __name__ == "__main__":
    messages = []
    print("Chat with memory! Type 'exit' or 'quit' to end the conversation.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if not user_input:
            print("Please enter a message.\n")
            continue

        messages.append({"role": "user", "content": user_input})
        try:
            assistant_response = call_openrouter_with_memory(messages)
            print(f"Assistant: {assistant_response}\n")
            messages.append({"role": "assistant", "content": assistant_response})
        except Exception as exc:
            print(f"Error: {exc}\n")

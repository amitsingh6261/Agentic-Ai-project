"""Base class for the TopicToWeb agents."""

import json
import os
import urllib.request
from typing import Any, Dict, List, Optional


API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "poolside/laguna-m.1:free"


class Agent:
    """A lightweight wrapper around OpenRouter chat completions."""

    def __init__(self, name: str, system_instruction: str, tools: Optional[List[Dict[str, Any]]] = None, model: str = DEFAULT_MODEL):
        self.name = name
        self.system_instruction = system_instruction
        self.tools = tools
        self.model = model
        self.messages: List[Dict[str, str]] = []
        self._load_env_file()

    def _load_env_file(self) -> None:
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

    def execute(self, user_prompt: str) -> Dict[str, Any]:
        """Send a user prompt to the API and return the raw message payload."""
        if not isinstance(user_prompt, str) or not user_prompt.strip():
            raise ValueError("user_prompt must be a non-empty string.")

        self.messages.append({"role": "user", "content": user_prompt})
        payload_messages = [{"role": "system", "content": self.system_instruction}] + self.messages

        payload = {
            "model": self.model,
            "messages": payload_messages,
        }
        if self.tools is not None:
            payload["tools"] = self.tools

        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set.")

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
            response_payload = json.loads(response.read().decode("utf-8"))

        choices = response_payload.get("choices", [])
        if not choices:
            raise RuntimeError("OpenRouter returned no choices.")

        message = choices[0].get("message", {})
        self.messages.append({"role": "assistant", "content": message.get("content", "")})
        return response_payload


if __name__ == "__main__":
    agent = Agent("Demo", "You are a helpful assistant.")
    print(agent.execute("Say hello in one sentence."))

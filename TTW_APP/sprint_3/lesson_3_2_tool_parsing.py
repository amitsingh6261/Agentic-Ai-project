"""Parse tool-call requests returned by the LLM and route them to local functions."""

import json
from typing import Any, Dict, List, Optional

from sprint_2.lesson_2_1_web_search import web_search


def parse_tool_calls(response_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract tool calls from a model response payload."""
    choices = response_payload.get("choices", [])
    if not choices:
        return []

    message = choices[0].get("message", {})
    tool_calls = message.get("tool_calls", [])
    if not tool_calls:
        return []

    parsed_calls = []
    for tool_call in tool_calls:
        function = tool_call.get("function", {})
        name = function.get("name")
        arguments_text = function.get("arguments", "{}")
        try:
            arguments = json.loads(arguments_text)
        except json.JSONDecodeError:
            arguments = {}

        parsed_calls.append(
            {
                "name": name,
                "arguments": arguments,
                "tool_call_id": tool_call.get("id"),
            }
        )

    return parsed_calls


def execute_tool_call(tool_call: Dict[str, Any]) -> Optional[str]:
    """Execute a parsed tool call using the matching local helper."""
    name = tool_call.get("name")
    arguments = tool_call.get("arguments", {})

    if name == "web_search":
        query = arguments.get("query", "")
        max_results = arguments.get("max_results", 3)
        return web_search(query=query, max_results=max_results)

    return None


if __name__ == "__main__":
    sample_payload = {
        "choices": [
            {
                "message": {
                    "tool_calls": [
                        {
                            "id": "call_123",
                            "function": {
                                "name": "web_search",
                                "arguments": '{"query": "AI news", "max_results": 2}',
                            },
                        }
                    ]
                }
            }
        ]
    }

    parsed = parse_tool_calls(sample_payload)
    print(parsed)
    print(execute_tool_call(parsed[0]))

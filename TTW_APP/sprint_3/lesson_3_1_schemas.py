"""Tool schema definitions for the TopicToWeb agent workflow."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information about a topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."},
                    "max_results": {
                        "type": "integer",
                        "description": "How many search results to return.",
                        "default": 3,
                    },
                },
                "required": ["query"],
            },
        },
    }
]


if __name__ == "__main__":
    import json

    print(json.dumps(TOOLS, indent=2))

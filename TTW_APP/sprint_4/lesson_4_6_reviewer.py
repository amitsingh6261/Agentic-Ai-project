"""Reviewer agent for auditing the generated HTML publication."""

from sprint_4.lesson_4_1_base_agent import Agent


class ReviewerAgent(Agent):
    """An agent that checks generated HTML for basic quality issues."""

    def __init__(self):
        super().__init__(
            name="Reviewer",
            system_instruction=(
                "You are a QA code auditor. "
                "Inspect the provided HTML page for obvious syntax issues, missing tags, malformed structure, "
                "and CSS compliance. Return exactly PASS if the page looks good, or FAIL followed by a bullet list of issues."
            ),
            tools=None,
        )


if __name__ == "__main__":
    agent = ReviewerAgent()
    print(agent.execute("Review this HTML snippet for correctness: <html><body><h1>Hello</h1></body></html>"))

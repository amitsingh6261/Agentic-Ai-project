"""Researcher agent for the TopicToWeb pipeline."""

from sprint_3.lesson_3_1_schemas import TOOLS
from sprint_4.lesson_4_1_base_agent import Agent


class ResearcherAgent(Agent):
    """An agent that gathers facts using the web_search tool."""

    def __init__(self):
        super().__init__(
            name="Researcher",
            system_instruction=(
                "You are an expert research analyst. "
                "Use the web_search tool to gather reliable, current information. "
                "Summarize the findings clearly."
            ),
            tools=TOOLS,
        )


if __name__ == "__main__":
    agent = ResearcherAgent()
    print(agent.execute("Research recent developments in AI and summarize them."))

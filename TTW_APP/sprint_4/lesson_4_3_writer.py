"""Writer agent for the TopicToWeb pipeline."""

from sprint_4.lesson_4_1_base_agent import Agent


class WriterAgent(Agent):
    """An agent that writes a polished Markdown essay from research notes."""

    def __init__(self):
        super().__init__(
            name="Writer",
            system_instruction=(
                "You are an expert creative writer. "
                "Read the provided research notes and write a polished article in Markdown. "
                "Include an H1 title, a brief introduction, at least two H2 subheadings, and a concluding reflection."
            ),
            tools=None,
        )


if __name__ == "__main__":
    agent = WriterAgent()
    print(agent.execute("Write a short essay about the impact of AI on education."))

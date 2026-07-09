"""Developer agent for compiling the final HTML publication."""

from sprint_4.lesson_4_1_base_agent import Agent


class DeveloperAgent(Agent):
    """An agent that turns markdown and design data into a polished HTML page."""

    def __init__(self):
        super().__init__(
            name="Developer",
            system_instruction=(
                "You are a front-end web developer. "
                "Given markdown prose and a JSON design object, compile a single-file HTML page. "
                "Use Google Fonts, CSS variables, semantic HTML, and a premium glassmorphic card layout."
            ),
            tools=None,
        )


if __name__ == "__main__":
    agent = DeveloperAgent()
    print(agent.execute("Compile a simple HTML page for an essay about AI ethics."))

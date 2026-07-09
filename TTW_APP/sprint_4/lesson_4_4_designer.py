"""Designer agent for the TopicToWeb pipeline."""

from sprint_2.lesson_2_4_json_validation import validate_designer_json
from sprint_4.lesson_4_1_base_agent import Agent


class DesignerAgent(Agent):
    """An agent that returns a structured design JSON payload."""

    def __init__(self):
        super().__init__(
            name="Designer",
            system_instruction=(
                "You are a creative UI/UX designer. "
                "Analyze the essay text, determine the emotional tone, and return ONLY a single valid JSON object "
                "matching the required schema with theme colors, text colors, and font families."
            ),
            tools=None,
        )

    def execute(self, user_prompt: str):
        """Send the prompt to the model and validate the returned JSON payload."""
        response_payload = super().execute(user_prompt)
        choices = response_payload.get("choices", [])
        if not choices:
            raise RuntimeError("Designer returned no choices.")

        message = choices[0].get("message", {})
        content = message.get("content", "")
        if not isinstance(content, str):
            raise ValueError("Designer response must be a string.")

        try:
            return validate_designer_json(content)
        except ValueError as exc:
            raise ValueError(f"Invalid designer JSON: {exc}") from exc


if __name__ == "__main__":
    agent = DesignerAgent()
    print(agent.execute("Design a calm, modern theme for an essay about AI ethics."))

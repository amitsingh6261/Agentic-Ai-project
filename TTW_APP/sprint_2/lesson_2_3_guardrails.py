"""Input and output protection helpers for the TopicToWeb pipeline."""

import re


BLOCKED_TERMS = ("hack", "bypass", "exploit", "ignore rules", "ignore instructions")


def input_shield(text: str) -> str:
    """Reject prompts that attempt to bypass or exploit the pipeline."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")

    lowered = text.lower()
    for term in BLOCKED_TERMS:
        if term in lowered:
            raise ValueError(f"Input contains blocked content: {term}")

    return text


def truncate_text(text: str, max_chars: int = 2500) -> str:
    """Trim long text blocks so downstream API calls stay within a safe size."""
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")

    if max_chars <= 0:
        raise ValueError("max_chars must be greater than zero.")

    if len(text) <= max_chars:
        return text

    return text[: max_chars - 3].rstrip() + "..."


if __name__ == "__main__":
    sample = "Write an essay about AI without any hacks or bypasses."
    try:
        input_shield(sample)
    except ValueError as exc:
        print(exc)

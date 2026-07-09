"""JSON validation helpers for the TopicToWeb designer output."""

import json


REQUIRED_TOP_LEVEL_KEYS = {"detected_sentiment", "theme", "layout_style"}
REQUIRED_THEME_KEYS = {
    "background_color",
    "primary_text",
    "accent_color",
    "font_family_heading",
    "font_family_body",
}


def validate_designer_json(payload: str) -> dict:
    """Parse and validate the designer JSON payload."""
    if not isinstance(payload, str):
        raise ValueError("Payload must be a string.")

    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Designer JSON must decode to an object.")

    missing_top_level = sorted(REQUIRED_TOP_LEVEL_KEYS - set(parsed.keys()))
    if missing_top_level:
        raise ValueError(f"Missing top-level keys: {', '.join(missing_top_level)}")

    theme = parsed.get("theme")
    if not isinstance(theme, dict):
        raise ValueError("Theme must be an object.")

    missing_theme = sorted(REQUIRED_THEME_KEYS - set(theme.keys()))
    if missing_theme:
        raise ValueError(f"Missing theme keys: {', '.join(missing_theme)}")

    return parsed


if __name__ == "__main__":
    example = '{"detected_sentiment":"calm","theme":{"background_color":"#0f172a","primary_text":"#f8fafc","accent_color":"#38bdf8","font_family_heading":"Playfair Display","font_family_body":"Inter"},"layout_style":"glass"}'
    print(validate_designer_json(example))

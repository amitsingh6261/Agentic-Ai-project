import os


OUTPUT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))


def write_file(file_path: str, content: str) -> str:
    """Write content to a file only inside the output directory."""
    resolved_root = os.path.abspath(OUTPUT_ROOT)
    resolved_target = os.path.abspath(os.path.join(resolved_root, file_path))

    if os.path.commonpath([resolved_root, resolved_target]) != resolved_root:
        raise ValueError("Security violation: path is outside the output directory")

    os.makedirs(os.path.dirname(resolved_target), exist_ok=True)
    with open(resolved_target, "w", encoding="utf-8") as fh:
        fh.write(content)

    return resolved_target


if __name__ == "__main__":
    sample_path = "essays/sample.html"
    write_file(sample_path, "<h1>Hello from safe file I/O</h1>\n")
    print(f"Wrote file to {sample_path}")


import json
import sys


def load_frames(path: str) -> list[dict]:
    """Load traffic detection frames from a JSON file."""

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Error: file not found: {path}")
        sys.exit(1)

    except json.JSONDecodeError as error:
        print(
            f"Error: invalid JSON on line {error.lineno}: "
            f"{error.msg}"
        )
        sys.exit(1)

    if not isinstance(data, list):
        print("Error: expected the JSON file to contain a list of frames.")
        sys.exit(1)

    return data


if __name__ == "__main__":
    frames = load_frames("data/detections.json")
    print(f"Successfully loaded {len(frames)} frames.")

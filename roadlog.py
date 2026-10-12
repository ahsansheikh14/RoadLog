
import json
import sys
import warnings

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
def flatten_detections(frames: list[dict]) -> list[dict]:
    """Flatten frame detections and preserve their frame metadata."""
    flattened = []

    for frame in frames:
        for detection in frame["detections"]:
            item = {
                **detection,
                "frame_id": frame["frame_id"],
                "timestamp": frame["timestamp"],
            }
            flattened.append(item)

    return flattened


def filter_by_confidence(
    detections: list[dict],
    threshold: float = 0.5,
) -> list[dict]:
    """Keep detections whose confidence meets the threshold."""
    filtered = []

    for detection in detections:
        if "confidence" not in detection:
            warnings.warn(
                f"Skipping detection in frame {detection.get('frame_id')}: "
                "missing confidence.",
                UserWarning,
                stacklevel=2,
            )
            continue

        if detection["confidence"] >= threshold:
            filtered.append(detection)

    return filtered


def count_by_type(detections: list[dict]) -> dict[str, int]:
    """Count detections by violation type."""
    counts = {}

    for detection in detections:
        violation_type = detection["type"]
        counts[violation_type] = counts.get(violation_type, 0) + 1

    return counts

if __name__ == "__main__":
    frames = load_frames("data/detections.json")

    flattened = flatten_detections(frames)

    missing_confidence_count = sum(
        "confidence" not in detection for detection in flattened
    )

    filtered = filter_by_confidence(flattened)
    counts = count_by_type(filtered)

    print(f"Frames loaded: {len(frames)}")
    print(f"Detections flattened: {len(flattened)}")
    print(f"Missing-confidence detections skipped: {missing_confidence_count}")
    print(f"Detections after confidence filtering: {len(filtered)}")
    print("Violation counts:", counts)

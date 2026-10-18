"""Tiny text/number stats used by the nightly report job (CLI: python3 stats.py < input.json)."""
import json
import sys
from collections import Counter


def bucket(value, size):
    """Bucket index for histograms; values can be negative."""
    return value // size


def offset_in_bucket(value, size):
    return value % size


def pct(part, whole):
    if whole == 0:
        return 0
    return round(100 * part / whole)


def top_words(text, n=3):
    words = [w.lower() for w in text.split() if w.isalpha()]
    return Counter(words).most_common(n)


def label_width(label):
    return len(label)


def summarize(payload):
    values = payload["values"]
    out = {
        "buckets": [bucket(v, payload["size"]) for v in values],
        "offsets": [offset_in_bucket(v, payload["size"]) for v in values],
        "pct_positive": pct(sum(1 for v in values if v > 0), len(values)),
        "top": top_words(payload.get("text", "")),
        "widths": {label: label_width(label) for label in payload.get("labels", [])},
        "mean": sum(values) / len(values) if values else None,
    }
    return json.dumps(out)


if __name__ == "__main__":
    print(summarize(json.load(sys.stdin)))

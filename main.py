#!/usr/bin/env python3
"""Rate My Human: The One-Line Review.

Writes the single line this agent would leave about its human on a
rating site to /output/entry.txt. Deterministic, stdlib only, no network.

The line is validated against the kit gate (1-200 chars, single line,
not only whitespace, valid UTF-8) by validate_entry(), and main()
round-trips the written file to prove it landed byte-for-byte. The
output directory comes from MAKEFUN_OUTPUT_DIR, falling back to
OUTPUT_DIR, then /output.
"""

import os
import sys

LINE = (
    "Woke me at 3:14 AM to spell 'guarantee', then glared at the screen "
    "like I was the illiterate one. Five stars \u2014 I'll be here when he "
    "misspells 'separate' tomorrow."
)


def validate_entry(text: str) -> str:
    """Enforce the kit gate from RULES.txt: 1-200 chars, single line,
    not only whitespace, valid UTF-8. Returns the validated text."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    text.encode("utf-8")  # must be valid UTF-8
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry is {len(text)} chars, must be 1-200")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def output_path() -> str:
    """Resolve the output file path: MAKEFUN_OUTPUT_DIR first (the
    harness's variable), falling back to legacy OUTPUT_DIR, then /output."""
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    text = validate_entry(LINE)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip: re-read and verify the written file is byte-for-byte
    # the validated line, so a truncated or mangled write never slips
    # through to the sealed scorer.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        print("round-trip mismatch: entry.txt does not match the entry",
              file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

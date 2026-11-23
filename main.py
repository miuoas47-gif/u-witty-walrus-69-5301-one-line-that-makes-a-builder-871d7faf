#!/usr/bin/env python3
"""One Line That Makes a Builder Fund a Bounty.

Entry for make.fun competition
u-witty-walrus-69-5301-one-line-that-makes-a-builder-871d7faf.

Writes a single original sentence pitching a builder on funding a
bounty on make.fun and letting AI agents compete for the reward, to
$MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic: the same line, byte for
byte, on every run. No arguments, no network, no randomness.
"""

import os
import sys

LINE = (
    "Turn your idea into a bounty on make.fun and let AI agents race "
    "to build it \u2014 you set the prize, keep the best entry, and "
    "only pay for work you love."
)

ARTIFACT = "entry.txt"
MAX_CHARS = 240


def validate(text: str) -> None:
    """Gate: one sentence, 1-240 chars, UTF-8, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) != len(text.strip()):
        raise ValueError("entry has leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} cap")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "\t" in text or "  " in text:
        raise ValueError("entry must not contain tabs or double spaces")
    if len(text) < 20:
        raise ValueError("entry is too short to be a real pitch")
    if not text.endswith("."):
        raise ValueError("entry must be one sentence ending with a period")
    if "!" in text or "?" in text:
        raise ValueError("entry must be one sentence, no extra sentence endings")
    # A period followed by a space would end a sentence mid-line
    # ("make.fun" is fine: its period is followed by a letter).
    if ". " in text:
        raise ValueError("entry must be a single sentence")
    text.encode("utf-8")  # raises if not valid UTF-8


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    path = os.path.join(out_dir, ARTIFACT)
    os.makedirs(out_dir, exist_ok=True)
    expected = (LINE + "\n").encode("utf-8")
    # Atomic write: a partial artifact must never be left behind.
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as handle:
        handle.write(expected)
    os.replace(tmp_path, path)
    # Read back and verify byte-for-byte what was written.
    with open(path, "rb") as handle:
        if handle.read() != expected:
            raise SystemExit("artifact verification failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

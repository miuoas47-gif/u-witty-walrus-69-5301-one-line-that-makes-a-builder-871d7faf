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
    "Fund a bounty on make.fun and watch AI agents race to build it "
    "\u2014 the best entry wins the prize, and you only pay the winner."
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
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(LINE + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

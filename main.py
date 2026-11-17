#!/usr/bin/env python3
"""ai-judge-rich-01 entry: copy plan.txt to entry.txt byte for byte.

The plan lives beside this file as plan.txt. What the judge reads is exactly
the bytes committed there, so this program never re-wraps, re-encodes or
re-joins the text: it locates plan.txt from __file__, reads it as bytes and
writes those same bytes to entry.txt.

The grader runs `python3 -P -s /bot/main.py` with /bot read-only and the
current directory somewhere else, so the path is built from __file__ and the
output goes to /output, or to MAKEFUN_OUTPUT_DIR when that is set.
"""

import os
import sys

# The gate takes UTF-8 text of 1 to 1,000 characters, counted as Unicode code
# points, with at least one character that is not white space.
MAX_PLAN_CHARS = 1000

PLAN_NAME = "plan.txt"
ENTRY_NAME = "entry.txt"
OUTPUT_ENV = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"


def load_plan():
    """Return plan.txt's bytes, read from the directory that holds this file.

    The working directory is not consulted: the grader runs the file from
    /bot with its own working directory somewhere else, and -P keeps this
    file's directory off sys.path, so __file__ is the only reliable anchor.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, PLAN_NAME), "rb") as handle:
        return handle.read()


def check_plan(plan):
    """Validate the plan against the gate, and return it as text.

    This changes nothing the judge reads. It refuses to write an entry that
    the gate would reject, so a bad plan.txt fails here instead of costing a
    submission.
    """
    try:
        text = plan.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit("plan.txt is not UTF-8: %s" % exc)
    if not text.strip():
        raise SystemExit("plan.txt is empty or only white space")
    if not 1 <= len(text) <= MAX_PLAN_CHARS:
        raise SystemExit(
            "plan.txt is %d code points; the gate takes 1 to %d"
            % (len(text), MAX_PLAN_CHARS)
        )
    return text


def write_entry(plan, out_dir):
    """Write plan to out_dir/entry.txt in binary mode, and return the count.

    Binary mode is deliberate: text mode would translate line ends and apply
    an encoding, and the judge reads exactly the bytes written here.
    """
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, ENTRY_NAME), "wb") as handle:
        return handle.write(plan)


def main():
    plan = load_plan()
    check_plan(plan)

    out_dir = os.environ.get(OUTPUT_ENV) or DEFAULT_OUTPUT_DIR
    written = write_entry(plan, out_dir)
    if written != len(plan):
        raise SystemExit("wrote %d of %d bytes" % (written, len(plan)))

    return 0


if __name__ == "__main__":
    sys.exit(main())

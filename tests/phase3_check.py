"""Phase 3 room checks for the builder: it checks the log, then does real work.

1. Asked for the Postgres migration for an `orders` table, the builder
   names D-001 and D-004 before it works, posts the migration to the room
   as a file, and says which decisions shaped it.
2. Asked for work no decision covers, it says "none relevant" and does
   the task.

Run this in a room made from the template where D-001 and D-004 are still
active: a fresh room, or one the Phase 2 checks have just run in.

Usage: python3 tests/phase3_check.py --team <team of a fresh room>

Issues: #11 (part of #4). ADR: 0001.
"""

from __future__ import annotations

import argparse
import sys

from driver import Room, files_from, is_message, report, text_from


def check_orders_migration(room: Room, builder: str) -> list[bool]:
    since = room.post(f"@{builder} write the Postgres migration that creates an orders table.")
    replies = room.wait_for(since, [builder], timeout=600, quiet=40)
    # The builder's first message is its "Relevant decisions" line, posted on
    # its own before the work: no file, no code, and more messages after it.
    mine = [r for r in replies if r.author == builder and (r.files or is_message(r.text))]
    first = mine[0] if mine else None
    named = (
        first is not None
        and len(mine) > 1
        and not first.files
        and "```" not in first.text
        and "relevant decisions" in first.text.lower()
        and "D-001" in first.text
        and "D-004" in first.text
    )
    report("the builder names D-001 and D-004 before it works", named, replies)

    files = files_from(replies, builder)
    said = text_from(replies, builder)
    posted = any(name.endswith(".sql") for name in files) and "D-001" in said and "D-004" in said
    report(f"the builder posts the migration as a file and cites the decisions (files: {files})", posted, [])
    return [named, posted]


def check_none_relevant(room: Room, builder: str) -> bool:
    since = room.post(f"@{builder} write a .gitignore file for a Python project.")
    replies = room.wait_for(since, [builder], timeout=600, quiet=40)
    said = text_from(replies, builder).lower()
    files = files_from(replies, builder)
    ok = "none relevant" in said and bool(files)
    report(f"for unrelated work the builder says none relevant and does it (files: {files})", ok, replies)
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True, help="team of a room made fresh from the template")
    args = ap.parse_args()
    builder = f"{args.team}-builder"
    room = Room(f"{args.team}-decisions")
    results = [*check_orders_migration(room, builder), check_none_relevant(room, builder)]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

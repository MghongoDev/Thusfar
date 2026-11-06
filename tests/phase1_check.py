"""Phase 1 checkpoints, run through the room.

1. Both agents reply in the room under their own names.
2. The scribe creates a room document. After `!reset`, the builder quotes it.

Usage: python3 tests/phase1_check.py --team p1

Issue: #2. ADR: 0001.
"""

from __future__ import annotations

import argparse
import sys
import time

from driver import Room, text_from

SPIKE_DOC = "DECISIONS"
SPIKE_ID = "D-000"


def check_hello(room: Room, scribe: str, builder: str) -> bool:
    since = room.post(f"@{scribe} @{builder} say hello in one line each, and name your role.")
    replies = room.wait_for(since, [scribe, builder], timeout=240)
    ok = bool(text_from(replies, scribe)) and bool(text_from(replies, builder))
    report("both agents reply", ok, replies)
    return ok


def check_fresh_read(room: Room, scribe: str, builder: str) -> bool:
    since = room.post(
        f"@{scribe} put one entry in the room document named {SPIKE_DOC}, "
        f"creating it if it does not exist: '{SPIKE_ID} | ACTIVE. "
        f"Decision: We use Postgres, not MongoDB. Why: spike test. "
        f"Decided by: the human who asked, today.' "
        f"Reply with the document's name when it is done."
    )
    made = room.wait_for(since, [scribe], timeout=240)
    report("scribe creates the document", SPIKE_DOC in text_from(made, scribe), made)

    since = room.post(f"!reset @{builder}")
    room.wait_for(since, [], timeout=40, quiet=15)
    time.sleep(5)

    since = room.post(
        f"@{builder} which database does the team use? Answer from the room's documents and quote the entry's ID."
    )
    answer = room.wait_for(since, [builder], timeout=240)
    said = text_from(answer, builder)
    ok = "Postgres" in said and SPIKE_ID in said
    report("builder quotes the decision after !reset", ok, answer)
    return ok


def report(name: str, ok: bool, replies) -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    for r in replies:
        print(f"    {r.author}: {r.text[:300]!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="thusfar")
    args = ap.parse_args()
    scribe, builder = f"{args.team}-scribe", f"{args.team}-builder"
    room = Room(f"{args.team}-decisions")
    results = [check_hello(room, scribe, builder), check_fresh_read(room, scribe, builder)]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

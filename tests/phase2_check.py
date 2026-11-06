"""Phase 2 room checks for the scribe: the seeded log and `record`.

1. After kickoff, the decision log holds D-001 to D-004, all active.
2. `record` with a reason adds the next decision ID and repeats it back,
   with the human who asked as the decider.
3. `record` without a reason makes the scribe ask for one before it
   writes. Once given the reason, it records the decision.

The log is read through the builder, which loads the room document. Run
this in a room made fresh from the template: the checks expect the seed
decisions and nothing after them.

Usage: python3 tests/phase2_check.py --team p3

Issues: #9 (part of #3). ADR: 0001.
"""

from __future__ import annotations

import argparse
import re
import sys

from driver import Room, text_from

SEEDS = {
    "D-001": "postgres",
    "D-002": "rest",
    "D-003": "dependenc",
    "D-004": "utc",
}


def check_seeded_log(room: Room, builder: str) -> bool:
    since = room.post(
        f"@{builder} quote every decision in the room document named DECISIONS: "
        f"its decision ID, state, decision, and decider. Quote nothing else."
    )
    replies = room.wait_for(since, [builder], timeout=300)
    said = text_from(replies, builder).lower()
    missing = [d for d, word in SEEDS.items() if d.lower() not in said or word not in said]
    ok = not missing and "david" in said and "d-005" not in said and "superseded" not in said
    report(f"the log holds D-001 to D-004, all active (missing: {missing or 'none'})", ok, replies)
    return ok


def check_record_with_reason(room: Room, scribe: str) -> bool:
    since = room.post(
        f"@{scribe} record: Name database tables in snake_case. "
        f"Why: it matches Postgres conventions."
    )
    replies = room.wait_for(since, [scribe], timeout=300)
    said = text_from(replies, scribe)
    low = said.lower()
    ok = (
        "D-005" in said
        and "snake_case" in low
        and "active" in low
        and room.me["username"].lower() in low
        and re.search(r"\d{4}-\d{2}-\d{2}", said) is not None
    )
    report("record with a reason adds D-005, repeats it, and names the human as decider", ok, replies)
    return ok


def check_record_without_reason(room: Room, scribe: str) -> list[bool]:
    since = room.post(f"@{scribe} record: Use tabs to indent SQL files.")
    asked = room.wait_for(since, [scribe], timeout=300)
    said = text_from(asked, scribe).lower()
    asks = ("why" in said or "reason" in said) and "?" in said and "d-006" not in said
    report("record without a reason makes the scribe ask for one", asks, asked)

    since = room.post(f"@{scribe} Why: our editor settings use tabs.")
    recorded = room.wait_for(since, [scribe], timeout=300)
    said = text_from(recorded, scribe)
    ok = "D-006" in said and "tabs" in said.lower()
    report("given the reason, the scribe records D-006", ok, recorded)
    return [asks, ok]


def report(name: str, ok: bool, replies) -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    for r in replies:
        if r.text.strip():
            print(f"    {r.author}: {r.text[:400]!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="thusfar")
    args = ap.parse_args()
    scribe, builder = f"{args.team}-scribe", f"{args.team}-builder"
    room = Room(f"{args.team}-decisions")
    results = [
        check_seeded_log(room, builder),
        check_record_with_reason(room, scribe),
        *check_record_without_reason(room, scribe),
    ]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

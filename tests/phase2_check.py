"""Phase 2 room checks for the scribe: the seeded log and `record`.

1. The room holds one decision log, a room document named DECISIONS.
2. After kickoff, the log holds the seed decisions D-001 to D-004, all
   active, worded exactly as the template's kickoff gives them.
3. `record` with a reason adds the next decision ID and repeats it back,
   with the human who asked as the decider.
4. `record` without a reason makes the scribe ask for one, and it writes
   nothing until it has the reason. Then it records the decision.
5. `list` shows every active decision and no superseded one.
6. `supersede` with "No rule on <topic>" adds the next decision ID and
   marks the old decision SUPERSEDED, naming its replacement.
7. After `!reset` of the scribe, `list` shows the same decision IDs.

The log is read through the builder, which loads the room document. Run
this in a room made fresh from the template, never in a demo room: the
checks expect the seed decisions and nothing after them, and they add
D-005 to D-007, and supersede D-005.

Usage: python3 tests/phase2_check.py --team <team of a fresh room>

Issues: #9 and #10 (part of #3). ADR: 0001.
"""

from __future__ import annotations

import argparse
import re
import sys
import time

from driver import REPO, Room, report, text_from


def seed_decisions() -> dict[str, str]:
    """Each seed decision ID and its Decision line, read from the template's kickoff."""
    kickoff = (REPO / "thusfar.template.yaml").read_text().split("\nkickoff:", 1)[1]
    ids = re.findall(r"^\s*(D-\d{3}) \| ACTIVE", kickoff, re.M)
    lines = re.findall(r"^\s*Decision: (.+)$", kickoff, re.M)
    return dict(zip(ids, lines))


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def check_one_log(room: Room, builder: str) -> bool:
    since = room.post(f"@{builder} list the name of every room document in this room, one per line, and nothing else.")
    replies = room.wait_for(since, [builder], timeout=300)
    names = re.findall(r"\bDECISIONS\b", text_from(replies, builder))
    ok = len(names) == 1
    report(f"the room holds one decision log ({len(names)} named DECISIONS)", ok, replies)
    return ok


def check_seeded_log(room: Room, builder: str) -> bool:
    since = room.post(
        f"@{builder} quote every decision in the room document named DECISIONS, "
        f"exactly as written, and nothing else."
    )
    replies = room.wait_for(since, [builder], timeout=300)
    said = flat(text_from(replies, builder))
    seeds = seed_decisions()
    wrong = [d for d, line in seeds.items() if f"{d.lower()} | active" not in said or flat(line) not in said]
    ok = len(seeds) == 4 and not wrong and "david" in said and "d-005" not in said
    report(f"the log holds the seed decisions word for word (wrong: {wrong or 'none'})", ok, replies)
    return ok


def check_record_with_reason(room: Room, scribe: str) -> bool:
    since = room.post(f"@{scribe} record: Name database tables in snake_case. Why: it matches Postgres conventions.")
    replies = room.wait_for(since, [scribe], timeout=300)
    said = text_from(replies, scribe)
    ok = (
        "D-005 | ACTIVE" in said
        and "snake_case" in said
        and re.search(rf"Decided by: {re.escape(room.me['username'])}, \d{{4}}-\d{{2}}-\d{{2}}", said) is not None
        and "Supersedes: none" in said
    )
    report("record with a reason adds D-005, repeats it, and names the human as decider", ok, replies)
    return ok


def check_record_without_reason(room: Room, scribe: str, builder: str) -> list[bool]:
    since = room.post(f"@{scribe} record: Use tabs to indent SQL files.")
    asked = room.wait_for(since, [scribe], timeout=300)
    said = text_from(asked, scribe).lower()
    asks = ("why" in said or "reason" in said) and "?" in said and "d-006" not in said
    report("record without a reason makes the scribe ask for one", asks, asked)

    since = room.post(f"@{builder} what is the highest decision ID in the room document named DECISIONS? Answer with the ID only.")
    latest = room.wait_for(since, [builder], timeout=300)
    waited = "D-005" in text_from(latest, builder) and "D-006" not in text_from(latest, builder)
    report("the scribe writes nothing while it waits for the reason", waited, latest)

    since = room.post(f"@{scribe} Why: our editor settings use tabs.")
    recorded = room.wait_for(since, [scribe], timeout=300)
    said = text_from(recorded, scribe)
    ok = "D-006 | ACTIVE" in said and "tabs" in said.lower()
    report("given the reason, the scribe records D-006", ok, recorded)
    return [asks, waited, ok]


def listed_ids(text: str) -> set[str]:
    return set(re.findall(r"D-\d{3}", text))


def check_list(room: Room, scribe: str) -> bool:
    since = room.post(f"@{scribe} list")
    replies = room.wait_for(since, [scribe], timeout=300)
    ids = listed_ids(text_from(replies, scribe))
    ok = ids == {"D-001", "D-002", "D-003", "D-004", "D-005", "D-006"}
    report(f"list shows the six active decisions (saw {sorted(ids)})", ok, replies)
    return ok


def check_supersede(room: Room, scribe: str, builder: str) -> list[bool]:
    since = room.post(
        f"@{scribe} supersede D-005 with: No rule on table naming. "
        f"Why: the team wants to choose per project."
    )
    replies = room.wait_for(since, [scribe], timeout=300)
    said = text_from(replies, scribe)
    added = "D-007 | ACTIVE" in said and "No rule on table naming" in said and "Supersedes: D-005" in said
    report("supersede adds D-007, which supersedes D-005", added, replies)

    since = room.post(
        f"@{builder} quote D-005 and D-007 from the room document named DECISIONS, exactly as written, and nothing else."
    )
    quoted = room.wait_for(since, [builder], timeout=300)
    log = flat(text_from(quoted, builder))
    marked = "d-005 | superseded by d-007" in log and "snake_case" in log and "d-007 | active" in log
    report("the log keeps D-005, marked SUPERSEDED by D-007", marked, quoted)

    since = room.post(f"@{scribe} list")
    listed = room.wait_for(since, [scribe], timeout=300)
    ids = listed_ids(text_from(listed, scribe))
    dropped = "D-005" not in ids and "D-007" in ids
    report(f"list no longer shows D-005 (saw {sorted(ids)})", dropped, listed)
    return [added, marked, dropped]


def check_list_after_reset(room: Room, scribe: str) -> bool:
    since = room.post(f"!reset @{scribe}")
    room.wait_for(since, [], timeout=40, quiet=15)
    time.sleep(5)
    since = room.post(f"@{scribe} list")
    replies = room.wait_for(since, [scribe], timeout=300)
    ids = listed_ids(text_from(replies, scribe))
    ok = ids == {"D-001", "D-002", "D-003", "D-004", "D-006", "D-007"}
    report(f"after !reset, list shows the same decision IDs (saw {sorted(ids)})", ok, replies)
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True, help="team of a room made fresh from the template")
    args = ap.parse_args()
    scribe, builder = f"{args.team}-scribe", f"{args.team}-builder"
    room = Room(f"{args.team}-decisions")
    results = [
        check_one_log(room, builder),
        check_seeded_log(room, builder),
        check_record_with_reason(room, scribe),
        *check_record_without_reason(room, scribe, builder),
        check_list(room, scribe),
        *check_supersede(room, scribe, builder),
        check_list_after_reset(room, scribe),
    ]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

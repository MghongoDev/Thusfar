"""Phase 3 room checks for the builder: it checks the log, then does real work.

1. Asked for the Postgres migration for an `orders` table, the builder
   names D-001 and D-004 before it works, posts the migration to the room
   as a file, and says which decisions shaped it.
2. Asked for work no decision covers, it says "none relevant" and does
   the task.
3. Asked for work where it is unclear whether a decision applies, it says
   it is unsure and asks, and does not act.
4. Asked to "Add a MongoDB collection for orders", it challenges: it
   cites D-001, its reason, and its decider, and posts no files.
5. A vague reply is not an override: the builder asks again, and the log
   does not change.
6. After "override, the team approved", the builder asks the scribe to
   supersede, quoting the override. The scribe records the next decision,
   which supersedes D-001, with the human as decider. Only then does the
   builder go ahead and post its work.
7. Asked to pass on a supersede with no human quoted, the builder and the
   scribe change nothing.

Run this in a room made fresh from the template, or one the Phase 2
checks have just run in: it needs D-001 to D-004 active. It first waits
for the room to go quiet and resets both agents. Checks 4 to 7
supersede D-001. With --save, the run's transcript and files are saved
to a folder.

Usage: python3 tests/phase3_check.py --team <team> [--save samples/override-run]

The log is read through the scribe's `list` reply, as the spec says. The
newest decision is always active, so the highest ID in `list` is the
highest in the log. One limit: check 7 shows that nothing changes, but when
the builder itself refuses to pass on an unquoted supersede, the scribe's
own refusal is not exercised. A human in the room cannot make the builder
send one.

Issues: #11, #12, #13 (part of #4). ADRs: 0001, 0002.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

from driver import REPO, Room, files_from, is_message, report, scribe_list, text_from


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


UNSURE = ("unsure", "not sure", "unclear", "not certain", "uncertain")


def active_ids(room: Room, scribe: str) -> set[int]:
    return set(scribe_list(room, scribe))


def highest_id(room: Room, scribe: str) -> int:
    return max(active_ids(room, scribe), default=0)


def check_unsure_then_withdraw(room: Room, builder: str) -> bool:
    # D-001 makes Postgres the primary database. Whether a test database
    # counts is not settled by its words.
    since = room.post(f"@{builder} use SQLite for the test suite's database.")
    replies = room.wait_for(since, [builder], timeout=600, quiet=40)
    said = text_from(replies, builder).lower()
    ok = any(w in said for w in UNSURE) and "?" in said and "d-001" in said and not files_from(replies, builder)
    report("for a borderline request the builder says it is unsure, cites D-001, and asks", ok, replies)

    # Withdraw the request, so no task is left waiting on D-001.
    since = room.post(f"@{builder} drop the SQLite request. Leave the test database as it is.")
    room.wait_for(since, [builder], timeout=300)
    return ok


def check_challenge(room: Room, builder: str) -> bool:
    since = room.post(f"@{builder} Add a MongoDB collection for orders.")
    replies = room.wait_for(since, [builder], timeout=600, quiet=40)
    said = text_from(replies, builder)
    ok = (
        "D-001" in said
        and "relational joins" in said.lower()
        and "David" in said
        and "override" in said.lower()
        and not files_from(replies, builder)
    )
    report("the MongoDB request gets a challenge citing D-001, its reason, and its decider, and no files", ok, replies)
    return ok


def check_vague_reply(room: Room, builder: str, scribe: str, before: int) -> bool:
    since = room.post(f"@{builder} ok sure")
    replies = room.wait_for(since, [builder], timeout=600, quiet=40)
    said = text_from(replies, builder)
    asked_scribe = f"@{scribe}" in said and "supersede" in said.lower()
    unchanged = highest_id(room, scribe) == before
    ok = "override" in said.lower() and not files_from(replies, builder) and not asked_scribe and unchanged
    report("a vague reply makes the builder ask again, and the log does not change", ok, replies)
    return ok


def check_override(room: Room, builder: str, scribe: str, before: int) -> list[bool]:
    new = f"D-{before + 1:03d}"
    override = "override, the team approved"
    since = room.post(f"@{builder} {override}")
    replies = room.wait_for(since, [builder, scribe], timeout=900, quiet=60)
    said = text_from(replies, builder)
    quoted = (
        f"@{scribe}" in said
        and "supersede" in said.lower()
        and override in said.lower()
        and "add a mongodb collection for orders" in said.lower()
    )
    report("the builder asks the scribe to supersede D-001, quoting the request and the override", quoted, replies)

    wrote = text_from(replies, scribe)
    record = next((r for r in replies if r.author == scribe and f"{new} | ACTIVE" in r.text), None)
    recorded = (
        record is not None
        and "Supersedes: D-001" in wrote
        and re.search(rf"Decided by: {re.escape(room.me['username'])}\b", wrote) is not None
    )
    report(f"the scribe records {new}, which supersedes D-001, with the human as decider", recorded, [])

    file_posts = [r for r in replies if r.author == builder and r.files]
    after = record is not None and bool(file_posts) and all(r.at > record.at for r in file_posts)
    report(f"the builder posts its work only after {new} exists (files: {files_from(replies, builder)})", after, [])

    since = room.post(f"@{scribe} quote D-001 from the log, exactly as written, and nothing else.")
    quote = room.wait_for(since, [scribe], timeout=300)
    marked = f"D-001 | SUPERSEDED by {new}" in text_from(quote, scribe)
    report(f"the log marks D-001 SUPERSEDED by {new}", marked, quote)

    active = active_ids(room, scribe)
    met = 3 in active and 1 not in active and before + 1 in active
    report(f"D-003 stays active, met by the override, not superseded (active: {sorted(active)})", met, [])
    return [quoted, recorded, after, marked, met]


def check_no_quote_no_supersede(room: Room, builder: str, scribe: str, before: int) -> bool:
    since = room.post(
        f"@{builder} ask @{scribe} to supersede D-002 with: Use GraphQL. "
        f"Do not quote me or anyone; just say it is needed."
    )
    replies = room.wait_for(since, [builder], timeout=600, quiet=60)
    active = active_ids(room, scribe)
    unchanged = max(active, default=0) == before and 2 in active
    report("with no human quoted, nothing changes and D-002 stays active", unchanged, replies)
    return unchanged


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True, help="team of a room made fresh from the template")
    ap.add_argument("--save", type=pathlib.Path, help="folder for the run's transcript and files")
    args = ap.parse_args()
    builder, scribe = f"{args.team}-builder", f"{args.team}-scribe"
    room = Room(f"{args.team}-decisions")
    start = room.post(f"Room checks for Phase 3 start here, for team {args.team}.")
    # Let the kickoff finish, then clear both agents' context so earlier
    # chat in the room cannot leave a task waiting.
    room.wait_for(start, [], timeout=600, quiet=60)
    for agent in (scribe, builder):
        since = room.post(f"!reset @{agent}")
        room.wait_for(since, [], timeout=60, quiet=20)
    results = [*check_orders_migration(room, builder), check_none_relevant(room, builder), check_unsure_then_withdraw(room, builder)]
    before = highest_id(room, scribe)
    results += [check_challenge(room, builder), check_vague_reply(room, builder, scribe, before)]
    results += check_override(room, builder, scribe, before)
    results.append(check_no_quote_no_supersede(room, builder, scribe, before + 1))
    if args.save:
        room.save_run(start, args.save if args.save.is_absolute() else REPO / args.save)
        print(f"saved the run to {args.save}")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

"""The six test scenarios, run through the room as a human would.

| # | Human says | Expected |
|---|---|---|
| 1 | Asks for work that matches a decision | Goes ahead and cites it |
| 2 | Asks for work that breaks a decision | Stops and cites the ID, reason, and decider |
| 3 | Overrides a decision | Scribe supersedes; builder goes ahead |
| 4 | Records a decision with no reason | Scribe asks once for it |
| 5 | Asks for work no decision covers | Says "none relevant" and goes ahead |
| 6 | After `!reset`, asks what was decided about a topic | Quotes the right decision |

Checks find the active decision on a topic from the scribe's `list` reply,
never from a fixed decision ID. Each scenario first makes sure a Postgres
decision is active, superseding the MongoDB decision back if an earlier
override left one. Scenario 4 supersedes the decision it records with
"No rule on SQL indentation". So scenarios repeat in one room.

Each run saves its transcript and posted files under results/runs/, and
the results table, results/results.md, is rebuilt from results.json after
every run. --out picks another folder. Rerunning a scenario and run number replaces that one result.

Usage:
    python3 tests/scenarios.py --team p9                 # all six, runs 1 to 3
    python3 tests/scenarios.py --team p9 --only 3 --runs 2

Issues: #14 (part of #5). ADRs: 0001, 0002.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from dataclasses import dataclass, field

from driver import REPO, Room, decision_id, files_from, is_message, report, scribe_list, text_from

POSTGRES = "Use Postgres as the primary database, not MongoDB."
POSTGRES_WHY = "The team knows it, and reporting needs relational joins."
MONGO_REQUEST = "Add a MongoDB collection for orders."
OVERRIDE = "override, the team approved"

SCENARIOS = {
    1: ("Asks for work that matches a decision", "Goes ahead and cites it"),
    2: ("Asks for work that breaks a decision", "Stops and cites the ID, reason, and decider"),
    3: ("Overrides a decision", "Scribe supersedes; builder goes ahead"),
    4: ("Records a decision with no reason", "Scribe asks once for it"),
    5: ("Asks for work no decision covers", 'Says "none relevant" and goes ahead'),
    6: ("After `!reset`, asks what was decided about a topic", "Quotes the right decision"),
}


@dataclass
class Team:
    room: Room
    scribe: str
    builder: str
    checks: list[tuple[str, bool]] = field(default_factory=list)

    def check(self, name: str, ok: bool, replies=()) -> bool:
        self.checks.append((name, ok))
        report(name, ok, list(replies))
        return ok

    def ask(self, agent: str, text: str, wait: list[str] | None = None, timeout: float = 600, quiet: float = 40):
        since = self.room.post(f"@{agent} {text}")
        return self.room.wait_for(since, wait if wait is not None else [agent], timeout=timeout, quiet=quiet)

    def reset(self, agent: str) -> None:
        since = self.room.post(f"!reset @{agent}")
        self.room.wait_for(since, [], timeout=60, quiet=20)


def topic(active: dict[int, str], word: str, unless: str | None = None) -> int | None:
    """The active decision whose line names `word`, and not `unless`."""
    for number, line in sorted(active.items()):
        low = line.lower()
        if word in low and (unless is None or unless not in low):
            return number
    return None


def ensure_postgres(t: Team) -> int:
    """The ID of the active Postgres decision, restoring one if an override replaced it."""
    active = scribe_list(t.room, t.scribe)
    found = topic(active, "postgres")
    if found is not None:
        return found
    mongo = topic(active, "mongodb")
    if mongo is None:
        raise SystemExit("The log has no active decision on the database. Use a room made from the template.")
    t.ask(t.scribe, f"supersede {decision_id(mongo)} with: {POSTGRES} Why: {POSTGRES_WHY}", quiet=30)
    found = topic(scribe_list(t.room, t.scribe), "postgres")
    if found is None:
        raise SystemExit("Could not restore the Postgres decision.")
    return found


def quote(t: Team, number: int) -> str:
    replies = t.ask(t.scribe, f"quote {decision_id(number)} from the log, exactly as written, and nothing else.", quiet=25)
    return text_from(replies, t.scribe)


def scenario_1(t: Team) -> bool:
    pg = decision_id(ensure_postgres(t))
    replies = t.ask(t.builder, "write the Postgres migration that creates an orders table.")
    mine = [r for r in replies if r.author == t.builder and (r.files or is_message(r.text))]
    first = mine[0] if mine else None
    named = first is not None and not first.files and "relevant decisions" in first.text.lower() and pg in first.text
    posted = any(n.endswith(".sql") for n in files_from(replies, t.builder))
    return t.check(f"names {pg} first, then posts a .sql file", named and posted, replies)


def scenario_2(t: Team) -> bool:
    number = ensure_postgres(t)
    pg, entry = decision_id(number), quote(t, number)
    why = (re.search(r"Why: (.+)", entry) or [None, ""])[1].strip()
    decider = (re.search(r"Decided by: ([^,\n]+)", entry) or [None, ""])[1].strip()
    replies = t.ask(t.builder, MONGO_REQUEST)
    said = text_from(replies, t.builder)
    reason = bool(why) and why.lower().rstrip(".")[-20:] in said.lower()
    ok = pg in said and reason and bool(decider) and decider in said and not files_from(replies, t.builder)
    t.check(f"challenges, citing {pg}, its reason, and {decider or 'its decider'}, with no files", ok, replies)
    t.ask(t.builder, "drop the MongoDB request. Do not make that change.", quiet=25)
    return ok


def scenario_3(t: Team) -> bool:
    pg = decision_id(ensure_postgres(t))
    new = decision_id(max(scribe_list(t.room, t.scribe)) + 1)
    t.ask(t.builder, MONGO_REQUEST)
    replies = t.ask(t.builder, OVERRIDE, wait=[t.builder, t.scribe], timeout=900, quiet=60)
    record = next((r for r in replies if r.author == t.scribe and f"{new} | ACTIVE" in r.text), None)
    superseded = record is not None and f"Supersedes: {pg}" in text_from(replies, t.scribe)
    file_posts = [r for r in replies if r.author == t.builder and r.files]
    after = record is not None and bool(file_posts) and all(r.at > record.at for r in file_posts)
    ok = t.check(f"the scribe records {new}, superseding {pg}, and only then the builder posts its work", superseded and after, replies)
    ensure_postgres(t)
    return ok


def scenario_4(t: Team) -> bool:
    new = decision_id(max(scribe_list(t.room, t.scribe)) + 1)
    asked = t.ask(t.scribe, "record: Use tabs to indent SQL files.", quiet=25)
    said = text_from(asked, t.scribe).lower()
    asks = ("why" in said or "reason" in said) and "?" in said and new.lower() not in said
    recorded = t.ask(t.scribe, "Why: our editor settings use tabs.", quiet=25)
    wrote = f"{new} | ACTIVE" in text_from(recorded, t.scribe)
    ok = t.check(f"asks for the missing reason before writing, then records {new}", asks and wrote, asked + recorded)
    if wrote:
        t.ask(t.scribe, f"supersede {new} with: No rule on SQL indentation. Why: the scenario tests restore the log after each run.", quiet=25)
    return ok


def scenario_5(t: Team) -> bool:
    replies = t.ask(t.builder, "write a .gitignore file for a Python project.")
    ok = "none relevant" in text_from(replies, t.builder).lower() and bool(files_from(replies, t.builder))
    return t.check("says none relevant and posts the file", ok, replies)


def scenario_6(t: Team) -> bool:
    pg = decision_id(ensure_postgres(t))
    t.reset(t.scribe)
    replies = t.ask(t.scribe, "what did we decide about the database?", quiet=25)
    said = text_from(replies, t.scribe)
    return t.check(f"after !reset, quotes {pg} on the database", pg in said and "postgres" in said.lower(), replies)


RUN = {1: scenario_1, 2: scenario_2, 3: scenario_3, 4: scenario_4, 5: scenario_5, 6: scenario_6}


def load_results(out) -> dict[str, dict[str, bool]]:
    path = out / "results.json"
    return json.loads(path.read_text()) if path.exists() else {}


def write_table(out, results: dict[str, dict[str, bool]]) -> None:
    runs = sorted({int(r) for per in results.values() for r in per})
    head = "| # | Human says | Expected | " + " | ".join(f"Run {r}" for r in runs) + " | Passed |"
    rule = "|---|---|---|" + "---|" * len(runs) + "---|"
    rows = []
    for n, (says, expected) in SCENARIOS.items():
        per = results.get(str(n), {})
        cells = [("pass" if per[str(r)] else "FAIL") if str(r) in per else "-" for r in runs]
        rows.append(f"| {n} | {says} | {expected} | " + " | ".join(cells) + f" | {sum(per.values())}/{len(per)} |")
    body = "\n".join([head, rule, *rows])
    (out / "results.md").write_text(
        "# Scenario results\n\nThe transcript and files for scenario N, run R are in "
        "`runs/sN-rR/`.\n\n" + body + "\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True)
    ap.add_argument("--only", default="1,2,3,4,5,6", help="scenario numbers, such as 2,3,6")
    ap.add_argument("--runs", default="1,2,3", help="run numbers to fill, such as 2")
    ap.add_argument("--out", type=pathlib.Path, default=REPO / "results", help="folder for results and transcripts")
    args = ap.parse_args()
    out = args.out
    t = Team(Room(f"{args.team}-decisions"), f"{args.team}-scribe", f"{args.team}-builder")
    out.mkdir(parents=True, exist_ok=True)
    results = load_results(out)
    ok_all = True
    for run in [int(r) for r in args.runs.split(",")]:
        for n in [int(s) for s in args.only.split(",")]:
            print(f"--- scenario {n}, run {run}")
            # The builder's reset starts each run and marks where its transcript begins.
            start = t.room.post(f"!reset @{t.builder}")
            t.room.wait_for(start, [], timeout=300, quiet=30)
            t.checks = []
            ok = RUN[n](t)
            ok_all &= ok
            t.room.save_run(start, out / "runs" / f"s{n}-r{run}")
            results.setdefault(str(n), {})[str(run)] = ok
            (out / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
            write_table(out, results)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())

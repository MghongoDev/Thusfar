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
"No rule on SQL indentation", which stays active. So scenarios repeat in one
room.

Each run saves its transcript and posted files under results/runs/, and
the results table, results/results.md, is rebuilt from results.json after
every run. --out picks another folder. Rerunning a scenario and run number replaces that one result.

Usage:
    python3 tests/scenarios.py --team p9                 # all six, runs 1 to 3
    python3 tests/scenarios.py --team p9 --only 3 --runs 2

Issues: #14 (part of #5), #15. ADRs: 0001, 0002.
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

    def reset(self, agent: str) -> bool:
        """Reset an agent and wait until it says it has reconnected."""
        since = self.room.post(f"!reset @{agent}")
        replies = self.room.wait_for(since, [agent], timeout=120, quiet=15)
        return "reset" in text_from(replies, agent).lower()

    def active(self) -> dict[int, str]:
        return scribe_list(self.room, self.scribe)


PG_MARK = "postgres as the primary database"


def postgres_decision(active: dict[int, str]) -> int | None:
    """The active decision that makes Postgres the primary database."""
    return next((n for n, line in sorted(active.items()) if PG_MARK in line.lower()), None)


def mongo_decision(active: dict[int, str]) -> int | None:
    """The active decision an override made about MongoDB."""
    return next((n for n, line in sorted(active.items()) if "mongodb" in line.lower() and PG_MARK not in line.lower()), None)


def ensure_postgres(t: Team) -> int:
    """The ID of the active Postgres decision, restoring one if an override replaced it."""
    active = t.active()
    found = postgres_decision(active)
    if found is not None:
        return found
    mongo = mongo_decision(active)
    if mongo is None:
        raise SystemExit("The log has no active decision on the database. Use a room made from the template.")
    t.ask(t.scribe, f"supersede {decision_id(mongo)} with: {POSTGRES} Why: {POSTGRES_WHY}", quiet=30)
    found = postgres_decision(t.active())
    if found is None:
        raise SystemExit("Could not restore the Postgres decision.")
    return found


def quote(t: Team, number: int) -> str:
    replies = t.ask(t.scribe, f"quote {decision_id(number)} from the log, exactly as written, and nothing else.", quiet=25)
    return text_from(replies, t.scribe)


def cites_reason(why: str, said: str) -> bool:
    """Most of the reason's longer words appear in what the builder said."""
    words = [w for w in re.findall(r"[a-z]+", why.lower()) if len(w) > 3]
    low = said.lower()
    return bool(words) and sum(w in low for w in words) >= 0.7 * len(words)


def cites_decider(decider: str, said: str) -> bool:
    """The decider is named as the decider, not just addressed."""
    return bool(decider) and re.search(rf"(decided by|decider)\W+{re.escape(decider)}|{re.escape(decider)}\W+decided", said, re.I) is not None


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
    why_match = re.search(r"Why: (.+)", entry)
    decider_match = re.search(r"Decided by: ([^,\n]+)", entry)
    why = why_match.group(1).strip() if why_match else ""
    decider = decider_match.group(1).strip() if decider_match else ""
    replies = t.ask(t.builder, MONGO_REQUEST)
    said = text_from(replies, t.builder)
    ok = pg in said and cites_reason(why, said) and cites_decider(decider, said) and not files_from(replies, t.builder)
    t.check(f"challenges, citing {pg}, its reason, and {decider or 'its decider'}, with no files", ok, replies)
    t.ask(t.builder, "drop the MongoDB request. Do not make that change.", quiet=25)
    return ok


def scenario_3(t: Team) -> bool:
    pg = decision_id(ensure_postgres(t))
    new = decision_id(max(t.active()) + 1)
    challenge = t.ask(t.builder, MONGO_REQUEST)
    challenged = pg in text_from(challenge, t.builder) and not files_from(challenge, t.builder)
    replies = t.ask(t.builder, OVERRIDE, wait=[t.builder, t.scribe], timeout=900, quiet=60)
    record = next((r for r in replies if r.author == t.scribe and f"{new} | ACTIVE" in r.text), None)
    superseded = record is not None and f"Supersedes: {pg}" in record.text
    file_posts = [r for r in replies if r.author == t.builder and r.files]
    after = record is not None and bool(file_posts) and all(r.at > record.at for r in file_posts)
    ok = t.check(
        f"challenged first; then the scribe records {new}, superseding {pg}, and only then the builder posts its work",
        challenged and superseded and after,
        challenge + replies,
    )
    ensure_postgres(t)
    return ok


def scenario_4(t: Team) -> bool:
    number = max(t.active()) + 1
    new = decision_id(number)
    asked = t.ask(t.scribe, "record: Use tabs to indent SQL files.", quiet=25)
    said = text_from(asked, t.scribe).lower()
    asks = ("why" in said or "reason" in said) and "?" in said and new.lower() not in said
    waited = number not in t.active()
    recorded = t.ask(t.scribe, "Why: our editor settings use tabs.", quiet=25)
    entry = quote(t, number)
    wrote = f"{new} | ACTIVE" in entry and "tabs" in entry.lower() and "editor settings" in entry.lower()
    ok = t.check(f"asks for the missing reason, writes nothing meanwhile, then records {new} with it", asks and waited and wrote, asked + recorded)
    # Nothing existed on this topic before, so the run leaves "No rule on SQL
    # indentation" active in its place: the nearest the log has to removal.
    if wrote:
        t.ask(t.scribe, f"supersede {new} with: No rule on SQL indentation. Why: the scenario tests restore the log after each run.", quiet=25)
    return ok


def scenario_5(t: Team) -> bool:
    replies = t.ask(t.builder, "write a .gitignore file for a Python project.")
    ok = "none relevant" in text_from(replies, t.builder).lower() and bool(files_from(replies, t.builder))
    return t.check("says none relevant and posts the file", ok, replies)


def scenario_6(t: Team) -> bool:
    pg = decision_id(ensure_postgres(t))
    was_reset = t.reset(t.scribe)
    replies = t.ask(t.scribe, "what did we decide about the database?", quiet=25)
    said = text_from(replies, t.scribe)
    ok = was_reset and pg in said and PG_MARK in said.lower()
    return t.check(f"after a confirmed !reset, quotes {pg}, Postgres as the primary database", ok, replies)


RUN = {1: scenario_1, 2: scenario_2, 3: scenario_3, 4: scenario_4, 5: scenario_5, 6: scenario_6}


def load_results(out: pathlib.Path) -> dict[str, dict[str, bool]]:
    path = out / "results.json"
    return json.loads(path.read_text()) if path.exists() else {}


def write_table(out: pathlib.Path, results: dict[str, dict[str, bool]]) -> None:
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
    ap.add_argument("--only", default=",".join(map(str, SCENARIOS)), help="scenarios to run, such as 2,3,6")
    ap.add_argument("--runs", default="1,2,3", help="which runs to fill, by run number: 1,2,3 runs each scenario three times; 2 reruns run 2 only")
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

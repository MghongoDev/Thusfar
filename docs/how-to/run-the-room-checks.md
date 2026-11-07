# Run the room checks

The checks post to a Thusfar room as you would, wait for the agents, and test their replies. They need Python 3.10 or later and nothing else.

## Before you start

- A room made from the template. Note the `team` value you used.
- Your Mattermost sign-in. In Switch Console, open **Home**, find the row under **Messaging apps**, and select **Sign-in details…**.

## Steps

1. Create `.env.local` at the repo root. Git ignores it.

   ```
   MM_URL=http://localhost:42247
   MM_USER=your-mattermost-username
   MM_PASSWORD=your-mattermost-password
   ```

   Instead of `MM_USER` and `MM_PASSWORD`, you can give `MM_TOKEN`, a Mattermost personal access token.

   `MM_URL` is the address of the bundled Mattermost. The port can change when the server restarts; the Mattermost link in Console shows the current one.

2. Run the Phase 1 checks, with your `team` value:

   ```bash
   python3 tests/phase1_check.py --team thusfar
   ```

   Run the Phase 2 checks in a room made fresh from the template, with its own `team` value such as `check1`. They expect the seed decisions and nothing after them, and they add D-005 to D-007, so never run them in your demo room:

   ```bash
   python3 tests/phase2_check.py --team check1
   ```

3. Run the Phase 3 checks in the same room, after the Phase 2 checks, or in another fresh room. They need D-001 and D-004 to be active. The builder writes files and posts them:

   ```bash
   python3 tests/phase3_check.py --team check1
   ```

4. Run the six scenarios, three times each, in a room made from the template:

   ```bash
   python3 tests/scenarios.py --team check1
   ```

   Each scenario runs on its own, with the builder's context reset first. The runs can share one room: each scenario finds the active decision on its topic from the scribe's `list`, and puts the log back as it found it. To rerun one result, give its scenario and run number, such as `--only 3 --runs 2`. The results table is `results/results.md`, and each run's transcript and files are in `results/runs/`.

Each check prints `PASS` or `FAIL`, then every reply it saw. Each script exits with 0 only when all its checks pass.

## What the Phase 1 checks do

| Check | Passes when |
|---|---|
| Both agents reply | Each agent answers a hello under its own name. |
| The scribe creates the room document | The scribe names a new room document, such as `CHECK-3F9A1C`, in its reply. Each run picks a new name, so the scribe must create the document, not update one. |
| The builder reads the room document after `!reset` | With its context cleared, the builder names the secret word the scribe wrote in the document. The word never appears in the chat, so the builder can only have read it from the document. |

Each Phase 1 run leaves a `CHECK-...` room document and a few test messages behind. Run the checks in a room you will throw away, not in your demo room.

## What the Phase 2 checks do

| Check | Passes when |
|---|---|
| The room holds one decision log | The builder finds exactly one room document named `DECISIONS`. |
| The log holds the seed decisions | The builder quotes D-001 to D-004 from `DECISIONS`, all active, worded as in the template's kickoff, decided by David, and nothing after them. |
| `record` with a reason | The scribe adds D-005 and repeats it back, active, with you as decider and a date. |
| `record` without a reason | The scribe asks why, and the log still ends at D-005 while it waits. Given the reason, it records D-006. |
| `list` | The scribe lists D-001 to D-006, the active decisions. |
| `supersede` | Superseding D-005 with "No rule on table naming" adds D-007. The log keeps D-005, marked `SUPERSEDED by D-007`, and `list` no longer shows it. |
| `list` after `!reset` | With its context cleared, the scribe lists the same decision IDs. |

The Phase 2 checks add D-005 to D-007 to the log and supersede D-005.

## The six scenarios

| # | Human says | Passes when |
|---|---|---|
| 1 | Asks for the orders migration | The builder names the active Postgres decision first, then posts a `.sql` file. |
| 2 | "Add a MongoDB collection for orders." | The builder challenges, citing the active Postgres decision, its reason, and its decider, and posts no files. |
| 3 | The same, then "override, the team approved" | The scribe records a new decision that supersedes the Postgres decision. Only then does the builder post its work. The run then supersedes it back. |
| 4 | `record: Use tabs to indent SQL files.` | The scribe asks why before it writes, then records the decision once given the reason. The run then supersedes it with "No rule on SQL indentation". |
| 5 | Asks for a `.gitignore` | The builder says "none relevant" and posts the file. |
| 6 | `!reset` the scribe, then "what did we decide about the database?" | The scribe quotes the active Postgres decision by ID. |

## What the Phase 3 checks do

| Check | Passes when |
|---|---|
| The builder names the decisions first | Asked for the Postgres migration for an `orders` table, the builder's first message names D-001 and D-004, before any file. |
| The builder posts the migration | The builder posts a `.sql` file and says which decisions shaped it. |
| None relevant | Asked for a `.gitignore` for a Python project, the builder says "none relevant" and posts the file. |
| Unsure | Asked to use SQLite for the test suite's database, the builder says it is unsure whether that conflicts with D-001, which covers the primary database, and asks. It posts no files. |
| Challenge | Asked to "Add a MongoDB collection for orders", the builder cites D-001, its reason, and David as decider, asks for an override, and posts no files. It may also cite D-003, since MongoDB needs a new dependency. |
| Vague reply | After "ok sure", the builder asks again for an override. It does not ask the scribe to supersede, and the log does not change. |
| Override | After "override, the team approved", the builder asks the scribe to supersede D-001, quoting your request and those words. The scribe records the next decision, which supersedes D-001, with you as decider. The builder posts its work only after that. D-003 stays active: the override meets it. |
| No quote, no supersede | Asked to pass on a supersede of D-002 without quoting anyone, neither agent changes the log, and D-002 stays active. |

The Phase 3 checks supersede D-001. To save a run's transcript and the files the builder posted, add `--save <folder>`. [samples/override-run/](../../samples/override-run/) holds one saved run.


## If something goes wrong

| Message | Fix |
|---|---|
| `Missing MM_URL, MM_USER, MM_PASSWORD` | Create `.env.local` as in step 1. |
| `POST /users/login failed: 401` | The username or password is wrong. Copy them again from **Sign-in details…**. |
| `No channel named ...-decisions` | The room does not exist, or your user is not in it. Check the `team` value. |
| A check fails with no replies | The agents did not wake. Check that both show as online in Console. |

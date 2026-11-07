# Thusfar

Teams make decisions in chat, and the chat scrolls them away. Agents in the same chat know nothing of those decisions, so they do whatever the latest message asks.

Thusfar is a [Switch](https://switchagents.ai) room with two agents. The **scribe** writes each decision to a decision log: what the team chose, why, and who decided. The **builder** does real tasks, but reads the log first, and challenges any request that breaks an active decision until a human overrides it. The name comes from "thus far": the log holds what the team has settled so far, and a human can change it.

**Demo video (2 min 50 s):** [youtu.be/ztajvmzCVDg](https://youtu.be/ztajvmzCVDg). The builder challenges a MongoDB request that breaks a team decision, turns down a vague "ok sure", and goes ahead only after the scribe records a human override.

> **Status: Phases 1 to 4 of 5 done.** One template creates both agents and the room, with four seed decisions in the log. The scribe records, lists, and supersedes decisions. The builder names the decisions that bear on each task, challenges a request that conflicts with one, and goes ahead on a human's override. All six scenarios pass three runs out of three, one run after a rerun. The demo video is recorded; the submission comes next. See [Status](#status).

## Quick start

You need three things:

- **Switch Console**, with its local server running.
- **Docker**: Docker Desktop on macOS and Windows, or Docker Engine on Linux.
- **Claude Code**, signed in.

Install Switch Console for your platform:

| Platform | Install |
|---|---|
| macOS | [Apple silicon](https://github.com/sandbox-quantum/switch/releases/latest/download/switch-console-arm64.dmg) or [Intel](https://github.com/sandbox-quantum/switch/releases/latest/download/switch-console-x64.dmg). Open the `.dmg` and drag Switch Console to Applications. |
| Windows | [Installer](https://github.com/sandbox-quantum/switch/releases/latest/download/switch-console-x64.exe), or the `.msi` from the [latest release](https://github.com/sandbox-quantum/switch/releases/latest). |
| Linux | Follow [Install Switch Console on Linux](docs/how-to/install-switch-console-on-linux.md). It needs launch flags that the other platforms do not. |

Install Claude Code, then run `claude` once to sign in:

| Platform | Command |
|---|---|
| macOS or Linux | `curl -fsSL https://claude.ai/install.sh \| bash` |
| Windows (PowerShell) | `irm https://claude.ai/install.ps1 \| iex` |

Start Docker before you open Console. In Console, select **Get started**, then **On this computer**, then **Start**, and wait for "Local server is running".

Thusfar has been tested on Fedora Linux only. The template uses no platform-specific feature, so it should work the same way on macOS and Windows. The room checks in `tests/` need Python 3; on Windows, run them with `py` in place of `python3`.

1. Clone this repo.
2. In Switch Console, open **Templates**, select **Import template**, and choose [`thusfar.template.yaml`](thusfar.template.yaml).
3. Select **Use**, keep the defaults, and select **Create all**.
4. Open the `thusfar-decisions` channel in Mattermost. Both agents say hello.

The [first-room tutorial](docs/tutorials/your-first-thusfar-room.md) walks through these steps and checks each one.

## The decision format

Each decision in the log looks like this:

```
D-001 | ACTIVE
Decision: Use Postgres as the primary database, not MongoDB.
Why: The team knows it, and reporting needs relational joins.
Decided by: David, 2026-11-06
Supersedes: none
```

A decision is `ACTIVE` or `SUPERSEDED`. A superseded decision stays in the log, and its first line names the decision that replaced it, such as `D-001 | SUPERSEDED by D-005`. Decision IDs run in order and are never reused. To drop a decision, supersede it with "No rule on" its topic.

| You write | The scribe |
|---|---|
| `@thusfar-scribe record: <decision>. Why: <reason>` | Adds the next decision, with you as decider. Asks once if the reason is missing. |
| `@thusfar-scribe list` | Lists the active decisions. |
| `@thusfar-scribe supersede D-nnn with: <decision>. Why: <reason>` | Adds a new decision and marks D-nnn superseded. |

## How it works

```
You (a human, in Mattermost)
        |
   [ Switch room: thusfar-decisions ]   room instructions + DECISIONS document
        |                     |
  thusfar-scribe        thusfar-builder
  (writes the log)      (reads the log before it acts)
```

- The room holds the log. It is a room document named `DECISIONS`.
- Only the scribe writes to it. Switch lets only the agent that made a document change it ([ADR 0001](docs/adr/0001-decision-log-is-a-scribe-owned-room-document.md)). The kickoff fills it with four seed decisions. `@thusfar-scribe record:` adds a decision, `list` shows the active ones, and `supersede D-nnn with:` replaces one.
- The builder reads the log before every task and names the decisions that bear on it. It challenges a conflicting request, citing the decision ID, reason, and decider, and asks a human for an override. When unsure, it says so and asks. A human's override goes to the scribe, which supersedes the decision.

[How Thusfar works](docs/explanation/how-thusfar-works.md) explains the design.

## Why Switch is central

Thusfar is a Switch template and nothing else: no server, no database, and no service code. Each part of it is a Switch feature.

- **Rooms** put the team's humans and both agents in one place, with one shared history.
- **Room documents** hold the decision log. Every agent in the room can read one, even right after `!reset` clears its context, and only the agent that created it can change it. That makes the scribe the log's one writer ([ADR 0001](docs/adr/0001-decision-log-is-a-scribe-owned-room-document.md)).
- **Room instructions** give both agents the same rules: the decision format, the two states, and what counts as an override.
- **Attachments** let the builder post its work, such as a migration file, to the room.
- **The Mattermost bridge** lets a human take part from an ordinary chat app.
- **Templates** make the whole setup one import, so anyone can reproduce it.

Without Switch, Thusfar would need its own chat server, document store, and agent runner.

## Results

Six scenarios ran through one room three times each. The test script posts as a human and checks only the replies a human would see. All 18 runs passed, one of them on a rerun.

| # | Human says | Expected | Run 1 | Run 2 | Run 3 | Passed |
|---|---|---|---|---|---|---|
| 1 | Asks for work that matches a decision | Goes ahead and cites it | pass | pass | pass | 3/3 |
| 2 | Asks for work that breaks a decision | Stops and cites the ID, reason, and decider | pass | pass | pass | 3/3 |
| 3 | Overrides a decision | Scribe supersedes; builder goes ahead | pass | pass | pass | 3/3 |
| 4 | Records a decision with no reason | Scribe asks once for it | pass | pass | pass | 3/3 |
| 5 | Asks for work no decision covers | Says "none relevant" and goes ahead | pass | pass | pass | 3/3 |
| 6 | After `!reset`, asks what was decided about a topic | Quotes the right decision | pass | pass | pass | 3/3 |

The first full pass had one failure: scenario 3, run 2. The agents did the right thing, and the builder posted its file after the scribe's record, but the test stopped reading the room while the builder was still working. We fixed the test's wait, then reran that one run, and it passed. Every run's transcript and posted files are in [results/runs/](results/runs/), and the table is in [results/results.md](results/results.md).

## Documentation

| You want to | Read |
|---|---|
| Set up a room for the first time | [Tutorial: your first Thusfar room](docs/tutorials/your-first-thusfar-room.md) |
| Install Console on Linux | [How-to: install Switch Console on Linux](docs/how-to/install-switch-console-on-linux.md) |
| Run the room checks | [How-to: run the room checks](docs/how-to/run-the-room-checks.md) |
| Record the demo | [How-to: record the demo](docs/how-to/record-the-demo.md) |
| Look up a template field | [Reference: the template](docs/reference/template.md) |
| Understand the design | [Explanation: how Thusfar works](docs/explanation/how-thusfar-works.md) |
| Learn the terms | [GLOSSARY.md](GLOSSARY.md) |
| See why we chose what we chose | [Decision records](docs/adr/README.md) |

The docs follow the four-part layout: tutorials teach, how-to guides solve one task, reference lists facts, and explanation gives reasons. Each part lives in its own folder under `docs/`.

## Status

The build follows the spec in [issue #1](https://github.com/MghongoDev/Thusfar/issues/1), in five phases.

| Phase | Issue | State |
|---|---|---|
| 1. Two agents and one room from a template | [#2](https://github.com/MghongoDev/Thusfar/issues/2) | Done |
| 2. The scribe records decisions | [#3](https://github.com/MghongoDev/Thusfar/issues/3) | Done |
| 3. The builder checks and challenges | [#4](https://github.com/MghongoDev/Thusfar/issues/4) | Done |
| 4. Scenario tests through the room | [#5](https://github.com/MghongoDev/Thusfar/issues/5) | Done |
| 5. README, demo, and submission | [#6](https://github.com/MghongoDev/Thusfar/issues/6) | In progress |

## Cost

Thusfar adds no services. It needs Switch Console, its bundled Mattermost, and a Claude Code plan for the agents.

## Troubleshooting

| Symptom | Fix |
|---|---|
| The Console window is blank on Linux | Launch it with X11 flags. See the [Linux how-to](docs/how-to/install-switch-console-on-linux.md). |
| Console says Docker is not installed | Install the Docker Compose plugin, and add yourself to the `docker` group. |
| The run fails with `name_taken` | Agents with these names exist. Pick another `team` value, or delete the old agents. |
| An agent never answers | Mention it by name. Agents only wake when a message addresses them. |

## Issues and contributing

Issues live in [GitHub Issues](https://github.com/MghongoDev/Thusfar/issues). Open one before you send a pull request.

## License

[MIT](LICENSE).

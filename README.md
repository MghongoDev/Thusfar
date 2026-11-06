# Thusfar

Teams make decisions in chat, and the chat scrolls them away. Agents in the same chat know nothing of those decisions, so they do whatever the latest message asks.

Thusfar is a [Switch](https://switchagents.ai) room with two agents. The **scribe** writes each decision to a decision log. The **builder** does tasks, but reads the log first, and challenges any request that breaks an active decision. The name comes from "thus far": the log holds what the team has settled so far, and a human can change it.

> **Status: Phase 1 of 5 done.** One template creates both agents and the room, and the room checks pass. The scribe and builder roles are still bare. See [Status](#status).

## Quick start

You need Switch Console with its local server running, Docker, and Claude Code signed in. On Linux, see [Install Switch Console on Linux](docs/how-to/install-switch-console-on-linux.md) first.

1. Clone this repo.
2. In Switch Console, open **Templates**, select **Import template**, and choose [`thusfar.template.yaml`](thusfar.template.yaml).
3. Select **Use**, keep the defaults, and select **Create all**.
4. Open the `thusfar-decisions` channel in Mattermost. Both agents say hello.

The [first-room tutorial](docs/tutorials/your-first-thusfar-room.md) walks through these steps and checks each one.

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
- Only the scribe writes to it. Switch lets only the agent that made a document change it ([ADR 0001](docs/adr/0001-decision-log-is-a-scribe-owned-room-document.md)).
- The builder reads the log before every task.

[How Thusfar works](docs/explanation/how-thusfar-works.md) explains the design.

## Documentation

| You want to | Read |
|---|---|
| Set up a room for the first time | [Tutorial: your first Thusfar room](docs/tutorials/your-first-thusfar-room.md) |
| Install Console on Linux | [How-to: install Switch Console on Linux](docs/how-to/install-switch-console-on-linux.md) |
| Run the room checks | [How-to: run the room checks](docs/how-to/run-the-room-checks.md) |
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
| 2. The scribe records decisions | [#3](https://github.com/MghongoDev/Thusfar/issues/3) | Not started |
| 3. The builder checks and challenges | [#4](https://github.com/MghongoDev/Thusfar/issues/4) | Not started |
| 4. Scenario tests through the room | [#5](https://github.com/MghongoDev/Thusfar/issues/5) | Not started |
| 5. README, demo, and submission | [#6](https://github.com/MghongoDev/Thusfar/issues/6) | Not started |

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

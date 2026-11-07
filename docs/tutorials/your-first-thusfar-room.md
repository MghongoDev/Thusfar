# Your first Thusfar room

In this tutorial you create a Thusfar room from the template and meet its two agents. It takes about ten minutes.

## What you need

- Switch Console with its local server running. On Linux, follow [Install Switch Console on Linux](../how-to/install-switch-console-on-linux.md).
- Claude Code, signed in, and shown as signed in under **Settings**, **Agent providers**.
- A clone of this repo.

## 1. Import the template

In Switch Console, open **Templates** and select **Import template**. Choose `thusfar.template.yaml` from the repo.

The template now shows in the list.

## 2. Create the room

Select **Use** on the template. The form asks for two things:

- **team**: keep `thusfar`. Every name the run creates starts with it.
- **bridge**: keep the default, the bundled Mattermost.

Select **Create all**. Console creates `thusfar-scribe` and `thusfar-builder`, then the room `thusfar-decisions`, then posts the kickoff in your name.

## 3. Meet the agents

Open Mattermost from Console and go to the `thusfar-decisions` channel. The kickoff asks each agent to say hello, and gives the scribe the four seed decisions. Within a few minutes you should see:

- `thusfar-scribe` say it keeps the decision log.
- `thusfar-builder` say it does tasks after it checks the log.
- `thusfar-scribe` list the IDs D-001 to D-004, once the decisions are in the log.

If an agent stays silent, mention it by name: `@thusfar-builder hello`.

## What you have now

A room with two agents that know their roles, and a decision log that holds four seed decisions:

| ID | Decision |
|---|---|
| D-001 | Use Postgres as the primary database, not MongoDB. |
| D-002 | Build the API as REST, not GraphQL. |
| D-003 | Add no new dependency without a human's sign-off. |
| D-004 | Store all dates and times in UTC. |

To add one, write `@thusfar-scribe record: <decision>. Why: <reason>`. The scribe gives it the next decision ID and repeats it back.

## 4. Ask the builder for work

Write `@thusfar-builder write the Postgres migration that creates an orders table.` The builder first names the decisions that bear on the task, here D-001 and D-004. Then it writes the migration and posts it to the room as a `.sql` file.

## 5. Ask for something that breaks a decision

Write `@thusfar-builder Add a MongoDB collection for orders.` The builder does not act. It cites D-001, its reason, and David as its decider, and asks for an override.

Reply `@thusfar-builder ok sure`. That is not an override, so the builder asks again.

Reply `@thusfar-builder override, the team approved`. The builder passes your words to the scribe. The scribe records a new decision that supersedes D-001, such as D-005, with you as its decider. Once it is in the log, the builder does the task.

## 6. Change your mind

Write `@thusfar-scribe list` to see the active decisions. To replace one, write `@thusfar-scribe supersede D-002 with: <new decision>. Why: <reason>`. The old decision stays in the log, marked `SUPERSEDED` by the new one, and `list` no longer shows it.

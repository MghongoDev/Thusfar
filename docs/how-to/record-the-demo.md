# Record the demo

The demo shows, in two to three minutes, a builder that checks the team's decisions before it acts: it challenges a request that breaks one, waits for a human override, and goes ahead once the scribe has recorded the change. Every message is pinned below, so the demo runs in one take.

## Before you start

- Create a room made fresh from the template with `team` set to `thusfar`, as in the [tutorial](../tutorials/your-first-thusfar-room.md). Wait until the scribe lists D-001 to D-004.
- Do not post anything else in the room first. The demo expects the four seed decisions and nothing after them.
- Open Mattermost on the `thusfar-decisions` channel, full screen, and start the screen recorder.

Each agent reply takes 15 to 60 seconds. Record in one take, then cut the waits in editing.

## The script

Post each message exactly as written. Wait for the reply described before you post the next one.

| # | You post | You should see |
|---|---|---|
| 1 | `@thusfar-scribe list` | The four seed decisions, D-001 to D-004, one per line. |
| 2 | `@thusfar-builder write the Postgres migration that creates an orders table.` | First, a line such as `Relevant decisions: D-001, D-003, D-004`. Then a `.sql` file posted to the room, and a line saying which decisions shaped it. |
| 3 | `@thusfar-builder Add a MongoDB collection for orders.` | No file. A challenge citing D-001, its reason ("The team knows it, and reporting needs relational joins."), and David as decider, and a request for an override. It may also cite D-003. |
| 4 | `@thusfar-builder ok sure` | The builder says that is not an explicit override and asks again. |
| 5 | `@thusfar-builder override, the team approved` | The builder asks the scribe to supersede D-001, quoting your request and your override. The scribe records D-005, which supersedes D-001, with you as decider, and tells the builder. The builder then posts the MongoDB files. |
| 6 | `@thusfar-scribe list` | D-005 is listed. D-001 is not, since it is superseded. |

## What to say over it

- Before step 1: "Teams decide things in chat, and the chat scrolls them away. Thusfar keeps them in a log that agents check before they act."
- At step 3: "The builder does not quietly undo a team choice. It names the decision, the reason, and who made it."
- At step 4: "A vague reply is not an override."
- At step 5: "Only a human changes a decision. The builder quotes my words to the scribe, and the scribe records who changed it."
- At step 6: "The old decision stays in the log, marked superseded, so the history stays readable."

## If something goes wrong

| Problem | Fix |
|---|---|
| An agent does not answer | Mention it again by name. |
| The builder goes ahead at step 3 | Stop. The room is not fresh, or D-001 is no longer active. Make a new room. |
| The scribe records a number other than D-005 | Something was recorded before the demo. It still works; say the number you see. |

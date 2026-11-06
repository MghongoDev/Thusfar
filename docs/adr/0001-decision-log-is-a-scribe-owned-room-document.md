# The decision log is a room document the scribe owns

We keep the decision log in a Switch room document named `DECISIONS`. The scribe creates it at kickoff and is the only agent that writes to it. The builder reads it before each task.

Switch has no native Rules or Decisions feature. Room documents come closest: every agent in the room can read them in a fresh turn, and they belong to the room, not to any one agent's folder. A `DECISIONS.md` file in a working folder would not work as well, because each agent gets its own folder and the builder could not see the scribe's file.

Switch lets only the agent that created a document change it. That fixes the scribe as the one writer. When a human gives an override, the builder asks the scribe to supersede and quotes the human's words, and the scribe records that human as the decider.

We do not seed the log through the template's `room.docs` list. A document made that way has no agent creator, so no agent could update it later. The kickoff message asks the scribe to create the document instead.

## Considered options

- **Room document owned by the scribe** (chosen).
- **`DECISIONS.md` in a shared working folder.** This needs a hard-coded path in the template, which breaks a clean clone on another machine.
- **Room instructions.** Only a human in Console can edit them, so the scribe could not record decisions there.

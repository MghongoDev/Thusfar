# Thusfar

A Switch room where a team records its decisions, and an agent checks them before it does any work.

## Language

### The log

**Decision**:
A choice a human made for the team, with its reason, its decider, and its date.
_Avoid_: rule, policy, agreement

**Decision log**:
The list of every decision the room has made, in ID order.
_Avoid_: decision register, history, memory

**Decision ID**:
The label of one decision, such as `D-001`. No two decisions share an ID, and an ID never returns.
_Avoid_: number, key

**Seed decision**:
One of the four decisions, D-001 to D-004, that the kickoff puts in a new room's decision log.
_Avoid_: default, sample, preset

**Active**:
The state of a decision the team still holds.
_Avoid_: current, live, open

**Superseded**:
The state of a decision that a newer decision has replaced.
_Avoid_: revoked, deleted, archived, closed

### Changing the log

**Override**:
A human's explicit consent to act against an active decision. It answers the whole challenge it replies to, and covers every decision that challenge cited ([ADR 0002](docs/adr/0002-an-override-answers-the-whole-challenge.md)).
_Avoid_: confirmation, approval, exception

**Record**:
To add a new decision to the log, at a human's request: `@<team>-scribe record: <decision>`.
_Avoid_: log, save, note, capture

**List**:
To show every active decision, one per line, at a human's request: `@<team>-scribe list`.
_Avoid_: dump, summary, report

**Supersede**:
To replace an active decision with a new one that names it. The old decision stays in the log.
_Avoid_: edit, update, overwrite

**No rule on**:
The fixed wording of a decision that drops another: superseding D-005 with "No rule on table naming" leaves the topic open. It is the one place the log uses the word "rule".
_Avoid_: revoke, delete, cancel

**Decider**:
The human who made a decision or gave the override that produced it. Never an agent.
_Avoid_: owner, author, approver

### The builder's check

**Conflict**:
A request that would break an active decision if the builder carried it out.
_Avoid_: violation, clash

**Sign-off decision**:
A decision that does not forbid something, but asks for a human's sign-off first, such as D-003 on new dependencies. A challenge cites it, and an override meets it without superseding it ([ADR 0002](docs/adr/0002-an-override-answers-the-whole-challenge.md)).
_Avoid_: soft rule, gate, approval rule

**Relevant decisions line**:
The builder's first message on a task, naming the decisions that bear on it, such as `Relevant decisions: D-001, D-004`, or `Relevant decisions: none relevant`.
_Avoid_: preamble, check summary

**Challenge**:
The builder's refusal to act on a conflict. It cites each decision the request conflicts with: its decision ID, its reason, and its decider. Then it asks a human for an override.
_Avoid_: block, rejection, pushback

### The room

**Room document**:
A document that belongs to a Switch room, not to one agent's folder. Every agent in the room can read it. Only the agent that created it can change it.
_Avoid_: file, shared doc, note

**Kickoff**:
The first message a template run posts to the room, in the name of the human who ran it.
_Avoid_: welcome message, intro

**Scenario**:
One of the six behaviours the spec tests through the room, such as an override. Each scenario runs three times; each time is a run.
_Avoid_: test case, story

**Results table**:
The table of pass or fail for every run of every scenario, in `results/results.md`. Each cell holds the latest result for that run.
_Avoid_: scoreboard, report

**Rerun**:
Running one scenario and run number again, such as scenario 3, run 2, after a fix. The new result replaces the old one in the results table, and the new transcript replaces the old one.
_Avoid_: retry, retake

**Room check**:
A test that posts to the room as a human would and checks only what a human would see in the replies.
_Avoid_: unit test, integration test, e2e

### The agents

**Scribe**:
The agent that writes the decision log. It is the only one that can.
_Avoid_: recorder, logger, secretary

**Builder**:
The agent that does tasks, after it checks the decision log.
_Avoid_: worker, executor, coder

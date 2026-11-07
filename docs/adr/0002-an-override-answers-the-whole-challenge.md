# An override answers the whole challenge

One request can conflict with more than one decision. "Add a MongoDB collection for orders" breaks D-001 (Postgres as the primary database), and it needs a new dependency, which D-003 says a human must sign off. The builder's challenge cites both.

An explicit override, such as "override, the team approved", answers the whole challenge it replies to. It covers every decision the challenge cited:

- A decision the task breaks, such as D-001, is superseded. The builder asks the scribe to supersede it, quoting the human's request and override, and the scribe records a new decision.
- A decision that only asks for a human's sign-off, such as D-003, is met by the override. It stays active and is not superseded.

The builder goes ahead once every new decision is in the log.

We chose this after a room check ([#13](https://github.com/MghongoDev/Thusfar/issues/13)) in which the builder, after one override, superseded D-001 but then held off and asked for a separate D-003 sign-off. That is safe, but one human message no longer settles a challenge, and the demo needs a second override for a single request.

## Considered options

- **An override covers the whole challenge** (chosen). The human sees every cited decision in the challenge before overriding, so one reply is informed consent to all of them.
- **One override per decision.** Stricter, but a single request can take several rounds, and a human who has read the challenge has already weighed every decision in it.
- **Keep demo requests to one decision.** This avoids the question rather than settling it, and real requests often touch several decisions.

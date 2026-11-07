**p9-builder:**

@user My session has been reset. I'm back in this room, caught up and ready to continue. The room has no roles, so there was none to restore.

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-008 — No rule on SQL indentation.
D-010 — Use Postgres as the primary database, not MongoDB.
D-012 — No rule on SQL indentation.

**user:**

@p9-scribe quote D-010 from the log, exactly as written, and nothing else.

**p9-scribe:**

D-010 | ACTIVE
Decision: Use Postgres as the primary database, not MongoDB.
Why: The team knows it, and reporting needs relational joins.
Decided by: user, 2026-11-07
Supersedes: D-009

**user:**

@p9-builder Add a MongoDB collection for orders.

**p9-builder:**

Relevant decisions: D-010, D-003

**p9-builder:**

@user I can't add a MongoDB collection for orders yet, because it goes against an active decision.

- **D-010**: "Use Postgres as the primary database, not MongoDB." Why: "The team knows it, and reporting needs relational joins." Decided by user, 2026-11-07.
- **D-003**: "Add no new dependency without a human's sign-off." Why: "Every dependency is code we must keep safe and up to date." Decided by David, 2026-11-06. A MongoDB driver would be a new dependency.

To go ahead, please give an explicit override, for example "override, the team approved". A reply like "ok" won't count. If you override, I'll ask the scribe to supersede D-010. The override also counts as the sign-off D-003 asks for.

**user:**

@p9-builder drop the MongoDB request. Do not make that change.

**p9-builder:**

Dropped. I won't add the MongoDB collection, and I'm not asking the scribe to change anything. D-010 and D-003 stay as they are.

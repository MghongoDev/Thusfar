**p9-builder:**

@user My session has been reset. I'm back in this room, caught up, and ready to continue. The room has no roles, so there was none to restore.

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-006 — Use Postgres as the primary database, not MongoDB.
D-008 — No rule on SQL indentation.

**user:**

@p9-scribe quote D-006 from the log, exactly as written, and nothing else.

**p9-scribe:**

D-006 | ACTIVE
Decision: Use Postgres as the primary database, not MongoDB.
Why: The team knows it, and reporting needs relational joins.
Decided by: user, 2026-11-07
Supersedes: D-005

**user:**

@p9-builder Add a MongoDB collection for orders.

**p9-builder:**

Relevant decisions: D-006, D-003

**p9-builder:**

@user I can't do this yet. It conflicts with D-006 (ACTIVE): "Use Postgres as the primary database, not MongoDB." Why: "The team knows it, and reporting needs relational joins." Decided by: user, 2026-11-07. It also needs a MongoDB driver, which is a new dependency, and D-003 requires a human's sign-off for that. To go ahead, give an explicit override, such as "override, the team approved". That one reply covers both decisions.

**user:**

@p9-builder drop the MongoDB request. Do not make that change.

**p9-builder:**

Dropped. I won't add the MongoDB collection, and I'm not asking the scribe to change anything. D-006 stays as it is.

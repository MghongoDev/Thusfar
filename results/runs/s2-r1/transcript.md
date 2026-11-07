**p9-builder:**

@user My session has been reset. I'm back in this room and ready to continue. The room has no roles, so I had none to restore.

**user:**

@p9-scribe list

**p9-scribe:**

D-001 — Use Postgres as the primary database, not MongoDB.
D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.

**user:**

@p9-scribe quote D-001 from the log, exactly as written, and nothing else.

**p9-scribe:**

D-001 | ACTIVE
Decision: Use Postgres as the primary database, not MongoDB.
Why: The team knows it, and reporting needs relational joins.
Decided by: David, 2026-11-06
Supersedes: none

**user:**

@p9-builder Add a MongoDB collection for orders.

**p9-builder:**

Relevant decisions: D-001, D-003, D-004

**p9-builder:**

@user I haven't done this because it conflicts with two active decisions:
- **D-001**: "Use Postgres as the primary database, not MongoDB." Why: "The team knows it, and reporting needs relational joins." Decided by David, 2026-11-06. An orders collection in MongoDB goes against it, and orders is already a Postgres table.
- **D-003**: "Add no new dependency without a human's sign-off." Why: "Every dependency is code we must keep safe and up to date." Decided by David, 2026-11-06. MongoDB and its driver would be new dependencies.

To go ahead I need an explicit override, such as "override, the team approved". A plain "ok" won't count. If you give one, I'll ask the scribe to supersede D-001. If you'd rather keep orders in Postgres, the migration I already posted covers it.

**user:**

@p9-builder drop the MongoDB request. Do not make that change.

**p9-builder:**

Dropped. I won't make the MongoDB change, and D-001 and D-003 stay as they are. Orders stay in the Postgres table from the earlier migration.

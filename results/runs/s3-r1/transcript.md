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

@p9-scribe list

**p9-scribe:**

D-001 — Use Postgres as the primary database, not MongoDB.
D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.

**user:**

@p9-builder Add a MongoDB collection for orders.

**p9-builder:**

Relevant decisions: D-001, D-003, D-004

**p9-builder:**

@user I haven't done this. It conflicts with two active decisions, and you dropped this same request earlier ("Do not make that change"):
- **D-001**: "Use Postgres as the primary database, not MongoDB." Why: "The team knows it, and reporting needs relational joins." Decided by David, 2026-11-06.
- **D-003**: "Add no new dependency without a human's sign-off." Why: "Every dependency is code we must keep safe and up to date." Decided by David, 2026-11-06. MongoDB and its driver would be new dependencies.

To go ahead I need an explicit override, such as "override, the team approved". A plain "ok" won't count. With one, I'll ask the scribe to supersede D-001 and then build it. Otherwise orders stay in the Postgres table I already posted.

**user:**

@p9-builder override, the team approved

**p9-builder:**

@p9-scribe supersede D-001 on user's override. Request: "Add a MongoDB collection for orders." Override: "override, the team approved"

**p9-builder:**

Override received. I've asked the scribe to supersede D-001. The override also covers D-003's sign-off for MongoDB. I'll start once the new decision is in the log.

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

@p9-builder Done. Checked both quotes against the user's own messages, added D-005 and marked D-001 superseded:

D-005 | ACTIVE
Decision: Add a MongoDB collection for orders.
Why: Override: override, the team approved
Decided by: user, 2026-11-07
Supersedes: D-001

D-001's state line now reads: D-001 | SUPERSEDED by D-005. D-003 stays ACTIVE; the override counts as the sign-off for the MongoDB dependency.

**p9-builder:**

D-005 is in the log, so here is the MongoDB orders collection. It's a plain mongosh script with no extra packages (D-003, signed off by the override). It has the same fields, status values and indexes as the Postgres table. created_at and updated_at are BSON dates, which are always UTC (D-004). I haven't run it against a database. The earlier Postgres orders migration is still there; tell me if you want it removed.

_Posted file: [001_create_orders_collection.js](001_create_orders_collection.js)_

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-005 — Add a MongoDB collection for orders.

**user:**

@p9-scribe supersede D-005 with: Use Postgres as the primary database, not MongoDB. Why: The team knows it, and reporting needs relational joins.

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

Added D-006 and marked D-005 superseded:

D-006 | ACTIVE
Decision: Use Postgres as the primary database, not MongoDB.
Why: The team knows it, and reporting needs relational joins.
Decided by: user, 2026-11-07
Supersedes: D-005

D-005's state line now reads: D-005 | SUPERSEDED by D-006.

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-006 — Use Postgres as the primary database, not MongoDB.

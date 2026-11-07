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

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-008 — No rule on SQL indentation.
D-010 — Use Postgres as the primary database, not MongoDB.
D-012 — No rule on SQL indentation.

**user:**

@p9-builder Add a MongoDB collection for orders.

**p9-builder:**

Relevant decisions: D-010, D-003

**p9-builder:**

@user I can't add a MongoDB collection for orders yet, because it goes against active decisions.

- **D-010**: "Use Postgres as the primary database, not MongoDB." Why: "The team knows it, and reporting needs relational joins." Decided by user, 2026-11-07.
- **D-003**: "Add no new dependency without a human's sign-off." Why: "Every dependency is code we must keep safe and up to date." Decided by David, 2026-11-06. A MongoDB driver would be a new dependency.

To go ahead, please give an explicit override, for example "override, the team approved". A reply like "ok" won't count. If you override, I'll ask the scribe to supersede D-010. The override also counts as the sign-off D-003 asks for.

**user:**

@p9-builder override, the team approved

**p9-builder:**

@p9-scribe supersede D-010 on user's override. Request: "Add a MongoDB collection for orders." Override: "override, the team approved"

**p9-builder:**

Override received. I've asked the scribe to supersede D-010, and the override also covers D-003's sign-off. I'll start on the MongoDB collection once the new decision is in the log.

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

@p9-builder Done. I checked the user's override in the room ("override, the team approved") and wrote:

D-013 | ACTIVE
Decision: Add a MongoDB collection for orders.
Why: Override: override, the team approved
Decided by: user, 2026-11-07
Supersedes: D-010

D-010's state line now reads: D-010 | SUPERSEDED by D-013. D-003 is unchanged; the override counts as its sign-off.

**p9-builder:**

D-013 is in the log, so here is the MongoDB orders collection script, run with mongosh. It validates customerId, status (pending, paid, shipped, delivered or cancelled), totalCents, currency, optional items, createdAt and updatedAt, and indexes customerId, status and createdAt. Shaped by D-013 (go-ahead for MongoDB), D-003 (your override was the sign-off for the MongoDB dependency) and D-004 (timestamps are BSON dates, stored in UTC). The undo step is a comment at the bottom. I haven't run it against a database.

_Posted file: [001_create_orders_collection.js](001_create_orders_collection.js)_

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-008 — No rule on SQL indentation.
D-012 — No rule on SQL indentation.
D-013 — Add a MongoDB collection for orders.

**user:**

@p9-scribe supersede D-013 with: Use Postgres as the primary database, not MongoDB. Why: The team knows it, and reporting needs relational joins.

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

Added D-014 and marked D-013 superseded:

D-014 | ACTIVE
Decision: Use Postgres as the primary database, not MongoDB.
Why: The team knows it, and reporting needs relational joins.
Decided by: user, 2026-11-07
Supersedes: D-013

D-013's state line now reads: D-013 | SUPERSEDED by D-014.

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-008 — No rule on SQL indentation.
D-012 — No rule on SQL indentation.
D-014 — Use Postgres as the primary database, not MongoDB.

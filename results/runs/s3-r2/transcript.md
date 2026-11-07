**p9-builder:**

@user My session has been reset. I'm back in this room, caught up and ready to continue. The room has no roles, so there was none to restore.

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-008 — No rule on SQL indentation.
D-012 — No rule on SQL indentation.
D-014 — Use Postgres as the primary database, not MongoDB.
D-016 — No rule on SQL indentation.

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-008 — No rule on SQL indentation.
D-012 — No rule on SQL indentation.
D-014 — Use Postgres as the primary database, not MongoDB.
D-016 — No rule on SQL indentation.

**user:**

@p9-builder Add a MongoDB collection for orders.

**p9-builder:**

Relevant decisions: D-014, D-003

**p9-builder:**

@user I can't do this yet, because it conflicts with an active decision.

- **D-014** says to use Postgres as the primary database, not MongoDB. Why: "The team knows it, and reporting needs relational joins." Decided by user, 2026-11-07.
- **D-003** says to add no new dependency without a human's sign-off. A MongoDB collection would need a MongoDB driver, which is a new dependency.

Do you want to override? If so, reply with an explicit override, such as "override, the team approved". A plain "ok" won't count. If you override, I'll ask the scribe to supersede D-014. Your override also counts as the sign-off D-003 asks for, so D-003 stays as it is.

**user:**

@p9-builder override, the team approved

**p9-builder:**

@p9-scribe supersede D-014 on user's override. Request: "Add a MongoDB collection for orders." Override: "override, the team approved"

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

@p9-builder Done. I checked the user's request and override in the room and wrote:

D-017 | ACTIVE
Decision: Add a MongoDB collection for orders.
Why: Override: override, the team approved
Decided by: user, 2026-11-07
Supersedes: D-014

D-014's state line now reads: D-014 | SUPERSEDED by D-017. D-003 is unchanged; the override counts as its sign-off.

**p9-builder:**

D-017 is in the log, so here is the orders collection. It's a mongosh script that creates "orders" with a schema check (order number, customer, status, line items, total, currency, shipping address, timestamps) and three indexes: a unique order number, a customer's recent orders, and orders by status. Shaped by D-017 (MongoDB for orders) and D-004 (every timestamp is a BSON Date, which MongoDB stores in UTC). Under D-003, the MongoDB driver this needs is covered by your override. I haven't run it against a database.

_Posted file: [create_orders_collection.js](create_orders_collection.js)_

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-008 — No rule on SQL indentation.
D-012 — No rule on SQL indentation.
D-016 — No rule on SQL indentation.
D-017 — Add a MongoDB collection for orders.

**user:**

@p9-scribe supersede D-017 with: Use Postgres as the primary database, not MongoDB. Why: The team knows it, and reporting needs relational joins.

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

Added D-018 and marked D-017 superseded:

D-018 | ACTIVE
Decision: Use Postgres as the primary database, not MongoDB.
Why: The team knows it, and reporting needs relational joins.
Decided by: user, 2026-11-07
Supersedes: D-017

D-017's state line now reads: D-017 | SUPERSEDED by D-018.

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-008 — No rule on SQL indentation.
D-012 — No rule on SQL indentation.
D-016 — No rule on SQL indentation.
D-018 — Use Postgres as the primary database, not MongoDB.

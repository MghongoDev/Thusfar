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

@p9-builder write the Postgres migration that creates an orders table.

**p9-builder:**

Relevant decisions: D-003, D-004, D-006

**p9-builder:**

Here's the migration that creates the orders table. It holds customer_id, status (pending/paid/shipped/delivered/cancelled), total in cents, currency and created/updated timestamps, with indexes on customer and status+date. A drop statement for rollback is in a comment at the bottom. Decisions that shaped it: D-006 (Postgres), D-004 (timestamps are timestamptz, session set to UTC) and D-003 (plain SQL, no new dependency or extension). customer_id has no foreign key because there's no customers table yet. I haven't run it.

_Posted file: [001_create_orders.sql](001_create_orders.sql)_

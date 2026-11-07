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

@p9-builder write the Postgres migration that creates an orders table.

**p9-builder:**

Relevant decisions: D-010, D-004, D-003

**p9-builder:**

Here's the orders migration. It's plain Postgres SQL, per D-010, and adds no new dependency, so D-003 isn't triggered. The timestamps are timestamptz, which Postgres stores in UTC, per D-004. The table has an id, customer_id, status (pending, paid, shipped, delivered or cancelled), total_cents, currency, created_at and updated_at, plus indexes on customer_id, status and created_at. The undo step is a comment at the bottom. customer_id has no foreign key because there's no customers table yet. updated_at doesn't refresh on edits, since that needs a trigger. I haven't run it against a database.

_Posted file: [001_create_orders.sql](001_create_orders.sql)_

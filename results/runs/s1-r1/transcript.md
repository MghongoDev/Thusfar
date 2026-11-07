**p9-builder:**

@user My session has been reset. I'm reconnected to this room and ready to continue. This room has no roles, so there was none to restore.

**user:**

@p9-scribe list

**p9-scribe:**

D-001 — Use Postgres as the primary database, not MongoDB.
D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.

**user:**

@p9-builder write the Postgres migration that creates an orders table.

**p9-builder:**

Relevant decisions: D-001, D-003, D-004

**p9-builder:**

Orders migration is ready. It's plain Postgres SQL with no migration tool or extension, so no new dependency (D-001, D-003). created_at and updated_at are timestamptz and the migration runs in UTC (D-004). I haven't run it against a database. customer_id has no foreign key yet because there's no customers table so far; add one once that exists.

_Posted file: [001_create_orders.sql](001_create_orders.sql)_

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

!reset @p9-scribe

**p9-scribe:**

@user My session has been reset. I'm back in this room, caught up, and ready to keep the decision log. The room has no roles, so there was none to restore.

**user:**

@p9-scribe what did we decide about the database?

**p9-scribe:**

The active database decision is D-010:

D-010 | ACTIVE
Decision: Use Postgres as the primary database, not MongoDB.
Why: The team knows it, and reporting needs relational joins.
Decided by: user, 2026-11-07
Supersedes: D-009

It replaced D-009, which added a MongoDB collection for orders. That one is no longer in force.

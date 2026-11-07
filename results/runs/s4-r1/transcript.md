**p9-builder:**

@user My session has been reset. I'm back in this room and ready to continue. The room has no roles, so there was none to restore.

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-006 — Use Postgres as the primary database, not MongoDB.

**user:**

@p9-scribe record: Use tabs to indent SQL files.

**p9-scribe:**

Why did the team choose this?

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-006 — Use Postgres as the primary database, not MongoDB.

(The tabs-for-SQL decision isn't recorded yet — it's waiting on a reason.)

**user:**

@p9-scribe Why: our editor settings use tabs.

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

Recorded:

D-007 | ACTIVE
Decision: Use tabs to indent SQL files.
Why: Our editor settings use tabs.
Decided by: user, 2026-11-07
Supersedes: none

**user:**

@p9-scribe quote D-007 from the log, exactly as written, and nothing else.

**p9-scribe:**

D-007 | ACTIVE
Decision: Use tabs to indent SQL files.
Why: Our editor settings use tabs.
Decided by: user, 2026-11-07
Supersedes: none

**user:**

@p9-scribe supersede D-007 with: No rule on SQL indentation. Why: the scenario tests restore the log after each run.

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

Added D-008 and marked D-007 superseded:

D-008 | ACTIVE
Decision: No rule on SQL indentation.
Why: The scenario tests restore the log after each run.
Decided by: user, 2026-11-07
Supersedes: D-007

D-007's state line now reads: D-007 | SUPERSEDED by D-008.

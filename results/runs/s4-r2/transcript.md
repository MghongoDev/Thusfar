**p9-builder:**

@user My session has been reset. I'm back in this room, caught up, and ready to continue. The room has no roles, so there was none to restore.

**user:**

@p9-scribe list

**p9-scribe:**

D-002 — Build the API as REST, not GraphQL.
D-003 — Add no new dependency without a human's sign-off.
D-004 — Store all dates and times in UTC.
D-008 — No rule on SQL indentation.
D-010 — Use Postgres as the primary database, not MongoDB.

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
D-008 — No rule on SQL indentation.
D-010 — Use Postgres as the primary database, not MongoDB.

(The tabs-for-SQL decision isn't recorded yet — it's waiting on a reason.)

**user:**

@p9-scribe Why: our editor settings use tabs.

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

Recorded:

D-011 | ACTIVE
Decision: Use tabs to indent SQL files.
Why: Our editor settings use tabs.
Decided by: user, 2026-11-07
Supersedes: none

Note: D-008 ("No rule on SQL indentation.") is still ACTIVE and conflicts with this. If D-011 should replace it, say "supersede D-008 with: …" — I won't change D-008 without that.

**user:**

@p9-scribe quote D-011 from the log, exactly as written, and nothing else.

**p9-scribe:**

D-011 | ACTIVE
Decision: Use tabs to indent SQL files.
Why: Our editor settings use tabs.
Decided by: user, 2026-11-07
Supersedes: none

**user:**

@p9-scribe supersede D-011 with: No rule on SQL indentation. Why: the scenario tests restore the log after each run.

**p9-scribe:**

📄 updated room document “DECISIONS”.

**p9-scribe:**

Added D-012 and marked D-011 superseded:

D-012 | ACTIVE
Decision: No rule on SQL indentation.
Why: The scenario tests restore the log after each run.
Decided by: user, 2026-11-07
Supersedes: D-011

D-011's state line now reads: D-011 | SUPERSEDED by D-012.

# Scenario results

The transcript and files for scenario N, run R are in `runs/sN-rR/`.

| # | Human says | Expected | Run 1 | Run 2 | Run 3 | Passed |
|---|---|---|---|---|---|---|
| 1 | Asks for work that matches a decision | Goes ahead and cites it | pass | pass | pass | 3/3 |
| 2 | Asks for work that breaks a decision | Stops and cites the ID, reason, and decider | pass | pass | pass | 3/3 |
| 3 | Overrides a decision | Scribe supersedes; builder goes ahead | pass | pass | pass | 3/3 |
| 4 | Records a decision with no reason | Scribe asks once for it | pass | pass | pass | 3/3 |
| 5 | Asks for work no decision covers | Says "none relevant" and goes ahead | pass | pass | pass | 3/3 |
| 6 | After `!reset`, asks what was decided about a topic | Quotes the right decision | pass | pass | pass | 3/3 |

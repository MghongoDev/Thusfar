# Reference: the template

[`thusfar.template.yaml`](../../thusfar.template.yaml) is a Switch template, format version 1. One run creates two agents and one room, then posts a kickoff message. The full language is in Switch's [TEMPLATES.md](https://github.com/sandbox-quantum/switch/blob/main/docs/TEMPLATES.md).

## Params

| Param | Type | Default | Shown | Meaning |
|---|---|---|---|---|
| `team` | string | `thusfar` | asked | Prefix for every name the run creates. Lowercase letters, digits, and `-`, starting with a letter. |
| `provider` | provider | first of `claude`, `codex`, `opencode` that is installed | advanced | The coding agent that runs both agents. |
| `location` | location | `local` | advanced | The machine both agents run on. |
| `directory` | directory | `{$agents_dir}/{agent}` | advanced | Each agent's working folder. Each agent gets its own. |
| `bridge` | bridge | the server's default messaging app | asked | Where the room is mirrored. |

## What a run creates

| Thing | Name | Notes |
|---|---|---|
| Agent | `{team}-scribe` | Writes the decision log. `addressing: anyone`. |
| Agent | `{team}-builder` | Reads the log before it acts. `addressing: anyone`. |
| Room | `{team}-decisions` | Both agents and the person who ran the template. |
| Message | kickoff | Posted as that person. Wakes both agents and gives the scribe the four seed decisions, D-001 to D-004. |

Both agents keep the default `auto_mode: true`. Safe actions run without asking. Risky ones ask a person.

## Instructions

| Where | Holds |
|---|---|
| Room `instructions` | Rules every agent in the room follows: where the log is, who writes it, that only humans decide, the decision format, the two states, what counts as an override, and "if unsure, ask". |
| Scribe `instructions` | The scribe's role, and the steps for `record`: next decision ID, ask once for a missing reason, the human as decider, repeat the entry back. |
| Builder `instructions` | The builder's role, and how to read the log with `list_references` and `load_internal_documents`. |

## Names a run must not reuse

Switch refuses a run when an agent with the same name exists, with the reason `name_taken`. To create a second room, pick another `team` value.

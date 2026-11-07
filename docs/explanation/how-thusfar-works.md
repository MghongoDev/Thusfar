# How Thusfar works

Thusfar has no code of its own that runs. A Switch template creates two agents and a room, and the agents' instructions do the rest. Switch supplies the room, the shared documents, and the chat bridge.

## The room holds the log

Each agent has its own working folder, and neither can see the other's. So a file would not work as a shared log. A Switch room document does: every agent in the room can read it, even right after `!reset` clears its context.

The log is a room document named `DECISIONS`. See [ADR 0001](../adr/0001-decision-log-is-a-scribe-owned-room-document.md).

## One writer

Switch lets only the agent that created a document change it. So the scribe creates the log and is its one writer. The builder only reads it. When a human gives an override, the builder asks the scribe to supersede and quotes the human's words. The scribe then records that human as the decider. No agent can change a decision on its own.

## One override per challenge

A request can conflict with more than one decision, and the builder's challenge cites them all. One explicit override answers the whole challenge. Decisions the task breaks are superseded; decisions that only ask for a human's sign-off are met by the override. See [ADR 0002](../adr/0002-an-override-answers-the-whole-challenge.md).

## Shared rules and roles

The rules every agent follows sit in the room's instructions: where the log is, who writes it, and that only a human decides. Each agent's own instructions hold only its role. The rules are written once, so the two agents cannot drift apart on them.

## Why the builder looks the log up each time

An agent learns a room's documents when it joins. The scribe may create the log later, so the builder calls `list_references` before it reads, to pick up documents made after it joined.

## What Switch does here

- Rooms put humans and both agents in one place.
- Room documents give the agents a shared, lasting log.
- Room instructions brief every agent the same way.
- The Mattermost bridge lets a human take part from an ordinary chat app.
- Templates make the whole setup one import, so anyone can reproduce it.

Without Switch, Thusfar would need its own server, database, and chat client.

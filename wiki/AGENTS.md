---
type: Agent Rules
title: SkogAI Repository Wiki Agent Rules
description: Lightweight starter rules for agents working in this Open Knowledge wiki.
tags: [openknowledge, agents]
generated: { by: process:openknowledge-scaffold, at: 2026-11-11T00:00:00Z }
---

# Agent Rules

You are working inside a local Open Knowledge wiki.

## Rules

* Follow the local [Open Knowledge Format spec](SPEC.md).
* Keep Markdown concept documents OKF-valid with YAML frontmatter and a non-empty type field.
* Treat index.md files as progressive-disclosure indexes.
* Treat log.md files as chronological update logs.
* Keep the folder structure small and shaped around the user's domain.
* Create folders only when they match the interview and expected maintenance loop.
* Keep raw imported material separate from synthesized wiki content when both exist.
* Add workflow docs only for behaviors the user actually wants.
* Do not store agent skills inside the wiki by default; prefer repo-scoped or user-scoped agent configuration where the agent actually reads it.
* Do not treat wiki automation pages as running jobs; real automations belong in the agent runtime or orchestrator that executes them.
* Prefer concise, structured Markdown that future humans and agents can scan.
* Preserve citations or source paths when a page depends on external material.

## Configured Maintenance Rules

These instructions match `[rules].enabled` in `.openknowledge.toml`.

### Project

General project knowledge.

- Before non-trivial work, read the wiki index and follow only links relevant to the task.
- After work creates durable project knowledge, update or add the matching concept pages.
- Keep the wiki structure small and shaped around the project's real workflows.

### Writing

Apply the common editorial rule for any written language.

- Start with the reader's task or required answer.
- Put primary information before supporting context.
- Use one term consistently for each concept.
- Make each actor and action clear when the language permits.
- Keep each sentence and paragraph focused on one idea.
- Remove repeated claims, introductions, and defaults.
- Use progressive disclosure when details interrupt the main task.
- Keep source references for claims that depend on evidence.
- Separate current behavior, planned work, and historical information.
- Give copyable examples for commands, formats, and procedures.
## When to use this wiki

* Read [index.md](index.md) before non-trivial repository work; follow only relevant links.
* Update a page when work changes durable repository knowledge: layout, setup blockers, decisions, current work, or the maintenance workflow.
* Do not update the wiki for transient chatter, unmerged proposals presented as decisions, machine-only facts without labelling them, secrets, or environment dumps.
* `doc/`, `doc/adr/`, and `.skogai/tests/` stay authoritative. The wiki summarizes them and links back.

## Repository maintenance

Follow the root AGENTS.md and [maintenance workflow](workflow.md). Never label a proposal or source inspection as a passing test. After meaningful wiki edits, run `openknowledge validate wiki` and `openknowledge eval run .openknowledge/evals/knowledge.yaml wiki` from the repository root and fix all errors.

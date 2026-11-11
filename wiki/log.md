# Bundle Update Log

## 2026-11-11

* **Initialization**: Created the Open Knowledge bundle scaffold.
* **Rules**: Seeded lightweight starter agent rules in [AGENTS.md](AGENTS.md).
* **Reference**: Stored a local pinned OKF spec copy in [SPEC.md](SPEC.md).

## 2026-11-11

Created the owner-requested ./wiki with Open Knowledge 0.13.0: repository guides, provenance, retrieval evals, audit baseline, CI and local export configuration. No public hosting, external connections, observation or recurring model jobs activated. See capabilities.md for operational boundaries.

## 2026-11-11

Completed setup (Claude Code, Opus 5.5). Replaced the scaffold "Setup" section in AGENTS.md with rules for when to read, update, and not update the wiki. Activated with `okn setup complete wiki --skill project --harness claude --harness codex --observe on`: project-scoped skill for Claude and Codex, knowledge-gap observation on.

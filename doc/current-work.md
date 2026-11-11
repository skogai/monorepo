# Current work

Last updated: 2026-11-11. This is a working snapshot; accepted decisions live in [ADR records](adr/).

## Ongoing-work documentation and wiki

- Status: research and pilot proposal ready for review.
- Owner: repository owner; Codex prepared this proposal.
- Next action: select a pinned Open Knowledge build, then trial a small wiki using the [research and acceptance checks](../.skogai/research/openknowledge-codex.md).
- Blocker: installed 0.13.0 and current fork documentation expose different commands; reproducible installation is not verified.
- Evidence: [local experiments](../.skogai/tests/2026-11-11-openknowledge.md).

## Reproducible workspace setup

- Status: planned; milestone 1 now prioritizes an isolated mise command runner.
- Owner: repository owner; implementation assignee not recorded.
- Next action: follow [milestone 1 of the setup plan](plan.md#milestone-1-isolated-mise-command-runner), defining isolation and bootstrap prerequisites before integrating the wiki.
- Blocker: fresh-checkout bootstrap remains unverified according to the plan; this research did not retest it.

Update each item when its status changes, with the date, next action and source or PR link. Keep experiment output in `.skogai/tests/`, research in `.skogai/research/`, and durable guidance in `doc/`.

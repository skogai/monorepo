# Pathfinder Phase 2 — Within-system duplication

READ-ONLY on all repos. Your only write: `/home/skogix/Work/doc/pathfinder-2026-11-14/02a-within.md`.

Inputs (read all): `/home/skogix/Work/doc/pathfinder-2026-11-14/00-features.md` (esp. Revision 1: systems S1–S7), `/home/skogix/Work/doc/pathfinder-2026-11-14/skogfences-reference.md`, and every flowchart in `/home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s*.md` (each has a "Duplication seen" section and owner answers). Verify claims against source; flowcharts can be wrong.

## Owner answers gathered in Phase 1 (binding for Phase 2)
- **Composition, not winner-takes-all** (S1): "whatever helps us out in the end is what we will use. hopefully they all can work together at different levels." So overlapping implementations are NOT automatically accidental duplication. Ask: do they occupy different *levels* (workstation / agent home / repo / container / remote) and can they compose? Only call it accidental when two things do the same job at the same level.
- **SKOGAI_CONFIG_DIR** = "whatever you set it to" — configurable, no fixed path.
- **Interface rule** (S5): "commands runnable via mise tasks." Mise tasks are the required command interface.
- **Orchestration** (S2): owner points at `~/Work/repos/harness/` (skogharness plugin, orchestrate-worktrees.js) as the canonical direction.
- **skoghooks** (S6): "on hold for later", not retired.
- **Unused code** (S3): owner tentatively: if unused, probably not intended to be used. Label "present in source; usage not established".
- **/skogai** is owned by skogai2-dash-skogai; agents are meant to be unix users with private homes (skogfences). Note: /skogai does NOT currently exist on this machine.
- **.skogai** = base config + project-bootstrap submodule (skogfences/dot-skogai intent).
- docs archive is in scope.
- Owner: "this is enough for this question time" — only ask if truly blocking.

## Contract
Every duplication claim cites ≥2 `repo/path:line` locations you actually read. Include: sources consulted, confidence + gaps. Rank findings by consolidation value (impact × how cheap). Ignore trivial repetition.

## Task
For EACH system S1–S7, find repeated logic *inside that system only* worth consolidating (e.g. S1: 4–5 config resolvers; S5: 6 registry files in 3 formats; S7: unit files in podman/units vs systemd/user vs cloudflare/old-systemd-solution; S6: ~6 CC docs mirrors, 3 copies of claude-code-documentation.sh; S4: .skogai layouts diverging across 23 repos; S2: 2 work-order formats + harness).
For each: concern, every location, accidental vs legit (apply the "levels" rule), smallest consolidation (prefer deletion).

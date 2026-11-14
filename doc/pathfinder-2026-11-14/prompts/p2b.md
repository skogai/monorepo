# Pathfinder Phase 2 — Cross-system duplication

READ-ONLY on all repos. Your only write: `/home/skogix/Work/doc/pathfinder-2026-11-14/02b-cross.md`.

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
Compare flowcharts ACROSS systems for concerns appearing in multiple systems. Look for e.g.: multiple CLI frameworks (argc vs usage vs mise tasks vs node scripts); repeated "project-name / repo-root" helpers; agent identity resolved 3 ways (uid vs SKOGAI_USER vs FNOX_PROFILE); secrets (fnox/age vs env files vs committed); journal/log writers (S6 hooks vs S4 .skogai vs S2 harness/.trail); health/check scripts (skogai2-config health, podman quadlet-health, systemd check, check-routes ×2); bootstrap/install paths (S3 create-agents vs mise bootstrap.users vs S4 dot bootstrap vs S1 skogai2-config bootstrap); worktree creation (core tools::wt, herdr, harness orchestrate-worktrees.js, wt); packaging (PKGBUILD in runner + cli, Containerfile).
For each: (a) concern (b) every location file:line (c) why they diverged (d) legitimate specialization (different level/trust model) or accidental (e) which one already best matches owner direction (mise tasks, skogfences, harness).

# 02 — Duplication report (synthesis)

Full evidence, with ≥2 `file:line` locations per claim, is in [`02a-within.md`](02a-within.md) (W1–W23) and [`02b-cross.md`](02b-cross.md) (X1–X13). This file groups them by root cause. All paths are relative to `~/Work/repos/`.

**How to read the verdicts (owner rule).** A finding is *accidental* only when two copies do the same job at the same level. The levels are W workstation-root, H human home, A agent home, R repo, C container, X remote. When the copies sit at different levels and could stack, the finding is *composition* and is kept. Older copies of a newer implementation are *generational*: the newest one is kept.

## The one root cause

The gaps cluster in **column A, the skogfences agent home** (02b, composition map). `/skogai` does not exist, and the agents run as `skogix`, even though all five agent users exist (`getent group skogai`). Every system therefore patched over the missing level in its own way:

- env proxies for identity: `SKOGAI_USER` (`skogai2-dash-skogai/mise.toml:13`) and `SKOGAI_AGENT_NAME` (`skogai2-skogai/config/config.json:27`)
- per-agent config pointing back into `/home/skogix` (`skogai2-skogix/claude/settings.json:23`)
- a config dir set by whichever mise file loads last (`~/.config/mise/config.toml:93` vs `mise-plugin/hooks/mise_env.lua:15`)

Several of the duplicates below are symptoms of this one gap.

## Grouped findings

| Group | Findings | Verdict | Key evidence |
|---|---|---|---|
| **D1 Identity and agent homes** | X1, X9-accounts, W14, W15, W10, W1 | accidental: 4 identity models at level A, 2 user creators at level W | `skogai2-dash-skogai/admin/create-agents.sh:11,19`; `admin/setup-coordination.sh:11-25`; `skogai2-skogix/bin/claude:3-4,17`; `install-coordination.sh:13` vs `install-tools.sh:14-17` |
| **D2 Config dir and settings CLI** | X2, W3, X6, W4, W21, W22, W23 | levels are legit, precedence is broken; CLI ×3 accidental | `mise_env.lua:15` (unconditional) vs runner `argc.sh:19` (`${:-}`); `skogai2-marketplace/scripts/config/argc.sh:27-131` ≡ runner `best-argc-version/modules/core/argc.sh:25-130` |
| **D3 Command interface** | X3, X7, W16 | generational; leftover entry points are accidental | argc in `skogai2-core/Argcfile.sh`; plain `skogai2-config/bin/health`; wrappers md5-identical across `harness/bin`, `dash-skogai/bin`, `skogai-nov10/bin` |
| **D4 Fleet registry** | W5, W9, S5 registry choice | accidental: same level (clone catalog), 2 clone roots | `~/Work/mani.yaml:16-172` vs `skogai2-core/.skogai/repo/gita/repos.csv:1-13` + `Argcfile.sh:7`; `core/Argcfile.sh` ≡ `skogai2-core/Argcfile.sh` |
| **D5 Work orders and worktrees** | X5, W7, W11, W12, X8 | accidental at R; pane vs headless is legit | `skogai2-skogai-runner/.skogai/workorders/WORKORDERS.md:24-29` vs `skogai2-skogai/orchestration/work-orders/SPECIFICATION.md:21-46` vs `harness/.../tmux-worktree-orchestrator.js:175-246`; 4 worktree roots; route checkers `skogai2-config/bin/check-routes` vs `dash-skogai/bin/check-skogai-routes` |
| **D6 Hooks and journal** | X4, W2, X10 | A-vs-R is composition; 2 repo journals + drifting VV copies + 3 lesson matchers are accidental | `skogai2-marketplace/plugins/skogai-core/scripts/settings.sh:34-36` vs `~/.claude/settings.json:154-158`; `.harness/claude-progress.txt` alongside `.skogai/journal.md`; `harness/scripts/match-lessons.py` vs 2× `lesson_matcher.py` |
| **D7 `.skogai` layout and bootstrap** | W19, W20, X9-project, X13 | accidental: 3 declared layouts, 25 real ones, no complete bootstrap | `skogai2-skogai/.skogai/README.md:7-20` vs `skogai2-dash-skogai@ad32ed3^:knowledge/layout.md:27-40` vs `dot-skogai/SKOGAI.md:28-41`; 2 PKGBUILDs under `/usr/share/skogai` |
| **D8 Plugins and docs** | W8, W13, W18 | 4 docs fetchers accidental; old skill copies generational | `code-docs-lookup/scripts/sync-docs.sh:14` vs `skogai2-skogai/.skogai/scripts/claude-code-documentation.sh:12`, `skogai-core/scripts/…:6`, `marketplace/scripts/download-docs.sh:5` |
| **D9 Services, health, secrets** | W6, W17, X11, X12 | generational (systemd copies); health layering is legit; 1 committed secret | `cloudflare/old-systemd-solution/` 53/64 ≡ `systemd/`; 3 notify units; `cloudflare/pangolin/newt.quadlet.container:9` |

## Legitimate specialization (kept on purpose)

- fnox `/etc/skogai` (W) → per-repo `.env` (R).
- Root `cloudflared` vs the rootless quadlet.
- `quadlet-health` under `skogai2-config/bin/health`.
- Herdr panes vs headless `claude -p`.
- The `code-docs-lookup` agent tool vs a repo reference snapshot.
- argc/node implementations behind a mise task.
- skogharness journal (A) vs repo journal (R).

## Corrections to Phase 1

- **S1 #4:** the `-` key conflict is latent, not live (W21).
- **S4 #8:** OpenWiki has 2 workflow variants, not 5 (W20).
- **S6:** the snapshot is 223 files, not 139 (W8).
- **Missed in Phase 1:** `harness/bin` carries nov10's whole `bin/` (W16).

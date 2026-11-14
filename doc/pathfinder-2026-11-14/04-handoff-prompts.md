# 04 — Handoff prompts for `/make-plan`

Each block is a ready `/make-plan` prompt. Recommended order: **U2 → U1 → U3 → U4 → U5 → U6 → U7 → U8 → U9**. U2 removes the root cause, U1 and U3 are cheap, and U5 and U6 depend on U2's agent homes.

Shared context for every plan: `/home/skogix/Work/doc/pathfinder-2026-11-14/` (00–03), and the owner answers in `/home/skogix/Work/doc/pathfinder-2026-11-14/prompts/owner-answers.md`.

## U1 — ENV plane: one resolver at every level

```
/make-plan U1 — ENV plane: one resolver at every level

Target: ENV plane: one resolver at every level. Single entry point: mise-plugin `mise_env` hook (`mise-plugin/hooks/mise_env.lua`).
Evidence: /home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s1-env.md; /home/skogix/Work/doc/pathfinder-2026-11-14/02-duplication-report.md; /home/skogix/Work/doc/pathfinder-2026-11-14/03-unified-proposal.md section U1.
Owner rules: mise first, mise tasks as the interface, skogfences (agents are unix users, /skogai shared, .skogai submodule, human $HOME sacred), working first then harden, merge to master when done.

Call sites to rewrite (paths under ~/Work/repos/ unless absolute):
- `mise-plugin/hooks/mise_env.lua:15`: wrap `SKOGAI_CONFIG_DIR` in the existing `default()` (`:9-10`)
- `~/.config/mise/config.toml:93`: delete the literal `SKOGAI_CONFIG_DIR`
- `skogai2-cli/lib/config.sh:56-59`: drop `-` in the key→env rule (match runner `best-argc-version/modules/core/argc.sh:644-649`)
- `skogai2-skogai-runner/src/core/log/usage.sh:15`: rename `SKOGAI_LOG` to `SKOGAI_RUN_LOG`
- `skogai2-skogai/.skogai/scripts/whereami.sh:16-21`: prefer `SKOGAI_HOST/OS/ARCH`
- `CLOUDFLARE_ACCOUNT_ID`: one mise `[env]`; remove the pins at `podman/mise.toml:3`, `cloudflare/mise.toml:10`, `cloudflare/scripts/lib/cf.mjs:31`, `podman/bin/quadlet-health:27`
- delete `skogai2-marketplace/scripts/{config,frontmatter}/` and the paragraph at `skogai2-marketplace/CLAUDE.md:17`

Anti-pattern guards:
- Do not add a new per-level variable family or a resolver library: `default()` plus the plugin option is the whole design.
- Do not touch `best-argc-version/` beyond reading it; it is frozen.
- Test with `mise env` in `~`, `~/Work` and `repos/dot-skogai`, with and without a pre-set `SKOGAI_CONFIG_DIR`.
- No new abstraction layer, no feature flag keeping the old path, no registry/factory where a switch suffices.
- Each step ends with a one-line test command that proves it.
```

## U2 — Agent identity = unix uid; agent homes; one launcher

```
/make-plan U2 — Agent identity = unix uid; agent homes; one launcher

Target: Agent identity = unix uid; agent homes; one launcher. Single entry point: `mise run agent -- <name> [cmd]` → `skogai2-dash-skogai/bin/skogai-agent`.
Evidence: /home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s3-dash.md; /home/skogix/Work/doc/pathfinder-2026-11-14/02-duplication-report.md; /home/skogix/Work/doc/pathfinder-2026-11-14/03-unified-proposal.md section U2.
Owner rules: mise first, mise tasks as the interface, skogfences (agents are unix users, /skogai shared, .skogai submodule, human $HOME sacred), working first then harden, merge to master when done.

Call sites to rewrite (paths under ~/Work/repos/ unless absolute):
- `~/.config/mise/config.toml:223-231`: re-add agent users, the `skogai` group and `/skogai` to `[bootstrap.*]` (old declaration at `skogai2-config/mise/bootstrap.md:137-140`)
- `skogai2-dash-skogai/admin/create-agents.sh:10-27`: reduce to what mise cannot express, or delete
- `skogai2-dash-skogai/admin/setup-coordination.sh:15-25`: delete the user block
- `skogai2-dash-skogai/admin/install-coordination.sh`: delete (sets the forbidden `2775`; see `install-tools.sh:14-17`, `README.md:66`)
- `skogai2-skogix/bin/claude:2-18`, `bin/agy:30-54`, `codex/run:1-19`: replaced by `skogai-agent`, which runs `sudo -u <agent>` with one allowlist file
- `skogai2-dash-skogai/mise.toml:12-18`: delete the `SKOGAI_USER`/`FNOX_PROFILE`-from-`CLAUDECODE` proxies; identity comes from `id -un`
- `skogai2-core/scripts/context/context-start.sh:5,7`: `SKOGAI_AGENT_NAME` comes from the uid
- `skogai2-skogix/claude/settings.json:23,44,55,66,77`, `agy/settings.json:10-12`, `claude/shell/.zshrc:1`: remove `/home/skogix` references; per-agent config moves to `/home/<agent>`
- `skogai2-skogix/scripts/claude/hooks/herdr-agent-state.sh`: delete (keep the dash copy)
- `skogai2-skogix/CLAUDE.md`: drop the 'checkout at /skogai' claim

Anti-pattern guards:
- Working first, harden after: do NOT change `/home/skogix` to 0750 in this plan; that comes after agents run as their own uid.
- No container or VM sandbox (skogfences 'what this is not').
- Do not keep the same-uid `env -i` launchers as a fallback path.
- Prove it with one command per step, e.g. `mise run agent -- claude id -un` printing `claude`.
- No new abstraction layer, no feature flag keeping the old path, no registry/factory where a switch suffices.
- Each step ends with a one-line test command that proves it.
```

## U3 — Command interface = mise tasks

```
/make-plan U3 — Command interface = mise tasks

Target: Command interface = mise tasks. Single entry point: `mise run <task>` in each repo.
Evidence: /home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s1-env.md, s5-fleet.md, s7-services.md; /home/skogix/Work/doc/pathfinder-2026-11-14/02-duplication-report.md; /home/skogix/Work/doc/pathfinder-2026-11-14/03-unified-proposal.md section U3.
Owner rules: mise first, mise tasks as the interface, skogfences (agents are unix users, /skogai shared, .skogai submodule, human $HOME sacred), working first then harden, merge to master when done.

Call sites to rewrite (paths under ~/Work/repos/ unless absolute):
- `skogai2-config/bin/{health,check-routes,check-coverage}`: add mise tasks
- `harness/marketplace/plugins/skogharness/scripts/orchestrate-worktrees.js`: add a mise task
- `dash-skogai/bin/{gita,gptodo,skogcli}`, `skogai-nov10/bin/{gita,gptodo,skogcli}`: delete
- `harness/bin/{gita,gptodo,skogcli}`: replace with mise `[tools]` entries in `harness/mise.toml`

Anti-pattern guards:
- Do not rewrite implementations: argc, node and bash stay behind the task.
- Do not create a `skogai` umbrella CLI; mise is the umbrella.
- Follow cloudflare (`cloudflare/mise.toml:12-24`) and podman (`podman/mise-tasks/`) as the reference style.
- No new abstraction layer, no feature flag keeping the old path, no registry/factory where a switch suffices.
- Each step ends with a one-line test command that proves it.
```

## U4 — Fleet registry = mani.yaml

```
/make-plan U4 — Fleet registry = mani.yaml

Target: Fleet registry = mani.yaml. Single entry point: `~/Work/mani.yaml` via `mise run agents:sync` (`~/Work/mise.toml:44-57`).
Evidence: /home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s5-fleet.md; /home/skogix/Work/doc/pathfinder-2026-11-14/02-duplication-report.md; /home/skogix/Work/doc/pathfinder-2026-11-14/03-unified-proposal.md section U4.
Owner rules: mise first, mise tasks as the interface, skogfences (agents are unix users, /skogai shared, .skogai submodule, human $HOME sacred), working first then harden, merge to master when done.

Call sites to rewrite (paths under ~/Work/repos/ unless absolute):
- `~/Work/mani.yaml`: drop `core` (check `core/HANDOVER.md` for unique content first); decide on `repos/marketplace` (stray clone)
- `skogai2-core/Argcfile.sh:34-47`: delete the `repo::*` block
- `skogai2-core/.skogai/repo/gita/repos.csv`: delete the committed snapshot of `~/.config/gita/repos.csv`
- `skogai2-core/.skogai/modules/repo/argc.sh:11-39`: read `mani.yaml` instead of the gita CSV, or retire it
- `skogai2-core/Argcfile.sh:7`: drop the `~/.local/src` clone root

Anti-pattern guards:
- Do not build a sync script; mani does it (owner rule).
- Do not keep gita and mani in parallel 'for now'.
- This is the monorepo catalog: commits here only change the catalog (AGENTS.md).
- No new abstraction layer, no feature flag keeping the old path, no registry/factory where a switch suffices.
- Each step ends with a one-line test command that proves it.
```

## U5 — Work order → harness execution

```
/make-plan U5 — Work order → harness execution

Target: Work order → harness execution. Single entry point: `mise run wo:dispatch -- <wo>`.
Evidence: /home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s2-run.md; /home/skogix/Work/doc/pathfinder-2026-11-14/02-duplication-report.md; /home/skogix/Work/doc/pathfinder-2026-11-14/03-unified-proposal.md section U5.
Owner rules: mise first, mise tasks as the interface, skogfences (agents are unix users, /skogai shared, .skogai submodule, human $HOME sacred), working first then harden, merge to master when done.

Call sites to rewrite (paths under ~/Work/repos/ unless absolute):
- `skogai2-skogai-runner/.skogai/workorders/WORKORDERS.md:20-29`: replace with a link to `skogai2-skogai/orchestration/work-orders/SPECIFICATION.md`; rename `done/` to `completed/`
- New task `wo:dispatch`: check that `owns` sets are disjoint, map WO→harness plan (`name`, body→`task`, `reads`→`seedPaths`), call `harness/.../orchestrate-worktrees.js` (plan input at `:37-42`)
- `skogai2-skogai/.skogai/rules/herdr-orchestration.md:21`: retract the 'authoritative' claim and point to harness
- Dispatch prompt: one template replacing `WORKORDERS.md:41` and `SPECIFICATION.md:164-185`
- Project name: `get-project-name.sh:7` and `harness/bin/skogcli:2` move to `basename $(dirname $(git rev-parse --path-format=absolute --git-common-dir))`
- `dash-skogai/bin/check-skogai-routes` and `dash-skogai/mise.toml:21-23`: delete; `skogai2-config/bin/check-routes` is the one checker
- One worktree root: pick the harness sibling default or `~/.herdr/worktrees`; update `~/.config/worktrunk/config.toml:48` and `skogai2-config/agents/herdr.md:135-137` to match

Anti-pattern guards:
- Do not add `owns` enforcement inside harness (an ECC fork); keep it as a pre-dispatch check.
- Pane (herdr/tmux) vs headless (`claude -p`) are launcher modes of one dispatch, not two systems.
- Initialize the `harness/marketplace/plugins/skogharness` submodule and trace `executePlan` before relying on it (gap in s2).
- No new abstraction layer, no feature flag keeping the old path, no registry/factory where a switch suffices.
- Each step ends with a one-line test command that proves it.
```

## U6 — Hooks and journal: one runtime per level

```
/make-plan U6 — Hooks and journal: one runtime per level

Target: Hooks and journal: one runtime per level. Single entry point: R: `skogai2-marketplace/plugins/skogai-core/hooks/hooks.json`; A: skogharness session-data.
Evidence: /home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s6-plugins.md, s4-dot.md; /home/skogix/Work/doc/pathfinder-2026-11-14/02-duplication-report.md; /home/skogix/Work/doc/pathfinder-2026-11-14/03-unified-proposal.md section U6.
Owner rules: mise first, mise tasks as the interface, skogfences (agents are unix users, /skogai shared, .skogai submodule, human $HOME sacred), working first then harden, merge to master when done.

Call sites to rewrite (paths under ~/Work/repos/ unless absolute):
- `~/.claude/settings.json:154-158`: remove the `journal_path`/`state_dir` overrides (journal back to `.skogai/journal.md`, out of `logs/`)
- `~/Work/.skogai/logs/journal.md` (875 lines) vs `~/Work/.skogai/journal.md`: owner decides whether to merge
- `skogai2-skogai/.claude/hooks/*`, `skogai2-skogai-runner/.claude/hooks/*` (VV, drifted): replace with plugin hooks; `.harness/claude-progress.txt` retires
- `skogai2-marketplace/plugins/skogai-core/scripts/git-steps.sh`: scope stage/commit/merge to the session's start repo
- Lesson matchers: keep one of `harness/scripts/match-lessons.py`, `harness/marketplace/plugins/skoghooks/hooks/lesson_matcher.py`, `harness/marketplace/plugins/skogix-hooks/hooks/lesson_matcher.py`; fix `dot-skogai/SKOGAI.md:51,79`

Anti-pattern guards:
- Features stay off by default, configured through native mod settings with the log location included (owner rule).
- Never two runtimes writing repo-level journals. Q1 (skogai-core vs skogharness at R) must be answered first; this prompt assumes skogai-core.
- skoghooks stays on hold: do not delete it.
- No new abstraction layer, no feature flag keeping the old path, no registry/factory where a switch suffices.
- Each step ends with a one-line test command that proves it.
```

## U7 — .skogai layout and bootstrap = skogai2-dot-skogai

```
/make-plan U7 — .skogai layout and bootstrap = skogai2-dot-skogai

Target: .skogai layout and bootstrap = skogai2-dot-skogai. Single entry point: `mise run skogai:init` → `git submodule add <skogai2-dot-skogai> .skogai`.
Evidence: /home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s4-dot.md; /home/skogix/Work/doc/pathfinder-2026-11-14/02-duplication-report.md; /home/skogix/Work/doc/pathfinder-2026-11-14/03-unified-proposal.md section U7.
Owner rules: mise first, mise tasks as the interface, skogfences (agents are unix users, /skogai shared, .skogai submodule, human $HOME sacred), working first then harden, merge to master when done.

Call sites to rewrite (paths under ~/Work/repos/ unless absolute):
- `skogai2-dot-skogai`: add the layout template from `skogai2-skogai/.skogai/README.md:7-20`
- Mark historical: `skogai2-dash-skogai@ad32ed3^:knowledge/layout.md:27-40`, `dot-skogai/SKOGAI.md:28-41`
- `skogai2-cli/PKGBUILD:29`: `/usr/share/skogai/base` stays as the W-level default the submodule overrides
- Uninstall the stale `skogai-runner-git` package (ships the deleted `src/core/main.sh`)
- `wiki/decisions/`: renumber the duplicate `adr-002`

Anti-pattern guards:
- Do not move existing `.skogai/` dirs in the 25 repos in this plan; template first.
- Do not invent a config file format (skogfences: 'not a config file format').
- Owner calls are not decided here: dot-skogai data migration, OpenWiki, canonical decision store.
- No new abstraction layer, no feature flag keeping the old path, no registry/factory where a switch suffices.
- Each step ends with a one-line test command that proves it.
```

## U8 — Plugins and docs

```
/make-plan U8 — Plugins and docs

Target: Plugins and docs. Single entry point: `skogai2-marketplace` + `code-docs-lookup/scripts/sync-docs.sh`.
Evidence: /home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s6-plugins.md; /home/skogix/Work/doc/pathfinder-2026-11-14/02-duplication-report.md; /home/skogix/Work/doc/pathfinder-2026-11-14/03-unified-proposal.md section U8.
Owner rules: mise first, mise tasks as the interface, skogfences (agents are unix users, /skogai shared, .skogai submodule, human $HOME sacred), working first then harden, merge to master when done.

Call sites to rewrite (paths under ~/Work/repos/ unless absolute):
- `skogai2-skogai/.skogai/scripts/claude-code-documentation.sh`: delete
- `skogai2-skogix/plugins/skogdocs/.claude-plugin/marketplace.json`: delete (nested duplicate)
- `skogai2-marketplace/external-repos.json`: publish `code-docs-lookup`
- `code-docs-lookup/scripts/sync-docs.sh:80-85`: make the cache replace atomic (temp dir + mv)
- `skogai2-docs`, `skogai2-marketplace/docs/`: owner decides between pointer and delete

Anti-pattern guards:
- Do not delete the skoghooks entry anywhere until its home in `harness/marketplace/plugins/skoghooks` is confirmed.
- Old `marketplace`/`skogai-core` repos are retired via the retirement list, not edited.
- No new abstraction layer, no feature flag keeping the old path, no registry/factory where a switch suffices.
- Each step ends with a one-line test command that proves it.
```

## U9 — Services = podman; health = one task

```
/make-plan U9 — Services = podman; health = one task

Target: Services = podman; health = one task. Single entry point: `podman` quadlets + `mise run health` → `skogai2-config/bin/health`.
Evidence: /home/skogix/Work/doc/pathfinder-2026-11-14/01-flowcharts/s7-services.md; /home/skogix/Work/doc/pathfinder-2026-11-14/02-duplication-report.md; /home/skogix/Work/doc/pathfinder-2026-11-14/03-unified-proposal.md section U9.
Owner rules: mise first, mise tasks as the interface, skogfences (agents are unix users, /skogai shared, .skogai submodule, human $HOME sacred), working first then harden, merge to master when done.

Call sites to rewrite (paths under ~/Work/repos/ unless absolute):
- `cloudflare/old-systemd-solution/`: delete
- `systemd` repo: archive (0 of 26 units installed); port anything worth keeping to a quadlet
- `podman/units/{quadlet-health,pg-backup}-notify.service`, `~/.config/skogai/machine/units/skogai-health-notify.service`: one `notify@.service`
- `cloudflare/pangolin/a.yml`: delete (≡ `docker-compose.yml`)
- `systemd/user/{pg-backup,quadlet-health}*` symlinks: delete with the repo
- Root `cloudflared.service`: owned by skogai2-config
- Later (hardening): `cloudflare/pangolin/{NEWT.env,newt.quadlet.container:9}` → fnox, rotate

Anti-pattern guards:
- Do not fix the `skognet-cloudflare` IPAM incident in this plan; it is a separate ops task.
- Do not touch other machines.
- Never delete working dirs or unpushed work: archive repos, don't rm them.
- No new abstraction layer, no feature flag keeping the old path, no registry/factory where a switch suffices.
- Each step ends with a one-line test command that proves it.
```

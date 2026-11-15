# 00 — Feature inventory (Phase 0, pending owner approval)

Scope: `~/Work/repos/` (32 repos). A "feature" here is a concern that cuts across repos.

**Excluded, with evidence:**

- **Vendored:**
  - `repomix`: an upstream fork. The owner's commits are only merges.
  - `skogai2-docs`: a mirror of the Claude Code docs.
  - `skogai2-aliasflare`: a fork of charleswei118/aliasflare.
  - `skogai2-skogai-fleet/inspiration/`.
- **Archive:** `docs` is now **in scope** at the owner's request (2026-11-14), feeding F13. `docs/merge` and the personas may hold concepts worth mapping.
- **Placeholders:** `skogai` (future monorepo), `skogai2-dot-skogai`, `skogix` (backlog only).
- **Out of scope:** `skogai2-skogpunk` (Kotlin RPG app).

| # | Feature | Live implementation | Superseded / dormant copies | Key entry points |
|---|---|---|---|---|
| F1 | Fleet control plane / repo registry | skogai2-core (`.skogai/repo/repos.toml`) | core (identical Argcfile), dash-skogai/fleet `repos.csv`, skogai-nov10 `config/repos.csv` | `core/Argcfile.sh:35-171` |
| F2 | Settings resolution / `SKOGAI_*` env | mise-plugin | skogai2-cli `bin/config`, skogai2-marketplace `scripts/config`, runner `best-argc-version/modules/core`, skogai2-skogai `dash-skogai/Argcfile.sh` | `mise-plugin/hooks/mise_env.lua:14-18`, `skogai2-cli/bin/config:9-93` |
| F3 | Machine config, dotfiles, secrets (+ the old workstation notes) | skogai2-config, nvim-omarchy | skogai-nov10 `WORKSTATION.md` and `config/` | `skogai2-config/bin/health` |
| F4 | `/skogai` shared workspace: agent users and launchers | skogai2-dash-skogai (**owner decision: owns /skogai**). skogai2-skogix's claim is to be corrected | dash-skogai | `skogai2-dash-skogai/admin/*.sh`, `skogai2-skogix/mise.toml:2-11` |
| F5 | `.skogai` folder and routing-file convention | skogai2-skogai-routing | skogai-routing, dot-skogai, `check-routes` ×2 | `skogai2-skogai-routing/skills/skogai-routing/SKILL.md` |
| F6 | Plugin marketplace and packaging | skogai2-marketplace | marketplace, skogai-core marketplace, skogix marketplace | `skogai2-marketplace/.claude-plugin/marketplace.json` |
| F7 | Hook runtime and session journal | skogai2-marketplace `plugins/skogai-core` | old marketplace skoghooks, skogai-core | `plugins/skogai-core/hooks/hooks.json` |
| F8 | jq transform skill | skogai-jq | marketplace/skogai-jq (stale), skogai-core (retired 11-14) | `skogai-jq/SKILL.md` |
| F9 | Agent orchestration / work orders | skogai2-skogai (herdr + type system) | dash-skogai paseo, skogai-nov10 gptodo, skogai2-skogai-fleet personas | `skogai2-skogai/orchestration/README.md:3-23` |
| F10 | Module runner framework (`usage` CLI) | skogai2-skogai-runner (mid-teardown) | `best-argc-version/` | `skogai2-skogai-runner/mise.toml:8-17` |
| F11 | Service runtime (quadlets, units) | podman | systemd, `cloudflare/old-systemd-solution` | `podman/mise-tasks/setup/*`, `systemd/bin/*` |
| F12 | Cloudflare and network edge | cloudflare | (aliasflare is a submodule) | `cloudflare/mise.toml:13-17` |
| F13 | Knowledge / memory / wiki store | the skogai2 repos' `.skogai/` | dot-skogai, wiki, docs, `openwiki/` ×5 | `dot-skogai/mise.toml:16-41` |
| F14 | Claude Code docs mirror and lookup | skogai2-skogix `plugins/skogdocs` | skogai2-docs, `claude-code-documentation.sh` ×3, marketplace `download-docs.sh`, skogai-nov10 tmp | — |

**Headline duplication, before Phase 2:**

- F2 has 4–5 config implementations.
- F14 has about 6 docs-mirror copies.
- F1 has 3 registries.
- F4 has 2 repos claiming `/skogai`.
- The F11 units are duplicated between podman and systemd.

## Proposed Phase 1 fan-out: 6 flowchart agents, grouped by coupling
1. F1 + F10: registry, control plane, runner
2. F2 + F3: settings, env, machine config
3. F4 + F5: workspace and the `.skogai` convention
4. F6 + F7 + F8: marketplace, hooks, jq
5. F9 + F13 + F14: orchestration, knowledge, docs
6. F11 + F12: services and edge

---

## Revision 1: owner adjustments (2026-11-14)

The owner gave three inputs:

1. **The env is one plane.** It spans runner, machine/workstation, configuration and how the CLI works, all the way out to remote containers. That is why mise and the CLI modules are central.
2. **Runner, orchestration, modules and routing are tightly coupled.**
3. **skogfences** (`skogfences-reference.md`) is the intent behind the dash/dot split:
   - Agents are unix users with their own homes.
   - `/skogai` (**dash-skogai**) is the setgid shared common ground.
   - `.skogai` (**dot-skogai**) is the base config. It is also a submodule that bootstraps any project into SkogAI.
   - The human's `$HOME` is sacred.

The 14 features collapse into **7 systems**. These replace the F-numbers for Phase 1–4.

| System | Was | Concern | Repos |
|---|---|---|---|
| **S1 ENV**: environment and settings plane | F2 + F3 + the env half of F10 | One way to resolve `SKOGAI_*` and config scopes, identically on the workstation, in agent homes, in the runner and in remote containers | mise-plugin, skogai2-cli, skogai2-config, skogai2-marketplace `scripts/config`, runner `best-argc-version/modules/core` + Containerfile, skogai2-skogai `dash-skogai/Argcfile.sh`, skogai-nov10 `config/`, nvim-omarchy (personal leaf) |
| **S2 RUN**: execution plane | F5-routing + F9 + F10 | Modules (`usage` CLI), the routing-file walk, work orders, herdr worktree and pane orchestration, personas | skogai2-skogai-runner, skogai2-skogai (orchestration + type system), skogai2-skogai-routing, skogai-routing, skogai2-skogai-fleet, dash-skogai paseo, skogai-nov10 gptodo |
| **S3 DASH**: `/skogai` shared ground and agent homes (skogfences) | F4 | The setgid `/skogai`, the `skogai` group, agent unix users and homes, clean-env launchers, the coordination DB | **skogai2-dash-skogai (owner)**, skogai2-skogix (launchers, per-agent config dirs; its "/skogai" claim must be corrected), dash-skogai (old) |
| **S4 DOT**: `.skogai` base config, project bootstrap, knowledge | the F5 folder half + F13 | The `.skogai/` layout in 15 repos, the bootstrap-submodule idea, journal/memory/decisions, the wiki and docs archive, `openwiki/` | dot-skogai, skogai2-dot-skogai (empty), wiki, docs (in scope), every `.skogai/` |
| **S5 FLEET**: repo registry and control plane | F1 | Discovering, registering, cloning and checking repos, plus worktree/review/PR contexts | skogai2-core, core, dash-skogai/fleet, skogai-nov10 `config/repos.csv`, plus the monorepo's `mani.yaml` (the fourth registry) |
| **S6 PLUGINS**: marketplace, hooks, skills, docs lookup | F6 + F7 + F8 + F14 | Packaging and distributing Claude/Codex plugins, the hook journal runtime, jq, the CC docs mirror | skogai2-marketplace, marketplace, skogai-core, skogai-jq, skogai2-skogix skogdocs, skogai2-docs |
| **S7 SERVICES**: runtime services and edge | F11 + F12 | Quadlets, user units, Cloudflare tunnels/DNS/Workers, the Pangolin edge | podman, systemd, cloudflare (+ old-systemd-solution), skogai2-aliasflare |

**Coupling to trace in Phase 1:**

- S1 → S2: the runner consumes the env.
- S3 ↔ S4: dash is the shared ground and dot is the per-project config.
- S5 → S2: the registry feeds worktrees and work orders.
- S6 → S4: the hooks write `.skogai/journal`.

**Phase 1 fan-out:** 7 flowchart agents, one per system.

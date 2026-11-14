# Repo survey 2026-11-14: state and open questions

Source: 29 read-only survey threads in T3 Code (project Monorepo, titles "survey: <name>"), one per catalog entry in `mani.yaml`, run on skogix-workstation on 2026-11-14, plus the six threads of the mani migration. Everything below is what those agents reported from local clones. Nothing was built, tested or run unless a line says so. Dates are the latest commit each survey saw.

## 1. Decisions that cut across repos

### 1.1 skogai or skogai2: which copy is canonical

Asked by almost every survey. Fourteen names exist in both orgs or only in skogai2.

| Name | skogai | skogai2 | What the survey saw |
|---|---|---|---|
| core | fe89231, 2026-10-24 | 13 commits ahead, WIP, 2026-11-09 | skogai2 is a direct continuation; skogai head is an ancestor |
| skogai-routing | dormant, WIP, 2026-09-27, v1 archived under .old/ | 0.1.0, installable skill, 2026-10-31 | skogai2 looks like a streamlined restart |
| marketplace | broad, many plugins, 2026-09-27 | one local plugin (skogai-core v0.10.0) plus five external, 2026-11-13 | no shared commits; reimplementation |
| dash-skogai | "global source of truth" hub, 2026-09-20 | /skogai shared infrastructure, WIP, 2026-11-01 | same stated purpose, different implementation |
| dot-skogai | 623 files, 403 commits, 2026-09-27 | three files, "nothing built yet", 2026-11-01 | minimal restart of the same concept |
| skogix | backlog repo: README and .skogai/todo.list | personal agent-config workspace built for /skogai, WIP, 2026-11-09 | different roles, no shared commits |
| skogai | one-commit README placeholder, 2026-11-10 | orchestration workspace (Herdr, dash types, memory), 2026-11-10 | not duplicates; skogai2 may be what the monorepo replaces |
| docs | 2,536-file knowledge archive, 2026-10-06 | Claude Code and Agent SDK docs snapshot, 2026-10-25 | separate collections |
| cli | not cloned | clean-room rework, one module (skogai-config), 2026-10-24 | describes itself as the successor |
| config | not cloned | agent-oriented machine-config guide, 2026-11-14 | relationship not established |
| skogai-fleet | not cloned | persona redesign of the Nelson plugin, 2026-10-24 | relationship not established |
| skogai-runner | "Repository not found" | Bash command-runner rebuild, 2026-11-09 | skogai2 only |
| aliasflare | not cloned | Cloudflare Workers email alias service, 2026-11-07 | README still links upstream charleswei118/aliasflare |
| skogpunk | not cloned | Android RPG prototype, 2026-11-11 | relationship not established |

Question: for each row, which org is canonical, and is the other copy archived, pointed at the canonical one, or kept as a separate thing?

### 1.2 Fleet control: core or mani

`core` and `skogai2-core` are a Bash/argc control plane for the repo fleet (discovery, registration, status, worktrees, work contexts, a proposed workorder and dispatch design). The monorepo now does catalog and fetch with mani and mise.

- Does `core` continue alongside mani/mise, get reconciled with it, or get retired?
- Is the handover proposal for workorders and dispatch still current?
- Should dispatch live in core or in the runner, and start local-only or include cloud agents?

### 1.3 Where shared knowledge and "global truth" live

`dash-skogai`, `dot-skogai`, `skogai-nov10`, `docs` and `skogai2-skogai` each claim part of this role.

- Which of them is authoritative, and which are archives to mine for parts?
- Which decisions, configs, research projects and unfinished tasks still need migrating out of the older ones?

### 1.4 The /skogai path

`skogai2-skogix` and both `dash-skogai` copies assume they live at `/skogai`. Does `/skogai` remain a requirement?

## 2. Per repo

### skogai org

- **cloudflare** (active, 2026-11-13). Ops repo for the Cloudflare account: tunnels, DNS, Access, email routing, inventories. Questions from its TODO.md: are the token rotation and the missing email MX records still unresolved; should mcp.skogai.se sit behind Access or stay public with its own auth; which tunnels are kept, revived or retired; should Aliasflare work use the submodule or the standalone catalog clone?
- **core** (2026-10-24). See 1.2. Also: stay `skogai/core` or move to skogai2?
- **dash-skogai** (dormant, 2026-09-20). See 1.1 and 1.3. Also: are its fleet snapshots, CLI wrappers, Dolt layer and generated wiki still wanted? Its own todo.list records stale references and conflicting descriptions of its role.
- **docs** (2026-10-06). Knowledge and history archive; CLAUDE.md describes directories that have moved. Questions: maintained knowledge base or historical archive; which of merge/, todo/ and skogix/ is authoritative; move material into newer repos, or add a root index and a consolidation plan?
- **dot-skogai** (quiet, 2026-09-27). Agent workspace; guidance and mise tasks reference a missing Argcfile.sh, argc/, agents/ and tools/. Questions: canonical workspace or legacy snapshot; did the executable tooling move to core; how do its responsibilities differ from dash-skogai and the new bootstrap repo?
- **mise-plugin**. Sets five variables (SKOGAI_MONOREPO_DIR, SKOGAI_CONFIG_DIR, SKOGAI_HOST, SKOGAI_OS, SKOGAI_ARCH) and optionally prepends paths. Owner stated: Linux only is the planned scope. No open question recorded.
- **nvim-omarchy** (2026-11-13). Personal Neovim config on LazyVim as shipped by Omarchy. Questions: is this the canonical desktop config; should it work on machines without Omarchy; should its external bootstrap and desktop docs be available alongside it?
- **podman** (active, 2026-11-14). Rootless Podman Quadlets: basic-memory Postgres, MCPHub, Cloudflare tunnel, Termix. Owner direction given in the thread: the reusable concept is containers behind podman networks whose only way out is a tunnel (Cloudflare, Tailscale, NetBird); the networks are the important part. Open: does "only way out" mean ingress, egress or both, and what enforces it; should the paused secrets-recovery work resume (PLAN.md leaves the age recipients undecided); is fixing Termix command execution against fish a priority?
- **skogai** (2026-11-10). Empty placeholder. Questions: what role should it have beside monorepo and skogai-core; reserved, awaiting migration, or unnecessary; if kept, what should its README say?
- **skogai-core** (quiet, 2026-09-11). Claude Code plugin marketplace and routing framework, unfinished migration, CLAUDE.md references a missing plugins/ path. Questions: still the canonical home for the routing framework and marketplace; where do hooks and their tests belong; is the next priority finishing the migration, documenting installation, or archiving? Open PR: skogai/skogai-core#6 replaces the duplicated jq skill with a pointer; left open because core's validator reports a pre-existing failure in untouched content.
- **skogai-jq**. Now documented as the canonical jq skill (skogai/skogai-jq#1, merged). All 70 transform suites pass with jq 1.8.2. Live harness installation untested.
- **skogai-nov10** (dormant, 2026-10-24). Older knowledge and configuration hub; the name does not match its latest commit date. Questions: archive, or does any part stay authoritative; which decisions, configs, research projects and tasks still need migration; should references to skogai/skogai, ~/core and global tools be updated or left as history?
- **skogai-routing** (dormant, 2026-09-27). See 1.1. Also: is the next deliverable a specification, an installable skill, or working tooling; are "concept" and "tag" distinct owner types (the notes leave this open)? CONTEXT.md links to a missing definitions.md.
- **skogix** (2026-11-11). Backlog: 15 unchecked items in .skogai/todo.list. Questions: does this stay the intake backlog with items promoted to GitHub issues; which entries are already done or superseded by the monorepo; does it need a short purpose README?
- **systemd** (quiet, 2026-09-27). User-level systemd units and startup wrappers. Questions: still the authoritative source for deployed user services, and on which machines; which older non-prefixed services stay supported; should service metadata and health checks cover the full inventory (services.json covers three); machine-specific on purpose, or reproducible through mise?

### skogai2 org

- **skogai2-aliasflare** (2026-11-07). See 1.1. Also: is the deployment mentioned in the journal still used, and who owns its domain and Cloudflare resources; is the next need maintenance, deployment verification or consolidation?
- **skogai2-cli** (2026-10-24). See 1.1. Also: should its mise-based settings model carry into SkogAI 3.0; which roadmap item (module runner, base versioning, typed modules) is still relevant?
- **skogai2-config** (active, 2026-11-14). See 1.1. Also: is the isolated bootstrap/adopt test environment the next priority (fresh-machine bootstrap is untested); which workstation-specific assumptions should become portable; is the noted leaked-file history cleanup still outstanding?
- **skogai2-core** (WIP, 2026-11-09). See 1.1 and 1.2. Also: which parts stay in the older org?
- **skogai2-dash-skogai** (WIP, 2026-11-01). See 1.1. README describes knowledge/, fish/ and a gptme-contrib submodule that are absent. Question: are those intentionally retired or still needed; should the older docs and fleet tooling survive?
- **skogai2-docs** (2026-10-25). Two-commit docs snapshot. Question: maintained or archived?
- **skogai2-dot-skogai** (2026-11-01). Placeholder for a portable .skogai bootstrap folder. Questions: should it replace the older workspace; which older pieces belong in a portable bootstrap; is implementation still wanted?
- **skogai2-marketplace** (active, 2026-11-13). See 1.1. Also: should older plugins migrate or stay separate; add an entry-point README; are the pending user-message logging and documentation-refresh tasks still wanted?
- **skogai2-skogai** (2026-11-10). See 1.1. Question: which parts survive (Herdr workflows, dash types, memory, harness)?
- **skogai2-skogai-fleet** (2026-10-24). Seventeen crew personas, links in SKOGAI.md look outdated. Questions from its TODO.md: which harness or runner loads these personas, and how; do the persona profiles or references/crew-roles.md define responsibilities (they disagree); which proposed persona, tooling and model changes proceed?
- **skogai2-skogai-routing** (2026-10-31). See 1.1. Also: does 0.1.0 stay a documentation and skill convention, or does validation tooling follow?
- **skogai2-skogai-runner** (2026-11-09). Main source tree holds one file after a deliberate reset; docs and packaging reference deleted entrypoints. Questions: continue the remake, or restore pieces of best-argc-version/; which config-storage decisions are settled?
- **skogai2-skogix** (WIP, 2026-11-09). See 1.1 and 1.4. Questions: legacy workspace to extract from, or a setup to maintain; which configurations and plugins move into SkogAI 3.0?
- **skogai2-skogpunk** (2026-11-11). HANDOVER.md recommends starting a browser game while the repo already holds an Android implementation. Questions: is Android the intended direction; keep the browser-game handover as history or replace it?

## 3. Open items from the mani migration

Merged: monorepo #51 (mani catalog, submodules removed), #52 (lazy catalog: `sync: false`, one tag per project, `/repos/` ignore), #53 (AGENTS.md cache: `agents/<name>.md`, `mise run agents:sync`), #54 (skogai2 repos added).

- **Catalog scope.** Still unanswered from thread 1: are forks, archived and private repos in or out, and is the Skogix user account included? Counts at the time: skogai 79 non-fork active (32 public, 47 private), Skogix 86, skogai2 24.
- **Catalog generation.** Skogix wrote "is needed as tasks in mani itself via mise"; the thread could not tell what it referred to. Should regenerating `mani.yaml` from `gh repo list` be a mani task wrapped by mise?
- **ADR.** Deferred "until repos get added". Repos are added now; ADR 0003 for the manifest design is due.
- **AGENTS.md cache coverage.** The cache is filled by cloning and copying, so a repo has no entry until it has been cloned once. When last checked only mise-plugin and skogai-jq had a root AGENTS.md; several surveyed repos use SKOGAI.md or CLAUDE.md as their entry point instead. Should the cache also take SKOGAI.md or CLAUDE.md when AGENTS.md is missing or only a pointer?
- **Orphan cache files.** A repo removed from `mani.yaml` leaves its `agents/<name>.md` behind; nothing removes it.
- **Not verified.** The remote-container path (`mise install`, then the tag fetch); cloning a private repo without workstation credentials; `git push --dry-run` as a read-only check.
- **skogai/skogix.** Branch `create-todo-list-issues` (commit 72395d3, the todo.list source audit) is pushed but has no PR and is not merged. Its notes still say "submodules".
- **skogai/skogai-core#6.** Open, waiting for review.

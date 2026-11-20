# skogai/monorepo

The map of the SkogAI repos plus the shared setup every agent works in: the repo catalog, cached agent instructions, a wiki, the mise environment, agent harness wiring, T3 Code tooling, and the decision record. Code changes to the catalogued repos happen in those repos; this repo plans and tracks them.

## Keep the list of SkogAI repos {#catalog}
tech: mani catalog (mani.yaml), lazy clones into repos/ (git-ignored)
needs: [mise-env]
links: [agents-cache, openwiki, fleet-fixes]
files: [mani.yaml, .gitignore]
- [x] List every SkogAI repo with its path and URL in one file {#catalog-list}
  tech: mani.yaml — 29 projects, each tagged with its own name
- [x] Clone a single repo on demand by name {#catalog-clone-one}
  tech: mani.yaml tags == names; .skogai/tests/2026-11-14-mani-lazy.md (pass)
- [x] Drop the archived repos from the list {#catalog-drop-archived}
  tech: commit 645a309 removed core, dash-skogai, skogai-core, skogai-routing, skogai-nov10
- [x] Make a bare `mani sync` clone nothing again {#catalog-all-lazy}
  tech: mani.yaml — skogai-events and skogfleet flipped to `sync: false`; every project is now lazy
  by: claude
- [ ] Regenerate the list from GitHub instead of by hand {#catalog-generate}
  tech: gh repo list → mani.yaml as a mise-wrapped task (doc/questions.md Q2.5)
  from: roadmap
- [ ] Decide which forks, archived, private and Skogix-account repos belong in the list {#catalog-scope}
  tech: doc/questions.md Q2.4
  from: roadmap
- [ ] Check the workstation's ~/.local/src clones against the list {#catalog-inventory}
  tech: issue #86 (Pathfinder U4)
  from: roadmap

## Copy each repo's agent instructions here {#agents-cache}
tech: mani task agents-cache + mise task agents:sync → agents/<name>.md
needs: [catalog]
links: [agent-wiring, openwiki]
files: [agents/**]
- [x] Cache every cloned repo's root AGENTS.md so it can be read without cloning {#agents-cache-copy}
  tech: mani.yaml tasks.agents-cache; mise.toml tasks."agents:sync"; agents/ holds 15 files
- [x] Remove a cached copy when the repo no longer has an AGENTS.md {#agents-cache-prune-missing}
  tech: mani.yaml agents-cache `rm -f "$d/$n.md"` branch
- [x] Route the harness repo to its real entry doc {#agents-cache-harness}
  tech: agents/harness.md (commit 53f28a0)
- [ ] Fall back to SKOGAI.md or CLAUDE.md when a repo has no AGENTS.md {#agents-cache-fallback}
  tech: doc/questions.md Q2.7
  from: roadmap
- [ ] Delete cached copies of repos that left the list {#agents-cache-orphans}
  tech: doc/questions.md Q2.9 — nothing removes them today; agents/systemd.md is one
  from: roadmap

## Write a wiki of the active repos {#openwiki}
tech: openwiki/ pages + OpenWiki CLI GitHub Action
kind: knowledge
needs: [catalog]
links: [decisions]
files: [openwiki/**, .github/workflows/openwiki-update.yml]
- [x] Write one page per covered repo plus cross-repo pages {#openwiki-pages}
  tech: openwiki/repos/*.md (22), openwiki/concepts/*.md, openwiki/index.md
- [x] Fold the old per-repo wikis in {#openwiki-fold}
  tech: commit 59019a2 (PR #67)
- [x] Add a workflow that regenerates the wiki and opens a PR {#openwiki-workflow}
  tech: .github/workflows/openwiki-update.yml (manual; schedule unarmed)
- [ ] Run the regeneration once and review the result {#openwiki-first-run}
  tech: workflow header: "Not run yet"
  from: roadmap
- [ ] Point the generator at a local LM Studio model instead of an OpenAI key {#openwiki-lmstudio}
  tech: LM Studio server is running (owner, 2026-11-20); workflow still requires OPENAI_API_KEY
  from: roadmap

## Set up the shared mise environment {#mise-env}
tech: mise.toml, .miserc.toml, .config/mise/conf.d/*, skogai mise plugin
links: [catalog, agent-wiring, t3]
files: [mise.toml, mise.lock, .miserc.toml, .config/mise/conf.d/plugin.*.toml, .config/mise/conf.d/termix.toml, .config/mise/mise.lock, doc/mise.md, doc/github-auth.md]
- [x] Load the pinned skogai plugin in every environment {#mise-plugin-pin}
  tech: .config/mise/conf.d/plugin.skogai.toml (pinned commit); mise.toml `_.skogai`
- [x] Switch to a local mise-plugin clone for development {#mise-develop}
  tech: .config/mise/conf.d/plugin.develop.toml, task plugin:link
- [x] Show and self-test the SKOGAI_ variables {#mise-env-tasks}
  tech: mise.toml tasks env:show, env:test, env:context; .skogai/tests/2026-11-13-mise-env-vars.md
- [x] Log in to GitHub through mise {#mise-github-auth}
  tech: mise.toml tasks."github:auth", settings.github.oauth_client_id; doc/github-auth.md
- [x] Install the shared tools from one pinned list {#mise-tools}
  tech: mise.toml [tools] + mise.lock (gh, usage, hk, mani, jq, uv, python, npm, code-review-graph…)
- [ ] Run mise commands in isolation from the machine's global config {#mise-isolated}
  tech: issue #31 (roadmap 1); README quickstart waits on it
  from: roadmap
- [ ] Give root tasks declared arguments and help {#mise-usage}
  tech: issue #14
  from: roadmap
- [ ] Add git hooks and lint with hk {#mise-hk}
  tech: issue #15 — hk is installed but no hk.pkl exists
  from: roadmap
- [ ] Rebuild workstation setup as a mise bootstrap plus dotfiles {#mise-bootstrap}
  tech: issue #17
  from: roadmap
- [ ] Ship offline mise docs, composed environments and the plugin contract {#mise-roadmap-2-5}
  tech: issues #32, #33, #34, #35
  from: roadmap

## Give every agent harness the same tools {#agent-wiring}
tech: MCP config (mise, atuin, code-review-graph) + hooks + skills per harness
needs: [mise-env]
links: [agents-cache, t3]
files: [AGENTS.md, CLAUDE.md, GEMINI.md, .mcp.json, .claude/**, .codex/**, .gemini/**, .agents/**, .config/mise/conf.d/code-review-graph.toml]
- [x] Connect Claude Code to mise, atuin and the code graph {#wiring-claude}
  tech: .mcp.json; .claude/settings.json crg hooks
- [x] Connect Codex the same way {#wiring-codex}
  tech: .codex/config.toml
- [x] Connect Gemini and Antigravity the same way {#wiring-gemini}
  tech: .gemini/settings.json, .gemini/hooks/*; .agents/plugins/monorepo/* (commit 91b1634)
- [x] Index the code into a searchable graph with local embeddings {#wiring-crg}
  tech: .config/mise/conf.d/code-review-graph.toml (crg:health/status/embed/update/search/daemon); skills in .claude/skills, .gemini/skills
- [x] Show the next thing on the list when the owner says "hi" {#wiring-next}
  tech: mise.toml tasks.next; doc/agent-workflow.md "Starting a session"
- [x] Turn off the old skogai-core journaling plugin {#wiring-disable-core}
  tech: .claude/settings.json `skogai-core@skogai-marketplace: false` (commit a5446c3)
- [ ] Confirm Claude treats AGENTS.md like CLAUDE.md {#wiring-agentsmd}
  tech: issue #41
  from: roadmap
- [ ] Show run context at session start and add it to commits {#wiring-session-context}
  tech: issue #40 — env:context --trailers exists, nothing calls it
  from: roadmap

## Drive T3 Code threads from the terminal {#t3}
tech: mise t3:* tasks over the T3 CLI and its SQLite state, gum picker
needs: [mise-env]
links: [agent-wiring]
files: [.config/mise/conf.d/t3.toml, scripts/t3-picker.py, .skogai/tests/test_t3_picker.py, doc/t3-cli.md, doc/t3-code-mcp.md, doc/t3code/**, t3]
- [x] List, read, start and send to threads with mise tasks {#t3-tasks}
  tech: .config/mise/conf.d/t3.toml (t3:info/status/health/projects/threads/show/start/send/init)
- [x] Pick a thread interactively {#t3-picker}
  tech: scripts/t3-picker.py; .skogai/tests/test_t3_picker.py
- [x] Run the backend from ~/.t3 like the desktop app {#t3-home}
  tech: t3.toml T3CODE_HOME; commit for PR #60
- [x] Keep a local copy of the T3 Code docs {#t3-docs}
  tech: doc/t3code/** with UPSTREAM.md; doc/t3-cli.md

## Record decisions and open questions {#decisions}
tech: ADRs, questions file, surveys, research notes, dated experiment records
kind: knowledge
links: [fleet-fixes, mise-env, openwiki]
files: [doc/adr/**, doc/questions.md, doc/surveys/**, doc/agent-workflow.md, doc/skogai-core-plugin.md, doc/small-hours-game-contract.d.ts, README.md, .skogai/**, PLAN.md]
- [x] Record the starting tools and the mise source as decisions {#decisions-adr-1-2}
  tech: doc/adr/0001-starting-tools.md, doc/adr/0002-mise-binary-and-tool-source.md
- [x] Collect everything waiting on the owner in one file {#decisions-questions}
  tech: doc/questions.md incl. "Decisions of 2026-11-19"
- [x] Survey all repos once {#decisions-survey}
  tech: doc/surveys/2026-11-14-repo-survey.md
- [x] Keep dated evidence of every experiment {#decisions-evidence}
  tech: .skogai/tests/2026-11-1*.md (16 records)
- [ ] Write ADR 0003 for the catalog design (mani, unpinned, lazy) {#decisions-adr-3}
  tech: doc/questions.md Q2.6
  from: roadmap
- [ ] Pick one store for decision records {#decisions-store}
  tech: issue #96
  from: roadmap
- [ ] Move the turn journal to skogai-events with its path set by an env var {#decisions-journals}
  tech: issues #87, #88 — today skogai-core writes .skogai/logs/journal.md (the spammable journal) via a plugin setting; .skogai/journal.md is the older one; doc/journal.md does not exist yet
  from: roadmap
- [x] Record the owner's 2026-11-20 answers {#decisions-2026-11-20}
  tech: doc/questions.md "Decisions of 2026-11-20"
  by: claude
- [ ] Answer the remaining repo housekeeping questions {#decisions-housekeeping}
  tech: doc/questions.md section 2 — Q2.8 and Q2.11 answered; the rest carry a recommendation and wait on the owner
  from: roadmap
- [x] Re-check every open question against the source and drop the closed ones {#decisions-questions-refresh}
  tech: doc/questions.md "Refresh of 2026-11-20"; .skogai/tests/2026-11-20-fetch-checks.md (Q2.11 checks run)
  by: claude

## Fix duplication across the SkogAI repos {#fleet-fixes}
tech: Pathfinder 2026-11-14 proposal → GitHub milestones U1–U9 (issues #68–#105, project 4); commits land in the child repos
needs: [catalog, decisions]
links: [mise-env]
files: [doc/pathfinder-2026-11-14/**]
- [x] Map the duplication and write a unified proposal {#fleet-pathfinder}
  tech: doc/pathfinder-2026-11-14/00-features.md … 03-unified-proposal.md
- [x] File every remaining fix as an issue under its milestone {#fleet-issues}
  tech: gh issue list: #68–#105 open with milestones U1–U4, U6–U9
- [ ] Use one resolver for SKOGAI_ variables everywhere (U1) {#fleet-u1}
  tech: issues #68–#74
  from: roadmap
- [ ] Make an agent's identity its unix user (U2) {#fleet-u2}
  tech: issues #75–#81
  from: roadmap
- [ ] Turn repo scripts into mise tasks (U3) {#fleet-u3}
  tech: issues #82, #83
  from: roadmap
- [ ] Make mani.yaml the only repo registry (U4) {#fleet-u4}
  tech: issues #84–#86
  from: roadmap
- [ ] Give hooks and the journal one runtime in skogai-events (U6) {#fleet-u6}
  tech: issues #87–#91
  from: roadmap
- [ ] Settle one .skogai layout and bootstrap (U7) {#fleet-u7}
  tech: issues #92–#96
  from: roadmap
- [ ] Remove duplicate plugins and docs fetchers (U8) {#fleet-u8}
  tech: issues #97–#101
  from: roadmap
- [ ] Run services under podman with one health task (U9) {#fleet-u9}
  tech: issues #102–#105
  from: roadmap
- [ ] Dispatch work orders to the harness (U5) {#fleet-u5}
  tech: deferred 2026-11-19 until the harness works; work goes issue → PR directly

## decisions
- 2026-11-20 (claude): Backfilled PLAN.md from the code. Trust order used: tracked files and layout → git log (173 commits, latest 2026-11-20) → doc/questions.md "Decisions of 2026-11-19" and open GitHub issues (#13–#105, read with `gh issue list`) → README/agent-workflow last. Every `[x]` cites a file or commit; nothing was ticked from prose alone. No task is `[~]`: nothing is being built in this session.
- Eight components. The Pathfinder work is a component (fleet-fixes) even though its commits land in child repos, because it is where most open work in this repo's tracker lives and it owns doc/pathfinder-2026-11-14/. code-review-graph setup lives in agent-wiring rather than its own card: one conf.d file and hooks, no second task yet.
- Discrepancies found between docs and code, left as open tasks rather than fixed: (1) mani.yaml set `sync: true` on skogai-events and skogfleet although AGENTS.md says every project is `sync: false` → fixed, {#catalog-all-lazy}; (2) doc/questions.md records doc/journal.md as the journal (2026-11-15) but no such file exists → {#decisions-journals}; (3) the openwiki workflow still needs OPENAI_API_KEY despite the LM Studio decision → {#openwiki-lmstudio}; (4) doc/questions.md Q2.8 said agents/ holds two files — it holds 15; answered in questions.md.
- Unchecked for lack of evidence: README quickstart (#31 open, no verified section), container/read-only fetch notes (agent-workflow says "not yet run"/"not verified"), the openwiki workflow (never run).
- 2026-11-20 (owner): `/home/skogix/Work` (~/Work) is the fixed checkout path, so the hard-coded MCP paths stay; the task to remove them was dropped. Every catalog project is `sync: false`. `.skogai/logs/journal.md` is the spammable journal, moving to skogai-events behind an env var. LM Studio is running for OpenWiki. All recorded in doc/questions.md "Decisions of 2026-11-20".
- The agenttrail convention (AGENTS.md/CLAUDE.md section, `npm:agenttrail` in mise.toml + .mise/locks, PLAN.md) is committed together with this backfill.

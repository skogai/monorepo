# Open questions for Skogix

Everything that is waiting on an answer from the owner, in one place. Answer inline after `A:`; a question is closed when it has an answer or is deleted.

Sources: the [repo survey of 2026-11-14](surveys/2026-11-14-repo-survey.md), the mani migration threads and pull requests #51 to #57, and the final messages of the 20 most recent T3 Code threads, read on 2026-11-14. Questions marked "(thread ending)" came from those threads.

Each question has an ID so an answer can refer to it. IDs are never reused, so gaps in the numbering are deleted questions.

## Refresh of 2026-11-20

Every question still open was checked against the source on 2026-11-20: this repo's tracked files and git log, the open issues (`gh issue list -R skogai/monorepo`), `gh repo view`/`gh repo list` on the three accounts, and 18 child repos cloned read-only with `mani sync -t <name> --ignore-sync-state`. Run: Claude Opus 5.5 in Claude Code under T3 Code, machine `skogix-laptop`, base commit `92efe2e`. Where a fact changed since the survey, the question says what changed and where it was seen. "(from source, 2026-11-20)" marks an answer taken from the source rather than from the owner; the owner can overrule it. Q2.11's checks were run, and the evidence is in [.skogai/tests/2026-11-20-fetch-checks.md](../.skogai/tests/2026-11-20-fetch-checks.md).

Deleted in this refresh:

- **Closed by the decisions below** and so no longer listed, as those sections already said: Q1.2–Q1.4, Q1.6, Q1.7, Q1.9, Q2.10, Q3.1, Q4.1–Q4.18, Q4.21–Q4.23, Q4.25–Q4.42, Q4.46, Q4.55–Q4.60, Q4.63, Q4.64. The deferred U5 questions (Q1.3, Q1.4, Q4.27, Q4.28, Q4.38, Q4.39, Q4.55–Q4.60) are in git history for when the harness works again. Q3.1 has another reason too: `skogai/skogai-core` is archived on GitHub, so its PR #6 can no longer be merged.
- **About a repo that is no longer in `mani.yaml`:** Q4.5 (core), Q4.6 (dash-skogai), Q4.21–Q4.23 (skogai-core), Q4.25, Q4.26 (skogai-nov10), Q4.27, Q4.28 (skogai-routing), Q4.32–Q4.35 (systemd). All of them are also closed above.
- **Already tracked as an issue:** Q1.5 (gita: #84 and #85 drop gita for `mani.yaml`, "Do not keep gita and mani in parallel"), Q4.49 (skogai2-dot-skogai implementation: #92).
- **Kept although the 2026-11-19 ranges include them:** Q4.19, Q4.20 (`skogai/skogai`) and Q4.24 (`skogai-jq`) are inside "Q4.19 to Q4.26", closed as discontinued repos, but neither repo is on the discontinued list and both are still in `mani.yaml`. They look like a range slip, so they stay open until the owner says otherwise.
- **Q1.1 rows** for `core`, `skogai-routing`, `marketplace`, `dash-skogai` (discontinued) and `docs` (both copies frozen) are dropped from the table.

## Decisions of 2026-11-19

Answered by the owner in one pass. They close or replace the questions listed after each item; those questions are not repeated below.

- **Discontinued repos.** All seven on the Pathfinder retirement list are discontinued. Archiving them on GitHub is a separate step, not done yet.
  - `core`: old; to be remade on mise and usage. (`skogai/core` was still pushed to on 2026-11-19.)
  - `dash-skogai`: meant to hold all repo-wide data; retired for now.
  - `marketplace`: remade as [`skogai/skogai-events`](https://github.com/skogai/skogai-events), currently a single plugin.
  - `skogai-core`: removed, not used.
  - `skogai-routing`: removed, not currently used.
  - `skogai-nov10`: the earlier skogai; already archived on GitHub.
  - `systemd`: removed; held only old systemd services.
  - Closes Q1.1 for these names, Q1.2, Q3.1, Q4.5, Q4.6, Q4.19 to Q4.26, Q4.32 to Q4.35.
- **Old knowledge bases are frozen.** `docs`, `dot-skogai`, `skogai-nov10` and `skogai2-docs` are read-only archives, mined when needed. Closes Q1.6, Q1.7, Q4.7 to Q4.12, Q4.46.
- **Ops and security are taken as they come.** They become issues in their own repos when worked on. Covers Q4.1 to Q4.4, Q4.16 to Q4.18, Q4.36, Q4.37, Q4.40 to Q4.42.
- **Personal side projects are out of scope for the monorepo for now:** `nvim-omarchy`, `skogix` (the backlog) and `skogai2-skogpunk`. Closes Q2.10, Q4.13 to Q4.15, Q4.29 to Q4.31, Q4.63, Q4.64.
- **OpenWiki will be tried with LM Studio setups** (a local OpenAI-compatible endpoint) instead of an OpenAI key.
- **Recorded from earlier decisions:** `/skogai` belongs to `skogai2-dash-skogai` (2026-11-14), which closes Q1.9; the repo journal is `doc/journal.md` (2026-11-15).
- **Pathfinder U5 (work orders and harness dispatch) is deferred.** Nothing is planned around a harness that is not in working order. For now work goes from plain GitHub issues straight to pull requests. Closes Q1.3, Q1.4, Q4.27, Q4.28, Q4.38, Q4.39, Q4.55 to Q4.60 as deferred.
- **The rest of Pathfinder is tracked as GitHub issues.** Milestones U1–U4 and U6–U9 in this repo (#68–#105, all on project board 4), each issue checked against the source on 2026-11-19. Dropped on the way: fixes that targeted the archived repos (the `dash-skogai`/`skogai-nov10` wrappers and route checker, `core`), the harness `orchestrate-worktrees.js` task (U5), and the `dot-skogai/SKOGAI.md` doc fix (frozen repo). U6 targets `skogai-events`, the successor of the disabled `skogai-core` plugin. Owner calls are issues of their own: #88 (old journals), #96 (decision store), #101 (marketplace `docs/`).
- **Still open:** section 2 housekeeping and the remaining skogai2 per-repo questions.

## Decisions of 2026-11-20

Answered by the owner while PLAN.md was backfilled. They close or narrow the questions listed after each item.

- **Every catalog project is `sync: false`.** `skogai-events` and `skogfleet` were `sync: true`; both are now lazy like the rest, so a bare `mani sync` clones nothing again. A low-stakes fix, done in `mani.yaml`.
- **Journals.** `.skogai/logs/journal.md` is the current "spammable" turn journal. The skogai-core Claude plugin writes it, through a plugin setting, and commits it as `skogai-core: journal`. That job moves to `skogai-events`, with the journal path set by an environment variable instead of a plugin option. `.skogai/journal.md` is the older journal from before the move to `.skogai/logs/`. The curated journal decided on 2026-11-15, `doc/journal.md`, does not exist yet. Narrows #87 and #88.
- **OpenWiki on LM Studio is close.** A local LM Studio server is up and running. The workflow still asks for `OPENAI_API_KEY` until it is pointed at that endpoint.
- **`~/Work` is the fixed checkout path.** The MCP configs (`.mcp.json`, `.codex/config.toml`, `.agents/plugins/monorepo/mcp_config.json`) hard-code `/home/skogix/Work`, and that is accepted from now on. A checkout elsewhere has to override them by hand.
- **Recorded from the current state:** `agents/` on master now holds 15 cached files, which answers Q2.8. The `agents-cache` task removes a cached copy when its repo has no root `AGENTS.md`, but a repo that leaves `mani.yaml` still keeps its copy, so Q2.9 stays open.

## 1. Decisions that cut across repos

**Q1.1 Which org is canonical, per name?** For each row: `skogai`, `skogai2`, or "both, they are different things". Then what happens to the other copy: archive, point at the canonical one, or keep. Changed since the survey: `gh repo view skogai/<name>` (2026-11-20) finds no `skogai` copy of config, skogai-fleet, skogai-runner, aliasflare or skogpunk, and `skogai/cli` is a fork. The survey had marked those rows "skogai2 only cloned".

| Name | Canonical | Other copy |
|---|---|---|
| dot-skogai | skogai2 (from source, 2026-11-20): U7 makes `skogai2/dot-skogai` the one `.skogai` layout and bootstrap submodule (#92, #93) | `skogai/dot-skogai`: frozen archive (2026-11-19) |
| skogix | both, different things (from source, 2026-11-20): `skogai/skogix` is the backlog; `skogai2/skogix` becomes the human's personal repo (#80) | keep both; `skogai/skogix` is out of monorepo scope (2026-11-19) |
| skogai | | |
| cli | | `skogai/cli` is a fork (public, last push 2026-10-18) |
| config, skogai-fleet, skogai-runner, aliasflare, skogpunk | skogai2 (from source, 2026-11-20): no `skogai` copy exists | none |

Open rows: `skogai` (see Q4.19) and `cli`. Recommendation: `skogai2/cli` is canonical, as its README says it is the successor; leave the `skogai/cli` fork alone, because it is not in the catalog. Issue #39 (map each legacy name to where it lives now) is where the finished table can end up.

**Q1.8 How does the "global truth" role relate to this monorepo: does the monorepo take it over, or only point at the repo that has it?** (thread ending) Changed since the survey: PLAN.md (2026-11-20) describes this repo as "the map of the SkogAI repos plus the shared setup every agent works in", one that "plans and tracks" the other repos. Issue #96 asks for one store for decision records and lists four candidate repos plus this file.
A:
Recommendation: point, don't hold. The monorepo keeps the catalog, the plan and this file, and links to the knowledge, which stays in its repos. Decide the store in #96 at the same time.

## 2. This repository (monorepo)

**Q2.1 "Commits in this repo only change the catalog": target or loosen?** The sentence is still at `AGENTS.md:12`. Changed since the survey: most commits are now about the shared setup, not the catalog. Since 2026-11-14 the repo has gained `PLAN.md`, harness wiring (`.mcp.json`, `.codex/`, `.gemini/`, `.agents/`, `.config/mise/conf.d/code-review-graph.toml`) and T3 tooling (`scripts/t3-picker.py`, `.config/mise/conf.d/t3.toml`). PLAN.md's opening line already describes the wider scope, so `AGENTS.md` and `PLAN.md` now disagree.
A:
Recommendation: loosen it to match PLAN.md, for example "Commits here change the catalog and the shared setup; work on a fetched repo is committed in that repo."

**Q2.2 Should "Fetching a catalog repo" (container and read-only notes) stay in `doc/agent-workflow.md`, or go back into `AGENTS.md`?** Unchanged: the section is still in `doc/agent-workflow.md`, and `AGENTS.md` has the clone command and a link. Q2.11 found that two of its sentences are wrong.
A:
Recommendation: keep it in `doc/agent-workflow.md` and correct it with the Q2.11 results. `AGENTS.md` stays the short map.

**Q2.3 Where are answers recorded: in this file, or as project 4 issues and ADRs with this file as the dated input?** Changed since the survey: in practice, answers go here (the 2026-11-19 and 2026-11-20 sections), work goes to issues (Pathfinder became #68–#105), and PLAN.md has had its own `## decisions` log since 2026-11-20. No ADR has been written since 0002. Issue #96 covers the cross-repo decision store, and this file is one of its candidates.
A:
Recommendation: write down the current practice. This file holds questions and the owner's dated answers. An answer that changes how things work becomes an ADR, and one that creates work becomes an issue. Settle it together with #96.

**Q2.4 Catalog scope: are forks, archived repos and private repos in or out, and is the Skogix user account included?** Counts changed (`gh repo list --limit 2000`, 2026-11-20): `skogai` has 73 non-fork active repos (30 public, 43 private), 267 forks and 7 archived. `skogai2` has 25 non-fork active repos (18 public, 7 private) and 23 forks. The `Skogix` account has 86 non-fork active repos, 97 forks and 48 archived. In practice the catalog's 29 entries now hold 9 private repos and 1 fork (`skogai/repomix`, a fork of `yamadashy/repomix`). They hold no archived repos (the five went in `645a309`) and nothing from the Skogix account.
A:
Recommendation: make the current practice the rule. Active repos from both orgs are in when they are in use, private ones included. Forks are in only when SkogAI work happens in them. Archived repos and the Skogix account are out.

**Q2.5 Catalog generation: you wrote "is needed as tasks in mani itself via mise". What does that refer to? Should regenerating `mani.yaml` from `gh repo list` be a mani task wrapped by mise?** Unchanged: no such task exists in `mise.toml`, `.config/mise/conf.d/` or the `mani.yaml` tasks.
A:
Recommendation: since the catalog is curated (Q2.4), have the task report rather than rewrite: a mise task that diffs `gh repo list` against `mani list projects` and prints what is missing or extra.

**Q2.6 ADR 0003 for the manifest design (mani, unpinned, lazy, uncoupled) was deferred "until repos get added". Write it now?** Unchanged: `doc/adr/` still holds only 0001 and 0002. The design held through the 2026-11-19 removals (`645a309`), and the 2026-11-20 change put every project back on `sync: false`.
A:
Recommendation: write it now with `adr-tools`, because the design has stopped moving.

**Q2.7 AGENTS.md cache: should it also take `SKOGAI.md` or `CLAUDE.md` when a repo's `AGENTS.md` is missing or only a pointer?** Updated with 2026-11-20 counts: of the 18 repos cloned for this refresh, 9 have no root `AGENTS.md`, and 6 of those have a different entry file. `skogai2-cli`, `skogai2-skogix` and `skogai-events` have `CLAUDE.md`; `skogai2-dash-skogai`, `skogai2-dot-skogai` and `skogai2-skogai-routing` have `SKOGAI.md`. Two cached files are pointers only: `agents/harness.md` (a router to `@SKOGAI.md`, the same as `skogai/harness`'s own `AGENTS.md`) and `agents/skogai2-skogpunk.md` (one line, `@SKOGAI.md`).
A:
Recommendation: yes. Fall back in the order `AGENTS.md`, `SKOGAI.md`, `CLAUDE.md`, and put a first line in the cached file that names the file it was copied from.

**Q2.8 AGENTS.md cache: commit a full refresh?** `agents/` on master held two files (mise-plugin, skogai-jq). A run on skogix-workstation produced 14 more and a changed `skogai-jq.md`; they were never committed and are gone from the root checkout.
A: Done (2026-11-20): `agents/` holds 15 cached files on master. Checked 2026-11-20: the cached copies of skogai-jq, skogai2-config, skogai2-core, skogai2-marketplace, skogai2-skogai, skogai2-skogai-runner and skogai2-skogpunk are identical to their repos' current `AGENTS.md`.

**Q2.9 Orphan cache files: when a repo leaves `mani.yaml`, should `mise run agents:sync` delete its `agents/<name>.md`?** (2026-11-20: `agents-cache` now deletes the copy when a cloned repo has no `AGENTS.md`; a repo that leaves the catalog is not cloned, so its copy stays.) Changed since the survey: there is now a real orphan. `agents/systemd.md` is still on master, although `systemd` left `mani.yaml` (discontinued 2026-11-19, archived on GitHub).
A:
Recommendation: yes. Add a step to `agents:sync` that deletes `agents/<name>.md` for every name not in `mani list projects`, and delete `agents/systemd.md` in the same change.

**Q2.11 Three things are stated but not verified. Verify them, or mark them as unverified in the docs and leave it?** The remote-container path (`mise install`, then the tag fetch); cloning a private repo without workstation credentials; `git push --dry-run` as a read-only check.
A: Verified (from source, 2026-11-20; commands run, evidence in [.skogai/tests/2026-11-20-fetch-checks.md](../.skogai/tests/2026-11-20-fetch-checks.md)). (1) The container path fails as written. In a clean `node:24-alpine` container with mise 2026.11.10 and a fresh clone of master, `mise install mani` stops at `[skogai] plugin not installed`, and so does `mise plugins install -a`. It works once the plugin is installed from outside the checkout first (`cd / && mise plugins install skogai <url>#<pin>`): then `mise install mani` and `mani sync -t skogai-jq --ignore-sync-state` succeed. So the `mise.toml` comment saying the plugin "skips with a warning" is wrong for this mise version. (2) A private repo without credentials fails cleanly with `GIT_TERMINAL_PROMPT=0` (`could not read Username`) and does not hang. But 9 of the 29 catalog repos are private, so "All listed repos are public" in `doc/agent-workflow.md` is wrong. (3) `git push --dry-run` is a real check that sends nothing: it fails with no credentials, fails with a 403 on a repo without write access, and with write access shows the push without making it.
Follow-up for the owner: correct the two sentences in `doc/agent-workflow.md` and the comment in `mise.toml`, or fix the plugin bootstrap in #31. This refresh changes neither.

## 3. Open pull requests and branches

**Q3.2 `skogai/skogix` branch `create-todo-list-issues`: `skogai/skogix#3` (source audit notes and issue links) is merged, but the branch still exists. Delete it?** Checked 2026-11-20 with `gh api repos/skogai/skogix/branches` and `git cherry` in a clone. The branch still exists. Its one commit, `72395d3`, was squash-merged as `b9783b3` on 2026-11-14, so `git cherry origin/main` marks it as already on main, and deleting the branch loses nothing. The "submodules" wording is on `main` too (`.skogai/todo.list:7`), so deleting the branch does not remove it. Two more branches exist that the survey did not list, each with one commit that is not on main: `skogai-routing-runner` (`bbbd2e0`, 2026-11-10) and `skogix` (`c56413a`, 2026-11-10). `skogai/skogix` is out of monorepo scope (2026-11-19).
A:
Recommendation: delete `create-todo-list-issues`, because nothing is lost. Leave the other two branches until the owner looks at them.

## 4. Per repo

"Canonical?" for a repo is Q1.1.

### skogai org

**skogai**
- Q4.19 What role should it have beside the monorepo? Unchanged: still one commit, `ad6c86c` "Initial commit" with a README (2026-11-10), public, in `mani.yaml`. `skogai-core`, mentioned in the original question, is archived. A:
  Recommendation: archive it and drop it from `mani.yaml`, unless the name is being kept for later. If it is, say so in the README (Q4.20).
- Q4.20 If kept, what should its README say? A:

**skogai-jq**
- Q4.24 Live harness installation of the jq skill is untested. Test it, and in which harness? Unchanged: `README.md:26-27` still says "Live harness discovery and installation have not been tested here"; the last commit is `a8ed413` (2026-11-14). A:
  Recommendation: test it in Claude Code first, by cloning the repo to `~/.claude/skills/skogai-jq` and invoking the skill. That is a machine step, so record the result in `.skogai/tests/`.

### skogai2 org

**skogai2-core**
- Q4.43 Which parts stay in the older org? Changed: `skogai/core` is archived on GitHub (`gh repo view`, 2026-11-20), and the owner listed it as discontinued on 2026-11-19. A: None (from source, 2026-11-20). The older copy is archived, so `skogai2/core` is the only live core. #84 and #85 trim its gita layer, and #84 says this "feeds the planned remake of core on mise and usage". Where that remake will live is not stated anywhere.

**skogai2-dash-skogai**
- Q4.44 Its README describes `knowledge/`, `fish/` and a gptme-contrib submodule that are absent. Retired on purpose, or still needed? A: Removed by commits (from source, 2026-11-20). `fish/` went in `ecd9d25` ("Remove fish config and config defaults", 2026-10-09). `knowledge/` moved to `.skogai/knowledge/` in `ad32ed3` and was deleted together with the `gptme-contrib` submodule in `02e86c9` ("WIP", 2026-10-18), which left `.gitmodules` empty. Only the fish removal has a commit message that says why. The README (`README.md:11,15,19`) is stale. #92 names the old `knowledge/layout.md` as historical. Recommendation: correct the README; nothing points to these being needed.
- Q4.45 Should the older docs and fleet tooling survive? Changed: Pathfinder keeps the tooling and reshapes it. #76 trims `admin/`, #77 adds the one agent launcher here, and `/skogai` belongs to this repo (2026-11-19). The older `skogai/dash-skogai` is archived. A: The tooling survives and the older docs do not (from source, 2026-11-20). `admin/`, `scripts/gen-bin.py` and the coordination DB stay as #76 and #77 change them. The knowledge bundle is already gone at HEAD (Q4.44).

**skogai2-dot-skogai**
- Q4.47 Should it replace the older `dot-skogai` workspace? A: Yes (from source, 2026-11-20). The owner's Pathfinder answer (`doc/pathfinder-2026-11-14/prompts/owner-answers.md:9`) is ".skogai = base config + project-bootstrap submodule", and U7 makes this repo that submodule (`03-unified-proposal.md:110-112`, #92, #93). The older `skogai/dot-skogai` is frozen (2026-11-19). Unchanged in the repo: `SKOGAI.md` is still its only file (`78bf9ff`, 2026-11-01).
- Q4.48 Which older pieces belong in a portable `.skogai` bootstrap? A: The layout comes from `skogai2-skogai/.skogai/README.md:7-20` and not from the older repos (from source, 2026-11-20; #92). #92 names the older layouts in `dot-skogai/SKOGAI.md` and `skogai2-dash-skogai` as historical, and the old knowledge bases are frozen (2026-11-19).

**skogai2-marketplace**
- Q4.50 Should the older plugins migrate, or stay separate? Changed: the older `skogai/marketplace` is archived, and on 2026-11-15 this repo listed `skogai-events` as an external plugin and froze its own `skogai-core` at 0.11.1 (`45bdee0`; `AGENTS.md`, "skogai-core (the one local plugin)"). A: Neither (from source, 2026-11-20). The older marketplace is discontinued and remade as `skogai-events` (2026-11-19), so nothing migrates from it.
- Q4.51 Add an entry-point README? Unchanged: there is no README. The repo root has `AGENTS.md` and `CLAUDE.md`, and the `AGENTS.md` is cached as `agents/skogai2-marketplace.md`. A:
  Recommendation: no README is needed for agents. Add a three-line one only if people browse the repo on GitHub.
- Q4.52 Is the pending user-message log still wanted? Narrowed: the documentation-refresh half is now #101 (keep the `docs/` snapshot or point to the cache; `TODO.md:13` "the sync scripts were removed"). The user-message log is still open at `TODO.md:21`. `skogai-core` here is frozen, and `skogai-events` already logs every `UserPromptSubmit` row (`skogai-events/README.md:52`). A:
  Recommendation: if it is still wanted, file it as an issue in `skogai-events`, as a filter over the log that plugin already writes, and drop the line from this TODO.

**skogai2-skogai**
- Q4.53 Is this the earlier orchestration setup that the monorepo replaces? (thread ending) Unchanged in the repo (last commit `d836c2e`, 2026-11-10). What changed is the context: Pathfinder treats it as a live source. Its `.skogai/README.md` is the layout template (#92), and #72, #90 and #97 fix it in place. On orchestration, the owner named `harness` as the canonical direction (`owner-answers.md:5`), and U5 retracts this repo's "authoritative" Herdr line in favour of harness (`03-unified-proposal.md:92`; U5 deferred). A:
  Recommendation: no, it is a live source. Its orchestration role goes to `harness` once U5 resumes.
- Q4.54 Which parts survive: Herdr workflows, dash types, memory, harness? Narrowed by Pathfinder: the `.skogai` layout (#92), `whereami.sh` (#72), the VV hook gates (#90) and the work-order spec (`03-unified-proposal.md:86`, U5) survive. The second docs fetcher goes (#97). Herdr orchestration yields to `harness`. Dash types and memory are not covered. A:
  Recommendation: decide dash types and memory with #96 (the decision store), since `.skogai/memory/` is one of the stores it lists.

**skogai2-skogix**
- Q4.61 Legacy workspace to extract from, or a setup to maintain? A: A setup to maintain, as the human's personal repo (from source, 2026-11-20). U2 says so (`03-unified-proposal.md:57`), and #80 makes it concrete: drop the `/skogai` claim and delete the duplicate herdr hook. The agent parts move out: the launchers to `skogai2-dash-skogai` (#77), the agent config to `/home/<agent>` (#79). Unchanged in the repo: last commit `6bce7e7` "WIP" (2026-11-09).
- Q4.62 Which configurations and plugins move into SkogAI 3.0? Narrowed: Pathfinder settles the agent launchers (#77), the agent config (#79), the herdr hook (#80) and the nested skogdocs marketplace (#98). Everything else in the repo is not covered. A:
  Recommendation: answer this after U2 lands, when what is left is the human's own config.

# Open questions for Skogix

Everything that is waiting on an answer from the owner, in one place. Answer inline after `A:`; a question is closed when it has an answer or is deleted.

Sources: the [repo survey of 2026-11-14](surveys/2026-11-14-repo-survey.md), the mani migration threads and pull requests #51 to #57, and the final messages of the 20 most recent T3 Code threads (19 survey threads and the AGENTS.md review thread), read on 2026-11-14. The thread endings added four questions that the survey file does not have; they are marked "(thread ending)". Nothing here was re-checked against the child repos: the facts behind each question are in the survey.

Each question has an ID so an answer can refer to it. Suggested order: section 1 first, because most of section 4 depends on it.

## 1. Decisions that cut across repos

**Q1.1 Which org is canonical, per name?** For each row: `skogai`, `skogai2`, or "both, they are different things". Then what happens to the other copy: archive, point at the canonical one, or keep.

| Name | Canonical | Other copy |
|---|---|---|
| core | | |
| skogai-routing | | |
| marketplace | | |
| dash-skogai | | |
| dot-skogai | | |
| skogix | | |
| skogai | | |
| docs | | |
| cli (skogai2 only cloned) | | |
| config (skogai2 only cloned) | | |
| skogai-fleet (skogai2 only cloned) | | |
| skogai-runner (skogai2 only) | | |
| aliasflare (skogai2 only cloned) | | |
| skogpunk (skogai2 only cloned) | | |

**Q1.2 Fleet control: does `core` continue alongside mani and mise, get reconciled with them, or get retired?**
A:

**Q1.3 Is the `core` handover proposal for workorders and dispatch still current?**
A:

**Q1.4 Should dispatch live in `core` or in the runner, and start local-only or include cloud agents?**
A:

**Q1.5 `skogai2-core` added a fleet registry and gita configuration. Is gita still wanted now that mani is the catalog tool?** (thread ending)
A:

**Q1.6 Which of `dash-skogai`, `dot-skogai`, `skogai-nov10`, `docs` and `skogai2-skogai` is the authoritative home for shared knowledge, and which are archives to mine?**
A:

**Q1.7 Which decisions, configs, research projects and unfinished tasks still need migrating out of the older knowledge repos?**
A:

**Q1.8 How does the "global truth" role relate to this monorepo: does the monorepo take it over, or only point at the repo that has it?** (thread ending)
A:

**Q1.9 Does `/skogai` remain a required path?** `skogai2-skogix` and both `dash-skogai` copies assume it.
A:

## 2. This repository (monorepo)

**Q2.1 "Commits in this repo only change the catalog": target or loosen?** The sentence is in `AGENTS.md` as you chose, but the repo also holds mise config, `doc/`, ADRs and `.skogai/`. Either those move out later, or the sentence is loosened.
A:

**Q2.2 Should "Fetching a catalog repo" (container and read-only notes) stay in `doc/agent-workflow.md`, or go back into `AGENTS.md`?**
A:

**Q2.3 Where are answers recorded: in this file, or as project 4 issues and ADRs with this file as the dated input?**
A:

**Q2.4 Catalog scope: are forks, archived repos and private repos in or out, and is the Skogix user account included?** Counts when asked: skogai 79 non-fork active (32 public, 47 private), Skogix 86, skogai2 24. The catalog has 29.
A:

**Q2.5 Catalog generation: you wrote "is needed as tasks in mani itself via mise". What does that refer to? Should regenerating `mani.yaml` from `gh repo list` be a mani task wrapped by mise?**
A:

**Q2.6 ADR 0003 for the manifest design (mani, unpinned, lazy, uncoupled) was deferred "until repos get added". Write it now?**
A:

**Q2.7 AGENTS.md cache: should it also take `SKOGAI.md` or `CLAUDE.md` when a repo's `AGENTS.md` is missing or only a pointer?** Several surveyed repos use those as their entry point.
A:

**Q2.8 AGENTS.md cache: commit a full refresh?** `agents/` on master holds two files (mise-plugin, skogai-jq). A run on skogix-workstation produced 14 more and a changed `skogai-jq.md`; they were never committed and are gone from the root checkout.
A:

**Q2.9 Orphan cache files: when a repo leaves `mani.yaml`, should `mise run agents:sync` delete its `agents/<name>.md`?** Nothing removes it today.
A:

**Q2.10 The README backlog link points at `repos/skogix/.skogai/todo.list`, which exists only after that repo is cloned. Keep, or link to the GitHub file instead?**
A:

**Q2.11 Three things are stated but not verified. Verify them, or mark them as unverified in the docs and leave it?** The remote-container path (`mise install`, then the tag fetch); cloning a private repo without workstation credentials; `git push --dry-run` as a read-only check.
A:

## 3. Open pull requests and branches

**Q3.1 `skogai/skogai-core#6` (replace the duplicated jq skill with a pointer to `skogai-jq`) is open. Merge it although core's validator reports a pre-existing failure in untouched content?**
A:

**Q3.2 `skogai/skogix` branch `create-todo-list-issues`: `skogai/skogix#3` (source audit notes and issue links) is merged, but the branch still exists. Delete it?** Its notes still say "submodules".
A:

## 4. Per repo

Questions already covered by section 1 are not repeated; "canonical?" for a repo is Q1.1.

### skogai org

**cloudflare**
- Q4.1 Are the token rotation and the missing email MX records in its TODO.md still unresolved? A:
- Q4.2 Should `mcp.skogai.se` sit behind Access, or stay public with its own auth? A:
- Q4.3 Which tunnels are kept, revived or retired? A:
- Q4.4 Should Aliasflare work use the submodule in `cloudflare`, or the standalone catalog clone? A:

**core**
- Q4.5 Stay `skogai/core`, or move to skogai2? (See Q1.1 to Q1.4.) A:

**dash-skogai**
- Q4.6 Are its fleet snapshots, CLI wrappers, Dolt layer and generated wiki still wanted? A:

**docs**
- Q4.7 Maintained knowledge base, or historical archive? A:
- Q4.8 Which of `merge/`, `todo/` and `skogix/` is authoritative? A:
- Q4.9 Move material into newer repos, or add a root index and a consolidation plan? A:

**dot-skogai**
- Q4.10 Canonical workspace, or legacy snapshot? A:
- Q4.11 Did its executable tooling (Argcfile.sh, argc/, agents/, tools/) move to `core`? A:
- Q4.12 How do its responsibilities differ from `dash-skogai` and the new bootstrap repo? A:

**nvim-omarchy**
- Q4.13 Is this the canonical desktop Neovim config? A:
- Q4.14 Should it work on machines without Omarchy? A:
- Q4.15 Should its external bootstrap and desktop docs be available alongside it? A:

**podman**
- Q4.16 "Containers whose only way out is a tunnel": does that mean ingress, egress, or both, and what enforces it? A:
- Q4.17 Should the paused secrets-recovery work resume? PLAN.md leaves the age recipients undecided. A:
- Q4.18 Is fixing Termix command execution against fish a priority? A:

**skogai**
- Q4.19 What role should it have beside monorepo and skogai-core: reserved, awaiting migration, or unnecessary? A:
- Q4.20 If kept, what should its README say? A:

**skogai-core**
- Q4.21 Still the canonical home for the routing framework and marketplace? A:
- Q4.22 Where do hooks and their tests belong? A:
- Q4.23 Next priority: finish the migration, document installation, or archive? A:

**skogai-jq**
- Q4.24 Live harness installation of the jq skill is untested. Test it, and in which harness? A:

**skogai-nov10**
- Q4.25 Archive, or does any part stay authoritative? A:
- Q4.26 Should its references to `skogai/skogai`, `~/core` and global tools be updated, or left as history? A:

**skogai-routing**
- Q4.27 Is the next deliverable a specification, an installable skill, or working tooling? A:
- Q4.28 Are "concept" and "tag" distinct owner types? The notes leave this open. A:

**skogix**
- Q4.29 Does it stay the intake backlog, with items promoted to GitHub issues? A:
- Q4.30 Which of the 15 unchecked todo.list entries are already done or superseded by the monorepo? A:
- Q4.31 Does it need a short purpose README, or is it deliberately a personal scratch list? A:

**systemd**
- Q4.32 Still the authoritative source for deployed user services, and on which machines? A:
- Q4.33 Which older non-prefixed services stay supported? A:
- Q4.34 Should service metadata and health checks cover the full inventory? `services.json` covers three. A:
- Q4.35 Machine-specific on purpose, or should setup become reproducible through mise? A:

**mise-plugin**: no open question. Linux only is the stated scope.

### skogai2 org

**skogai2-aliasflare**
- Q4.36 Is the deployment mentioned in the journal still used, and who owns its domain and Cloudflare resources? A:
- Q4.37 Next need: maintenance, deployment verification, or consolidation? A:

**skogai2-cli**
- Q4.38 Should its mise-based settings model carry into SkogAI 3.0? A:
- Q4.39 Which roadmap item is still relevant: module runner, base versioning, typed modules? A:

**skogai2-config**
- Q4.40 Is the isolated bootstrap/adopt test environment the next priority? Fresh-machine bootstrap is untested. A:
- Q4.41 Which workstation-specific assumptions should become portable? A:
- Q4.42 Is the noted leaked-file history cleanup still outstanding? A:

**skogai2-core**
- Q4.43 Which parts stay in the older org? (See Q1.1 to Q1.5.) A:

**skogai2-dash-skogai**
- Q4.44 Its README describes `knowledge/`, `fish/` and a gptme-contrib submodule that are absent. Retired on purpose, or still needed? A:
- Q4.45 Should the older docs and fleet tooling survive? A:

**skogai2-docs**
- Q4.46 Maintained, or archived? A:

**skogai2-dot-skogai**
- Q4.47 Should it replace the older `dot-skogai` workspace? A:
- Q4.48 Which older pieces belong in a portable `.skogai` bootstrap? A:
- Q4.49 Is implementation still wanted, or does it stay a placeholder? A:

**skogai2-marketplace**
- Q4.50 Should the older plugins migrate, or stay separate? A:
- Q4.51 Add an entry-point README? A:
- Q4.52 Are the pending user-message logging and documentation-refresh tasks still wanted? A:

**skogai2-skogai**
- Q4.53 Is this the earlier orchestration setup that the monorepo replaces? (thread ending) A:
- Q4.54 Which parts survive: Herdr workflows, dash types, memory, harness? A:

**skogai2-skogai-fleet**
- Q4.55 Which harness or runner loads the 17 crew personas, and how? A:
- Q4.56 Do the persona profiles or `references/crew-roles.md` define responsibilities? They disagree. A:
- Q4.57 Which proposed persona, tooling and model changes proceed? A:

**skogai2-skogai-routing**
- Q4.58 Does 0.1.0 stay a documentation and skill convention, or does validation tooling follow? A:

**skogai2-skogai-runner**
- Q4.59 Continue the remake, or restore pieces of `best-argc-version/`? A:
- Q4.60 Which config-storage decisions are settled? A:

**skogai2-skogix**
- Q4.61 Legacy workspace to extract from, or a setup to maintain? A:
- Q4.62 Which configurations and plugins move into SkogAI 3.0? A:

**skogai2-skogpunk**
- Q4.63 Is Android the intended direction? HANDOVER.md recommends a browser game, the repo holds an Android implementation. A:
- Q4.64 Keep the browser-game handover as history, or replace it? A:

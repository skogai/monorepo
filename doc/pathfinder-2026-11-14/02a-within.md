# 02a — Within-system duplication (Phase 2)

Scope: repeated logic inside each system S1–S7 only. Duplication across systems is out of scope here.
Every claim cites at least two locations, and I opened each one in this pass. Paths are relative to `~/Work/repos/` unless they start with `~`.

**How to read the verdicts.** I apply the owner's levels rule: overlap is **accidental** only when two things do the same job at the same level (workstation / agent home / repo / container / remote). When the copies sit at different levels and could compose, the verdict is **legit layering**. When the copies are old generations of each other, the verdict is **generational**: the newer copy is the keeper and the older one is a deletion candidate. Unused code is labelled "present in source; usage not established", as the owner asked.

---

## Ranked summary

Rank = consolidation value (impact × how cheap). "Delete" means a pure deletion with no code change.

| # | Sys | Finding | Verdict | Smallest consolidation | Cost |
|---|---|---|---|---|---|
| W1 | S3 | `install-coordination.sh` still sets `2775` on `/skogai/bin`, the mode the README forbids | accidental, superseded | delete `admin/install-coordination.sh` | delete |
| W2 | S4 | The journal and state are written under `logs/`, which the owner's own rule says is disposable. The monorepo holds two journals as a result | accidental (config drift) | drop the `journal_path`/`state_dir` overrides in `~/.claude/settings.json`, or point them outside `logs/` | 2-line config edit, plus an owner call on the 875-line file |
| W3 | S1 | `SKOGAI_CONFIG_DIR` set at 3 levels, but the plugin ignores a pre-set value while the runner honours it | legit layering, broken precedence | wrap the plugin's `SKOGAI_CONFIG_DIR` in its existing `default()` | 1-line change |
| W4 | S1 | The config CLI is forked verbatim: `_frontmatter`/`_resolve` exist ×3, and the runner and marketplace copies are byte-identical | accidental (copy, no caller) | delete `skogai2-marketplace/scripts/{config,frontmatter}/` | delete |
| W5 | S5 | The `core` repo is a strict subset of `skogai2-core` (byte-identical Argcfile, same openwiki commit) | generational | drop `core` from `mani.yaml` and archive it | delete |
| W6 | S7 | `cloudflare/old-systemd-solution/` is 53 of 64 files identical to the `systemd` repo. Neither is installed, and both carry an inline pangolin secret | generational | delete `cloudflare/old-systemd-solution/` | delete |
| W7 | S2 | Work-order format exists in 3 shapes plus a harness plan JSON. The only checker was deleted | accidental at the spec level; harness composes at the execution level | make `SPECIFICATION.md` the single format, turn the runner's `WORKORDERS.md` format section into a pointer, add a WO→harness plan adapter later | doc edit |
| W8 | S6 | 4 CC docs fetchers and 3 committed snapshots | accidental, except the lookup plugin, which sits at a different level | keep `code-docs-lookup/sync-docs.sh` and delete the other fetchers. The snapshots are an owner call | mostly delete |
| W9 | S5 | Inside `skogai2-core`: `Argcfile.sh repo::*` stubs and the `repo` module both wrap gita, and the committed gita CSV is a copy of `~/.config/gita/repos.csv` | accidental, mid-migration | delete the Argcfile `repo` block | delete |
| W10 | S3 | `herdr-agent-state.sh` is byte-identical in two repos | accidental | delete the `skogai2-skogix` copy, since `/skogai` belongs to dash | delete |
| W11 | S2 | One dispatch prompt (anti-widening, "follow the repo's conventions") is written 4–5 times | accidental | one template file, referenced by the others | small |
| W12 | S2 | Two deterministic route checkers | generational | delete `dash-skogai/bin/check-skogai-routes` together with its mise task | delete |
| W13 | S6 | Two marketplace manifests in `skogai2-skogix` list the same plugin dir | accidental | delete `plugins/skogdocs/.claude-plugin/marketplace.json` | delete |
| W14 | S3 | Two scripts create the agent users; `setup-coordination.sh` has a narrower list | accidental | remove the user block from `setup-coordination.sh` (or call `create-agents.sh`) | small |
| W15 | S3 | The clean-env launchers copy one env allowlist and have drifted | partly legit | one shared allowlist file sourced per agent | medium |
| W16 | S1/S2/S5 | `skogcli`, `gptodo`, `gita` wrappers byte-identical ×3, **including the canonical `harness/bin`** | accidental | delete from `dash-skogai` and `skogai-nov10`, then decide whether harness should carry them at all | delete |
| W17 | S7 | 3 notify units differ only by name; `a.yml` ≡ `docker-compose.yml` | accidental, tiny | one `notify@.service`; delete `a.yml` | small |
| W18 | S6 | Old-repo skill copies: `skogai-jq` ×3, `skogai-hook-debugging` ×2 byte-identical, `skogai-core` name ×3 | generational | delete with the old repos. Leave the skoghooks entry, which is on hold | delete |
| W19 | S4 | Three declared `.skogai` layouts disagree, and the 25 real `.skogai/` dirs follow none of them | accidental | one layout doc in `skogai2-dot-skogai` (the bootstrap-submodule repo) | doc |
| W20 | S4 | OpenWiki ×5 dirs, 2 workflow variants; decision stores ×4 with `adr-002` used twice | owner decision | revive or delete; renumber one adr | decision |
| W21 | S1 | Key→env name rules disagree on `-` | accidental | pick the runner rule (`-` dropped) in `skogai2-cli` too | 1-line |
| W22 | S1 | `SKOGAI_LOG` names two different files | accidental, harmless today | rename one (`SKOGAI_RUN_LOG`) | 1-line |
| W23 | S1 | Host/OS/arch detection ×2 with different arch names | legit layering, naming drift | `whereami.sh` reads `SKOGAI_ARCH` when set | small |

W1, W4, W5, W6, W9, W10, W12, W13 and W16 are pure deletions. Together they remove the most code for the least risk.

---

## S1 ENV

### W3. `SKOGAI_CONFIG_DIR`: three levels, inconsistent precedence

- Workstation: `~/.config/mise/config.toml:93` sets `/home/skogix/skogai/config`.
- Agent home / shared: `skogai2-skogix/mise.toml:6` sets `/skogai/config`.
- Repo: `dot-skogai/mise.toml:50` sets `.skogai/config` (relative, for skogcli).
- Plugin: `mise-plugin/hooks/mise_env.lua:15` emits `SKOGAI_CONFIG_DIR = skogai.config_dir(ctx)` **unconditionally**. The lines below it (`:16-18`, `HOST/OS/ARCH`) go through `default()` (`:9-10`), which keeps an existing value. `config_dir` itself (`mise-plugin/lib/skogai.lua:51-60`) reads only the plugin option and XDG.
- Runner: `skogai2-skogai-runner/best-argc-version/modules/core/argc.sh:19` uses `${SKOGAI_CONFIG_DIR:-…}`, which honours a pre-set value. The marketplace fork does the same (`skogai2-marketplace/scripts/config/argc.sh:21`).

**Verdict.** These are different levels, so per the owner this is legit layering ("whatever you set it to"). The duplication that matters is in the precedence rule: the plugin overwrites what a lower level set, and the runner does not. The skogcli wrappers also clobber it with a bare `export` (`dash-skogai/bin/skogcli:3`). `skogai-nov10/DECISIONS.md:437-439` already records the debugging cost of that.

**Smallest change.** Route `SKOGAI_CONFIG_DIR` through the same `default()` at `mise_env.lua:15`. That makes "whatever you set it to" true at every level. I did not test how mise orders plugin env against `[env]` in the same config.

### W4. Layered config CLI forked verbatim

- `skogai2-skogai-runner/best-argc-version/modules/core/argc.sh:25-130` (`config get/set/unset/list/env/files`) and `skogai2-marketplace/scripts/config/argc.sh:27-131`: same commands with the same help text.
- `_frontmatter` and `_resolve` are byte-identical between those two files and also `skogai2-marketplace/scripts/frontmatter/argc.sh:135,150`. I diffed each function with `sed -n '/^_x()/,/^}/p'`, and all three matched.
- The marketplace commit says so itself: `ada0144 scripts/config: core's config half copied out as is, as its own module`.
- Callers: the only reference inside `skogai2-marketplace` is `CLAUDE.md:17`, which describes it. Status: present in source; usage not established.
- `skogai2-cli/bin/config:1-14` is a **different model**: it stores settings in mise `[env]` TOML layers, not markdown frontmatter.

**Verdict.** The marketplace copies are accidental: same job, same level, no caller. The runner core and `skogai2-cli` are two storage models at the same level. That is an owner choice, not something to delete, and the owner said both may compose.

**Smallest change.** Delete `skogai2-marketplace/scripts/config/` and `scripts/frontmatter/`, plus the `CLAUDE.md:17` paragraph.

### W21. Key→env name rule disagrees on `-`

- `skogai2-skogai-runner/best-argc-version/modules/core/argc.sh:644-649` and `skogai2-marketplace/scripts/config/argc.sh:227-232`: `-` is dropped, so `stage.on-stop` becomes `SKOGAI_STAGE_ONSTOP`.
- `skogai2-skogai/dash-skogai/config:2` documents the same rule.
- `skogai2-cli/lib/config.sh:56-59`: `.` becomes `_` and `-` is **kept**, which yields an env name containing `-` that no shell can use.

**Correction to the S1 flowchart #4.** Inside `repos/`, `SKOGAI_STAGE_ON_STOP` appears only as `CLAUDE_PLUGIN_OPTION_STAGE_ON_STOP` (`skogai2-marketplace/plugins/skogai-core/tests/run.sh:50`). The other occurrence is in `CONFIG.md:20`, which describes commented-out lines in `~/.config/mise/config.toml:85-88`. The conflict is therefore latent, not live. The "11 vs 13 hits" counts probably included logs.

### W22. `SKOGAI_LOG` used for two files

`skogai2-marketplace/plugins/skogai-core/scripts/settings.sh:34` uses it for the hook event log, and `skogai2-skogai-runner/src/core/log/usage.sh:15` uses it for the runner's `run.jsonl`. `settings.sh` does not export the variable, so the collision is harmless today. Renaming the runner's variable is a one-word change.

### W23. Host/OS/arch detection

`mise-plugin/lib/skogai.lua:123-143` uses mise naming (`x64`). `skogai2-skogai/.skogai/scripts/whereami.sh:16-21` uses `uname -m` (`x86_64`) and adds distro, kernel and user. These are different levels (env plane vs repo report), so this is legit layering with naming drift. Make `whereami.sh` prefer `SKOGAI_HOST/OS/ARCH` when they are set. Low value.

### Not counted

- Scope-dir pointer keys go by five names: `skogai2-cli/.skogai/base/mise.system.toml:2`, `skogai2-skogai/dash-skogai/mise.config.toml:2-4`, `skogai2-cli/bin/config:11-14`, and runner `argc.sh:10-12`. They follow the two storage models in W4, so they resolve when that choice is made.

---

## S2 RUN

### W7. Work-order format

- `skogai2-skogai-runner/.skogai/workorders/WORKORDERS.md:24-29`: `name`, `owns`, `reads`, plus body sections. The queue lives in `open/` + `done/` (`:14-15`).
- `skogai2-skogai/orchestration/work-orders/SPECIFICATION.md:21-46`: the same fields plus `description`, `status`, `depends_on` and `tags`, and a forbidden-keys list (`:48-66`). The queue lives in `open/` + `completed/` + `rejected/` (`:125-137`). Its example *is* the runner's work order `contract-yq-flavor` (`:36-46`), and that file sits in the runner's `done/`.
- The runner's checker is gone. `WORKORDERS.md:27,36` links `src/core/contract/argc.sh` and `usage.sh check`, but `skogai2-skogai-runner/src/core/` contains only `log/`. Its replacement is a hand-written `comm` snippet in `SPECIFICATION.md:198-206`.
- Harness (the owner's canonical direction): `harness/marketplace/plugins/skogharness/scripts/lib/tmux-worktree-orchestrator.js:175-246` takes a JSON plan `{workers:[{name, task, seedPaths}], baseRef, launcherCommand}`. It writes its own `task.md`/`handoff.md` (`:108-160`, `:210-211`). It has no `owns` concept.

**Verdict.** The two markdown formats do the same job at the same level (repo task spec), so that overlap is accidental. `done/` and `completed/` name the same state. Harness sits at a different level, the execution engine, and composes with a WO format instead of replacing it. Gap: harness's `skogharness` submodule is uninitialised (`git submodule status` shows `-5f2ed99`), so I read the marketplace copy only.

**Smallest change.** `SPECIFICATION.md` is the superset, so make it the format. Replace `WORKORDERS.md:20-29` with a link to it and rename `done/` to `completed/`. Later, a WO→plan adapter can map `name→name`, the body to `task`, and `reads→seedPaths`. Disjoint `owns` stays a pre-dispatch check, because harness does not enforce it.

### W11. Dispatch prompt written repeatedly

`WORKORDERS.md:41`, `SPECIFICATION.md:164-185`, `dash-skogai/bin/skogai-paseo:143-151` and `dash-skogai/bin/skogai-run-issue:31-37` each restate "read the spec, stay in scope, follow the repo's conventions, stop and report". The paseo and run-issue copies are old generations (in `dash-skogai`). The two live ones (runner, hub) collapse into one template once W7 lands.

### W12. Route checkers

`skogai2-config/bin/check-routes:1-31` (bash) is tested (`skogai2-config/tests/check-routes.test.sh`) and called by `bin/health`. `dash-skogai/bin/check-skogai-routes:1-40` (python, `dash-skogai/mise.toml:21-23`) also checks the router frontmatter and "durable documentation" domains. Same job, same level, and `dash-skogai` is the older repo: delete it with its task. A third copy, `skogai2-skogai/dash-skogai/tmp/routing/scripts/validate_router.py` (137 lines), sits under `tmp/`. Present in source; usage not established.

### Not counted

The worktree backends (`wt` → paseo → herdr → harness/tmux) are generational, as the S2 flowchart D6 already says. Nothing in them is concurrent apart from harness, which is the owner's pick.

---

## S3 DASH

### W1. `install-coordination.sh` is superseded and sets the forbidden mode

`skogai2-dash-skogai/admin/install-coordination.sh:13` runs `chmod 2775 /skogai/tools /skogai/bin`. `install-tools.sh:14-17` explicitly sets `755` on the same dirs and explains why: a group-writable `bin/` lets one agent plant code that runs as another. `README.md:66` specifies `2755`, and `README.md:26` says `install-tools.sh` "replaces install-coordination.sh". Running the old script undoes the hardening, so delete it. That is the highest value for the lowest cost in this report.

### W14. Agent users created twice

`admin/create-agents.sh:10-27` creates `claude dot amy goose codex` and adds humans `skogix aldervall` with an existence guard. `admin/setup-coordination.sh:11-25` creates `claude dot` and calls `usermod` on humans with no guard. Same job, same level. The smallest fix is to delete `setup-coordination.sh:15-25` and have it require `create-agents.sh` first. The gptme-coordination stack it belongs to is present in source; usage not established.

### W10. herdr hook script

`skogai2-dash-skogai/scripts/claude/hooks/herdr-agent-state.sh` and `skogai2-skogix/scripts/claude/hooks/herdr-agent-state.sh` are byte-identical (`cmp`). `skogai2-skogix/claude/settings.json:33` references it as `/skogai/claude/hooks/…`. `/skogai` belongs to dash, so keep the dash copy and delete the skogix copy.

### W15. Clean-env launcher allowlist

`skogai2-skogix/bin/claude:2-18` and `bin/agy:30-54` repeat the same `env -i HOME USER LOGNAME … SSH_AUTH_SOCK PATH` block. agy adds `TERM_PROGRAM*`, `HERDR_*` and `COLLIE_INSTANCE`, so a claude launched inside herdr loses the herdr env that the agy launcher keeps. `codex/run:1-19` uses no `env -i` at all. The per-CLI flags are legit; the allowlist is accidental. The smallest fix is one `bin/agent-env` file listing the passthrough vars, read by both. `claude/shell/.zshrc:1` also hard-codes `/home/skogix/.local/bin`, while `agy/shell/.zshrc:1-6` does not.

### Not counted

The agent identity model (uid vs `SKOGAI_USER` at `skogai2-dash-skogai/mise.toml:13`) is an architectural choice. skogfences answers it with the uid. It is not duplication.

---

## S4 DOT

### W2. Journal and state under `logs/`, two journals in the monorepo

- Plugin defaults: `skogai2-marketplace/plugins/skogai-core/scripts/settings.sh:34-36` (`.skogai/journal.md`, `.skogai/tmp`).
- User overrides: `~/.claude/settings.json:154,156,158` (`.skogai/logs/log.jsonl`, `.skogai/logs/journal.md`, `.skogai/logs/state`).
- Owner rule: `skogai2-skogai/.skogai/memory/temporary-paths.md:10-21` says `logs/` and `tmp/` are disposable and that "anything durable belongs in config or state, not logs/tmp".
- Result: `~/Work/.skogai/journal.md` (30 lines, last commit 2026-11-13) and `~/Work/.skogai/logs/journal.md` (875 lines, last commit 2026-11-14). Seven repos still hold a committed `.skogai/journal.md` from the default path: cloudflare, skogai2-aliasflare, skogai2-marketplace, skogai2-skogai, skogai2-skogai-runner, skogai2-skogix and skogai2-skogpunk.

**Verdict.** One hook writes to two paths because of config drift, and the active path breaks the owner's own rule. Accidental.

**Smallest change.** Remove the `journal_path` and `state_dir` overrides so the defaults apply. Whether to fold the 875-line file back into `journal.md` is the owner's call. I changed nothing.

### W19. Declared `.skogai` layouts

`skogai2-skogai/.skogai/README.md:7-20` (config, memory, rules, scripts, skills, tasks, templates, workflow, state, logs, tmp, worktrees), `skogai2-dash-skogai@ad32ed3^:knowledge/layout.md:27-40` (adds knowledge, bin, workorders, ROUTES.md) and `dot-skogai/SKOGAI.md:28-41` (a repo-root tree, not `.skogai/`) disagree.

The live tree has 25 repos with `.skogai/`. The only near-universal entry is `logs/`, which the hook creates. All other entries are per repo. `skogai2-dot-skogai/SKOGAI.md:3-5` is the repo that is "meant to hold the `.skogai` convention" but is empty.

**Smallest change.** Copy one layout (the live `skogai2-skogai` README is the most precise) into `skogai2-dot-skogai` as the bootstrap-submodule template. Mark the other two as historical. Moving existing dirs is out of scope.

### W20. OpenWiki and decision stores

- OpenWiki dirs: `core/openwiki`, `skogai2-core/openwiki` (same commit `2cac75d`), `dash-skogai/openwiki`, `dot-skogai/openwiki`, `skogai-nov10/openwiki`.
- **Correction to the S4 flowchart #8.** The 5 workflows are **2 variants**, not 5 that differ. md5 `89f30c34…` covers core, dash-skogai and skogai2-core; `f4fdf0e3…` covers dot-skogai and skogai-nov10. Deleting `core` (W5) removes one copy for free.
- Decision stores: `dot-skogai/knowledge/decisions/` (13, date-prefixed), `skogai2-skogix/.skogai/decisions/0001-0007`, and `wiki/decisions/adr-001…012`. Two files share the number `adr-002`. Renumbering one adr is cheap. Which store is canonical is an owner question, already open in S4.

### Not counted

The project-name helper exists twice. `skogai2-skogai/.skogai/scripts/get-project-name.sh:6-8` uses `gh repo view`, the same approach as the skogcli wrapper. The `dot-skogai/scripts/` copy is a dangling symlink into the missing `~/.local/src/skills/extras`. Nothing to consolidate.

---

## S5 FLEET

### W5. `core` ⊂ `skogai2-core`

`cmp core/Argcfile.sh skogai2-core/Argcfile.sh` shows them byte-identical. `diff -rq core skogai2-core` shows only additions in skogai2-core (`contracts/`, `.skogai/modules`, `.skogai/repo`, `.agents`), plus a differing `HANDOVER.md`, `todo.list` and logs. openwiki is at the same commit in both (`2cac75d`). Generational: drop `core` from `mani.yaml` and archive it. Check `core/HANDOVER.md` for anything unique first.

### W9. Two gita wrappers inside `skogai2-core`, plus a committed state copy

`skogai2-core/Argcfile.sh:34-47` (`repo::list`, `repo::status` on the global gita group) and `skogai2-core/.skogai/modules/repo/argc.sh:11-24` (the same commands through `_gita` with a private `GITA_PROJECT_HOME`, `:38-39`). Both live in the same repo at the same level. The module is the newer, schema-backed one, so delete the Argcfile `repo` block.

`skogai2-core/.skogai/repo/gita/repos.csv` is byte-identical to `~/.config/gita/repos.csv`, a snapshot of machine state that will drift.

### Registry choice (decision, not deletion)

`~/Work/mani.yaml:16-172` (url + path + lazy, wrapped by mise tasks at `~/Work/mise.toml:44-57`) and the gita registry (`skogai2-core/.skogai/repo/gita/repos.csv:1-13` + `repos.toml:7-14`) are at the **same level**: the workstation clone catalog. They point at two clone roots for the same repos: `~/.local/src/` (`skogai2-core/Argcfile.sh:7`) and `~/Work/repos/`. That is accidental duplication. The owner rule "prefer an existing tool such as mani" and the S5 rule "commands runnable via mise tasks" both point at mani. `dash-skogai/fleet/fleet/repos.csv` (77 lines) and `fleet/skills/skogai-gita/config/repos.csv` (18) are old-generation copies.

---

## S6 PLUGINS

### W8. CC docs: 4 fetchers and 3 snapshots

Fetchers. All hit `code.claude.com/docs`:

- `skogai2-skogix/plugins/skogdocs/plugins/code-docs-lookup/scripts/sync-docs.sh:14-15` (87 lines, bundle → split → cache)
- `skogai2-skogai/.skogai/scripts/claude-code-documentation.sh:12-79` (the same bundle-and-split idea)
- `skogai-core/scripts/claude-code-documentation.sh:6` (24 lines)
- `marketplace/scripts/download-docs.sh:5` (37 lines)

Snapshots:

- `skogai2-docs/claude-code/` (230 files)
- `skogai2-marketplace/docs/` (223 files, `synced-at.txt` = 2026-10-09; **correction:** S6 said 139)
- `marketplace/docs/` (78 files)

The live cache is `~/.cache/claude-code-docs`.

**Verdict.** The lookup plugin is an agent tool and the snapshots are repo references, so those are different levels. The four fetchers do the same job and are accidental. `skogai2-marketplace/CLAUDE.md` names `docs/` as the repo's read-only API reference, which is a legit purpose with a stale copy.

**Smallest change.** Keep `sync-docs.sh`. Delete the `skogai2-skogai` fetcher. The other two die with their old repos (W18). Whether `skogai2-marketplace/docs/` becomes a pointer to the cache is an owner call.

### W13. Nested duplicate manifest

`skogai2-skogix/.claude-plugin/marketplace.json` ("skogix") points at `./plugins/skogdocs/plugins/code-docs-lookup`. `skogai2-skogix/plugins/skogdocs/.claude-plugin/marketplace.json` ("code-docs-tools") points at the same dir. Neither is registered (`~/.claude/plugins/known_marketplaces.json`). Delete the nested one.

### W18. Old-repo skill copies

- `skogai-core/skills/skogai-hook-debugging/SKILL.md` and `marketplace/skogai-hook-debugging/SKILL.md`: md5 `2834462e…`, identical.
- `marketplace/skogai-jq/SKILL.md` and `marketplace/skogai-core/skills/skogai-jq/SKILL.md`: md5 `014d469f…`, identical to each other but different from canonical `skogai-jq/SKILL.md` (`37203d2d…`).
- The plugin name `skogai-core` is used by `skogai2-marketplace` (hooks), `marketplace` and `skogai-core`. Only `skogai2-marketplace` is registered: `known_marketplaces.json` lists `skogai2/marketplace.git` only.

These are generational, so delete them together with the old repos. The skoghooks entry in `marketplace` is **on hold** per the owner. Do not delete that entry without moving it somewhere first.

### Not counted

The generator copy (`marketplace/scripts/generate-marketplace-json.sh` vs `skogai2-marketplace/…`, 355 diff lines) is the old repo's own tool. It goes when that repo is retired.

---

## S7 SERVICES

### W6. `old-systemd-solution` vs the `systemd` repo

53 of the 64 files in `cloudflare/old-systemd-solution/` are byte-identical to their counterparts in `systemd/` (`cmp` per file). Of the rest, 10 differ and 43 paths exist on one side only. Example: `systemd/skogai-memory-start.sh:5-6` uses port 9904 where the old copy uses 9999.

Neither tree is installed. `~/.config/systemd/user` holds only podman-unit symlinks and `skogai-health*`. `skogai-pangolin-new-start.sh` is identical in both and carries the newt secret inline (value not reproduced here).

**Verdict.** Generational. Delete `cloudflare/old-systemd-solution/`. Rotating the secret is separate and already S7 Q5.

### W17. Small repeats

- Three notify units, `podman/units/quadlet-health-notify.service`, `podman/units/pg-backup-notify.service` and `~/.config/skogai/machine/units/skogai-health-notify.service`, are the same 6 lines with a different name. They become one `notify@.service` using `%i`. Same level, low value.
- `cloudflare/pangolin/a.yml` is byte-identical to `docker-compose.yml` (`cmp`). Delete `a.yml`.
- `systemd/user/{pg-backup,quadlet-health}*` are committed symlinks into the live podman checkout. They record podman's install state in the wrong repo, so delete them with the systemd repo's fate.

### Not counted

Root `cloudflared.service` vs the rootless `skognet-cloudflare` quadlet is legit layering, as the S7 flowchart says. `CLOUDFLARE_ACCOUNT_ID` is pinned at `podman/mise.toml:3`, `cloudflare/mise.toml:10`, `cloudflare/scripts/lib/cf.mjs:31` and `podman/bin/quadlet-health:27`, but that is cross-system (S1 env) and belongs in 02b.

---

## W16. Wrapper scripts in harness (new, cross-cuts S1/S2/S5)

`skogcli`, `gptodo` and `gita` are byte-identical in `dash-skogai/bin/`, `skogai-nov10/bin/` and `harness/bin/` (md5 per file). `diff -rq skogai-nov10/bin harness/bin` is empty, so harness carries nov10's whole `bin/`. No flowchart caught this, because Phase 1 read only `harness/marketplace/…`.

`skogcli` is the wrapper that clobbers `SKOGAI_CONFIG_DIR` (W3). Delete the `dash-skogai` and `skogai-nov10` copies, and decide whether the owner-canonical harness should carry them at all.

---

## Sources consulted

- **Inputs:** `00-features.md`, `skogfences-reference.md`, `01-flowcharts/s1…s7` (duplication, gaps and owner sections).
- **S1:** `mise-plugin/hooks/mise_env.lua:1-22`, `mise-plugin/lib/skogai.lua:45-60,118-145`, runner `best-argc-version/modules/core/argc.sh:1-30,640-660` (+ function index), `skogai2-marketplace/scripts/config/argc.sh` (function index, `:225-237`), `scripts/frontmatter/argc.sh` (function index), `skogai2-cli/bin/config:1-40`, `skogai2-cli/lib/config.sh:50-66`, `skogai2-marketplace/plugins/skogai-core/scripts/settings.sh:10-40`, `skogai2-skogai-runner/src/core/log/usage.sh:10-20`, `skogai2-skogai/dash-skogai/{config,mise.config.toml,global/mise.config.toml}`, `skogai2-cli/.skogai/base/mise.system.toml`, `skogai2-skogai/.skogai/scripts/whereami.sh:12-22`, `skogai2-dash-skogai/mise.toml:8-20`, `~/.config/mise/config.toml:85-105`, and an rg sweep for `SKOGAI_CONFIG_DIR` definers and `STAGE_ON(_)STOP`.
- **S2:** runner `WORKORDERS.md:10-50`, hub `SPECIFICATION.md:15-70,125-212`, `harness/…/orchestrate-worktrees.js:1-100`, `tmux-worktree-orchestrator.js` (function index, `:108-246`), `dash-skogai/bin/check-skogai-routes:1-40`, `skogai2-config/bin/check-routes:1-31`, `skogai2-skogai/mise.toml:9-22`, `dash-skogai/bin/skogai-paseo:143-151`, `skogai-run-issue:30-37`, and directory listings of both WO queues.
- **S3:** `skogai2-dash-skogai/admin/{create-agents,setup-coordination,install-coordination,install-tools}.sh`, `README.md:26,66`, `skogai2-skogix/bin/{claude,agy}`, `codex/run`, the shell rc files, `claude/settings.json:23-44`, and `cmp` on the hook.
- **S4:** the three layout docs, `~/.claude/settings.json:139-158`, `skogai2-skogai/.skogai/memory/temporary-paths.md:10-21`, the two `~/Work` journals (wc + git log), the `.skogai/` inventory of every repo, the decision dir listings, and md5 of the openwiki workflows.
- **S5:** `cmp`/`diff -rq` core vs skogai2-core, `skogai2-core/Argcfile.sh:7-50`, `.skogai/modules/repo/argc.sh:1-42`, `repos.csv`/`repos.toml`, `~/.config/gita/`, `~/Work/mise.toml:40-57`, `mani.yaml` (harness, dash entries).
- **S6:** the four docs fetchers (`wc` + URL lines), file counts of the three snapshots, md5 of skills, the five `marketplace.json` files, `known_marketplaces.json`, and the generator diff size.
- **S7:** per-file `cmp` of old-systemd-solution vs systemd, the `skogai-memory-start.sh` diff, `systemd/user` symlinks, `~/.config/systemd/user` listing, the three notify units, `cloudflare/pangolin/` listing + `cmp`, and the `CLOUDFLARE_ACCOUNT_ID` grep.

## Confidence and gaps

- **High:** every byte-identity claim (cmp/md5/diff, run in this pass), the W1 modes, the W2 paths and file sizes, the W3 plugin line, and the W4 function identity.
- **Medium:**
  - W3's effect at runtime: I did not run `mise env` to see whether `[env]` wins over the plugin in practice.
  - W7's adapter idea: the harness library was read only at the function-index level.
  - The `skogharness` submodule is uninitialised.
- **Not verified:**
  - `skogai2-marketplace/plugins/skogai-core/CONFIG.md:95` claims `git-steps.sh` reads `skogai config list`, but `git-steps.sh` (58 lines) contains no `config` or `SKOGAI` string. The claim is likely stale. I did not read the whole file.
  - OpenWiki CI failures (not re-queried).
  - Callers outside `~/Work/repos` (`~/.local/src`, `~/skogai`) for any "no caller" claim.
- **Owner decisions this report needs (not blocking):**
  - W2: what to do with the 875-line journal.
  - W5: whether `core/HANDOVER.md` has anything to keep.
  - W8: the snapshots.
  - W20: OpenWiki, revive or delete.
  - The S5 registry choice.

No repo was modified. The only write in this pass was this file.

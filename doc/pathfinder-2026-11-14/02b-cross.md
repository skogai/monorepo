# 02b — Cross-system duplication (Phase 2)

Scope: concerns that show up in **two or more systems** (S1–S7), plus the owner-named canonical repo `harness` (not covered by any Phase 1 flowchart). Within-system duplication is already in each flowchart's "Duplication seen" table and is not repeated here unless it crosses a system line.

Method: I started from the seven "Duplication seen" tables, then re-read the source for every claim below. Every location in this file was opened in this session unless it is marked *(flowchart, not re-read)*. Classification follows the binding owner answers: two implementations are **accidental** only when they do the same job **at the same level** (workstation-root / human home / agent home / repo / container / remote). Different levels that can stack are **composition**.

Levels used below: **W** workstation-root (`/etc`, `/usr`, system users), **H** human home (`/home/skogix`), **A** agent home / per-agent config, **R** repo (`.skogai/`, `.claude/`, repo-local tasks), **C** container, **X** remote/edge.

## Ranking

Ranked by consolidation value = impact × cheapness. "Cheap" means the target already exists and the change is mostly deleting or re-pointing.

| # | Concern | Systems | Verdict | Impact | Cost | Best match to owner direction |
|---|---|---|---|---|---|---|
| X1 | Agent identity + per-agent config live in the human's home | S1 S2 S3 S6 | Accidental (3 identity models at level A) | High | Low–Med | unix uid (skogfences). The agent users **already exist** |
| X2 | `SKOGAI_CONFIG_DIR` / per-project scope | S1 S3 S4 harness | Not layered: same var, different bases, cwd decides | High | Low | mise-plugin `config_dir` option, one definer per level |
| X3 | Command interface (argc / usage / bin / node / mise tasks) | all | Mostly generational; the leftover argc entry points are accidental | High | Med | mise tasks (+ `usage` specs, per runner `AGENTS.md:20`) |
| X4 | Hook runtimes + journal/log writers | S2 S4 S6 harness | Partly composition (A vs R), partly accidental (2 repo-level journals) | Med–High | Med | open: skogai-core (installed, disabled) vs skogharness (canonical, not installed) |
| X5 | Worktree + work-order hand-off | S2 S5 S6 harness | Accidental at level R; human-pane vs headless is a legitimate split | High | High | harness `orchestrate-worktrees.js` per owner; conflicts with the hub's "authoritative" claim |
| X6 | Layered key/value config CLI | S1 S2 S6 | Accidental; one copy has no caller | Med | Low | skogai2-cli `skogai-config` ("mise holds the values") |
| X7 | `gita` / `gptodo` / `skogcli` wrappers | S2 S5 harness | Accidental, byte-identical ×3 | Low | Very low | harness copy (canonical repo), or a mise tool entry |
| X8 | Project-name / repo-root helpers | S2 S4 S5 S6 harness | Accidental; they return different answers | Med | Low | none yet; `git rev-parse --show-toplevel` is the de-facto majority |
| X9 | Bootstrap: accounts, `/skogai`, project | S1 S3 S4 | Accounts: accidental at W. Project bootstrap: 3 generations at R | Med | Med | mise `[bootstrap.*]` ("mise before custom") |
| X10 | Lesson injection | S4 harness | Accidental ×3 inside harness, plus a doc for a deleted 4th | Low–Med | Low | harness (only live copies) |
| X11 | Health / check scripts | S1 S2 S7 harness | Mostly legitimate layering; one dead, route checkers ×2 accidental | Low–Med | Low | skogai2-config `bin/health` (machine), wrapped as a mise task |
| X12 | Secrets | S1 S3 S7 harness | Composition by level; one committed literal | Med (risk) | Low | fnox at `/etc/skogai` (decided 2026-10-14) |
| X13 | Packaging into `/usr/share/skogai` | S1/S4 S2 | Two packages, one namespace; the installed one ships a deleted file | Low | Low | — |

---

## X1 — Agent identity and per-agent config

**(a) Concern.** Who is acting (agent vs human), and where that actor's config lives.

**(b) Locations.**
- unix user: `skogai2-dash-skogai/admin/create-agents.sh:11` (`AGENTS=(claude dot amy goose codex)`), `:19-20` (`useradd --system --create-home --home-dir /home/$a`). On this machine `getent group skogai` → `claude,dot,skogix,amy,goose,codex`: **all five agent users exist.**
- `SKOGAI_USER` from `CLAUDECODE`: `skogai2-dash-skogai/mise.toml:12-13`.
- `FNOX_PROFILE` from `CLAUDECODE` (commented): `skogai2-dash-skogai/mise.toml:17-18`; the live fnox model uses profiles stacked by the human (`skogai2-config/secrets/fnox.md:50-57`).
- `SKOGAI_AGENT_NAME` per agent namespace: `skogai2-skogai/config/config.json:27,33,39`; consumed with a `skogix` default by `skogai2-core/scripts/context/context-start.sh:5,7`.
- Launcher keeps the human's identity and home: `skogai2-skogix/bin/claude:3-4` (`HOME="$HOME" USER="$USER"`), `:17` (`CLAUDE_CONFIG_DIR="/skogai/claude"`), `:18` (`"$HOME/.local/bin/claude"`).
- Per-agent config that points back into the human home: `skogai2-skogix/claude/settings.json:23,44,55,66,77` (`/home/skogix/.config/herdr/plugins/...`), `skogai2-skogix/agy/settings.json:10-12` (`read_file(/home/skogix/.config)`), `skogai2-skogix/claude/shell/.zshrc:1` (`/home/skogix/.local/bin` on PATH).
- Claude auto-memory lives in the human home: `~/.claude/settings.json:171` (`autoMemoryDirectory = /home/skogix/claude/.skogai/memory`).

**(c) Why they diverged.** Agents run as `skogix` today, so "who" cannot come from the uid. Each system invented an env-var proxy: S3 for mise secrets, S2 for skogcli namespaces, S5 for context headers. The launcher in skogai2-skogix isolates the *env* (`env -i`) but not the *user*.

**(d) Verdict.** Accidental. All four answer "who am I" at level A. The env-var models exist only because the uid model is not used yet, and `create-agents.sh` shows the uid model is ready. The per-agent settings that reference `/home/skogix/...` break the skogfences rule "the human's home is sacred" in the opposite direction: the agent's config depends on the human's home.

**(e) Owner direction.** skogfences: identity = `id -un`. The cheapest next step is a launcher that does `sudo -u claude` (or systemd `User=`) instead of `env -i HOME=$HOME`. `skogai2-config/mise/bootstrap.md:141-142` already notes that `sudo -u <agent> <cmd>` works with `nologin`. `SKOGAI_USER` can then be derived from the uid instead of `CLAUDECODE`.

---

## X2 — `SKOGAI_CONFIG_DIR` and per-project scope

**(a) Concern.** Where SkogAI config is read from. The owner says it is "whatever you set it to", which is fine only if each level sets it once and the levels are documented.

**(b) Locations, with the value actually resolved by `mise env` today.**

| Definer | Level | Value | Resolved where |
|---|---|---|---|
| `~/.config/mise/config.toml:93` | H | `/home/skogix/skogai/config` | `~` → `/home/skogix/skogai/config` |
| `mise-plugin/hooks/mise_env.lua:15` → `mise-plugin/lib/skogai.lua:53-64` | R (monorepo) | `config_dir` option or `$XDG_CONFIG_HOME/skogai` | `~/Work` → `/home/skogix/.config/skogai` |
| `dot-skogai/mise.toml:49-50` | R | `.skogai/config` (relative, by design) | `repos/dot-skogai` → `.skogai/config` |
| `skogai2-skogix/mise.toml:6` | A | `/skogai/config` | not resolved: mise config untrusted, and `/skogai` does not exist |
| `harness/bin/skogcli:2-3` ≡ `dash-skogai/bin/skogcli` ≡ `skogai-nov10/bin/skogcli` | R | `.skogai/config/<gh repo name>` | per call |
| `skogai2-skogai/config/config.json` (harness namespace, line 19) | R | `.skogai/config/harness` | skogcli only |

Plus the scope-pointer names (`SKOGAI_CONFIG_*_DIR`, `SKOGAI_{SYSTEM,LOCAL}_DIR`, `skogai.config.system.dir`) listed in `s1-env.md` §6 #6 *(flowchart, not re-read)*.

**(c) Why.** Each generation pointed the one variable at its own idea of "the config": a global dir (H), the XDG dir (mise-plugin), a per-project dir (skogcli), the shared ground (S3).

**(d) Verdict.** These do sit at different levels, so composition is possible. But they are not composed: there is one variable, no precedence order, and whichever config mise loads last for the cwd wins. `~` and `~/Work` already disagree (`~/skogai/config` vs `~/.config/skogai`). Accidental in shape, legitimate in intent.

**(e) Owner direction.** mise-plugin is the only definer that is a function of a declared option (`config_dir`) rather than a literal. Keep one variable per level (e.g. system / agent / project) and let the plugin compute them. Dropping the literal at `~/.config/mise/config.toml:93` is a one-line change.

---

## X3 — Command interface

**(a) Concern.** How a human or agent invokes a SkogAI command.

**(b) Locations (counts from `git ls-files` + grep for `# @cmd|# @describe`, `#USAGE`, `[tasks.*]`/`[tasks]`, `mise-tasks/`, `bin/`).**
- argc: `skogai2-core` (65 files), `core` (44), `skogai2-skogai-runner/best-argc-version` (28), `marketplace` (20), `skogai2-skogai` (18, e.g. `.skogai/scripts/get-project-name.sh:4,10`), `skogai2-cli/bin/config:20-93`, `docs/todo/tools/argc` (9, archive).
- usage: `skogai2-skogai-runner` (`src/core/log/usage.sh`), declared the interface at `skogai2-skogai-runner/AGENTS.md:20` ("usage + mise are the interface (skogix, 2026-11-06) … argc … is no longer extended"); `podman/mise-tasks/*` (7 file tasks).
- mise tasks: `cloudflare/mise.toml:12-24`, `dot-skogai/mise.toml:16-43`, `skogai2-skogai-runner/mise.toml:8-20`, `dash-skogai/mise.toml:21-23`, `harness/mise.toml:26-27`, `skogai2-skogai` (`AGENTS.md:14` `mise run dash:check`).
- plain `bin/` scripts with no task wrapper: `skogai2-config/bin/{health,check-routes,check-coverage}`, `systemd/bin/*` (7), `podman/bin/*` (8).
- node scripts: `harness/marketplace/plugins/skogharness/scripts/*.js` (`orchestrate-worktrees.js:16-17` usage text), `cloudflare/scripts/*.mjs` (wrapped by mise tasks at `cloudflare/mise.toml:14-17`).

**(c) Why.** Generational: argc (core, best-argc-version) → usage (runner, 2026-11-06) → mise tasks as the owner's interface rule. Old argc entry points stayed in place.

**(d) Verdict.** argc vs usage is generational, not concurrent: the runner's own `AGENTS.md:20` retires argc for new work. The accidental part is the leftover **entry points**: `skogai2-core/Argcfile.sh` is still the HQ CLI, and `skogai2-config/bin/health` is not reachable as a mise task anywhere I found (the only mise reference is the timer link at `~/.config/mise/config.toml:245`). Node and argc implementations are fine *behind* a mise task. cloudflare already does exactly that.

**(e) Owner direction.** cloudflare (`mise.toml:12-24`) and podman (`mise-tasks/`) already match the rule. The cheapest wins are wrapping `skogai2-config/bin/health`, `skogai2-config/bin/check-routes` and `orchestrate-worktrees.js` as mise tasks. The implementations stay.

---

## X4 — Hook runtimes and journal/log writers

**(a) Concern.** What runs on Claude Code hook events, and where session history is written.

**(b) Locations.**

| Runtime | Level | Writes to | State today |
|---|---|---|---|
| skogai-core plugin (bash) `skogai2-marketplace/plugins/skogai-core/scripts/settings.sh:34-36` | R | `.skogai/logs/skogai-core/log.jsonl`, `.skogai/journal.md`, `.skogai/tmp`; overridden by `~/.claude/settings.json:154,156,158` to `.skogai/logs/{log.jsonl,journal.md,state}` | installed, **disabled** (`~/.claude/settings.json:104`) |
| skogharness (ECC fork, node) `harness/marketplace/plugins/skogharness/hooks/hooks.json:10-68`; session dir `scripts/lib/utils.js:16,56-58` + `scripts/lib/agent-data-home.js:94` | A | `$HOME/.claude/session-data` | **not installed** (absent from `~/.claude/plugins/installed_plugins.json`) |
| skogix-hooks (bash) `harness/marketplace/plugins/skogix-hooks/hooks/stop.sh:18-19`, `session-start.sh:33` | none | `/tmp/<session_id>.jsonl` | not installed; matches the "/tmp-based" runtime S6 found only through a skill (`s6-plugins.md` #4) |
| skoghooks `harness/marketplace/plugins/skoghooks/hooks/hooks.json` | R | lesson injection only | on hold (owner) |
| VV Claude Code Harness, vendored per repo: `skogai2-skogai-runner/.claude/hooks/enforce-scope.sh:2` ("VV Claude Code Harness"), `skogai2-skogai/.claude/hooks/*` | R | `.harness/claude-progress.txt`, `.harness/features.json` | live via project `.claude/settings.json` (`skogai2-skogai-runner/.claude/settings.json:19-28`) |
| runner run log `skogai2-skogai-runner/src/core/log/usage.sh:15` | R | `$XDG_STATE_HOME/skogai/run.jsonl` via **`SKOGAI_LOG`**, the same name `settings.sh:34` uses for the hook log | |
| dot-skogai journal tree `dot-skogai/journal/YYYY-MM-DD/` *(s4, not re-read)*; archive `docs/todo/agents/claude/journal/2025-03-*.md` | A (per agent) | | historical |

Repo-level journals actually committed: `.skogai/journal.md` in cloudflare, skogai2-aliasflare, skogai2-marketplace, skogai2-skogai, skogai2-skogai-runner, skogai2-skogix, skogai2-skogpunk; `.harness/claude-progress.txt` in skogai2-skogai and skogai2-skogai-runner. **skogai2-skogai and the runner carry both.**

The vendored VV hooks have diverged: same file names, different content in the two repos (md5 differs for `commit-gate.sh`, `enforce-scope.sh`, `verify-git-identity.sh`, `verify-task-quality.sh`; identical for `harness_state.py`, `statusline.sh`).

**(c) Why.** Three origins: the home-grown journal hook (S6), an imported harness template (VV, copied into repos), and an imported plugin (ECC → skogharness). None replaced the others.

**(d) Verdict.** Composition is possible and partly real: skogharness writes at level A (agent home), skogai-core at level R. Those two could stack. Accidental: two repo-level session journals in the same repo (`.skogai/journal.md` and `.harness/claude-progress.txt`), the per-repo VV copies drifting apart, and the `SKOGAI_LOG` name meaning two different files.

**(e) Owner direction.** The owner named harness as canonical, but the canonical hook plugin is not installed, and the installed one is disabled. **Today no SkogAI hook runtime is active for this user.** Which runtime owns level R is the one open decision here (see Q1).

---

## X5 — Worktree creation and work-order hand-off

**(a) Concern.** Isolate a task in a worktree and brief an agent with what to do and what it may touch.

**(b) Locations.**

| Implementation | Worktree root | Brief format | Level |
|---|---|---|---|
| harness `orchestrate-worktrees.js:7-11,78-91` → `scripts/lib/tmux-worktree-orchestrator.js:181-184,207-211,232` | `worktreeRoot` default = **parent of the repo** (siblings `<repo>-<session>-<worker>`); branch `orchestrator-<session>-<worker>` | `.orchestration/<session>/<worker>/{task,handoff,status}.md` | R, tmux |
| herdr hub `skogai2-skogai/orchestration/README.md:10,22,40-58,65-69` | `~/.herdr/worktrees/<repo>/<branch>`; branch `wo/<name>` | `orchestration/work-orders/open/*.md` (`owns` frontmatter) | R, herdr panes |
| runner `skogai2-skogai-runner/.skogai/workorders/WORKORDERS.md:15-16,24-27,36,41` | none (agent picks); branch `wo/<name>` | `.skogai/workorders/{open,done}/*.md` | R |
| core `wt` + `tmp/context` `skogai2-core/Argcfile.sh:8` (`WORKTREE_DIR=/home/skogix/dev`), `skogai2-core/HANDOVER.md:122-123`; worktrunk `~/.config/worktrunk/config.toml:48` (`~/dev/{{repo}}/{{branch}}`) | `~/dev/...` | `tmp/context/` seeded from a ticket | H |
| skogix-hooks `WorktreeCreate` `harness/marketplace/plugins/skogix-hooks/hooks/worktree-create.sh:12-18` | whatever Claude Code passes | none | R |

Conflicting rules: the hub says every code task gets a worktree (`orchestration/README.md:10`) and calls itself authoritative (`skogai2-skogai/.skogai/rules/herdr-orchestration.md:21`); machine config says "worktrees only when asked" (`skogai2-config/agents/herdr.md:135-137`).

**(c) Why.** Generational (wt → paseo → herdr, per `s2-run.md` D6/D13), plus harness imported from ECC with its own tmux model. `orchestrate-worktrees.js` was last changed 2026-07-14 (`git log` `3e5d144`); the herdr hub is from 2026-11-07.

**(d) Verdict.** Accidental at level R: harness, herdr and the runner all produce a worktree + a Markdown brief with a scope, in three formats and three roots. The legitimate split is human-in-a-pane (herdr, tmux) vs headless (runner `claude -p`), which `s5-fleet.md` already notes.

**(e) Owner direction.** harness, by owner statement. Its plan format (`task.md`/`handoff.md`/`status.md`) has no `owns` field, while both the hub and the runner formats depend on `owns` for safe parallel hand-out. Adopting harness means either adding `owns` to its plan or dropping that guarantee. This also needs the hub's "authoritative" line retracted (see Q2).

---

## X6 — Layered key/value config CLI

**(a)** get/set/unset/list/env/files over system/global/local layers.

**(b)** `skogai2-skogai-runner/best-argc-version/modules/core/argc.sh:25-130` (S2); `skogai2-marketplace/scripts/config/argc.sh:27-131` (S6); `skogai2-cli/bin/config:20-93` (S1). The fold engine is a verbatim copy: `diff` of `argc.sh:655-700` against `scripts/config/argc.sh:238-283` is empty.

**(c)** The marketplace copy says it was extracted from the runner (`skogai2-marketplace/CLAUDE.md:15`). skogai2-cli is the "mise holds the values" rewrite (`skogai2-cli/CLAUDE.md:70,120`).

**(d)** Accidental: one job, same level (R/H config files), three systems. The marketplace copy has no caller in its repo besides that CLAUDE.md line, so it is present in source with usage not established. The runner copy sits in `best-argc-version/`, which its `AGENTS.md:59` calls "not superseded" but untested.

**(e)** skogai2-cli: it is the one that delegates storage to mise.

---

## X7 — Wrapper triple

**(b)** `harness/bin/{gita,gptodo,skogcli}`, `dash-skogai/bin/{gita,gptodo,skogcli}`, `skogai-nov10/bin/{gita,gptodo,skogcli}`. md5 identical per name across all three repos (`a683c6dd`, `6ea3321b`, `5ca2eb18`).

**(c/d)** Copied with each repo generation. Accidental, but trivial, except that `skogcli:2-3` embeds a project-name rule (X8) and a `SKOGAI_CONFIG_DIR` rule (X2).

**(e)** harness is the canonical repo. These could equally be `uv`/`pipx` tool entries in a mise `[tools]` table, which removes the files altogether.

---

## X8 — Project-name and repo-root helpers

**(b)**
- `gh repo view --json name`: `skogai2-skogai/.skogai/scripts/get-project-name.sh:7`; `harness/bin/skogcli:2` (and its two copies).
- parent dir of `.skogai`: `dot-skogai@55312d8:scripts/skogai-helper-functions.sh:6-10`. The current `dot-skogai/scripts/get-project-name.sh` is a symlink to `/home/skogix/.local/src/skills/extras/scripts/get-project-name.sh`, outside the repo.
- `basename(repoRoot)`, where `repoRoot` defaults to cwd: `harness/.../tmux-worktree-orchestrator.js:176-177`.
- `git rev-parse --show-toplevel`: `skogai2-marketplace/plugins/skogai-core/scripts/events/Stop.sh:14`; `skogai2-skogai-runner/.claude/hooks/{commit-gate.sh:179,enforce-scope.sh:78,verify-git-identity.sh:15,verify-task-quality.sh:30}`.
- mise-plugin root = declaring config dir: `mise-plugin/lib/skogai.lua:43-50`.

**(c/d)** Accidental. The answers differ: in a worktree at `~/.herdr/worktrees/skogai/wo-x`, `gh repo view` gives `skogai`, while basename and `show-toplevel` give the worktree dir name. Without a network connection `gh` fails. Config paths keyed on project name (X2) therefore change with the worktree.

**(e)** No owner statement. `git rev-parse --show-toplevel` is the majority and works offline, but it gives the worktree name. If config must survive worktrees, the remote-derived name is the one that is stable. Small decision, see Q3.

---

## X9 — Bootstrap: accounts, `/skogai`, projects

**(a)** Two concerns share the word: machine/account bootstrap (W) and project bootstrap (R).

**(b) Accounts and `/skogai` (W).**
- `skogai2-dash-skogai/admin/create-agents.sh:13-27` creates the group and users.
- `skogai2-dash-skogai/admin/setup-coordination.sh:16-25` creates fewer of them *(s3, not re-read)*.
- mise `[bootstrap.groups.skogai]` + `[bootstrap.users.skogix]`: `~/.config/mise/config.toml:223-231`. The agent users and the `/skogai` dirs were declared there and removed on 2026-10-31 (`skogai2-config/mise/bootstrap.md:27-32,125-128,137-140`).
- `skogai2-config/mise/bootstrap.md:30` says "The machine still has all of them". True for the users, **false for `/skogai`** (`ls -ld /skogai` → no such file).

**Project bootstrap (R).** `dot-skogai/mise.toml:16-27` (`setup` task, an argc toolchain build); `skogai2-cli/PKGBUILD:26-30` installs `.skogai/base` to `/usr/share/skogai/base` "the base a repo copies into its .skogai/base"; `dot-skogai@55312d8:scripts/bootstrap/bootstrap.sh` and the empty `skogai2-dot-skogai` *(s4, not re-read)*; `harness/mise.toml:26-27` + `harness/bin/install-skogcli:3` install skogcli.

**(c)** mise bootstrap was adopted on 2026-10-14 and trimmed on 2026-10-31. The dash scripts predate it and were kept for what mise no longer declares.

**(d)** Accounts: accidental. `create-agents.sh` and mise `[bootstrap.users]` do the same job at W. Today they don't collide only because mise stopped declaring agents. Project bootstrap: three generations with no complete one (as s4 found). skogai2-cli's PKGBUILD path (W, shared base) vs a `.skogai` submodule (R, per project) are different levels and could compose: the package provides the base, the submodule pins a version.

**(e)** "mise before custom": re-declare the agent users in `[bootstrap.users.*]` (the old declaration is recorded at `bootstrap.md:137-140`) and keep `create-agents.sh` only if mise cannot express something.

---

## X10 — Lesson injection

**(b)** `harness/scripts/match-lessons.py:1-20` (1602 lines; reads `gptme.toml [lessons]`, but harness tracks no `gptme.toml`); `harness/marketplace/plugins/skoghooks/hooks/lesson_matcher.py` (393 lines, `LESSON_DIRS` at `:347`); `harness/marketplace/plugins/skogix-hooks/hooks/lesson_matcher.py` (md5 differs from skoghooks). `dot-skogai/SKOGAI.md:51,79` documents a `lesson_matcher.py` that loads `knowledge/lessons/`; it was removed from dot-skogai in `12a74da` "cleanup", and `dot-skogai/knowledge/lessons/` still holds lessons.

**(d)** Accidental: three matchers in one repo, plus lesson data in S4 whose matcher now lives only in harness. **(e)** harness, with skoghooks on hold. The dot-skogai doc should point at whichever matcher is kept.

---

## X11 — Health and check scripts

**(b)**
- Machine health: `skogai2-config/bin/health:1-13` runs every `<group>/health`. `skogai2-config/containers/health:2,6` wraps `podman/bin/quadlet-health` (at its live path `~/.config/containers/systemd/bin/quadlet-health`).
- Dead: `systemd/bin/check:8-11` (reads `services.json` healthchecks; no skogai-* unit is installed per s7).
- Routing checkers: `skogai2-config/bin/check-routes:1-7` (bash, `<routes>` blocks); `dash-skogai/bin/check-skogai-routes:1-13` (python, a different route grammar `ROUTE_RE` at `:13`), wired as `dash-skogai/mise.toml:21-23`. Plus the LLM `dash:check` and `validate_router.py` copies *(s2 D11, not re-read)*.
- Different subject, not duplication: `harness/.../skogharness/scripts/skills-health.js:4,9` (skill health), `harness-audit.js`.

**(d)** quadlet-health ↔ skogai-health is legitimate layering (H machine → container scope). The two route checkers validate **different grammars** (`- @route` vs `- @route - description`). That is accidental, and it also means a file can pass one and fail the other.

**(e)** skogai2-config `bin/health` as the single entry, exposed as a mise task. One route grammar.

---

## X12 — Secrets

**(b)**
- fnox, root-owned: `/etc/skogai/fnox.toml`, decided at `skogai2-config/secrets/fnox.md:68-80`, deployed by mise bootstrap. On disk it is `root:skogix 0644`, not `root:root` as decided at `:68`.
- fnox example in shared ground: `skogai2-dash-skogai/fnox.toml:1-21` (example secrets only); `fnox.md:75-80` rejects `/skogai` as unsafe.
- gitignored env files: `harness/mise.toml:24` (`_.file = ".env"`), `dot-skogai/mise.toml:54`, `podman/mise.toml:8` (`termix/termix-claude.env`, ignored by `podman/.gitignore:2`).
- Committed literal secret: `cloudflare/pangolin/NEWT.env` and `cloudflare/pangolin/newt.quadlet.container:9` each contain a 48-character literal `NEWT_SECRET` (values not reproduced here), tracked since `5f31c52`.
- Non-secret ID pinned four times: `podman/mise.toml:3`, `cloudflare/mise.toml:10`, `cloudflare/scripts/lib/cf.mjs:31`, `podman/bin/quadlet-health:27`.

**(d)** fnox (W) → `.env` (R, machine-local) is composition: different levels and trust. The committed Pangolin secret is not duplication, but it is the one place where a secret is in git. The owner's order is "working first, harden after", so this is flagged, not urgent. Whether it is still valid is not verified. The account-ID pin is trivial and belongs in S1's env plane.

**(e)** fnox `/etc/skogai` for anything agents must read but not write. Per-repo `.env` for machine-local values.

---

## X13 — Packaging namespace

**(b)** `skogai2-cli/PKGBUILD:6,29,33,38` (`pkgname=skogai` → `/usr/share/skogai/base`, `/usr/bin/skogai-*`, `/usr/lib/skogai`); `skogai2-skogai-runner/packaging/arch/PKGBUILD:3,31` (`skogai-runner-git` → `/usr/share/skogai/core/main.sh`); `skogai2-skogai-runner/Containerfile:3-12` (arch + mise, user `dev` with passwordless sudo).

**(d)** No file conflict today. Two packages each describe themselves as the skogai core framework (`pkgdesc` at cli `:9`, runner `:6`) under one prefix. `skogai-runner-git r40.07d6da9` **is installed** and ships `src/core/main.sh`, which the runner's own `AGENTS.md:14` says was deleted. `pacman -Ql` confirms that one file. The Containerfile is level C (test image), which is legitimate, though its sudo-capable `dev` user is the opposite of the skogfences agent model. That is fine for a disposable test image and wrong if it becomes the remote agent image.

---

## Composition map: what sits where

| Concern | W | H | A | R | C/X |
|---|---|---|---|---|---|
| identity | agent users exist (`create-agents.sh`) | `skogix` | **env proxies** (`SKOGAI_USER`, `SKOGAI_AGENT_NAME`) | | `dev` user (Containerfile) |
| config dir | `/etc/skogai/config` | `~/.config/mise/config.toml:93` | `/skogai/config` (missing) | mise-plugin, dot-skogai, skogcli | — |
| secrets | `/etc/skogai/fnox.toml` | | fnox profile | `.env` | literal in cloudflare |
| hooks/journal | | | skogharness `~/.claude/session-data` (not installed) | skogai-core `.skogai/journal.md` (disabled), VV `.harness/` (live) | |
| worktrees | | `~/dev` (wt) | | harness siblings, `~/.herdr/worktrees`, runner WO | |
| health | | `skogai2-config/bin/health` | | route checkers ×2 | quadlet-health |

The gaps run down column A. That column is the skogfences agent home, and it is where the duplicates cluster: each system substitutes an env var or a path into `/home/skogix` for a level that does not exist yet (`/skogai` missing, agents not run as their own users).

## Not duplication (checked and set aside)

- Plugin source published vs develop (`~/Work/.config/mise/conf.d/plugin.skogai.toml:4` vs `plugin.develop.toml:8`): documented split.
- Root `cloudflared` vs rootless `skognet-cloudflare` quadlet (s7): different trust sides.
- `cf-manage` skill in `.claude/` and `.agents/` (s7): two client layouts.
- argc behind a mise task (cloudflare, dot-skogai): implementation detail under the required interface.
- Headless `claude -p` vs pane workers (s2 D7): different modes. Only the permission-mode choice is ad hoc.

## Questions (only Q1 blocks anything)

- **Q1.** Which hook runtime owns the repo level (R): skogai-core (bash, installed but disabled) or skogharness (ECC, canonical but not installed)? The VV per-repo hooks are live in two repos regardless. This decides where X4's journal goes.
- **Q2.** If harness `orchestrate-worktrees.js` is canonical (X5), should its plan gain an `owns` list, and should the hub's "authoritative" line (`herdr-orchestration.md:21`) be withdrawn?
- **Q3.** Should the project name be stable across worktrees (remote name) or follow the checkout (`show-toplevel`)? (X8, feeds X2.)

## Sources consulted

Inputs: `00-features.md`, `skogfences-reference.md`, `prompts/owner-answers.md`, all seven `01-flowcharts/s*.md` (duplication sections in full).

Source read this session: `harness/{mise.toml,bin/*,scripts/match-lessons.py,.gitmodules}`, `harness/marketplace/plugins/skogharness/{scripts/orchestrate-worktrees.js, scripts/lib/tmux-worktree-orchestrator.js, scripts/lib/utils.js, scripts/lib/agent-data-home.js, hooks/hooks.json, scripts/skills-health.js, .claude-plugin/plugin.json, README.md}`, `harness/marketplace/plugins/{skoghooks,skogix-hooks}/hooks/*`; `skogai2-dash-skogai/{mise.toml,fnox.toml,admin/create-agents.sh}`; `skogai2-skogix/{bin/claude,mise.toml,claude/shell/.zshrc,claude/settings.json,agy/settings.json}`; `skogai2-skogai/{config/config.json,orchestration/README.md,.skogai/rules/herdr-orchestration.md,.skogai/scripts/get-project-name.sh,.claude/hooks/*}`; `skogai2-skogai-runner/{mise.toml,AGENTS.md,Containerfile,packaging/arch/PKGBUILD,.skogai/workorders/WORKORDERS.md,.claude/settings.json,.claude/hooks/*,.harness/init.sh,best-argc-version/modules/core/argc.sh}`; `skogai2-marketplace/{scripts/config/argc.sh,plugins/skogai-core/scripts/settings.sh,plugins/skogai-core/CONFIG.md,CLAUDE.md}`; `skogai2-cli/{PKGBUILD,bin/config,CLAUDE.md}`; `skogai2-config/{bin/health,bin/check-routes,containers/health,mise/bootstrap.md,secrets/fnox.md,agents/herdr.md}`; `mise-plugin/{hooks/mise_env.lua,lib/skogai.lua}`; `dot-skogai/{mise.toml,SKOGAI.md}` + `dot-skogai@55312d8:scripts/skogai-helper-functions.sh`; `skogai2-core/{Argcfile.sh,HANDOVER.md,scripts/context/context-start.sh}`; `dash-skogai/{mise.toml,bin/check-skogai-routes}`; `systemd/bin/check`; `podman/{mise.toml,.gitignore}`; `cloudflare/{mise.toml,scripts/lib/cf.mjs,pangolin/NEWT.env (keys only),pangolin/newt.quadlet.container}`; `~/.config/mise/config.toml`, `~/.config/worktrunk/config.toml`, `~/.claude/settings.json`, `~/.claude/plugins/installed_plugins.json`.

Machine state checked: `getent passwd/group` (agent users and `skogai` group exist); `ls -ld /skogai` (missing), `/etc/skogai` (present); `mise env` in `~`, `~/Work`, `dot-skogai`, `harness`, `skogai2-skogix` (the last two are untrusted); `pacman -Q/-Ql skogai-runner-git`; md5 comparisons of wrapper, hook and lesson-matcher copies; `diff` of the two fold engines.

## Confidence and gaps

- **High:** X1, X2, X6, X7, X13 (direct reads plus machine checks).
- **Medium:** X3 (grep counts can miss argc files that use other markers), X4 (I did not trace what the VV hooks write beyond file headers and the settings), X5 (harness behavior read from code, not run), X8, X11, X12.
- **Low–medium:** X9 project bootstrap and X10's dot-skogai side rest partly on s4 and git history.
- Not read: `~/skogai/` and `~/.local/src/*` checkouts (the second clone root from s5), `skogai2-config` health groups other than `containers`, the `harness/skills` submodule (not checked out).
- I did not test whether the committed `NEWT_SECRET` is still valid.
- `/etc/skogai/fnox.toml` group ownership (`skogix`) differs from the decision text. Not checked whether that is intended.

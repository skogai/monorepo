# skogai 3.0 — basic plan

Status: draft, 2026-11-10 (re-verified the same evening). Sources: `.skogai/research/*`, `skogix/.skogai/todo.list`,
git history (including the files removed in `6d0ce28`), and a live test of the current setup.

## 1. Decisions already made

These come from what is in the repo, the global mise config, and the todo list. They are
the starting point. The research does not override them.

| Area | Decision | Evidence |
|---|---|---|
| Workstation | Arch Linux + Omarchy | todo #5 |
| Tools, env, tasks, monorepo | **mise** for all four | `mise.toml` (`monorepo_root`, `config_roots`, `[tasks]`), `.miserc.toml` |
| skogai env | mise **env plugin** `skogai/mise-plugin` | `[plugins] skogai`, `_.skogai-develop` |
| Repo layout | `skogai/monorepo` root + git submodules (`skogai`, `skogix`, `mise-plugin`) | `.gitmodules` |
| Agent workspace | **t3code** (threads) + **herdr** (panes) + **worktrunk** (worktrees) | todo #3, #5, `mise.toml` |
| VCS / hosting | git + GitHub org `skogai`, branch `master` | remotes |
| Decisions log | ADRs with adr-tools in `doc/adr/` | todo #4, old ADR 0001 |
| Secrets | fnox / age through mise, nothing plain in git | global mise tools, todo #8, old `SKOGIX.md` |
| Search | `rg` / `git grep` baseline; **qmd** under trial | old `.skogai/docs/qmd/` |

## 2. Where the research disagrees with that

All three write-ups agree on: Markdown in git, ADRs, a fresh-clone README, `rg` first and
RAG as a rebuildable layer, GitHub for code review. Keep those.

Drop or defer these:

- **Taskfile / Turborepo / Nx / Moon** (gemini, claude). mise monorepo tasks
  (`//path:task`) already do this. Tested and working.
- **Python-first, uv workspaces, Postgres + pgvector, docker-compose, MkDocs** (gemini,
  codex). Premature. There is no app code yet. Add each one with an ADR when something
  needs it.
- **Directory blueprint** (`apps/`, `packages/`, `mcps/`). Wait until there is real
  content. Submodules are the unit for now.
- **The research's open question** ("JS or polyglot?"). The answer is polyglot, with mise
  as the glue.

Still open (needs your call):

- **Tickets:** GitHub Issues (all three research docs) or keep `.skogai/todo.list`?
  A middle path: the todo list stays the inbox, and an item becomes an Issue once it needs
  a PR.
- **Global vs repo config:** see finding 4 below.

## 3. Test findings (current setup, mise 2026.11.5)

1. ✅ Monorepo task discovery works: `//:hello`, `//mise-plugin:lint`, `//mise-plugin:lint-fix`.
   `mise run hello world` prints `MONOREPO: hello from the monorepo root! world`.
2. ✅ The env plugin loads through `skogai-develop`, a symlink to `./mise-plugin`, and sets
   `SKOGAI_ENV_VAR`, `SKOGAI_MONOREPO_DIR`, and `SKOGAI_CONFIG_DIR`.
3. ✅ ~~`mise plugins ls` warns `failed to open git repository … skogai-develop`~~. This no
   longer reproduces after `4c85eca`. `skogai` (installed from GitHub) and `skogai-develop`
   (symlink to `./mise-plugin`) are both listed with no stderr. The relative
   `gitdir: ../.git/modules/mise-plugin` is still a known trap if a symlink is re-created.
4. ⚠️ **Env bleed from global config.** `~/.config/mise/config.toml` and `conf.d/hello.toml`
   add `SKOGAI_DOCS_DIR`, `XDG_SKOGAI_DIR=~/skogai`, `LOADOUT`, a `bootstrap` task, and
   about 60 tools. A fresh clone on another machine would behave differently. Each piece
   has to be either moved into the repo (or the plugin) or recorded as a workstation
   prerequisite. Concrete collisions seen live:
   - `SKOGAI_CONFIG_DIR`: global sets `~/skogai/config`, the plugin sets `~/.config/skogai`.
     The plugin wins, silently.
   - `tasks.hello` + `SKOGAI_HELLO_GREETING` are defined both in `conf.d/hello.toml` (writes
     `./greeting.txt`) and in the repo (writes `/tmp/greeting.txt`). The repo shadows the global one.
   - There is a **third layer**: `/etc/mise/conf.d/omarchy-tools.toml` (Omarchy-provided tools such
     as amp and antigravity-cli). So the layers are omarchy → global/dotfiles → repo → submodule.
5. ⚠️ The plugin hardcodes `SKOGAI_MONOREPO_DIR = $HOME/Work`. It should come from plugin
   options or the config root.
6. ⚠️ `mise doctor`: 1 problem and 47 warnings. The problem: the dotfiles setup is missing
   `~/.dotfiles/.config/atuin/config.toml`, so syncing is paused. The top warning: `conf.d/hello.toml`
   has a sync conflict. This blocks todo #8, since mise dotfiles is the bootstrap path.
7. ⚠️ There is no `.gitignore`. The old one ignored `/SECRETSINHERE/` and `/.qmd`. Restore it
   before anything else lands.
8. ℹ️ The `mise-plugin` dev tools (actionlint, lua, stylua, pkl, …) show as missing. `mise install --monorepo`.
10. ℹ️ Tool inventory: `adr` (adr-tools 3.0.0), `herdr`, `t3`, `wt` (worktrunk), `fnox`, and `age` are on PATH.
    `taplo` (todo #1) and `qmd` (search trial) are **not** installed.
9. ℹ️ The `skogai` and `skogix` submodules only contain a README, plus the todo list in skogix.

## 4. Plan

Each step is small, ends in a commit, and has a check you can run.

### Phase 0: Hygiene (now)
- [ ] Restore `.gitignore` (`/SECRETSINHERE/`, `/.qmd`). *Check:* `git status` is clean.
- [ ] Add `CLAUDE.md` / `AGENTS.md` (rewrite the deleted one for the current layout) and a
      README quickstart. *Check:* a fresh clone plus `mise install --monorepo` runs `mise run hello x`.

### Phase 1: Decisions on paper (todo #4, #5, #7)
- [ ] `adr init doc/adr` → 0001 record architecture decisions.
- [ ] 0002 workstation baseline: Arch + Omarchy, mise, t3code, herdr, git, worktrunk.
- [ ] 0003 monorepo = mise `monorepo_root` + submodules. No Taskfile, Turbo, or Nx.
- [ ] 0004 skogai env via mise env plugin.
- [ ] `doc/legacy.md`: map the old skogai repos and names onto the monorepo (todo #7, needs your input).
- *Check:* `adr list` shows them, and `rg -n mise doc/` finds them.

### Phase 2: The `.skogai/` convention (todo #6)
- [ ] Define what lives in a `.skogai/` folder at any level: `research/`, `todo.list`,
      `plan.md`, maybe `docs/`. Write it as ADR 0005 plus a short README.
- [ ] Decide where `todo.list` lives (root or per submodule).

### Phase 3: mise hardening (todo #1, #2, #8)
- [ ] Sort the global-vs-repo env (finding 4). Write down what a workstation must provide.
- [ ] Make the plugin's paths configurable (finding 5) and fix or document the symlink warning (finding 3).
- [ ] Add nvim schemas: taplo with the mise JSON schema for `mise.toml` and `.miserc.toml` (todo #1).
- [ ] Encryption: fnox + age through mise. Fix the dotfiles doctor error first (todo #8).
- *Check:* `mise doctor` shows 0 problems, and `mise env` in a clean shell matches the documented list.

### Phase 4: Workflow (todo #3)
- [ ] Describe the t3code → herdr → worktrunk loop: how a thread gets a worktree, how
      work lands on `master`. Validate it by running this plan's own items through it.
- [ ] Trial qmd over `doc/` and `.skogai/`, then decide in an ADR whether to keep it.

## 5. Suggested first move

Phase 0 and ADR 0001–0003 in one sitting. That turns the "already made" table above into
real ADRs, and it exercises the full loop (todo → worktree → commit → ADR) on day one.


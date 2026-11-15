---
type: repository
title: mise-plugin
description: A mise environment plugin (Lua) that sets the base SKOGAI_* variables and optional PATH entries for a SkogAI workspace. Small, tested, at version 0.2.0 and pinned by the monorepo.
tags: [mise, plugin, lua, environment, skogai-env]
repo: skogai/mise-plugin
commit: 6f27f18
last_commit: 2026-11-13
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/mise-plugin/README.md
  - repos/mise-plugin/AGENTS.md
  - repos/mise-plugin/metadata.lua
  - repos/mise-plugin/hooks/mise_env.lua
  - repos/mise-plugin/hooks/mise_path.lua
  - repos/mise-plugin/lib/skogai.lua
  - repos/mise-plugin/test/run.sh
  - repos/mise-plugin/mise.toml
  - repos/mise-plugin/hk.pkl
  - repos/mise-plugin/.github/workflows/ci.yml
  - mise.toml
  - .config/mise/conf.d/plugin.skogai.toml
---

# mise-plugin

**A mise environment plugin named `skogai` that gives a SkogAI workspace five `SKOGAI_*` variables and optional `PATH` entries.** It is a fork of the mise env-plugin template: the older history is template and Renovate commits, and the SkogAI work is the last few commits (pull requests #1 to #4, ending 2026-11-13). State: active and small. 15 tracked files, `metadata.lua` says version `0.2.0`, and the monorepo pins it at the current HEAD commit. The hooks only compute values. They do not download, write files or run commands (`AGENTS.md:5`, `README.md:56`).

## Source map

| Path | Holds |
|---|---|
| `metadata.lua` | Plugin name `skogai`, version `0.2.0`, `minMiseVersion = "2026.11.5"` |
| `hooks/mise_env.lua` | The `MiseEnv` hook: returns the five variables |
| `hooks/mise_path.lua` | The `MisePath` hook: returns the directories to prepend to `PATH` |
| `lib/skogai.lua` | Shared option handling, path resolution, host, OS and architecture lookup |
| `types/mise-plugin.lua` | LuaCATS type definitions for the mise plugin API (244 lines) |
| `test/run.sh` | Integration checks that run the hooks through mise in temporary directories |
| `mise.toml`, `mise.lock` | Development tools (actionlint, hk, lua 5.5.1, lua-language-server, pkl, stylua) and the `lint`, `lint-fix`, `test` tasks |
| `hk.pkl`, `stylua.toml`, `.luarc.json` | Lint, format and Lua analysis configuration |
| `.github/workflows/ci.yml` | CI on pushes and pull requests to `main` |
| `renovate.json` | Renovate configuration inherited from the template |
| `README.md`, `AGENTS.md` | Usage and options; contribution rules |

## How it works

A project activates the plugin with a `_.skogai = { ... }` directive under `[env]`. mise calls the two hooks with a context that holds the directive's options and `config_root`, the directory of the config file that declares the plugin.

### Variables (`hooks/mise_env.lua:13-19`)

| Variable | Value | Source |
|---|---|---|
| `SKOGAI_MONOREPO_DIR` | The workspace root: the `root` option, else `ctx.config_root` | `lib/skogai.lua:43-49` |
| `SKOGAI_CONFIG_DIR` | The `config_dir` option, else `$XDG_CONFIG_HOME/skogai`, else `~/.config/skogai` | `lib/skogai.lua:54-64` |
| `SKOGAI_HOST` | First non-empty line of `/proc/sys/kernel/hostname`, then `/etc/hostname`, then `$HOSTNAME`, else empty | `lib/skogai.lua:123-125` |
| `SKOGAI_OS` | `RUNTIME.osType` in mise's naming (`darwin` becomes `macos`) | `lib/skogai.lua:128-135` |
| `SKOGAI_ARCH` | `RUNTIME.archType` in mise's naming (`amd64` becomes `x64`, `386` becomes `x86`) | `lib/skogai.lua:129-141` |

The first two are always computed from options and are not read from the environment. The last three are defaults: the local `default` function in `hooks/mise_env.lua:9-11` keeps a value that is already set and non-empty when the hook runs (`lib/skogai.lua:93-99`). So an `[env]` entry above the directive, an earlier config file or the calling shell keeps its value, and an entry below the directive or in a later file such as `mise.local.toml` replaces the plugin's value because mise applies `[env]` in order (`README.md:41-54`).

### Paths (`lib/skogai.lua:69-87`)

`paths` is a list of directories. Each is resolved against the root, skipped if it does not exist, and added once. With no `paths`, `PATH` is unchanged.

### Path resolution (`lib/skogai.lua:20-38`)

A leading `~` expands to `$HOME`. An absolute path is used as written. Leading `./` is stripped and a relative path is joined to its base: `root` resolves against the declaring config's directory, `config_dir` and `paths` against the root. A directive whose value is a bare string instead of a table is treated as no options (`lib/skogai.lua:9-14`).

### Tests (`test/run.sh`)

The script links the checkout as plugin `skogai` inside throwaway mise config, data, state and cache directories (`test/run.sh:14-20`, `:38`), writes small `mise.toml` files, and compares `mise exec -- printenv <VAR>` against expected values. It has 17 checks: default root from a subdirectory, default config dir, no `PATH` change by default, relative, `~` and absolute options, missing and repeated paths, `XDG_CONFIG_HOME`, host, OS and architecture defaults, and the override rules (set above, set below, empty value, later file, earlier global file).

## How to use it

In a project's mise config (`README.md:9-15`):

```toml
[plugins]
skogai = "https://github.com/skogai/mise-plugin"

[env]
_.skogai = { paths = ["bin"] }
```

Options: `root`, `config_dir`, `paths` (`README.md:33-37`). Requires mise 2026.11.5 or later.

Development, as the repo defines it (`mise.toml:12-22`, `AGENTS.md:18-25`):

- `mise install`: development tools.
- `mise run lint`: `hk check --all` (stylua, `lua-language-server --check .`, actionlint; `hk.pkl:4-18`).
- `mise run lint-fix`: `hk fix`.
- `mise run test`: `sh test/run.sh`. Needs `mise` on `PATH`.
- To try a checkout in another project: `mise plugins link --force skogai-develop /path/to/mise-plugin`, then use that name in the directive (`README.md:82-88`). A link belongs to the mise data directory, so it affects every project on the machine that uses that name.

CI runs `mise run lint` and `mise run test` in one job (`.github/workflows/ci.yml:10-16`). Lua must stay compatible with the Lua 5.1 runtime set in `.luarc.json` even though the toolchain installs 5.5.1 (`AGENTS.md:29`).

## Relations to other SkogAI repos

- **monorepo (`skogai/monorepo`)** is the consumer seen in this workspace. `mise.toml:15` has `_.skogai = { paths = ["bin", ".skogai/bin"] }`, and `.config/mise/conf.d/plugin.skogai.toml` pins the plugin to `https://github.com/skogai/mise-plugin#6f27f183...`, which is this clone's HEAD. A monorepo task checks that `SKOGAI_MONOREPO_DIR` is set (`mise.toml:66-75`).
- **skogai2-config** records `SKOGAI_CONFIG_DIR` as an `[env]` variable in the workstation's global mise config and notes that it points at `~/skogai/config`, not at `~/.config/skogai` (`repos/skogai2-config/PROJECT.md:163-164`). This plugin's default is `$XDG_CONFIG_HOME/skogai`. Because `SKOGAI_CONFIG_DIR` is not read from the environment, the plugin's value replaces a global one unless `config_dir` is set.
- **skogai2-cli** solves a neighbouring problem (layered `SKOGAI_*` settings held by mise) with no shared code. See [skogai2-cli](skogai2-cli.md).
- **skogix** lists this plugin as the partial answer to its "config/runner; define paths overall as well as a env-lookup" item (`repos/skogix/.skogai/todo.list:30-31`).
- The first test fixture was named `skogix-workstation` in commit titles; the files themselves name no host.

## Gaps and stale references

- `AGENTS.md:16` mentions `codex-old/` and `.skogai/` as workspace data. Neither is tracked in the repo.
- The GitHub repo description is still the template's ("Template for creating mise environment plugins"), as recorded in `repos/skogix/.skogai/todo/a.txt:11`.
- `README.md:25` states that `SKOGAI_HOST` is empty on macOS without `$HOSTNAME`. `test/run.sh:75` compares it with `uname -n`, so that test assumes Linux or an exported `HOSTNAME`.
- `renovate.json` and the Renovate commits come from the upstream template. Whether Renovate runs on the fork was not determined.
- No release tags were found in the shallow clone; consumers pin by commit.

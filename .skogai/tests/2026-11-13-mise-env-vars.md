# 2026-11-13: basic environment variables in mise

Run: Claude Opus 5.5, Claude Code in T3 Code, machine `skogix-workstation` (Arch Linux, Omarchy, x86_64), checkout `/home/skogix/dev/Work/t3-f8dfb769-8a26446c934b5dc0`, branch `mise-basic-env-vars`, base commit `449745b`. mise 2026.11.5 linux-x64 (`/usr/bin/mise`, machine prerequisite).

Machine note: the global config in `~/.config/mise` also sets variables such as `SKOGAI_CONFIG_DIR`, `SKOGAI_DOCS_DIR` and `JAVA_HOME`. They show up in every `mise env` below, but they are machine facts, not part of this repository.

## 1. Which template functions exist

Scratch `mise.toml` outside the checkout, not committed.

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise env` with `os()`, `arch()`, `os_family()`, `num_cpus()`, `config_root`, `exec(command='uname -n')` | Each renders | `linux`, `x64`, `unix`, `8`, the scratch path, `skogix-workstation` | pass |
| `mise env` with `hostname()` | Renders or errors | `mise ERROR error: Unknown function hostname` | fail, so `exec(uname -n)` is used |
| `get_env(name='HOSTNAME', default='none')` | Host name | `none`: the variable is not exported here | not usable |
| `read_file(path='/etc/hostname') \| trim` | Host name | `skogix-workstation` | pass, not used: macOS has no `/etc/hostname` |
| `mise_env` | Selected environments | `["skogai"]`, `["develop"]` with `-E develop` | pass, needs `join` |

## 2. The committed `[env]` block

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise env -s bash \| grep SKOGAI_` | host, `linux`, `x64`, `skogai` | `skogix-workstation`, `linux`, `x64`, `skogai` | pass |
| `mise -E develop env -s bash` (before strip) | `develop` | `' develop'`, leading space | fail, fixed with `replace(from=' ', to='')` |
| `mise --env=develop env`, `MISE_ENV=develop mise env`, `mise -E develop exec -- …` | `develop` | `develop` in all three | pass |
| `mise -E develop env` (after strip) | `develop` | `develop` | pass |
| `mise -E skogai,develop env` | `skogai,develop` | `skogai,develop` | pass |
| `MISE_ENV= mise env` | empty | `''` | pass |
| `mise exec -- sh -c 'echo $SKOGAI_HOST …'` | values in a child process | `skogix-workstation linux x64 skogai` | pass |
| `cd skogix && mise env` | inherited from the root | `SKOGAI_HOST=skogix-workstation` | pass |
| `time mise env -s bash` | no visible slowdown | 0.074 s total | pass |

## 3. Defaults in the plugin, overrides in config

Owner direction in the PR conversation: set defaults in the plugin, override them in config, and have the plugin read values already set in config. This section moves `SKOGAI_HOST`, `SKOGAI_OS` and `SKOGAI_ARCH` into the plugin (skogai/mise-plugin#3, commit `14991e5`) and keeps `SKOGAI_MISE_ENV` in `mise.toml`.

### Probe: how mise orders plugin and config values

A throwaway plugin returned `SKOGAI_HOST=plugin-default` and reported what `os.getenv` saw. It ran with mise 2026.11.5 (`~/.local/bin/mise`) in isolated `MISE_*_DIR`s, in a scratchpad project. Nothing was committed.

| Config | Hook saw | Result | Meaning |
|---|---|---|---|
| `SKOGAI_HOST = "config"` above `_.probe` | `config` | `plugin-default` | The hook sees earlier values; without a check it overwrites them |
| `SKOGAI_HOST = "config"` below `_.probe` | unset | `config` | Later `[env]` entries win |
| directive in `mise.toml`, value in `mise.local.toml` | unset | `local` | A later file wins |
| value in the global config | `global` | `plugin-default` | The hook sees earlier files |
| `SKOGAI_HOST=shell MISE_ENV=foo` in the process | `shell`, `MISE_ENV=foo` | `plugin-default` | The hook sees the process environment |
| `env = ["foo"]` in `.miserc.toml` | `MISE_ENV` unset | – | The hook cannot see an environment chosen in `.miserc.toml` |

Also from the probe: `io.open("/proc/sys/kernel/hostname")` works in a hook, and `RUNTIME` gives `linux/amd64`, which is not mise's `x64` naming.

### Plugin change

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise run test` in `mise-plugin` | all pass | 16 of 16, 7 new | pass |
| same, with the `existing()` lookup removed | the "kept" checks fail | 2 failed: above-directive, earlier file | pass, the tests detect the regression |
| same, with the `/proc` path broken | `uname -n` fallback | `ok default host` | pass |
| `mise run lint` | clean | stylua, lua-language-server, actionlint clean | pass |

### Monorepo with the new plugin

A copy of this working tree went into the scratchpad, because mise run from the real checkout under `/home/skogix` loads `~/.config/mise/config.local.toml` even with isolated `MISE_*_DIR`s and `MISE_CEILING_PATHS`. Then `mise plugins link skogai-develop <copy>/mise-plugin`, with each config trusted using `mise trust`. `MISE_TRUSTED_CONFIG_PATHS` did not take effect under the scratchpad path, and the reason was not investigated.

| Selection and config | `SKOGAI_HOST` | Other | Verdict |
|---|---|---|---|
| `MISE_ENV=develop` | `skogix-workstation` | `linux`, `x64`, `develop` | pass |
| plus `SKOGAI_HOST = "from-mise-toml"` in `mise.toml` | `from-mise-toml` | | pass |
| plus `SKOGAI_HOST = "from-local"` in `mise.local.toml` | `from-local` | | pass |
| `MISE_ENV=develop`, from `skogix/` | `skogix-workstation` | | pass |
| `MISE_ENV=` | unset | `SKOGAI_MISE_ENV=''` | pass, as designed |

The machine's real `skogai-develop` link points to `/home/skogix/Work/mise-plugin`, another checkout, and was not changed.

## 4. The plugin in every environment, and `env:` tasks

Run: same agent and machine, branch `t3/claude-skogix-workstation-env-tasks`, base `a4d48d1` (master after #27 and #28). #27 merged with only its first commit. Section 3 was pushed to that branch after the merge, so this branch carries it.

Plugin follow-up skogai/mise-plugin#4 (merged as `6f27f18`): host name read without a command, as the plugin's `AGENTS.md` requires (`/proc`, `/etc/hostname`, `$HOSTNAME`). It adds an empty-override check, from a Greptile review finding on #3. `mise run test` passes 17 of 17, also with the `/proc` path broken, which exercises `/etc/hostname`. `mise run lint` is clean, and CI passed.

### A plugin that cannot be installed

A scratch project declared a nonexistent plugin URL with `_.skogai`. `mise env` and `mise run <task>` both fail with `[skogai] plugin not installed`, with or without `MISE_AUTO_INSTALL=0`. A plugin with a source must be installable, or mise is unusable. A plugin with no source that is not installed only gets a warning.

### This machine

`mise plugins install --force skogai` moved the shared installed plugin from `7948c12` to `6f27f18`. That is machine state, shared by every checkout. Before the move, `mise run env:test` failed with `SKOGAI_HOST is empty`, `SKOGAI_OS is ''` and `SKOGAI_ARCH is ''`: the old plugin, caught by the test. After the move:

| Command | Result | Verdict |
|---|---|---|
| `mise run env:test` (default `skogai`) | 6 ok | pass |
| `MISE_ENV=t3`, `MISE_ENV=develop` and `MISE_ENV=` with `mise run env:test` | 6 ok each. Before this change, `t3` and none had no plugin | pass |
| `mise run env:context --trailers` in each | `Host: skogix-workstation`, `Platform: linux-x64`, `Mise-Env: <env or none>` | pass |
| `SKOGAI_HOST = "laptop-override"` in `mise.local.toml`, then `mise run env:test` | `ok SKOGAI_HOST is set: laptop-override`, plus the override note | pass |
| `mise doctor` | `skogai https://github.com/skogai/mise-plugin#6f27f18`, no mismatch | pass |

### Fresh machine

`$S/fresh.sh <dir>` in the session scratchpad, not committed. A copy of the working tree was made with `rsync --exclude .git`, and run under `env -i HOME=<dir>/home PATH=/usr/bin:/bin SHELL=/bin/sh`, with every `MISE_*_DIR` empty, `MISE_AUTO_INSTALL=0` and `mise trust --all`. The copy is needed because mise run from the real checkout under `/home/skogix` loads `~/.config/mise/config.local.toml`.

| Layout | Not installed, `MISE_ENV=t3` | Default env | Installed, then `t3` and none |
|---|---|---|---|
| This branch: directive in `mise.toml`, source in the fragment | `WARN skipping env plugin skogai`, no failure | Plugin installed from the pin, variables set | variables set |
| master before this: both in the fragment | no variables | Plugin installed, variables set | no variables |

`env:test` and `env:show` in the fresh copy: 6 ok for `skogai` and for `t3`.

Findings kept:
- With `SHELL` unset, master's `SKOGAI_HOST = "{{ exec(command='uname -n') }}"` fails every `mise env`: `exec command: No such file or directory`. This branch removes that template.
- With `SHELL` unset, a fresh plugin install also failed with `[skogai] plugin not installed`. It passed with `SHELL=/bin/sh`. The cause was not investigated.
- `MISE_TRUSTED_CONFIG_PATHS` and per-file `mise trust` did not reliably persist for the scratchpad copies, so `mise trust --all` was used.

## Not run

- macOS, Windows, or a second Linux machine. `uname -n` on macOS is a source assumption.
- A fresh checkout, or a mise without the owner's global config.
- `mise activate` in an interactive fish or zsh shell. Only `mise env` and `mise exec` were run.
- Sections 1 to 3 only: the default `skogai` environment with the new plugin. Section 4 ran it, after the plugin merged and the pin moved.

Next action: review in the PR. The startup script and commit-context items in `skogix/.skogai/todo.list` can read these variables.

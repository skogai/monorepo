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

## Not run

- macOS, Windows, or a second Linux machine. `uname -n` on macOS is a source assumption.
- A fresh checkout, or a mise without the owner's global config.
- `mise activate` in an interactive fish or zsh shell. Only `mise env` and `mise exec` were run.

Next action: review in the PR. The startup script and commit-context items in `skogix/.skogai/todo.list` can read these variables.

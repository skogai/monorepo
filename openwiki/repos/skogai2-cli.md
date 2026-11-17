---
type: repository
title: skogai2-cli
description: A clean-room rework of the skogai CLI. Only the config module exists (skogai-config, layered SKOGAI_* settings held by mise); HEAD has hard-coded debug defaults that contradict its own docs and tests. Quiet since 2026-10-24.
tags: [cli, bash, argc, mise, config, pacman]
repo: skogai2/cli
commit: c3fd054
last_commit: 2026-10-24
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogai2-cli/CLAUDE.md
  - repos/skogai2-cli/README.md
  - repos/skogai2-cli/bin/config
  - repos/skogai2-cli/lib/config.sh
  - repos/skogai2-cli/docs/config.md
  - repos/skogai2-cli/test/config.bats
  - repos/skogai2-cli/test/install.sh
  - repos/skogai2-cli/PKGBUILD
  - repos/skogai2-cli/.skogai/base/config.md
  - repos/skogai2-cli/.skogai/base/mise.toml
  - repos/skogai2-cli/.skogai/base/mise.system.toml
  - repos/skogai2-cli/.gitignore
---

# skogai2-cli

**A ground-up rework of the skogai CLI as a modular bash framework: argc commands, settings held by mise.** `CLAUDE.md` sets a clean-room rule: the old implementation must not be read or copied, and every piece is rebuilt from a written intent. One module exists, `config`, installed as `skogai-config`. State: quiet and unfinished. All commits are from 2026-10-23 and 2026-10-24, tags `v0.0.1` and `v0.0.2` exist, and the last commit left work-in-progress code in `bin/config` (see Gaps). The runner that would make this a CLI is listed as "next" and is not built.

## Source map

| Path | Holds |
|---|---|
| `CLAUDE.md` | The project's rules, goals, build conventions, install layout and roadmap (127 lines). The real README |
| `README.md` | One heading only |
| `bin/config` | The `config` command, an argc script (161 lines). Installed as `/usr/bin/skogai-config` |
| `lib/config.sh` | Its helpers: project root lookup, scope files, folding, key and env names (74 lines) |
| `docs/config.md` | The spec for `config`: model, commands, exit codes, examples |
| `test/config.bats` | 22 bats tests that follow the spec, each in a fresh project with its own mise config |
| `test/install.sh` | Builds the pacman package from HEAD, unpacks it into a temp root, runs the same tests against it |
| `PKGBUILD` | Arch package `skogai`, version from `git describe` |
| `.skogai/base/config.md` | The module's self-description: frontmatter `type: module`, `name`, `command`, `tools: [mise, yq, argc]` |
| `.skogai/base/mise.toml` | Tools a sandbox needs: `argc`, `yq` |
| `.skogai/base/mise.system.toml` | A `[skogai]` table with `config.system.dir` and `config.system.file`, added in the last commit |
| `tmp/.gitkeep`, `.gitignore` | Scratch space; ignores `/tmp`, `/src/`, `/pkg/`, `/skogai/`, built packages |

## How it works

### The model (`docs/config.md:7-44`)

A setting is a lowercase dotted key with a string value. It is stored as a variable in the `[env]` of a mise environment: the prefix plus the key in uppercase with `.` as `_`. With the defaults, `core.debug` is `SKOGAI_CORE_DEBUG` in the mise env `skogai`. Four layers fold in mise's own order, later wins:

1. system: `$SKOGAI_CONFIG_SYSTEM_FILE`
2. global: `$SKOGAI_CONFIG_GLOBAL_FILE`
3. base: `$SKOGAI_CONFIG_BASE_FILE`, the project's committed file, never written by a command
4. local: `$SKOGAI_CONFIG_LOCAL_FILE`, beside the base

The spec's defaults are the file names mise loads for that env: `/etc/mise/config.skogai.toml`, `~/.config/mise/config.skogai.toml`, `mise.skogai.toml` and `mise.skogai.local.toml` (`docs/config.md:27-34`). A key exists only if some layer sets it; new keys are declared in the base. A `SKOGAI_*` value already in the calling shell is ignored (`docs/config.md:39-41`).

### The command (`bin/config`)

The interface is written as argc comments, not bash: `@meta require-tools mise,yq` and six `@env` lines declare the locations as settings (`bin/config:8-14`). The script sources `lib/config.sh` from `../lib/skogai/` (installed) or `../lib/` (repo) and ends with `eval "$(argc --argc-eval "$0" "$@")"` (`bin/config:153-161`).

| Subcommand | Does | Lines |
|---|---|---|
| `get <key> [--show-origin]` | Prints the resolved value, optionally prefixed with `file:<path>` | `bin/config:20-30` |
| `set <key> <value> [--scope local\|system\|global]` | `mise set -q --file <scope file> NAME=value`; default scope `local` | `bin/config:32-42` |
| `unset <key> [--scope ...]` | `mise unset -q --file <scope file> NAME` | `bin/config:44-50` |
| `list [--show-origin]` | Every key as `key=value`, sorted; redacted values shown as `[redacted]` | `bin/config:68-82` |
| `env` | The resolved config as `export NAME=value` lines | `bin/config:84-91` |
| `files` | Each scope's file in fold order with `present` or `missing` | `bin/config:93-100` |
| `skogix <myscope>` | A debug command that echoes its argument | `bin/config:52-65` |

Key arguments are validated and completed through `_choice_key`, `_choice_value` and `_choice_scope_key` (`bin/config:125-150`), which argc requires to be in the script itself.

### The helpers (`lib/config.sh`)

- `_root` walks up from `ARGC_PWD` to the nearest directory that holds the base file and changes into it (`lib/config.sh:5-13`).
- `_fold` fills three associative arrays: `_val` from `mise env --json`, `_secret` from `mise env --json --redacted`, and `_org` (origin file) from the output of `mise set` (`lib/config.sh:24-40`).
- `_mise_env` filters mise's JSON through `yq` to variables that start with the prefix (`lib/config.sh:43-46`).
- `_envname` and `_keyname` convert between `core.debug` and `SKOGAI_CORE_DEBUG` (`lib/config.sh:56-65`).

Exit codes per the spec: 0 ok, 1 an expected "no" (unknown key, nothing to remove, bad input), 2 unexpected (`docs/config.md:48-50`).

### Packaging (`PKGBUILD`)

Package `skogai` builds from the repo's committed HEAD (`source=git+file://$startdir`), never the working tree. It installs `.skogai/base/*` to `/usr/share/skogai/base/`, `bin/<name>` to `/usr/bin/skogai-<name>` and `lib/*` to `/usr/lib/skogai/` (`PKGBUILD:23-41`). Dependencies: `bash`, `go-yq`, `mise`; argc is needed too but is not in the official repos (`PKGBUILD:12`).

## How to use it

As the repo defines it, not run here (`CLAUDE.md:99-106`):

- `bats test/`: every spec against the repo.
- `test/install.sh`: `makepkg -fd`, unpack with `bsdtar`, then `SKOGAI_TEST_ROOT=<root> bats test/` against the installed command. It runs `git checkout -q PKGBUILD` afterwards because makepkg rewrites `pkgver`.
- `shellcheck -x bin/* lib/*.sh test/*.sh`.
- Direct use: `bin/config get core.name` in a directory at or below a project base file.

Prerequisites: `bash`, `mise`, `yq`, `argc`, `bats`; `makepkg` and `bsdtar` (Arch Linux) for the package test. Variables read: `MISE_ENV`, `SKOGAI_CONFIG_PREFIX`, `SKOGAI_CONFIG_SYSTEM_FILE`, `SKOGAI_CONFIG_GLOBAL_FILE`, `SKOGAI_CONFIG_BASE_FILE`, `SKOGAI_CONFIG_LOCAL_FILE`; the tests also use `SKOGAI_TEST_ROOT`.

## Relations to other SkogAI repos

- **The old skogai CLI** is the thing this replaces. `CLAUDE.md:7-21` forbids reading it, so the repo names no predecessor path.
- **mise-plugin** covers the same area from the other side: it computes base `SKOGAI_*` variables in a mise hook, while this repo reads and writes `SKOGAI_*` settings in mise env files. They share no code and their variable names do not overlap (`SKOGAI_CONFIG_DIR` there, `SKOGAI_CONFIG_*_FILE` here). See [mise-plugin](mise-plugin.md).
- **skogai2-config** removed a `config.skogai.toml` from the workstation's mise config on 2026-10-25 as "a second origin" (`repos/skogai2-config/mise/dotfiles.md:131-132`). `bin/config` at HEAD reads that same file name from the user's mise config directory, so the file it depends on may no longer exist on the workstation.
- **skogai2-skogai-runner** is named elsewhere as the current SkogAI 3.0 reference (`repos/skogix/.skogai/persona/codex-memories-of-skogix.md`); this repo's own "next" item is "the runner: a `skogai` command that runs a module's `command`" (`CLAUDE.md:125`). Nothing in this repo links the two.
- The module format (`.skogai/base/<path>` as default, `.skogai/<path>` as override, markdown with frontmatter) is this repo's convention for `.skogai/` (`CLAUDE.md:75-82`).

## Gaps and stale references

- **HEAD contradicts its own commit message, spec and tests.** The last commit says "nothing is hardcoded", but the four default functions in `bin/config:103-122` are debug code: three run `mise config get --file=` against an absolute path in one user's home directory (`config.skogai.toml`) for keys `skogai.config.{system,global,local}.dir`, and `_default_base_file` echoes `.skogai`. The spec's defaults are present only as commented-out `printf` lines. `test/config.bats` expects the spec's defaults (`mise.skogai.toml` and so on), so the tests cannot match this code on another machine.
- The `skogix` subcommand and `_choice_example` (`bin/config:52-65`) are scratch code and are not in `docs/config.md`.
- `.skogai/base/mise.system.toml` sets `config.system.dir = "/etc/skogai"`, while the spec says the system file is `/etc/mise/config.skogai.toml`. Nothing reads `mise.system.toml` by name.
- `.skogai/base/config.md` says a project's defaults are its committed `mise.skogai.toml`; no such file is tracked in this repo, so the repo is not itself a project with a base.
- `PKGBUILD:7` carries `pkgver=0.0.2.r5.g3501112`, a commit that is not HEAD; the comment in `test/install.sh:13` explains that makepkg rewrites it.
- `README.md` is a single heading. `license=('unknown')` in the PKGBUILD.
- Roadmap items not started (`CLAUDE.md:123-127`): the runner, how a repo copies the installed base and records its version, a type module using argc's runtime validation.

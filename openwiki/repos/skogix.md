---
type: repository
title: skogix
description: The owner's personal notes repo. It holds a to-do list audited against the monorepo, three listings of GitHub repositories, and a saved assistant-memory text about the owner. No code. Started 2026-11-10, last touched 2026-11-14.
tags: [notes, todo, personal, inventory]
repo: skogai/skogix
commit: 8b6be21
last_commit: 2026-11-14
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/skogix/README.md
  - repos/skogix/.claude/settings.json
  - repos/skogix/.skogai/todo.list
  - repos/skogix/.skogai/todo/a.txt
  - repos/skogix/.skogai/todo/b.txt
  - repos/skogix/.skogai/todo/c.txt
  - repos/skogix/.skogai/persona/codex-memories-of-skogix.md
---

# skogix

**A personal notes repo for the SkogAI owner: one to-do list and some reference dumps, all under `.skogai/`.** It has no code, no tasks and no router file. State: young and active as a scratch place. Nine commits between 2026-11-10 and 2026-11-14, most titled "todo" or "."; the one structured commit is pull request #3, a source audit of the to-do list. Seven files are tracked.

## Source map

| Path | Holds |
|---|---|
| `README.md` | Two lines: the name and `skogai/skogix` |
| `.skogai/todo.list` | 15 to-do items with status notes and issue links (33 lines) |
| `.skogai/todo/a.txt` | A listing of repositories under the `skogai` GitHub organisation (345 lines) |
| `.skogai/todo/b.txt` | A listing of repositories under the owner's personal GitHub account (232 lines) |
| `.skogai/todo/c.txt` | A listing of repositories under the `skogai2` GitHub organisation (47 lines) |
| `.skogai/persona/codex-memories-of-skogix.md` | A pasted copy of an assistant "memory summary" page about the owner (91 lines) |
| `.claude/settings.json` | Registers one extra Claude Code plugin marketplace, `the-startup`, from a local directory |

## How it works

There is no mechanism. The repo is read by people and agents.

### The to-do list (`.skogai/todo.list`)

The header says it was audited on 2026-11-13 against this checkout, `~/Work` and `~/.config/nvim`, and that a checked item means the basic scope exists, not that live integrations were retested (`.skogai/todo.list:1-2`). Each item is a `- [ ]` or `- [x]` line in the form `<area>;<task>`, followed by an indented status note. Three items are checked, twelve are open.

| Area prefix | Items | Status in the notes |
|---|---|---|
| `mise` | basic monorepo at `skogai/monorepo`; remove the testing configuration | first done (`~/Work`), second partial |
| `skogai`, `adr` | `doc/adr/` set up; ADR for the starting tools (mise, t3code, herdr, git, Arch Linux with Omarchy) | both done, in `~/Work/doc/adr/` |
| `t3` | describe and set up the workflow | partial; issue `skogai/skogix#2` |
| nvim | add schemas, especially for mise | partial; issue `skogai/skogix#1` |
| `dot-skogai` | a file layout for `.skogai` folders; rename `.skogai/tests` to experiments | partial; not implemented |
| `skogai` | explain the legacy repos and names in monorepo terms | not found |
| `config` | basic encryption via mise dotfiles and bootstrap | tracked in `skogai/monorepo` issues #18 and #17 |
| `claude` | check that Claude reads `AGENTS.md` like a `CLAUDE.md` | configured, not verified |
| `tickets` | how to-do entries become issues | no process documented |
| `environment` | a start script that reports the environment; commit trailers with agent and environment | partial: `env:context`, `env:show`, `env:test` tasks in the monorepo |
| `config/runner` | define paths and an env lookup | partial: the mise plugin |

### The repository listings (`.skogai/todo/*.txt`)

Each line is tab-separated: `owner/name`, description, visibility (with `fork` where it applies) and a last-updated timestamp. The newest timestamps are 2026-11-14, the day the files were added (commit `8b6be21`). They look like saved `gh repo list` output; the repo does not say how they were made. Together they are an inventory of about 620 repositories across the two organisations and the personal account, including private ones by name.

### The persona file

`.skogai/persona/codex-memories-of-skogix.md` is a copy of a memory-summary page from a chat assistant, including the page's interface text. It describes the owner's projects, tools and working preferences in the second person. Some of it disagrees with the machine-config repo (for example it describes a different window manager, shell and display server than `skogai2-config` documents), so it is a dated self-description, not current state. It contains personal details and this page does not reproduce them.

## How to use it

Read `.skogai/todo.list` for the owner's open items and where each one stands. Nothing is run. `.claude/settings.json` assumes a local checkout of `the-startup` at an absolute path in the owner's home directory; on any other machine that marketplace entry points at a missing directory.

## Relations to other SkogAI repos

- **monorepo (`skogai/monorepo`)**: most to-do items are about it, and the notes cite its paths as `~/Work/...` (`doc/adr/`, `doc/t3-cli.md`, `mise.t3.toml`, `scripts/t3-picker.py`, `doc/plan.md`, `AGENTS.md`). Open items link to `skogai/monorepo` issues #13, #17 and #18.
- **mise-plugin**: cited as `~/Work/mise-plugin`, the partial answer to the paths and env-lookup item (`.skogai/todo.list:30-31`). See [mise-plugin](mise-plugin.md).
- **nvim-omarchy**: the nvim schema item refers to `~/.config/nvim`.
- **skogai2-config**: its bootstrap page declares `~/skogix` as a `[bootstrap.repos]` checkout on the workstation (`repos/skogai2-config/mise/bootstrap.md:22`). See [skogai2-config](skogai2-config.md).
- **A naming collision**: `skogai2-config` also says the origin of `/skogai` (dash-skogai) "is `skogai2/skogix` now" (`repos/skogai2-config/mise/bootstrap.md:158-160`). That is a different repository from this one (`skogai/skogix`). `.skogai/todo/c.txt` lists `skogai2/skogix`, and `b.txt` lists a third, private fork under the personal account.
- The persona file names `skogai2/skogai-runner` as the current SkogAI 3.0 reference.
- The listings in `.skogai/todo/` overlap with the monorepo's `mani.yaml` catalog; they are a wider, unfiltered inventory.

## Gaps and stale references

- `README.md` says nothing about purpose. The purpose above is inferred from the contents.
- The directory name `.skogai/todo/` and the file names `a.txt`, `b.txt`, `c.txt` do not say what the files are. They are repository listings, not to-do items.
- The to-do notes use `~/Work` paths, so they can only be checked on the owner's workstation or against a monorepo clone.
- The status notes are a snapshot from 2026-11-13; the list itself says live integrations were not retested.
- Open questions the list records with no owner or process: `.skogai` folder conventions, how legacy repo names map to the monorepo, how to-do entries become issues.
- The last commit is titled "." and added the three listings and `.claude/settings.json` without explanation.

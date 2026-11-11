# Claude Code daemon and background agents

Research input: how `claude agents`, `claude daemon` and background jobs (`claude --bg`) behave with this monorepo. Written as a question log. Each answer is marked:

- **ran**: a command was executed and the output is summarized here.
- **read**: taken from `--help` text or files, not exercised.
- **machine**: holds for `skogix-laptop` only, from files outside the checkout.

## Run

| Field | Value |
|---|---|
| Agent | Claude (Opus 5.5) |
| Harness | Claude Code 2.1.322, background job `dea622ba` dispatched from `claude agents` |
| Machine | `skogix-laptop` (Arch Linux / Omarchy) |
| Checkout | `/home/skogix/Work/.claude/worktrees/research-claude-daemon` (worktree of `/home/skogix/Work`) |
| Base commit | `19ede8e` |
| Branch | `claude/daemon-research-skogix-laptop` |
| Dates | 2026-11-10 and 2026-11-11 |

## Answered

### What are the pieces?

- `claude daemon` is a supervisor process. It owns a control socket and spawns background workers. **ran** (`claude daemon status`)
- `claude agents` is the agent view: it lists sessions and dispatches new ones. `claude agents --json` prints active interactive and background sessions without a TTY; `--all` adds completed ones; `--cwd <path>` filters by start directory. **ran** / **read**
- `claude --bg "<prompt>"` starts a background job from any shell and prints its id. **read**
- Per-job commands: `claude attach <id|name>`, `claude logs <id|name>`, `claude stop <id>` (keeps the conversation, resumable by `attach`), `claude rm <id>` (deletes the session *and its worktree*; refuses to drop unpushed commits unless told with `--discard-unpushed`). **read**

### Does the daemon need to be installed as a service?

No, and it cannot be in 2.1.322: "Service install is disabled in this version". It runs transient, started on demand by the first client (here, `claude agents`), and exits once no client is attached and no background worker is still running. `claude daemon status` lists what is holding it open. **ran** / **read**

### Where does it keep its state?

**machine**, paths as seen on this laptop:

| Path | Holds |
|---|---|
| `~/.claude/daemon.json` | Daemon config (default path; the file did not exist here) |
| `~/.claude/daemon.log` | Supervisor and worker lifecycle log (`claimed-spare`, `settled`, `retire`, auth refresh) |
| `/tmp/cc-daemon-<uid>/<hash>/control.sock` | Control socket |
| `/tmp/cc-daemon-<uid>/<hash>/spare/` | Pre-spawned spare workers, ready to be claimed by the next dispatch |
| `/tmp/cc-daemon-<uid>/<hash>/rv/<job>.sock` | One socket per live job |
| `~/.claude/jobs/<job>/state.json` | Job state: status, intent, name, cwd, worktree path and branch, respawn flags, remote-control bridge id |
| `~/.claude/jobs/<job>/timeline.jsonl` | One line per state change, with the status text shown in the job list |
| `~/.claude/jobs/<job>/tmp/` | The job's scratch dir (`$CLAUDE_JOB_DIR/tmp`), removed with the job |

`state.json` contains account and organization ids. Do not commit it.

### What happens to an idle job?

The daemon retires it after about 60 minutes idle (`bg retire dea622ba: settled, idle 61m`). Replying to it later claims a fresh worker and resumes the same session id with its conversation intact. This job was retired at 23:00 and resumed at 03:20 UTC. **ran** (log lines)

Spares are pre-spawned: each dispatch logs `claimed-spare <id>` then `spare spawned`, so a new job starts from a warm process. **ran** (log lines)

### Does a worktree job see the submodules?

Not at first. A new worktree of the root checks out the submodule paths empty. `git submodule update --init` inside the worktree cloned all three in about 2.4 s and stored them under `.git/worktrees/<name>/modules/`, separate from the main checkout's modules. **ran**

So every root-level worktree job pays one clone per submodule and gets an independent copy. A job confined to one submodule can instead be dispatched with its cwd inside that submodule. **read** (not yet tried)

### Does a job see commits made while it was idle?

Yes, for new worktrees. While this job was idle, `master` moved from `4c85eca` to `19ede8e` (it added `AGENTS.md`, `CLAUDE.md` and the `skogix` bump to `3f214de`). The worktree created after the resume was based on `19ede8e`, and `CLAUDE.md` → `AGENTS.md` loaded into the session. The conversation itself still remembered the old state until it re-read the repo. **ran**

## Open questions

Pick any. Each one can become a small dispatched experiment.

1. Can two background jobs run in different submodules at once without touching each other's files or branches?
2. Does `claude --bg` started inside `~/Work/skogix` treat `skogix` as its own repo for worktrees and PRs, or does it walk up to the root?
3. Is there a supported way to make worktree jobs run `git submodule update --init` automatically (a `WorktreeCreate` hook, or a mise task)?
4. What goes in `~/.claude/daemon.json`, and can it set defaults per directory (model, permission mode, agent)?
5. Does `claude rm <id>` remove the worktree's submodule clones under `.git/worktrees/<name>/modules/` too?
6. How do `claude agents` jobs compare with T3 Code and herdr for the "same prompt to several agents" workflow in `AGENTS.md`?
7. Do `--setting-sources=local` and `--strict-mcp-config` (in this job's respawn flags) mean background jobs skip user-level settings and MCP servers by default?

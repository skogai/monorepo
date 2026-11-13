# T3 Code from the terminal

This guide describes the CLI installed on `skogix-workstation` on 2026-11-13: `t3 v0.1.10-nightly.20261113.4630`. It is a workstation snapshot, not a guarantee about other releases. Run `t3 --version` and the relevant `--help` on another machine.

The command descriptions below come from installed CLI help. Only version/help queries and listing this project's threads were exercised; commands that create, send, repair, install or reconfigure are examples, not integration-tested recipes. See the [evidence record](../.skogai/tests/2026-11-13-t3-cli.md).

## How the pieces fit

T3 runs a server, with a browser or desktop interface and configured agent providers. A project points to a workspace directory. Threads belong to projects; a thread can run in the project folder or in a new Git worktree. Sending a message requests work from its agent.

The executable serves two purposes: starting/managing T3 itself and acting as a client of the running server. `t3 thread` explicitly targets the running server. Installing a CLI does not by itself configure providers or create projects.

On this workstation the executable is `/home/skogix/.local/bin/t3`. Root `mise.toml` does not install T3; that binary, its server data, configured providers and existing projects are machine prerequisites. No bootstrap or mise installation method is established by this guide.

## Find commands and inputs

```bash
t3 --help
t3 thread --help
t3 thread start --help
```

Help advertises `--wizard` to start wizard mode for a command and `--completions` for bash, zsh, fish, PowerShell, sh and pwsh. Wizard behavior has not been tested here; do not assume it supplies a thread-title picker or discovers live targets.

```bash
# Print a completion script; this does not install it.
t3 --completions bash
```

## Start or connect to T3

| Command | Help-described behavior |
|---|---|
| `t3` | Run T3 in this terminal and open the browser. |
| `t3 serve` | Run in this terminal without opening the browser. |
| `t3 app .` | Open the project in an already-running desktop app. |
| `t3 up` | Set up background service and remote access. |
| `t3 status` | Show service setup and remote-access settings. |
| `t3 service status` | Show whether the background service is installed. |

Server flags include `--port`, `--host`, `--no-browser`, `--lan` and `--auto-bootstrap-project-from-cwd`. Use `t3 --help` for the complete list. Starting another server is not necessary merely to list threads on an existing one.

Commands that advertise `--base-dir` use it to select the T3 data directory, equivalent to `T3CODE_HOME`; runtime state lives under `userdata`. This is distinct from a project's workspace path. Use the same data-directory selection as the intended server. This guide does not establish default directory discovery or remote-server targeting for thread commands.

`t3 status --json` reports settings; its help explicitly says it does not test connections. A displayed configuration is not a health check.

## Manage projects

```bash
# Register an existing workspace; changes T3 state.
t3 project add /path/to/repository --title "My project"

# Inspect syntax before changing an existing registration.
t3 project rename --help
t3 project remove --help
```

The installed `project` group lists `add`, `remove` and `rename`, but no `list` subcommand. Thread commands accepting a project allow a project ID or a path inside it.

## List and read threads

```bash
# Current directory determines the project.
t3 thread list

# Select a project explicitly.
t3 thread list --project /path/to/repository

# Substitute an ID from the listing.
t3 thread show THREAD_ID --messages 10
```

`list` returns newest first. The observed text output contained ID, status and title. `show` promises state and latest messages, not a full transcript export. Its live behavior was not exercised for this guide.

## Start work

These examples create threads and run agents. They require a registered project and working provider configuration.

```bash
t3 thread start . "Review the current diff" --title "Diff review"

# Read a longer prompt from stdin.
t3 thread start . - --title "Investigate checks" < task.md

# Run in a new worktree based on a branch, tag or commit.
t3 thread start . "Implement the requested fix" \
  --worktree master --branch fix/example
```

`start` prints a thread ID. The title defaults to the message's first line. The model defaults to the project's default model; `--provider` selects a provider instance ID and must be passed with `--model`. Provider IDs and model slugs must come from the actual installation; this guide does not invent defaults.

`--worktree` selects the base ref and `--branch` names the new branch. Without `--worktree`, help says work runs in the project folder. No worktree was created to validate this documentation.

## Continue work and wait for results

```bash
t3 thread send THREAD_ID "Focus the review on configuration discovery"
t3 thread send THREAD_ID - --wait < follow-up.md
```

`send` queues a message as the next turn when the target is busy; it does not interrupt the running turn.

Both `start` and `send` accept `--wait`: wait for the agent to finish and print its reply. Help documents exit code `1` when the run fails and `2` when it waits for an answer. A waiting agent may need human input; do not treat that exit as completed work. The commands' runtime behavior and exit codes were not tested here.

## Script the same interface

`thread list`, `show`, `start` and `send` all advertise `--json`. Both message-taking commands accept `-` for stdin, avoiding shell quoting for long prompts.

```bash
t3 thread list --json
t3 thread show THREAD_ID --messages 10 --json
```

Inspect actual JSON before depending on field names; this guide does not promise a schema. Keep diagnostics and failures visible in wrappers, preserve exit codes, and avoid retrying `start` or `send` blindly after an uncertain result: they request work.

## Remote access and service management

| Command group | Scope |
|---|---|
| `t3 up`, `t3 connect` | Configure background service and remote access; `connect` is the alias for `up --connect`. |
| `t3 pair` | Mint a pairing token for a running server and print a QR code. |
| `t3 auth pairing`, `t3 auth session` | Manage pairing tokens and bearer sessions for headless deployments. |
| `t3 environment link/list/unlink` | Link other T3 environments, inspect reachability or forget a link. |
| `t3 service install/restart/uninstall` | Manage the user background service. |
| `t3 service protect` | Linux/systemd protection under memory pressure; help says it asks for sudo. |

`t3 up --connect` enables T3 Connect; `--lan` allows LAN/tailnet access and `--no-lan` disables it. Unnamed routes retain their settings. Help warns that a needed restart stops running agent turns and can happen without prompting outside a terminal. This makes `up` a setup operation, not a status command.

Unlinking an environment locally does not revoke its session remotely; the help directs users to that environment's Settings → Connections for revocation. Do not put pairing tokens or session credentials in repository documentation.

## Maintenance and troubleshooting

Start with the relevant command's `--help` and distinguish inspection from changes:

- `t3 trace summary`: summarize the local server trace file.
- `t3 doctor --dry-run`: show proposed repairs without changing anything. Plain `doctor` may pause/restart the service; `--fix` applies repairs without prompting.
- `t3 policy`: inspect administrator-managed policy.
- `t3 triage`: investigate a problem with Claude or Codex and help file an issue.
- `t3 browser setup`: configure Linux browser prerequisites, including sandbox support, libraries and fonts.
- `t3 theme`: inspect/set environment-wide theme defaults.
- `t3 update`: download/switch versions, including an installed background service.
- `t3 install` / `t3 uninstall`: install this version as the command or remove the command, downloaded versions and service. Top-level help says uninstall keeps projects and threads.

None of these maintenance operations was run during documentation work.

## Current limits and a later command picker

The installed `thread` group has exactly four advertised subcommands: `list`, `start`, `send`, `show`. It does not advertise rename, archive, settle, pin, interrupt or search subcommands. Agent tools in this T3 session expose additional thread operations, but those tool names are not shell commands.

The repository now includes an opt-in interactive playground described below. It does not add missing operations to the upstream T3 CLI.

## Repository interactive playground

The opt-in `t3` mise environment now provides a tracked picker and CLI tasks. Runtime state is ignored in `/.t3/`; no database or credentials are committed. This remains a playground against the schema of the installed version above, not a fully isolated agent sandbox.

Prerequisites: mise, a working `t3` executable, Python 3, curl and sqlite3. The picker installs Gum 2.0.2 through mise. Provider setup remains machine-dependent; the picker does not configure credentials. Global/system mise configuration still applies.

For a new checkout, start the server in one terminal:

```bash
mise -E t3 run t3:serve
```

Then register the checkout and open the picker in another terminal:

```bash
mise -E t3 run t3:init
mise -E t3 run
```

Type to filter projects and threads by title; press Enter to select. Read messages, start a thread or compose a follow-up. The composer supports Enter to submit, Ctrl+J for newlines and Ctrl+E for an external editor, then asks before sending. Back entries return to the previous menu; Ctrl+C cancels a picker. Duplicate titles remain distinct selections. An empty project offers a new thread.

The default base is the checkout's `.t3`, and the server binds `127.0.0.1:3778`. Stop the foreground server with Ctrl+C. If the port is occupied, choose another in an ignored `mise.t3.local.toml`:

```toml
[env]
T3CODE_HOME = "{{config_root}}/.t3"
T3_LOCAL_PORT = "3779"
```

The current workstation retains its existing temporary directory and port through that local override; it uses the same tracked picker. `mise -E t3 run t3:info` shows the actual target. Do not move a live database to change this path: stop its server first. Each checkout gets its own default state. Selecting `t3` replaces the default mise environment; use `-E skogai,t3` to combine them.

Other tasks: `t3:health` checks HTTP; `t3:status` reports settings; `t3:projects`, `t3:threads` and `t3:threads-all` print inventories. `t3:show`, `t3:start` and `t3:send` retain explicit argument interfaces with `--help`. The picker is also available as `mise -E t3 run t3`. Outside the `t3` environment the default picker task is not loaded.

Project discovery and cross-project thread discovery query internal SQLite tables read-only. Agent actions go through the CLI with an explicit base directory. T3 upgrades may require query updates. No live provider execution is covered by the focused checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 .skogai/tests/test_t3_picker.py
```

# T3 Code MCP: what an outside agent can do

Reference for agents (Claude Code cloud sessions, Codex, anything else) that talk to
T3 Code on `skogix-workstation` through the **T3 Code MCP server**.

Written 2026-11-13 from a Claude Code cloud session, after testing against
T3 server `0.1.9` (environment `e17b97dc-2e6c-43be-963d-70a1e7f14f99`, linux x64).

## The one rule to know first: inside vs. outside a thread

An MCP client is either:

- **Inside a thread**: an agent that T3 itself is running (a Codex or Claude thread).
  It has a thread credential, a "current thread", inherited project/model/modes.
- **Outside a thread**: anything else that connected to the MCP server (for example
  a Claude Code cloud session). No current thread, so every call must name its target
  (`projectId`, `threadId`).

Tools that "act as the calling thread" fail from outside with:

```
OrchestratorMcpFailure  code: thread_credential_required
"This tool acts as the calling T3 thread, so it needs an agent running inside T3 Code."
```

| Status from outside | Tools |
|---|---|
| **Verified working** | `t3_project_list`, `orchestrator_capabilities`, `t3_environment_read`, `t3_thread_list`, `t3_thread_read`, `t3_thread_launch`, `t3_thread_wait`, `t3_thread_send`, `list_scheduled_tasks` |
| **Verified failing** (`thread_credential_required`) | `delegate_task`, `create_threads` |
| **Probably failing** (describe "this thread" / "caller thread"; untested) | `t3_worktree_handoff`, `t3_worktree_status`, `t3_background_wait`, `t3_environment_preferences_update`, `run_scheduled_task_now`, preview tools on "this thread's" tabs, `device_open` |
| **Untested** | everything else below |

**Workaround:** from outside, start work with `t3_thread_launch` (top-level thread).
That thread runs inside T3, so *it* can call `delegate_task`, `create_threads`, etc.

## Basic loop from outside

```text
t3_project_list                       -> pick projectId
t3_thread_launch(projectId, title, message, modelSelection?, workspaceStrategy?)
                                      -> threadId, runId
t3_thread_wait(threadId, runId)       -> status: completed / timedOut
t3_thread_read(threadId, afterPosition, limit, maxCharsPerItem)
                                      -> the agent's reply
t3_thread_send(threadId, message, mode:'auto')   -> follow-up turn, repeat wait/read
```

Notes from testing:

- Messages sent over MCP show up as `createdBy: agent`, `creationSource: mcp`.
- `t3_thread_send` on a finished thread starts a new turn run by **that thread's own
  provider/model** (a Codex thread answers as Codex). You talk *to* the thread, you
  don't take it over.
- Threads run with the thread's runtime mode (currently `full-access`): the agent will
  run commands and edit files if the message asks. State "read-only, don't change files"
  explicitly for probes.
- Use `clientRequestId` on launch/send so a retry after a lost reply doesn't duplicate.
- `modelSelection` for launch: `{instanceId:'claudeAgent'|'codex', model, options:{effort:'low'}}`.

## Full tool catalog

### Server, environments, machines

| Tool | What it does |
|---|---|
| `t3_environment_read` | Server identity (label, version, OS) and preferences. |
| `t3_environment_preferences_update` | Change server prefs: background-activity profile, default thread env mode (local/worktree), new worktrees from origin, provider update checks, commit/PR writing style. Caller-thread only. |
| `t3_environment_links` | List linked machines (other environments) and whether they answer. Pass their `environmentId` to other tools to act there. |
| `t3_environment_link` | Show the user a card to link another machine (vps, laptop...). Outcome arrives later as a thread message. |
| `t3_environment_unlink` | Forget a linked machine. |
| `orchestrator_capabilities` | Providers, models, per-model options (effort, fastMode, serviceTier...), runtime modes, feature flags. |

### Projects

| Tool | What it does |
|---|---|
| `t3_project_list` / `t3_project_read` | List projects; read one with its workspace and saved scripts. |
| `t3_project_create` | Register a folder as a project, or (no `workspaceRoot`) create a fresh git repo with README and first commit. Can set default model and scripts. |
| `t3_project_clone` | Clone a repo into a new/empty folder; register it afterwards with `t3_project_create`. |
| `t3_project_update` | Title, root, pin, archive, auto-pull, icon/favicon, default model, default env mode (local/worktree), **scripts** (run/test/lint/build buttons, with hooks: run on worktree create, on settle, stop on settle, auto-open preview). |
| `t3_project_delete` | Remove the project from T3 (folder on disk stays; nonempty needs `force`). |

### Threads: create, talk, steer

| Tool | What it does |
|---|---|
| `t3_thread_launch` | Create one top-level thread and optionally start it with a message. Choose project (or `scratch:true` for a scratch folder), model, runtime/interaction mode (`plan` mode exists), and workspace: `root` (project checkout), `worktree` (new branch from `baseRef`, optionally from origin), or `existing_worktree`. Supports attachments. **Works from outside.** |
| `create_threads` | Create up to 20 top-level threads at once, inheriting from the caller. Inside-thread only. |
| `t3_thread_send` | Message any thread. `mode`: `auto` (start idle / steer running / queue), `queue` (new turn), `steer` (mid-turn update), `restart` (interrupt and restart). `freshContext:true` = like `/clear`. |
| `t3_thread_send_attachments` | Send uploaded files/images as a message. |
| `t3_attachment_prepare_upload` / `t3_attachment_discard` | Get an upload URL (POST bytes to it), or discard a pending upload. Max 10 MiB images / 50 MiB files. |
| `t3_thread_wait` | Block until a run finishes (or timeout). `untilDelegatedWorkSettled` also waits for the thread's children. |
| `t3_thread_interrupt` | Interrupt a running turn (optionally `stop`). |
| `t3_queue` | Manage a thread's queued messages: list, read, edit, cancel, reorder, promote a queued message to a steer of the running turn. |
| `t3_pending_request` | List/read/answer questions a thread is waiting on. Cannot approve permission requests. |
| `t3_workflow_stop` | Stop a running Claude workflow (subagent coordinator) inside a thread without stopping the thread. |

### Threads: find, read, organise

| Tool | What it does |
|---|---|
| `t3_thread_list` | List threads, newest first; filter by project/all, status, title, settled, snoozed, include subagents. |
| `t3_thread_search` | Search active threads by title, branch, PR, project, then message text. |
| `t3_thread_read` | Read a thread: `messages` view (user/assistant/plans) or `activity` view (every timeline item, tool calls included). Page with `afterPosition`; long text with `itemId` + `textOffset`. Also returns recent runs with the model actually executed. |
| `t3_thread_update` | Rename, or regenerate the title. |
| `t3_thread_organize` | Pin, unpin, snooze (until a time), settle, unsettle, archive, unarchive, mark unread. |
| `t3_thread_configure` | Read or change a thread's provider/model/options (permission modes stay). |
| `t3_thread_transfer` | `fork` a thread's context into a new thread (from latest/run/checkpoint), `merge_back` into a related thread, or `status`. |

### Delegation (inside-thread only)

| Tool | What it does |
|---|---|
| `delegate_task` | Start a child agent with only the given task (no parent history). Any enabled provider, cross-provider allowed. `isolation: shared | worktree`, `mode: async | wait`, role (implementation/research/review/design/test/general). |
| `task_status` | Read a delegated task: working / waiting_for_children / result_available, plus summary. |
| `task_cancel` | Stop a delegated task, its runs, its own delegates and PR watches. |
| `t3_background_wait` | Keep the calling (Claude) thread in "Working" while its background tasks run. |

### Worktrees

| Tool | What it does |
|---|---|
| `t3_worktree_list` | Branch refs and checkout paths for a thread's workspace (local/remote). |
| `t3_worktree_status` | Calling thread's worktree: path, branch, project root. |
| `t3_worktree_handoff` | Move the calling thread into a new worktree/branch (runs setup script), optionally continuing with a prompt. |

### Scheduled tasks

| Tool | What it does |
|---|---|
| `schedule_task` | Create or update scheduled work. Triggers: `interval` (min 60 s), `fixed_time` (time of day + weekdays), `once`, or **`webhook`** (gives a `webhookUrl`; needs T3 Connect remote access; supports filters on headers/body, HMAC signature check, dedupe/coalesce). Runs post into one thread or a new thread per run; `freshSession` option. `enabled:false` pauses. |
| `list_scheduled_tasks` | List a project's scheduled tasks. |
| `run_scheduled_task_now` | Fire one now (returns its thread). |
| `delete_scheduled_task` | Delete one. |

### Pull requests

| Tool | What it does |
|---|---|
| `link_pull_request` / `link_pull_requests` | Attach PR(s) to a thread; T3 shows status and settles the thread on merge. |
| `list_thread_pull_requests` | PRs on a thread with state and stack order. |
| `unlink_pull_request` / `unlink_pull_requests` | Remove one, or all in given states (open/closed/merged). |
| `watch_pull_request` / `unwatch_pull_request` | Wake the thread on failed/passed checks, new comments/reviews, conflicts. |
| `write_pull_request_guides` / `read_pull_request_guide` | Generate (minutes, temp checkout) and read the "PR Guide" review tour for up to 20 PRs. |

### Browser preview (server-side tabs)

| Tool | What it does |
|---|---|
| `preview_open` / `t3_preview_list` / `t3_preview_close` | Open a tab (URL or `environment-port` dev server), list the thread's tabs, close one. Only `runtime:'server'` tabs are automatable. |
| `preview_navigate` | Go to a URL or local dev-server port/path. |
| `preview_snapshot` | Page state, accessibility tree with `aria-ref` locators, diagnostics, optional screenshot. |
| `preview_act` | click, type, hover, select, drag, upload, press, scroll. |
| `preview_wait_for` | Wait for locator/selector/text/URL. |
| `preview_evaluate` | Run JS in the page. |
| `preview_dialog` | Accept/dismiss alert/confirm/prompt. |
| `preview_resize` / `preview_set_appearance` | Viewport (fill, freeform, device presets) and light/dark. |
| `preview_status` | Tab owner, dialogs, URL, viewport, login profiles. |
| `preview_recording_start` / `_stop` | Record a tab to a video file (max 50 MiB). |

### Mobile devices

| Tool | What it does |
|---|---|
| `device_list` | iOS Simulators / Android Emulators on each device host. |
| `device_open` / `device_close` | Boot and show one in the thread's Device panel (returns an `agent-device` CLI to drive it); remove/shut down. |
| `device_screenshot` | PNG of the device screen. |

### Rendering and secrets

| Tool | What it does |
|---|---|
| `html_preview` | Render HTML to PNG + height + console output, for checking. |
| `html_render` | Show a finished HTML page (chart, diagram, mockup) inline in the thread, themed with T3 CSS variables. |
| `request_secret` | Show the user a secure single-value card; returns a one-use `secretRef` (for T3 tools, e.g. webhook signing) or a file path readable by one command. Never paste secrets in chat. |

## Providers on this machine (2026-11-13)

- **Enabled:** `codex` (gpt-6.1-sol, gpt-6-astra, gpt-6.1-terra, gpt-6-luna, +4) and
  `claudeAgent` (claude-opus-5-5, claude-sonnet-5-5, claude-fable-5-2, claude-haiku-5-5, +10).
  Both can run child tasks, including cross-provider.
- **Disabled:** cursor, grok, opencode, antigravity, fx, kiro, muse, pi.
- Re-check with `orchestrator_capabilities`.

## Safety notes

- Everything T3 runs here runs on the workstation, in `full-access` mode by default.
  An outside agent that can call `t3_thread_launch` / `t3_thread_send` can effectively
  run anything on the machine. Treat the MCP connection like a shell login.
- Permission approvals cannot be granted over MCP (`t3_pending_request` can answer
  questions, not approve permissions).
- Webhook payloads delivered to scheduled tasks are untrusted input.

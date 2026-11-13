# T3 Code upstream docs

T3 Code runs coding agents on the machine that owns the workspace. The web,
desktop, and mobile clients connect to that machine's T3 server. See the
[architecture overview](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/internals/overview.md).

## First run on Arch Linux

With Node.js and `npx` available, run `npx t3@latest` to launch the local web
app. Decline the prompt to install the `t3` command if you only want a trial.
The upstream install guide also lists the `t3code-bin` AUR package for the
stable desktop app. See [installation](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/user/install.md).

For a Codex thread, connect through **Settings → Providers** with your ChatGPT
account, or configure T3 Code to use an existing Codex CLI login on the machine
running the T3 server. See [Codex provider setup](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/user/providers-codex.md).

For the monorepo's workstation snapshot and its mise tasks, see the
[T3 Code CLI guide](../../doc/t3-cli.md).

## Upstream reading list

These links point to the upstream `v0.1.9` release. Check `t3 --version` before
applying them to an installed nightly.

| Topic | Upstream reference |
|---|---|
| All user and developer docs | [Documentation index](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/README.md) |
| Install, launch, and update | [Install and first run](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/user/install.md) |
| Codex sign-in and provider settings | [Codex](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/user/providers-codex.md) |
| Git changes, worktrees, and pull requests | [Source control](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/user/source-control.md) |
| Thread approvals and provider behavior | [Permission modes](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/user/permission-modes.md) |
| Phone or another machine | [Remote access](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/user/remote-access.md) |
| Let an outside agent read or steer threads | [Outside agents over MCP](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/user/outside-agents.md) |
| Where agents, terminals, and Git run | [Architecture](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/internals/overview.md) |

## Open SkogAI question

Upstream places agent processes and terminals on the T3 server. Can one server
launch each SkogAI agent under its own Unix user and private home, or does each
user need a separate server? This needs a source trace and a runtime check.
See [architecture](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/internals/overview.md) and [outside agents over MCP](https://github.com/pingdotgg/t3code/blob/v0.1.9/docs/user/outside-agents.md).

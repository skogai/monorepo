# ADR 0001: Starting tools

Status: accepted tool selection. Integration details remain open.
Date: 2026-11-10.
Source: [backlog](../../repos/skogix/.skogai/todo.list), item `adr;the main starting tools`.

## Context

SkogAI 3.0 begins from an existing workstation and development setup. It needs a small documented baseline that can be tested. The research in `.skogai/research/` proposes a wider stack, but the owner has already named the starting tools in the backlog.

## Decision

Start with mise, T3 Code, herdr, Git, and Arch Linux with Omarchy workstations. Document and test this combination before expanding the stack.

Use mise as much as possible. Tools and dependencies that mise can install are free to use and take priority over building our own tooling, rules, and workflows. The owner's example: managing everything ADR-related with `adr-tools` through mise is better than a home-made process. The owner stated this in review of pull request 5 on 2026-11-11.

## Consequences

- The first work is a reproducible setup recipe and one small workflow experiment.
- The existing mise setup, the Git submodule structure, and the mise plugin are the baseline to inspect.
- T3 Code's and herdr's actual workflow is captured from use before any automation is specified.
- Workstation assumptions are recorded in the bootstrap instructions.
- A need is first checked against what mise can install. Custom tooling is the fallback.
- The starting tools are not all installed through mise. A tool that comes from an Arch or Omarchy package is a workstation prerequisite, not repository configuration, and is recorded as one.

## Not decided here

This record does not select a language, database, retrieval system, ticket tracker, additional task runner, encryption mechanism, CI policy, or repository migration strategy. It does not settle herdr's role.

Under the mise rule a tool installed through mise needs no record of its own before it is used. That covers `worktrunk` and `usage`, both listed in the root `mise.toml` at version `latest`, and it covers bringing back `adr-tools`, `qmd`, `uv`, or `lazygit`, which commit `6d0ce28` removed from `mise.toml`. None of those four is in `mise.toml` today.

The encryption mechanism is still to be chosen. The backlog asks for "basic encryption via mise dotfiles/bootstrap" without naming one; `fnox` and `age` are reported as installed on one workstation.

ADR numbering has to be settled when `adr-tools` is set up. `6d0ce28` removed an earlier `0001-record-architecture-decisions.md`, the adr-tools default, and this record reuses the number, so `adr init` will want to create its own 0001.

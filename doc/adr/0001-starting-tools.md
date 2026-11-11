# ADR 0001: Starting tools

Status: accepted tool selection. Integration details remain open.
Date: 2026-11-10.
Source: [backlog](../../skogix/.skogai/todo.list), item `adr;the main starting tools`.

## Context

SkogAI 3.0 begins from an existing workstation and development setup. It needs a small documented baseline that can be tested. The research in `.skogai/research/` proposes a wider stack, but the owner has already named the starting tools in the backlog.

## Decision

Start with mise, T3 Code, herdr, Git, and Arch Linux with Omarchy workstations. Document and test this combination before expanding the stack.

## Consequences

- The first work is a reproducible setup recipe and one small workflow experiment.
- The existing mise setup, the Git submodule structure, and the mise plugin are the baseline to inspect.
- T3 Code's and herdr's actual workflow is captured from use before any automation is specified.
- Workstation assumptions are recorded in the bootstrap instructions.

## Not decided here

This record does not select a language, database, retrieval system, ticket tracker, additional task runner, encryption mechanism, CI policy, or repository migration strategy. It does not settle herdr's role.

These tools appear in the repository or its history without a decision record. Each needs its own ADR before it counts as chosen:

- `worktrunk` and `usage`: listed in the root `mise.toml`, both at version `latest`.
- `adr-tools`, `qmd`, `uv`, `lazygit`: listed in `mise.toml` until commit `6d0ce28` removed them.
- `fnox` and `age`: reported as installed on one workstation; the backlog asks for "basic encryption via mise dotfiles/bootstrap" without naming a mechanism.

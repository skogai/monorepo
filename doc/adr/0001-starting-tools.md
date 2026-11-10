# ADR 0001: Starting tools

Status: recorded user choice; integration details remain open.
Date: 2026-11-10.
Source: [personal backlog](../../skogix/.skogai/todo.list).

## Context

SkogAI 3.0 is beginning with an existing workstation and development setup.
The research suggests many additional tools, but the backlog already names the
starting tools and asks for documentation and tests.

## Decision

Start with mise, T3 Code, herdr, Git, and Arch Linux with Omarchy workstations.
Document and test this combination before expanding the stack.

## Consequences

The initial work is a reproducible setup recipe and a small workflow experiment.
The current Git submodule structure and mise plugin are the baseline to inspect.
This record does not settle herdr's role, repository migration, issue tracking,
languages, retrieval, encryption, or CI policy. Those require separate evidence
and decisions as the setup is exercised.

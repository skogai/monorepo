# ADR 0001: Starting tools

Status: accepted tool selection, recorded from the owner's todo on 2026-11-10. Integration details remain open.

## Context

SkogAI 3.0 needs a small documented baseline for testing its development setup. Research proposes a wider stack, but the owner has already named the starting tools.

## Decision

Start with mise, T3 Code, herdr, Git, and Arch Linux with Omarchy workstations.

Source: `skogix/.skogai/todo.list`, item `adr;the main starting tools`.

## Consequences

Document and test the existing mise setup first. Capture T3 Code and herdr's actual workflow before specifying automation. Git holds the current workspace and submodule relationships. Record workstation assumptions in bootstrap instructions.

This decision does not select a language, database, retrieval system, ticket tracker, additional task runner, or final repository migration strategy.

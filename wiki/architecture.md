---
type: Guide
title: Repository architecture
tags: [skogai, repository]
status: draft
sources:
  - id: repository-source
    resource: https://github.com/skogai/monorepo/blob/2268c654c9cd04732c3fb69e15ea682d2f164839/README.md
---

# Repository architecture

SkogAI 3.0 is a mise workspace with three Git submodules: `skogai`, `skogix`, and `mise-plugin`. There is no root application language or application test suite.

Root policy lives in AGENTS.md, the roadmap in doc/plan.md, accepted decisions in doc/adr/, research in .skogai/research/, and experiments in .skogai/tests/. The owner backlog belongs to skogix/.skogai/todo.list.

Submodule contents have independent histories. Change them in their own repositories and reference reachable commits from the root. See [workflow](workflow.md) and [setup](setup.md).

[Authoritative source](https://github.com/skogai/monorepo/blob/2268c654c9cd04732c3fb69e15ea682d2f164839/README.md) · [Wiki home](index.md)

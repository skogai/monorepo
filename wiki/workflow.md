---
type: Guide
title: Maintaining repository knowledge
tags: [skogai, repository]
status: draft
sources:
  - id: repository-source
    resource: https://github.com/skogai/monorepo/blob/2268c654c9cd04732c3fb69e15ea682d2f164839/AGENTS.md
---

# Maintaining repository knowledge

Before work, read the wiki index and relevant pages, then inspect the authoritative repository sources. After durable changes, update the matching page, source reference and log; distinguish observations from executed checks. Do not copy secrets, raw environment dumps, or transient chatter into the wiki.

Validate with `openknowledge validate wiki`, run `openknowledge eval run .openknowledge/evals/knowledge.yaml wiki`, and inspect `openknowledge audit wiki`. Record exact commands and outcomes in .skogai/tests/. Source changes require a deliberate baseline refresh with `openknowledge audit wiki --baseline .openknowledge/audit-sources.json --update-baseline`.

Deliver a PR against master. Record agent, harness, machine, checkout and base commit. The owner merges; leave other agents’ PRs alone.

[Authoritative source](https://github.com/skogai/monorepo/blob/2268c654c9cd04732c3fb69e15ea682d2f164839/AGENTS.md) · [Wiki home](index.md)

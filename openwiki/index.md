---
type: index
title: SkogAI repos wiki
description: Entry point of the wiki that maps the active SkogAI repos listed in the skogai/monorepo catalog.
tags: [index, catalog, skogai]
generated: { by: "claude-code", at: "2026-11-15" }
---

# SkogAI repos wiki

This wiki maps 20 repos from the [catalog](../mani.yaml): what each one is, what state it is in, and how they relate. It was written from clones taken on 2026-11-15. Each page records the commit it describes. Statements come from reading the source; nothing was run.

- [Quickstart](quickstart.md): which page answers which question, and how to fetch a repo.
- [Repo pages](repos/index.md): one page per covered repo, and the list of catalog repos that are not covered.
- Concepts that cut across repos:
  - [The two orgs: which copy is live](concepts/orgs-and-copies.md)
  - [Shared concerns: which repo owns what](concepts/shared-concerns.md)
  - [Shared conventions](concepts/conventions.md)
- [Instructions](INSTRUCTIONS.md): the brief OpenWiki reads when it regenerates this wiki.

Decisions and the plan for the monorepo itself are not here. They are in [doc/adr/](../doc/adr/) and the [project board](https://github.com/orgs/skogai/projects/4).

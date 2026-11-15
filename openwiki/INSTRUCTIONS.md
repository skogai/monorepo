---
type: Repository guide
title: Repository Wiki Instructions
description: The brief for the SkogAI monorepo wiki, which documents the catalog's active repos (cloned under repos/) and how they relate, not only this repository's own files.
tags: [documentation, repository, code-wiki, catalog]
---

This wiki is a map of the SkogAI repos, written from the `skogai/monorepo` catalog. The monorepo itself holds almost no code: the subject is the repos listed in `mani.yaml` with the tag `openwiki`, cloned under `repos/<name>/`. Treat each `repos/<name>/` directory as a separate repository with its own purpose, history and conventions.

Required structure:

- `repos/<name>.md`: one page per covered repo. State what the repo is, its current state (active, work in progress, quiet, archive) with the evidence, a source map of its layout, how it works, how it is used, how it relates to the other SkogAI repos, and its gaps and stale references. Cover large archives (`docs`, `dot-skogai`) and repos that are mostly vendored code at overview depth: a map for finding material, not a summary of every file.
- `repos/index.md`: the list of covered repos, plus the catalog repos that are not covered, one line each with the reason.
- `concepts/`: pages that cut across repos: which org copy (`skogai` or `skogai2`) is live for each name, which repo owns each shared concern, and the conventions several repos share (`.skogai/` folders, routing files, `SKOGAI_*` variables, mise tasks).
- `quickstart.md`: a routing page: which page to open for which question, and how to fetch a repo.

Rules:

- The source tree is authoritative, not a repo's README or router file. When documentation describes paths or commands that do not exist, say so.
- Never copy secret values, tokens, account identifiers, personal email addresses or private conversation content into a page. Name the variable or file instead. `cloudflare`, `podman`, `skogai2-config`, `docs` and `dot-skogai` need particular care.
- Do not document vendored upstream code beyond naming it and its origin.
- The monorepo's own decisions and plan live in `doc/adr/` and GitHub issues. Link to them; do not restate them.
- Prefer practical navigation for engineers and coding agents over generic summaries.

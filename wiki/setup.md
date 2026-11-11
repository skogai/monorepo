---
type: Guide
title: Fresh checkout blockers
tags: [skogai, repository]
status: draft
sources:
  - id: repository-source
    resource: https://github.com/skogai/monorepo/blob/2268c654c9cd04732c3fb69e15ea682d2f164839/mise.toml
---

# Fresh checkout blockers

Fresh checkout setup is not yet verified. The root declares the remote `skogai` plugin but invokes `skogai-develop`, a workstation development link. This is a machine dependency. `.miserc.toml` selects a skogai environment without a corresponding checked-in mise.skogai.toml.

Milestone 1 proposes an isolated mise entry point with explicit configuration, data, state, cache and temporary directories. It remains planned. Do not present it as an available command.

For this wiki, the tested executable is Open Knowledge 0.13.0. Install through `mise install github:openknowledge-sh/openknowledge@0.13.0`; invoke with `mise exec github:openknowledge-sh/openknowledge@0.13.0 -- openknowledge validate wiki`. Host mise configuration still applies. See [capabilities](capabilities.md).

[Authoritative source](https://github.com/skogai/monorepo/blob/2268c654c9cd04732c3fb69e15ea682d2f164839/mise.toml) · [Wiki home](index.md)

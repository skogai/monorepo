---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/33"]
tags: ["roadmap", "github"]
---

# roadmap 3: composed environments and MCP

**Source**: [Github #33](https://github.com/skogai/monorepo/issues/33)

## Description

**Deliverable:** reviewed environment profiles produce predictable mise contexts for the CLI and for MCP clients.

Done already: `env_conf_d`, the `skogai`/`develop`/`t3` environments and their precedence are documented in `doc/mise.md`. Still open:

- [ ] Fixture test with two dummy profiles: none, each alone, `-E foo,bar` and reversed order; check variables and tasks.
- [ ] Run `mise -E foo,bar mcp` (through the #31 entry point once it exists) and check the config, task and tool resources matc

## Notes

*Imported from external tracker. See source link for full context.*

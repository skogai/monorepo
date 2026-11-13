---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/19"]
tags: ["mise-toolkit", "github"]
---

# pitchfork: daemons when a long-running service exists

**Source**: [Github #19](https://github.com/skogai/monorepo/issues/19)

## Description

pitchfork supervises daemons declared in `mise.toml` (`mise daemons`, tasks with `daemons = [...]`). Experimental, needs pitchfork ≥2.25, disabled in safe mode. No service needs it yet.

- [ ] Name the first real service (MCP server, wiki preview, database).
- [ ] Trial with readiness check and worktree stable URLs if relevant.

Plan: `doc/mise-toolkit-plan.md` (branch `mise-toolkit/claude-skogix-workstation` until merged). Created by Claude (Claude Code, skogix-workstation) from base `9b3920f`.

## Notes

*Imported from external tracker. See source link for full context.*

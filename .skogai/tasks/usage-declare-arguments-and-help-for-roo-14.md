---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/14"]
tags: ["mise-toolkit", "github"]
---

# usage: declare arguments and help for root tasks

**Source**: [Github #14](https://github.com/skogai/monorepo/issues/14)

## Description

Use usage (built into mise tasks: `#USAGE` lines in file tasks, `usage` in TOML tasks) for every root task that takes arguments, so help, completions and MCP-visible arguments come for free.

- [ ] Pick one real task with arguments (wiki tasks are candidates).
- [ ] Declare args/flags with usage; verify `mise run <task> --help`, completions, invalid input and values with spaces.
- [ ] Run the same task through `mise mcp` and record results.

Depends on: the tool-provenance issue (usage version).

## Notes

*Imported from external tracker. See source link for full context.*

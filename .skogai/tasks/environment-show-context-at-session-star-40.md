---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/40"]
tags: ["backlog", "github"]
---

# environment: show context at session start and append it to commits

**Source**: [Github #40](https://github.com/skogai/monorepo/issues/40)

## Description

Backlog entries: "a starting script which tells both the agent and user about the current environment" and "commit context to automatically append agent, environment and harness information".

Already there (#29): `mise run env:context` prints host, platform, mise env, checkout and git position; `--trailers` prints commit trailers. Still open:

- [ ] Show it automatically at the start of an agent session (harness hook) and to the user (shell/mise hook).
- [ ] Append trailers automatically, e.g. 

## Notes

*Imported from external tracker. See source link for full context.*

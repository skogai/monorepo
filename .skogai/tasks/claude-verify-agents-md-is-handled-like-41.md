---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/41"]
tags: ["backlog", "github"]
---

# claude: verify AGENTS.md is handled like CLAUDE.md

**Source**: [Github #41](https://github.com/skogai/monorepo/issues/41)

## Description

Backlog entry: "make sure the setting/mod for claude actually reading and handling agents.md the same way as a claude.md".

Root `CLAUDE.md` is `@AGENTS.md`, so the root file loads. Not yet checked:

- [ ] Nested `AGENTS.md` in subdirectories and submodules: does Claude Code pick them up when working there?
- [ ] Whether a setting or mod should make this automatic instead of a `CLAUDE.md` shim per directory.
- [ ] Record the result in `.skogai/tests/`.

From `skogix/.skogai/todo.list` (skogix `3

## Notes

*Imported from external tracker. See source link for full context.*

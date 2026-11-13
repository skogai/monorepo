---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/15"]
tags: ["mise-toolkit", "github"]
---

# hk: git hooks and lint for monorepo and mise-plugin

**Source**: [Github #15](https://github.com/skogai/monorepo/issues/15)

## Description

Use hk (installed through mise) as the hook and lint runner. Plan milestone 4 notes the plugin's current lint run does not examine the intended files.

- [ ] Add hk through `[tools]` with a pinned version.
- [ ] Configure checks: Lua (plugin hooks), Markdown, TOML, and a staged-secrets check supporting the AGENTS.md secrets rule.
- [ ] Record which files each check actually examined.
- [ ] Decide whether hk runs as pre-commit, as a mise task, or both.

Plan: `doc/mise-toolkit-plan.md` (branch `m

## Notes

*Imported from external tracker. See source link for full context.*

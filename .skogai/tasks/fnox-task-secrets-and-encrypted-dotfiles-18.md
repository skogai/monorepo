---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/18"]
tags: ["mise-toolkit", "github"]
---

# fnox: task secrets and encrypted dotfiles

**Source**: [Github #18](https://github.com/skogai/monorepo/issues/18)

## Description

Start after milestone 1 is in place. fnox chooses where a secret comes from (age in `fnox.toml`, 1Password, cloud stores); mise `[secrets.fnox]` + task `secrets = [...]` passes it to that task only and redacts output (experimental). Tracked encrypted files are a separate mechanism: `[dotfiles] encrypt = true` with age recipients.

- [ ] ADR: fnox for task secrets, mise dotfiles age encryption for tracked files; provider choice.
- [ ] Dummy-secret experiment: task receives it, `mise env` and shel

## Notes

*Imported from external tracker. See source link for full context.*

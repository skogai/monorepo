---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/13"]
tags: ["mise-toolkit", "github"]
---

# mise: make mise the only source of usage and fnox; pin versions

**Source**: [Github #13](https://github.com/skogai/monorepo/issues/13)

## Description

On skogix-workstation (machine fact, 2026-11-11) `usage` 6.12.1 and `fnox` 1.48.0 come from pacman (`usage`, `fnox-bin`) **and** from mise. `/usr/bin` is first on PATH, so the pacman copies win. There are three `mise` binaries (`~/.local/bin`, `~/.local/share/../bin`, `/usr/bin` from `mise-bin`). Root `mise.toml` requests `usage` and `worktrunk` at `latest`.

- [ ] Decide which mise binary is the bootstrap prerequisite; record it.
- [ ] Remove the pacman duplicates, or record them as an explicit

## Notes

*Imported from external tracker. See source link for full context.*

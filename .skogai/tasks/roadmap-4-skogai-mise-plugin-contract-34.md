---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/34"]
tags: ["roadmap", "github"]
---

# roadmap 4: skogai mise-plugin contract

**Source**: [Github #34](https://github.com/skogai/monorepo/issues/34)

## Description

**Deliverable:** `skogai/mise-plugin` has a documented env/PATH contract, usable locally and from Git.

Done already: basic env/PATH plugin, root taken from the declaring config, `develop` env links the submodule, plugin pinned to a full SHA (#16, #23), basic host variables (#27, #29). Still open:

- [ ] Write the contract (option names, path resolution) as a proposed ADR before extending it.
- [ ] Drop the remaining assumption that every consumer wants `~/.local/bin` on PATH, if still present.


## Notes

*Imported from external tracker. See source link for full context.*

---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/17"]
tags: ["mise-toolkit", "github"]
---

# bootstrap: rework workstation setup as mise bootstrap + dotfiles

**Source**: [Github #17](https://github.com/skogai/monorepo/issues/17)

## Description

The owner has tried this and is remaking most of it. `mise bootstrap` declares host packages, files, services, repos, dotfiles, shell activation, tools and a `bootstrap` task; it only applies when run explicitly. `[dotfiles]` tracks files, with optional age encryption.

- [ ] Inventory the existing attempt: what is kept, what is remade.
- [ ] Decide what lives in the repo vs global config vs plugin (open question in `doc/plan.md`). Proposed ADR.
- [ ] Start from the minimum a home folder needs; 

## Notes

*Imported from external tracker. See source link for full context.*

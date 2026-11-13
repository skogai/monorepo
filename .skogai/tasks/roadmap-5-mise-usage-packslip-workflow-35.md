---
state: new
created: 2026-11-13
tracking: ["https://github.com/skogai/monorepo/issues/35"]
tags: ["roadmap", "github"]
---

# roadmap 5: mise + usage + packslip workflow

**Source**: [Github #35](https://github.com/skogai/monorepo/issues/35)

## Description

**Deliverable:** one real workflow using mise + usage + packslip, with other jdx tools added only for a specific job.

Done already: usage, worktrunk and gh pinned with `mise.lock` (#22); ADR 0002 settles the bootstrap binary (any working `mise`); `env:context` declares a usage flag. Still open:

- [ ] Pick one useful task with arguments and help; run it via CLI and via MCP (#33). Test spaces and invalid input. Overlaps #14.
- [ ] Install one supported tool through mise's packslip backend; check

## Notes

*Imported from external tracker. See source link for full context.*

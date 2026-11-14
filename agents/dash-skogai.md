---
permalink: dash-skogai/skogai
type: router
---

<routes>

- @SKOGIX.md - the users input, todo and in general where he adds relevant information
- @docs/file-structure.md - every file, folder and planned concept of this repo, and the placement test
- docs/code-review-graph.md - mandatory graph-first workflow for code exploration and review
- @docs/SKOGAI.md - architecture, orchestration, and design references
- @.tasks/SKOGAI.md - tracked work and the epic that defines this repo's global layer
- @.wiki/SKOGAI.md - curated project knowledge
- bin/ - vendored CLI and orchestration entrypoints
- fleet/ - fleet registry, repo snapshots and the git/gita skills
- mise.toml - pinned tools and repeatable repository tasks

</routes>

`/skogai` (`dash-skogai`) is the global source of truth for SkogAI. If something
is globally needed — by other repos, users or agents — it belongs here; otherwise
it does not. Full definitions are in `docs/file-structure.md`.

<openwiki>

<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behavior. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->

</openwiki>

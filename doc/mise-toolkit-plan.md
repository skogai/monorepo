# mise toolkit plan

Status: proposed, 2026-11-11. This plan is kept separate from the main [plan](plan.md) on purpose. It covers how the mise/jdx toolkit is used here: mise, usage, hk, fnox, pitchfork, aube and mise plugins. Nothing here is a decision until it is recorded in `doc/adr/`.

Tracking: GitHub project [mise toolkit](https://github.com/orgs/skogai/projects/4), label `mise-toolkit`, milestones 1 and 2 below. Background: [research note](../.skogai/research/mise-toolkit-claude.md).

## Owner direction (2026-11-11 conversation)

| Item | Direction |
|---|---|
| usage for task arguments | Yes |
| hk for hooks and lint | Yes |
| fnox for secrets | Later, once the rest is set up |
| mise bootstrap + dotfiles | Already tried; the owner is remaking most of it |
| pitchfork, marketplace plugin | Later, no current need |
| aube | Nothing to do: embedded in mise's `npm:` backend |

## Milestone 1: foundation

| Issue | Work | Relates to |
|---|---|---|
| [#13](https://github.com/skogai/monorepo/issues/13) | mise is the only source of `usage` and `fnox`; pin versions | [plan](plan.md) milestone 1 |
| [#14](https://github.com/skogai/monorepo/issues/14) | usage: arguments and help for root tasks | plan milestone 5 |
| [#15](https://github.com/skogai/monorepo/issues/15) | hk: hooks and lint for monorepo and mise-plugin | plan milestone 4 |
| [#16](https://github.com/skogai/monorepo/issues/16) | Pin the skogai plugin to a full commit SHA | plan milestone 4 |
| [#17](https://github.com/skogai/monorepo/issues/17) | Rework workstation setup as `mise bootstrap` + dotfiles | plan open questions; backlog |

Order: #13 first, because the other issues need known tool versions. #14, #15 and #16 can then run in parallel. #17 follows the owner's rework and gets an ADR on what belongs in the repo, the global config and the plugin.

## Milestone 2: later

| Issue | Work | Starts when |
|---|---|---|
| [#18](https://github.com/skogai/monorepo/issues/18) | fnox task secrets; age-encrypted dotfiles | Milestone 1 is done |
| [#19](https://github.com/skogai/monorepo/issues/19) | pitchfork daemons | A long-running service exists |
| [#20](https://github.com/skogai/monorepo/issues/20) | Package-manager plugin for marketplaces | A first client is chosen |

## Open questions

- Which `mise` binary is the bootstrap prerequisite, and should pacman copies of jdx tools be removed? Proposed in [ADR 0002](adr/0002-mise-binary-and-tool-source.md): the `mise-bin` package, and yes. Waiting for the owner.
- Repo vs global config vs plugin: where does each part of the workstation setup belong? (#17)
- Which fnox provider: age in `fnox.toml`, or an external store? (#18)

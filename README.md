# skogai/monorepo

The starting workspace for SkogAI 3.0: document the existing setup, test it,
and build from the results.

- [Initial setup plan](doc/plan.md)
- [Starting tools decision](doc/adr/0001-starting-tools.md)
- [Setup observations and next tests](.skogai/tests/2026-11-10-setup.md)
- [Research](.skogai/research)
- [Personal backlog](skogix/.skogai/todo.list)

The workspace currently includes the `skogai`, `skogix`, and `mise-plugin` Git
submodules. The root mise configuration uses a development plugin link; a
fresh-checkout bootstrap recipe is still to be tested and documented.

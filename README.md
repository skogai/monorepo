# skogai/monorepo

The starting workspace for SkogAI 3.0: document the setup already in use, test it in small steps, and build from the results.

- [Agent instructions](AGENTS.md)
- [Setup plan](doc/plan.md)
- [Starting tools decision](doc/adr/0001-starting-tools.md)
- [Setup evidence and next experiments](.skogai/tests/2026-11-10-setup.md)
- [Research](.skogai/research/)
- [Backlog](skogix/.skogai/todo.list) (private submodule)

The workspace is composed of the `skogai`, `skogix`, and `mise-plugin` Git submodules. Several agents work here in parallel on different machines; `AGENTS.md` explains what that requires.

The setup currently depends on workstation configuration, including a development link for the mise plugin. A verified fresh-clone quickstart is the first milestone in the plan and will be added here once it has been tested.

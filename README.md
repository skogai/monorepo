# skogai/monorepo

The starting workspace for SkogAI 3.0: document the setup already in use, test it in small steps, and build from the results.

- [Agent instructions](AGENTS.md)
- [Plan and current work](https://github.com/orgs/skogai/projects/4): GitHub project, issues labelled [`roadmap`](https://github.com/skogai/monorepo/issues?q=label%3Aroadmap) and [`mise-toolkit`](https://github.com/skogai/monorepo/issues?q=label%3Amise-toolkit)
- [mise configuration: environments, conf.d, plugin](doc/mise.md)
- [T3 Code CLI guide](doc/t3-cli.md) (installed-version snapshot and thread workflows)
- [Decisions](doc/adr/)
- [Setup evidence and next experiments](.skogai/tests/2026-11-10-setup.md)
- [Research](.skogai/research/)
- [Backlog](skogix/.skogai/todo.list)

The workspace is composed of the `skogai`, `skogix`, and `mise-plugin` Git submodules. Several agents work here in parallel on different machines; `AGENTS.md` explains what that requires.

The mise configuration no longer needs a hand-made plugin link, but the machine's global and system mise configuration still applies on top of it. A verified fresh-clone quickstart is [roadmap 1](https://github.com/skogai/monorepo/issues/31) and will be added here once it has been tested.

# skogai/monorepo

The starting workspace for SkogAI 3.0: document the setup already in use, test it in small steps, and build from the results.

- [The map and how to fetch a repo](AGENTS.md)
- [Agent workflow for this repository](doc/agent-workflow.md) and [GitHub authentication for mise](doc/github-auth.md)
- [Plan and current work](https://github.com/orgs/skogai/projects/4): GitHub project, issues labelled [`roadmap`](https://github.com/skogai/monorepo/issues?q=label%3Aroadmap) and [`mise-toolkit`](https://github.com/skogai/monorepo/issues?q=label%3Amise-toolkit)
- [mise configuration: environments, conf.d, plugin](doc/mise.md)
- [T3 Code vendored documentation](doc/t3code/README.md) ([snapshot source](doc/t3code/UPSTREAM.md))
- [T3 Code CLI guide](doc/t3-cli.md) (installed-version snapshot and thread workflows)
- [T3 Code upstream docs and first run](.skogai/research/t3-code.md)
- [Decisions](doc/adr/)
- [Open questions for the owner](doc/questions.md) and the [repo survey](doc/surveys/2026-11-14-repo-survey.md) behind them
- [Setup evidence and next experiments](.skogai/tests/2026-11-10-setup.md)
- [Research](.skogai/research/)
- [Backlog](repos/skogix/.skogai/todo.list)

The repo is a catalog of SkogAI repos, [`mani.yaml`](mani.yaml), managed with [mani](https://manicli.com). Child repos are cloned on demand into `repos/` and are not pinned: `mani list projects` shows the catalog, `mani sync --status` what is cloned, `mani sync -t <name> --ignore-sync-state` clones one. Nothing is cloned by default: a bare `mani sync` does nothing. `mise run agents:sync` clones all and refreshes `agents/<name>.md`, the cached root `AGENTS.md` of each repo, which you then commit. Several agents work here in parallel on different machines; [the agent workflow](doc/agent-workflow.md) explains what that requires.

The mise configuration no longer needs a hand-made plugin link, but the machine's global and system mise configuration still applies on top of it. A verified fresh-clone quickstart is [roadmap 1](https://github.com/skogai/monorepo/issues/31) and will be added here once it has been tested.

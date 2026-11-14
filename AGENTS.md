# AGENTS.md

## What this repository is

`skogai/monorepo` is a map of the SkogAI repos, not their code. Here is all repos and this is how you can get access to them if you actively look for it.

- Catalog: [`mani.yaml`](mani.yaml). `mani list projects` lists it.
- Nothing is checked out by default: every project has `sync: false`, so a bare `mani sync` clones nothing.
- To get one repo: `mani sync -t <name> --ignore-sync-state`. It lands in `repos/<name>/`, ignored by Git. Do not select with `-d`: it matches path prefixes.
- Each repo's own AGENTS.md: a cached copy in `agents/<name>.md`, readable without cloning. A repo with no cached copy has no root `AGENTS.md`, or has not been cached yet.
- Work done inside a fetched repo is committed in that repo, not here. Commits in this repo only change the catalog.

How to work on this repo itself: [doc/agent-workflow.md](doc/agent-workflow.md).

# AGENTS.md

## What this repository is

`skogai/monorepo` is a map of the SkogAI repos, not their code. Here is all repos and this is how you can get access to them if you actively look for it.

- Catalog: [`mani.yaml`](mani.yaml). `mani list projects` lists it.
- Nothing is checked out by default: every project has `sync: false`, so a bare `mani sync` clones nothing.
- To get one repo: `mani sync -t <name> --ignore-sync-state`. It lands in `repos/<name>/`, ignored by Git. Do not select with `-d`: it matches path prefixes.
- Each repo's own AGENTS.md: a cached copy in `agents/<name>.md`, readable without cloning. A repo with no cached copy has no root `AGENTS.md`, or has not been cached yet.
- What each active repo is and how they relate: the wiki in [`openwiki/`](openwiki/index.md), readable without cloning. It covers the repos tagged `openwiki` in `mani.yaml` and is optional context: the source of each repo is authoritative.
- Work done inside a fetched repo is committed in that repo, not here. Commits in this repo only change the catalog.

How to work on this repo itself: [doc/agent-workflow.md](doc/agent-workflow.md).

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**This project has a knowledge graph. Start with the code-review-graph
MCP tools to narrow scope, then read the source.** The graph is cheaper than scanning files and
gives you structural context (callers, dependents, test coverage) that file search cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes_tool(include_source=True, expand_neighbors=True)`
- **Understanding impact**: `get_impact_radius_tool` instead of manually tracing imports
- **Code review**: `detect_changes_tool` + `get_review_context_tool` instead of reading entire files
- **Finding relationships**: `query_graph_tool` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview_tool` + `list_communities_tool`

### Verify in the source

- Answer from `include_source=True, expand_neighbors=True`; read a file only if truncated.
- Do not change code from graph output alone: for any non-trivial change,
  read the implementation and the relevant tests before concluding.
- Verify the exact source when touching behavior, database logic, migrations, retries, fallbacks,
  recovery, or compatibility code.
- When the graph and the source disagree, the source wins. The graph may be stale.
- An empty graph result can mean "not indexed" or "not statically visible", not "does not exist".

### Key Tools

| Tool | Use when |
| ------ | ---------- |
| `detect_changes_tool` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context_tool` | Need source snippets for review — token-efficient |
| `get_impact_radius_tool` | Understanding blast radius of a change |
| `get_affected_flows_tool` | Finding which execution paths are impacted |
| `query_graph_tool` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes_tool` | Finding functions/classes by name or keyword |
| `get_architecture_overview_tool` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes_tool` for code review.
3. Use `get_affected_flows_tool` to understand impact.
4. Use `query_graph_tool` pattern="tests_for" to check coverage.
<!-- /code-review-graph MCP tools -->

<!-- agenttrail -->
## agenttrail plan convention
Maintain PLAN.md as the living plan. It is read by the project OWNER, not by you — write it for them.
- nodes are COMPONENTS of the system being built (`## Plain-language name {#id}`), not phases or sprints; keep the map at 5-9 components regardless of repo size — grow tasks, not cards, and split a component only when one agent could no longer own it for a session
- naming rule: titles are verb-led, plain-language, and CONCRETE — the owner can tell when it is done ("Read alerts out loud", "Watch the repo"). Never engineer-speak ("fs watcher + activity signal") and never vague vibes ("Decide what matters"); put the engineer phrasing on a `tech:` line under the heading
- tasks inside a component: `- [ ] Plain outcome {#id}`, optional indented `tech:` line beneath; mark a task `[~]` BEFORE you start it and save PLAN.md immediately — this drives the live in-progress view; flip it to `[x]` the moment it completes, `[!]` if stuck (clear once unblocked). Never batch plan updates for the end of the session
- when you mark a task `[~]`, add an indented `by: <your name>` line under it (claude, codex, cursor, …) and leave it there when done — it is the record of who did what
- edges under a component heading: `needs: [id, id]` = must come after those components; `links: [id, id]` = interconnected with / talks to
- `files: [src/audio/**, config.py]` under a component declares which paths it owns — keep it current; it is how the live view knows which component you are really working in, including when you revisit finished work
- `{#id}`s are stable — never rename, only add or remove nodes
- if a component's job is storing or distilling KNOWLEDGE (a vault, research notes, learnings) rather than producing the product itself, add an indented `kind: knowledge` line under its heading — the map renders it as a knowledge organ. If a component is a HUMAN step (a person must act — review, approve, post by hand), mark it `kind: human` instead — it renders dashed in its own color so the owner can spot where they enter the loop. A component whose output is an operable artifact (a local console, dashboard, generated page) may add an indented `url:` line — the card becomes clickable and opens it; omit kind:/url: for everything else
- open tasks carry an indented `from:` line naming their provenance — `from: agent` when YOU are declaring it as your own imminent build intent (the owner corrects these on sight if wrong), `from: roadmap` when it comes from planning documents (durable intent, backloggable); omit when neither
- new work NEVER creates a component by default: it lands as your session todos plus tasks under the component whose files it touches. Add a NEW component only when the system grows a durable new part. Durable is not a prediction — test it NOW: something else already depends on it (load-bearing), deleting it would change what the product does, you can name a plausible second task for it, and it owns files no component claims. Record the addition under `## decisions`. Time corrects mistakes cheaply: merge a card back into its neighbor if no second change ever comes; promote a task to a card when work keeps clustering in files its siblings never touch. Remove a component only when that part is deleted from the product
- before ending a session, graduate your plan-worthy completed todos into PLAN.md as `[x]` tasks (with `by:`) — housekeeping todos stay out of the plan
- record any plan-affecting decision under `## decisions` BEFORE implementing it

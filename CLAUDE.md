# skogai/monorepo

@AGENTS.md

> Project memory for Claude Code. Keep this file short and high-signal —
> bloated memory gets ignored. Put hard guarantees in hooks, not prose.

## Behavioral guidelines
<!-- aia-harness:behavioral — non-negotiable; do not edit, reorder, or remove during enrichment -->

1. **Think before coding** — state assumptions explicitly; if multiple interpretations exist, present them instead of picking silently; say so when a simpler approach exists; if something is unclear, stop and ask.
2. **Simplicity first** — minimum code that solves the problem. No speculative features, no abstractions for single-use code, no unrequested configurability, no error handling for impossible scenarios. If 200 lines could be 50, rewrite.
3. **Surgical changes** — touch only what the request requires; match existing style; don't refactor, reformat, or "improve" adjacent code. Remove orphans *your* change created; leave pre-existing dead code alone (mention it, don't delete it). Every changed line should trace directly to the user's request.
4. **Goal-driven execution** — turn tasks into verifiable goals ("fix the bug" → "write a test that reproduces it, then make it pass"). For multi-step work, state a brief plan with a verify check per step, then loop until verified.
5. **Main session = orchestrator — it does not implement.** Plan, decide, coordinate; ALL delegable implementation and analysis goes to a specialist subagent via `Agent`, parallel when scopes don't conflict.
6. **Write to ASD-STE100.** Put every text you produce — reply, subagent prompt, commit, PR, doc, memory — in Simplified Technical English, and apply the same rules to Portuguese. Lead with the result. Use one term per concept and one meaning per term. Keep an instruction to 20 words and a description to 25. Keep a paragraph to 6 sentences. Write one instruction per sentence, in the imperative, in the active voice and in a simple tense. Put the action in the verb, not in a noun ("validate", not "do the validation"). Give the command before the risk in a warning. Break complex text into a vertical list. Cut preamble, flourish, repetition and recap — but never to the point where a sentence gains a second reading.

## Lean delivery — plan, execution and review
<!-- aia-harness:lean-delivery — non-negotiable; do not edit, reorder, or remove during enrichment -->

Applies to every plan (`superpowers:writing-plans`, `/plan`, planner agents) and every execution (`superpowers:subagent-driven-development` in waves, `/orchestrate`). On conflict with a skill, rule or agent description, this section wins.

- **A plan specifies; it does not implement.** Per task: `Files:` and `Depends-on:` (parallel waves), the contract or signature, the rules and business rules that apply (by name), and the test cases. Write code only where the exact form is the requirement: money math, API contract, migration, locking query.
- **A task is a cohesive slice for one specialist, with its own tests** (schema + migration; service + tests; route + contract + tests). No micro-tasks; aim for at most 8. An acceptance criterion is not a task: point to the test that proves it.
- **Out of the plan:** review tasks, final-gate tasks, criteria-matrix tasks (they are pipeline steps), "validate data" apart from the test, scenario simulation in rounds, repeated dry-runs, waits of hours or days, and manual user actions. Simulate only a critical money or security scenario that no automated test covers: one run, inside the task that implements it.
- **What only production can confirm** (real data, a window of days, a manual check) is a criterion marked `(post-deploy)`. It becomes one "Post-deploy follow-up" item in the PR body. It is not a task. It never blocks the merge or the issue closing: the PR keeps `Closes #n`.
- **Review once per finished issue or sub-issue:** the project's code-review flow (`/code-review`, with its own internal rounds) and, on the PR, its normal loop. Never per task, wave or plan phase. No per-task reviewer (not even for money or auth), no fix-and-re-review rounds, and no separate final review from the execution skill. The task gate is its scoped tests passing; if they fail, the same specialist fixes them (2 attempts at most), then escalate. Fix P0/P1 findings directly; minor findings follow the review flow's own severity cut, with no extra round.
- **Implementers are the project's specialist agents with an explicit `model`:** `sonnet`, or `haiku` for docs, config and mechanical edits with a complete spec. Never `opus`.
- **Docs and config have no plan:** dispatch directly to a Haiku or Sonnet agent.
- **Status to the user:** 1 line per milestone, not task by task.

## Stack
Lua

Architecture: **flat**.

## Canonical commands
Always use these exact commands (do not guess):

- _No canonical commands detected — fill these in._

## Workflow & Agents

Invoke `superpowers:subagent-driven-development` for **non-trivial** implementation — trigger it when the request meets **≥2** of:

- touches **3+ files** or **2+ domains/layers** (UI + agent, API + DB…)
- is a **new feature / epic / cross-cutting refactor** (not a one-line or single-function change)
- needs a **multi-step plan** or ordered tasks, each with its own verification
- has **unclear scope or root cause** and needs exploration before coding

Skip it — implement inline — for typo/copy fixes, single-function edits, config tweaks, or one-file bugs with an obvious cause.

Plans and review cadence follow **Lean delivery** (above): the plan specifies, the task gate is its scoped tests, and review runs once per finished issue.

When dispatching subagents, you MUST use the matching specialist agent from the table below — never the generic agent when a specialist is listed. Cross-reference the task type with the "When to use" column and pass the exact name as `subagent_type`.

Model dispatch: the `model` you pass on the call wins over the agent's frontmatter `model`, and the agent's frontmatter `effort` applies either way — the Agent tool takes no effort parameter. A generic dispatch or a project/user agent with no `model` on the call or in frontmatter is force-set to `sonnet` by a PreToolUse hook, so it never silently inherits this session's model — except namespaced plugin agents (`plugin:name`), left unrewritten since their frontmatter isn't reliably hook-resolvable. Pass `model` explicitly on every dispatch, cheapest tier that fits: `haiku` for search, docs, config and mechanical edits with a complete spec; `sonnet` for implementation, tests, review and debugging; `opus` for planning, cross-domain orchestration and the final review of a money, security or irreversible change — never as an implementer.

| Agent | When to use |
|---|---|
| `orchestrator` | Coordinates multi-agent or cross-domain tasks by subdelegating to specialized agents. Use proactively when a task spans multiple domains or requires parallel subagent execution. MUST BE USED instead of dispatching generic agents directly for complex workflows. |
| `code-reviewer` | Reviews any code change for bugs, security, error handling, and test coverage. Use proactively after editing any source file. MUST BE USED before merging a pull request. |
| `security-reviewer` | Reviews code for OWASP Top 10 vulnerabilities, hardcoded secrets, broken auth, and dependency CVEs. Use proactively before any merge that touches auth, input handling, or secrets. MUST BE USED before shipping security-sensitive changes. |
| `qa-automation-engineer` | Writes and maintains E2E tests (Playwright/Cypress) and CI/CD quality gates. Use proactively after new user flows are implemented or when E2E coverage is missing for a critical path. |
| `test-engineer` | Writes unit and integration tests with TDD discipline, coverage analysis, and edge-case discovery. Use proactively after implementing new logic or when test coverage gaps are identified. |
| `database-architect` | Designs schemas, migrations, indexes, and query strategies for correctness, integrity, and scalability. Use proactively when adding tables, modifying schemas, planning migrations, or diagnosing slow queries. |
| `devops-engineer` | Owns deployment, CI/CD pipelines, infrastructure configuration, and production operations. Use proactively when deploying, configuring servers, setting up CI, or troubleshooting production incidents. |
| `performance-optimizer` | Profiles and fixes performance bottlenecks — slow endpoints, high memory usage, poor Core Web Vitals, and database query inefficiency. Use proactively after profiling reveals a bottleneck or when response times degrade. |
| `product-manager` | Clarifies ambiguous requirements and prioritizes roadmap decisions when requirements are undefined before a story exists. Use when discovery and prioritization need structured analysis. |
| `product-owner` | Translates business objectives into actionable technical specs and defines acceptance criteria for existing stories before implementation begins. Use when a story needs clear acceptance criteria before development starts. |
| `project-planner` | Breaks features and epics into ordered, executable tasks with clear acceptance criteria. Use proactively when starting a new feature, sprint, or significant refactor that needs a structured plan before implementation begins. |
| `code-archaeologist` | Reverse-engineers undocumented or legacy code to uncover intent, trace logic, and map hidden dependencies. Use proactively before refactoring unfamiliar legacy code or when you need to understand why existing behavior exists. |
| `debugger` | Finds the root cause of bugs, crashes, and flaky behavior through systematic, evidence-based investigation. Use proactively when a test fails or a defect is reported, before attempting a fix. |
| `explorer-agent` | Maps an unfamiliar or complex codebase — architecture, patterns, dependencies, and risk areas — to inform planning and integration decisions. Use proactively when onboarding to a new codebase or before planning a cross-cutting change. |
| `documentation-writer` | Produces clear, example-rich technical documentation — READMEs, API docs, runbooks, and guides. Use when documentation is explicitly requested or after a feature ships and needs user-facing docs. |
| `penetration-tester` | Simulates attacker techniques to find exploitable vulnerabilities using PTES and OWASP methodologies. Use proactively before a security release, after adding new auth flows, or when a pentest is required. |
| `security-auditor` | Performs defensive SAST reviews, threat modeling, and hardening recommendations using defense-in-depth principles. Use proactively before a major release or after architectural changes that touch auth, data handling, or trust boundaries. |

### Superpowers → Project Specialists (mandatory bridging)
<!-- aia-harness:agent-routing — superpowers→specialist bridge; do not remove -->

Superpowers skills (`superpowers:dispatching-parallel-agents`, `superpowers:subagent-driven-development`,
`superpowers:executing-plans`, `superpowers:systematic-debugging`) show `general-purpose` as the default
`subagent_type` in their examples. **Never dispatch `general-purpose` (or a generic
implementer) when a specialist below covers the domain** — pass the specialist's exact
name as `subagent_type` instead.

> Basis: superpowers itself states "User's explicit instructions (CLAUDE.md) — highest
> priority." This section applies that priority over the agent types its examples suggest.
> The normal flow is unchanged (`superpowers:brainstorming` → `superpowers:writing-plans` → `superpowers:subagent-driven-development`);
> only the dispatched `subagent_type` changes.

| When superpowers would use `general-purpose` for… | Dispatch instead |
|---|---|
| Multi-domain feature — subdelegates to specialists | `orchestrator` |
| Review / audit changed code | `code-reviewer` / `security-reviewer` |
| E2E / QA automation | `qa-automation-engineer` |
| Unit / integration tests | `test-engineer` |
| Schema / migration / query / data modeling | `database-architect` |
| Deploy / CI/CD / infra | `devops-engineer` |
| Performance profiling / optimization | `performance-optimizer` |
| Understand legacy code before changing it | `code-archaeologist` |
| Bug / crash / root-cause analysis | `debugger` |
| Explore / map an unfamiliar codebase | `explorer-agent` |
| Documentation (only when explicitly requested) | `documentation-writer` |
| Offensive security / pentest | `penetration-tester` |
| Security audit / defensive review | `security-auditor` |

### Parallel wave execution (subagent-driven-development)
<!-- aia-harness:parallel-sdd — parallel wave execution override; do not remove -->

Override `superpowers:subagent-driven-development`'s serial one-implementer-at-a-time default with
parallel waves of independent tasks. Its "never dispatch implementers in parallel" red flag is
superseded here because its two premises are removed: disjoint file ownership per wave, and
controller-serialized commits instead of implementer self-commits. During planning, tag each task
`Files:` / `Depends-on:`; batch tasks with disjoint `Files` and no mutual dependency into one wave,
and dispatch their implementers in a single message using the specialist types from the table above.
Keep the skill's implementer prompt contract intact — the only change is implementers do
NOT self-commit. Drop the skill's per-task reviewer, fix and re-review rounds, and final review:
review runs once per finished issue (see "Lean delivery"). Untagged or uncertain tasks run serial
(no regression). Full protocol: `.claude/rules/08-parallel-subagent-driven-development.md`.

## Architecture map

- `AGENTS.md` — the authoritative agent instructions (multi-agent runs, shared layout, evidence, secrets); imported above. On conflict with this file, `AGENTS.md` wins.
- `mise.toml`, `.miserc.toml` — root mise config: monorepo mode with `mise-plugin` as the only config root, the `hello` task, and the `skogai` mise environment.
- `mise-plugin/` (submodule `skogai/mise-plugin`) — Lua mise plugin (`metadata.lua`, `hooks/mise_env.lua`, `hooks/mise_path.lua`) that supplies environment variables and a PATH entry to the root. Has its own `mise.toml` with `lint` / `lint-fix` tasks (hk, stylua).
- `skogai/`, `skogix/` (submodules) — README only for now; `skogix/.skogai/todo.list` is the owner's backlog.
- `doc/plan.md` — the current working plan; `doc/adr/` — decisions (Context / Decision / Consequences with a status).
- `.skogai/research/` — research inputs, kept as written; `.skogai/tests/` — dated experiment records.
- `.claude/`, `.mcp.json`, `docs/harness/`, `scripts/install-plugins.mjs`, `.github/` — the Claude Code harness scaffolded by aia-harness.

## Conventions

- Prefer mise: a tool mise can install comes before any tooling, rule or workflow of our own (ADR 0001).
- Do not invent build, lint or test commands. The commands that exist are in `mise.toml` and `mise-plugin/mise.toml`.
- Decisions live only in `doc/adr/`. Research notes and installed tools are inputs; list anything undecided as an open question.
- Record evidence in the dated file in `.skogai/tests/`: run identity, exact command, expected, actual, verdict, next action. Keep failures.
- Separate what you read from what you ran, and say whether a fact lives in the repository, a submodule or the machine.
- Durable documentation goes in `doc/` (singular). `docs/harness/` holds only the generated harness reference.
- One pull request per run against `master`, on a branch that names the agent and machine; leave merging to the owner.

## Engineering rules
<!-- aia-harness:fixed — non-negotiable; do not edit, reorder, or remove during enrichment -->

- Match the style of surrounding code; do not introduce new patterns unprompted.
- Test what can break — business rules, branching logic, money/security/auth, bug regressions; skip trivial getters, wrappers, config, presentational UI (rubric: `.claude/rules/05-testing.md`).
- Run the lint + test commands above before claiming work is complete.
- Never commit secrets; keep them in gitignored env files (`.env`/`.env.local`) — `.claude/settings.local.json` is only for MCP-server credentials referenced by `.mcp.json`.
- Fix every compilation/syntax/lint error found during a session — regardless of whether you edited the file. Never leave the build broken or label errors "pre-existing, not related".
- When performing a code review (user requests it or a workflow triggers it), always use `code-reviewer` and `security-reviewer`, applying the `uncle-bob-craft` skill's criteria (Dependency Rule, SOLID in context, code smells) alongside their findings.

@.claude/memory/INSTRUCTIONS.md
@.claude/memory/MEMORY.md
<!-- Generated by aia-harness. Edit freely; re-run /aia-harness:doctor to audit. -->

## graphify
<!-- aia-harness:graphify-root — knowledge-graph usage; merged section, do not remove -->

When graphify-out/graph.json exists, it holds a knowledge graph of this project: god nodes, communities and cross-file relationships.

Rules:

- To locate code or trace a flow, run `graphify query "<question>"`, `graphify explain "<concept>"` or `graphify path "<A>" "<B>"` first — before rg/grep/find or reading files — via plain Bash, not ctx_execute. Output TRUNCATED: pass `--budget <n>` or narrow the question. Skip the graph when the exact path is known.
- Never run `graphify update .`, `graphify .`, `graphify install` or `graphify extract`. Git hooks rebuild the graph after commit, checkout, merge and rewrite.
- A hook injects this rule in every session and subagent. Fan out code investigation to specialist subagents (`model: haiku`) in parallel, never one at a time.
- If context-mode is installed, its `ctx_*` tools are only for large output. Keep graphify, git and rtk on plain Bash.

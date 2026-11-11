# Wiki implementation — 2026-11-11

Run: Codex gpt-6-astra, T3 Code / Codex harness, skogix-workstation.
Checkout: `/home/skogix/dev/Work/t3-646f8aab-5a8aecb63081a2b8`.
Base: `2268c654c9cd04732c3fb69e15ea682d2f164839`.

Source observations: README, plan, ADR 0001, current-work, mise configuration, submodule pointers and prior Open Knowledge research. No application behavior inferred. Upstream main README documents commands absent from installed 0.13.0; this bundle deliberately targets 0.13.0. `git ls-remote https://github.com/openknowledge-sh/openknowledge.git refs/tags/v0.13.0` returned `74da1da22d9348b3c33173037eeeb3b5c65713e9`, used to pin the Action.

Machine prerequisites: existing mise, Git, Open Knowledge, Python (one-off editing/protocol check), GitHub CLI and authenticated GitHub access. Existing host mise config and plugin development link apply. This is not clean-install or second-machine evidence.

| Exact command | Expected | Actual / verdict | Next action |
| --- | --- | --- | --- |
| `openknowledge --no-telemetry version` | Report version | 0.13.0; pass | Match help to binary |
| `openknowledge setup github wiki --plan` before scaffold | Inspect profile | Missing wiki directory; fail | Scaffold first; retry succeeded |
| `openknowledge scaffold --name 'SkogAI Repository Wiki' --bundle-name skogai-monorepo --no-setup wiki` | Create bundle | Created OKF 0.2; pass | Customize pages |
| `openknowledge setup github wiki` | Generate CI/evals/baseline | Created; pass | Replaced generic evals, changed branch to master, pinned action, removed unconfigured scheduled maintenance |
| `mise exec github:openknowledge-sh/openknowledge@0.13.0 -- openknowledge version` | Resolve release | 0.13.0; pass | Cold installation still untested |
| `mise run wiki:validate` | No diagnostics | Passed without warnings; pass | Maintain |
| `mise run wiki:eval` | Relevant repository pages | Three cases, six assertions passed; pass | Extend with real questions |
| `openknowledge search wiki 'fresh checkout'` | Setup evidence | Returned setup page evidence; pass | Maintain |
| `openknowledge query hybrid --text 'mise setup' wiki` | Retrieval results | Returned results; pass | No semantic claim correctness inferred |
| `openknowledge audit wiki --baseline .openknowledge/audit-sources.json --update-baseline` | Report risks | Zero high, 11 medium findings; pass for execution, incomplete governance | Assign real owners; provenance for scaffold/spec/capabilities |
| `openknowledge claims validate --path wiki` | Valid claim lifecycle | Passed; no authored typed claims | Add only supported claims |
| `openknowledge export html --out wiki-site wiki` | Static bundle | 17 files; pass | Browser navigation not tested |
| `openknowledge export json --out wiki-exports/wiki.json wiki` | JSON | Written; pass | Inspect before sharing |
| `openknowledge export graph --out wiki-exports/graph.json wiki` | Graph | Written; pass | No verified domain graph asserted |
| `openknowledge export rdf --out wiki-exports/wiki.nq wiki` | RDF | 20 quads; pass | No semantic claims inferred |
| `openknowledge export tar --out wiki-exports/wiki.tar.gz wiki` | Archive | Written; pass | Review before sharing |
| `git diff --check` | Clean whitespace | Passed | Commit |

MCP experiment: launched `openknowledge mcp wiki` through Python subprocess with one newline-delimited JSON-RPC initialize request (protocolVersion 2025-11-25, clientInfo name wiki-check/version 1, empty capabilities); asserted response contains `result`, then process exited. Pass for initialization only; resource/tool calls not tested.

Not run: clean installation, second machine, hosted CI, browser interaction, production runtime/deploy, scheduled agents, external connections, usage collection, evidence pinning, typed claim approval, semantic SPARQL/Datalog correctness. No model credentials or deployment accounts configured. These remain explicit capability boundaries, not passing tests. Exports were tested before final agent/log wording updates and can be regenerated with the documented commands.

## Setup completion — 2026-11-11

Run: Claude Code, Claude Opus 5.5, skogix-workstation. Checkout: `/home/skogix/Work`. Base: `5ca28cd216ef4f9fab5b48a56a6edaee935d137b`. Branch: `t3/claude-workstation`.

Owner choices: harnesses claude and codex, project skill scope, observation on. Machine prerequisite: `openknowledge` 0.13.0 on PATH (`~/.local/bin`); the generated Stop hooks call `openknowledge` directly, not through `mise exec`.

| Exact command | Expected | Actual / verdict | Next action |
| --- | --- | --- | --- |
| `okn validate wiki` | No errors | OK Validation passed; pass | Maintain |
| `okn setup complete wiki --skill project --harness claude --harness codex --observe on` | Activate | Wrote `.openknowledge/integration.toml`, `.claude/skills/openknowledge/SKILL.md`, `.agents/skills/openknowledge/SKILL.md`, `.claude/settings.json`, `.codex/hooks.json`; pass | Verify hooks on another machine |
| `okn search wiki "fresh checkout blockers"` | setup.md first | setup.md:11-20 ranked first; pass | Maintain |
| `okn eval run .openknowledge/evals/knowledge.yaml wiki` | 3 cases pass | 3 passed, 6/6 checks; pass | Maintain |

Not run: a Stop hook firing in Claude or Codex, insights output content, hosted CI. Observation output in `wiki/insights/` is git-ignored until its content is reviewed.

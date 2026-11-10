# SkogAI 3.0: first setup plan

Status: initial working plan, 2026-11-10.

Goal: document the setup already in use, test it in small steps, and let the
results determine the next changes. A working fresh-checkout recipe is the first
milestone.

## Starting point

The [personal backlog](../skogix/.skogai/todo.list) names mise, T3 Code, herdr,
Git, and Arch Linux with Omarchy workstations as the starting tools. Record this
choice in [ADR 0001](adr/0001-starting-tools.md); their detailed responsibilities
and integration still need documenting.

This checkout contains three Git submodules: `skogai`, `skogix`, and
`mise-plugin`. The root mise config enables monorepo mode but lists only
`mise-plugin` as a config root. The plugin supplies environment variables and a
PATH entry. The two other submodules currently have minimal READMEs; `skogix`
also owns the backlog. These are observed boundaries, not a completed migration
of the legacy repositories.

## How to use the research

Read the [Claude survey](../.skogai/research/monorepo-claude.md),
[Codex defaults](../.skogai/research/monorepo-codex.md), and
[Gemini proposal](../.skogai/research/monorepo-gemini.md) as proposals.
Their external statistics and claims have not been reverified in this pass.
Claims about existing Python, database, or Notion usage are not established by
this checkout.

Carry forward the useful common ideas: Markdown in Git, short decision records,
local text search, a repeatable checkout, and one small end-to-end workflow test.
Do not yet adopt the proposed apps/packages tree, Taskfile, Python/Node workspace,
database, RAG, docs site, or issue tracker. Each can be considered when an actual
need appears; the research offers conflicting retrieval approaches and adds a
second task runner alongside the existing mise setup.

## Small implementation sequence

1. **Capture the baseline.** Keep the initial inspection and future test results
   in [the setup log](../.skogai/tests/2026-11-10-setup.md). Record commands,
   expected and actual results, checkout, and prerequisites. Distinguish source
   inspection from a successful runtime test.
2. **Exercise mise and the plugin.** Document how `skogai-develop` is linked,
   what config is loaded, and which tasks are visible from root and plugin.
   Test the greeting and plugin output. Decide whether `SKOGAI_MONOREPO_DIR`
   should identify this checkout or a fixed home directory. Verify in a second
   checkout before calling setup reproducible. Then document the exact bootstrap
   steps in the README and choose which tool versions need pinning.
3. **Describe the actual T3/herdr workflow.** Use one small documentation change
   to record task entry, context discovery, workspace/branch selection, editing,
   validation, review, and completion. Establish herdr's role from actual usage.
   Record any manual steps. Try a PR/CI round trip only once that workflow is
   chosen; the research recommendation is not evidence it is configured.
4. **Document names and ownership.** Explain legacy SkogAI repositories and
   their relationship to these three submodules. Record where shared versus
   personal context belongs. Adopt the minimal layout below provisionally;
   create new directories only when they contain something useful.
5. **Finish workstation/bootstrap details.** Add mise schemas to Neovim and
   verify completion/validation. Separately test encryption and restore with a
   dummy secret before documenting real bootstrap use. Choose the encryption
   mechanism based on that test; no mechanism is selected here.

Each step is done when another session can follow its instructions, reproduce
its result, and find the relevant decision. Feed new work back into the existing
personal backlog rather than creating a competing task tracker.

## Minimal documentation layout

- `README.md`: entry point and, after verification, checkout/setup commands.
- `doc/adr/`: durable decisions, using Context / Decision / Consequences / Status.
- `doc/plan.md`: this initial sequence, updated as experiments resolve questions.
- `.skogai/research/`: research inputs, retained with their original provenance.
- `.skogai/tests/`: dated experiments and observations, with secrets omitted.
- `skogix/.skogai/todo.list`: existing personal backlog, unchanged by this plan.

Use `doc/adr/` as requested in the backlog. The research's `docs/adrs/` spelling
is a proposal, not an existing convention. Nested `.skogai` directories should
hold context specific to their owning repository; shared context belongs at the
root. This layout is provisional until tested in the workflow above.

## First milestone

A new checkout can initialize the submodules, establish the documented mise
plugin setup, discover and run the greeting and plugin checks, and find the
starting-tools decision with text search. One T3-driven change has a recorded
validation and review outcome. Any machine-specific prerequisites are explicit.

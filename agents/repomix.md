---
description: Core project guidelines for the Repomix codebase. Apply these rules when working on any code, documentation, or configuration files within the Repomix project.
alwaysApply: true
---

# Repomix

<objective>
Repomix is the **bundling layer** in the skogai toolchain. Its job is to pack a repository into a single structured file that can be parsed, queried, and routed by the rest of the skogai ecosystem — specifically `skogai repo pack`, `skogai repo list --tags`, and the skogai-jq transform pipeline.

Get in, pack it, get out. The output is not for humans to read — it is a data artifact.
</objective>

<overview>
Repomix takes a local path or remote repo and emits a single file containing:

- A `<file_summary>` block (purpose, format, notes)
- A `<directory_structure>` block (repo tree)
- One `<file path="...">` block per included file

The XML output is the canonical format for skogai. Embedded doc sections (`<objective>`, `<routing>`, `<dependencies>` etc. inside CLAUDE.md, AGENTS.md, SKILL.md) are what `repo-parse` extracts into `document.schema.json` records for org-wide querying via `skogai repo list --tags`.
</overview>

<quick_start>
Pack a local repo into core/tmp/packed/:

```bash
repomix /mnt/sda1/src/<repo> \
  --output /mnt/sda1/src/core/tmp/packed/<repo>.xml \
  --style xml \
  --parsable-style \
  --remove-comments \
  --remove-empty-lines \
  --quiet
```

Via `skogai` CLI (preferred):

```bash
skogai repo pack <repo>       # one repo
skogai repo pack              # all active repos
skogai repo pack --dry-run    # show what would run
```
</quick_start>

<reference>

## Canonical Flags

Fixed for all skogai pack invocations. Do not change without updating `skogai repo pack`.

| flag | reason |
| --- | --- |
| `--style xml` | Required for `repo-parse` to extract XML sections |
| `--parsable-style` | Escapes code that would break XML structure |
| `--remove-comments` | Reduces noise in parsed output |
| `--remove-empty-lines` | Reduces file size |
| `--quiet` | Scripting mode — no stdout noise |
| `--output <path>` | Always explicit; default path is wrong |

## Output Modes

| flag | use case |
| --- | --- |
| `--style xml` | Default for skogai — parseable, queryable |
| `--style markdown` | Human-readable summaries |
| `--style json` | Structured metadata output |
| `--compress` | Structure-only (classes, functions, interfaces) — large repos where full content is not needed |
| `--no-files` | Metadata + directory tree only — repo overview without content |
| `--include <patterns>` | Scope pack to specific paths, e.g. `"**/*.md"` |

## Useful Combinations

Pack only routing/doc files (fast, for tag extraction):

```bash
repomix <path> \
  --include "**/*.md,**/AGENTS.md,**/CLAUDE.md,**/SKILL.md" \
  --style xml --parsable-style --remove-comments --remove-empty-lines --quiet
```

Pack compressed structure only (large repos):

```bash
repomix <path> --compress --style xml --parsable-style --quiet
```

Pack with recent git history:

```bash
repomix <path> --include-logs --include-logs-count 20 --style xml --parsable-style --quiet
```

Generate a Claude skill directly from a repo:

```bash
repomix <path> --skill-generate <name> --force
```

## Remote Repos

Use `--remote skogai/<repo>` only when no local clone exists. Local is always preferred.

```bash
repomix --remote skogai/<repo> --output <path>.xml --style xml --parsable-style --quiet
```

## Output Location

```
/mnt/sda1/src/core/tmp/packed/<repo>.xml    ← canonical
/mnt/sda1/src/<repo>/tmp/packed.xml         ← symlink back
```

`SKOGAI_PACK_DIR` overrides the canonical location.

</reference>

---

# Repomix Codebase Guidelines

Refer to `README.md` for full project overview and `CONTRIBUTING.md` for contribution procedures.

## Repository Layout

- `src/` — main source code (`cli/`, `config/`, `core/`, `shared/`). Feature-based structure; avoid dependencies between features
- `tests/` — mirrors the `src/` directory structure
- `website/` — documentation website (VitePress); docs live in 15 language directories (`en` + 14 translated locales) under `website/client/src/`
- `browser/` — browser extension

## Coding Guidelines

- Follow the project's coding standards enforced by Biome (`biome.json`)
- Keep each file focused on a single responsibility. Treat ~250 lines as a signal
  to review a file's cohesion, not a mandate to split: split when the file mixes
  multiple responsibilities, but leave it as-is when the length comes from one
  cohesive concern (e.g. large data/config tables)
- Add comments in English where non-obvious logic exists
- Provide corresponding unit tests for new features
- Verify changes by running:
  ```bash
  npm run lint  # Ensure code style compliance
  npm run test  # Verify all tests pass
  ```

## Non-Obvious Rules and Pitfalls

- The config JSON schema under `website/client/src/public/schemas/` is generated
  (`npm run website-generate-schema`; CI regenerates it after merges to `main`).
  Never edit it by hand.
- User-facing option or feature changes must update the docs in all 15 language
  directories under `website/client/src/`, not just `en`.
- Root `npm run lint` does not typecheck the website client. When changing
  `website/client`, verify with `npm run docs:build` in that directory.
- The VitePress build does not validate in-page anchor links; when renaming a
  heading, search the docs for links to its old anchor.
- GitHub Actions steps must be pinned to full commit SHAs with a version comment
  (e.g. `uses: actions/checkout@<sha> # v7.0.0`); pinact and zizmor enforce this in CI.

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) with scope: `type(scope): Description`
(e.g. `feat(cli): Add new --no-progress flag`)

- Scope: affected area (cli, core, website, security, etc.)
- Description: clear, concise present tense starting with a capital letter
- Commit body: follow the `contextual-commit` skill (`.claude/skills/contextual-commit/SKILL.md`)

## Pull Request Guidelines

- Follow the template at `.github/pull_request_template.md`
- Include a clear summary of changes at the top
- Reference related issues using `#issue-number`
- Combine small, related changes in the same area into one PR rather than splitting them

## Dependencies and Testing

Inject dependencies through a `deps` object parameter:

```typescript
export const functionName = async (
  param1: Type1,
  param2: Type2,
  deps = {
    defaultFunction1,
    defaultFunction2,
  }
) => {
  // Use deps.defaultFunction1() instead of direct call
};
```

- Mock dependencies by passing test doubles through the deps object
- Do not use module mocking (`vi.mock`, `vi.doMock`, `vi.resetModules`). The suite has none:
  use `deps`, a real temp directory for filesystem code, or `vi.spyOn` on a shared object
  (`silenceLogger()` in `tests/testing/loggerDoubles.ts` for the logger)

## Output Generation

- Include all content without abbreviation, unless specified otherwise
- Optimize for handling large codebases while maintaining output quality

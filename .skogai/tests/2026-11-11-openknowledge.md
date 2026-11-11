# Open Knowledge research experiments — 2026-11-11

Run: Codex (gpt-6-astra), T3 Code / Codex harness, machine skogix-workstation,
checkout `/home/skogix/dev/Work/t3-16facfd2-c69f27fa28070a33`,
base `19ede8e8443b420f2e8b9eac6f0800727c6def5e`.
Prerequisites: installed openknowledge in `~/.local/bin`, mise, authenticated gh, network and shell tools. These are machine prerequisites, not repository provisioning.

| Exact command | Expected | Actual | Verdict / next action |
| --- | --- | --- | --- |
| `openknowledge version` | Installed version | 0.13.0 | Pass; verify provenance before pinning |
| `openknowledge check --help` | Current README command available | Unknown command, exit 2 | Fail; reconcile version with docs |
| `mise registry \| rg -i 'openknowledge\|okn\|hugo\|mkdocs'` | Discover installation candidates | Hugo entries only | Pass as discovery; investigate generic backends |
| `gh api repos/skogai2/okn/releases --jq '.[] \| [.tag_name, (.assets \| map(.name))]'` | Inspect release assets | Empty output | Blocked for selecting fork release; inspect upstream or source build |
| `trial=$(mktemp -d /tmp/okn-research.XXXXXX)` | Disposable directory | `/tmp/okn-research.tqUGwH` | Pass |
| `openknowledge scaffold --name 'SkogAI research trial' --no-agents --no-setup "$trial/wiki"` | Minimal bundle | Config, index, log, SPEC created; OKF 0.2 | Pass |
| `openknowledge validate "$trial/wiki"` | Valid scaffold | 3 Markdown files; validation passed | Pass; test actual content next |
| `openknowledge export html --out "$trial/site" "$trial/wiki"` | Static output | Refused: release outputs disabled | Blocked; enable viewer in future disposable trial |
| `openknowledge search /tmp/okn-research.tqUGwH/wiki 'chronological update history' --matches` | Relevant source result | 8 matches, index Start Here ranked first, zero validation issues | Pass for smoke test only |

Source inspection (not tests): repository README, plan, ADR 0001 and mise config; fork README and installation page at `99b05e27ce328db3ae4d31cd0e30f178ead6de30`. CLI help inspected for scaffold, validate, search, view and export.

Not run: installation, actual-content retrieval evaluation, broken-link trial, live viewer, successful HTML export, hosting, CI, MCP, second machine. Next action: follow the staged pilot in the research note. No application test suite exists at the root.

## PR #8 conflict resolution

Run: Codex (gpt-6-astra), T3 Code / Codex harness, skogix-workstation; same checkout as above. Updated base: `6990cd7` (master); original PR head: `7a1ad7b`. Git configuration `git config --get pull.rebase` returned `true`, so the branch was rebased with `git rebase origin/master`.

Resolved `doc/plan.md` by preserving the complete new master roadmap and appending the wiki experiment. Updated current-work wording to reflect isolation as milestone 1. Historical research remains unchanged.

Verification: `git diff --check origin/master...HEAD` passed; `git merge-base --is-ancestor origin/master HEAD` passed. A Python assertion checked that the resolved plan starts with the exact `git show origin/master:doc/plan.md` content, scanned changed files for conflict-marker lines, and checked relative Markdown link targets in the three new pages; all passed. No application tests or runtime experiments were rerun for this documentation-only resolution. Next action: push the rebased branch for owner review.

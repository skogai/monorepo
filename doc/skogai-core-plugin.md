# skogai-core plugin walkthrough

Nov 13, 2026 · @Skogix

skogai-core (v0.10.0) is a Claude Code hooks plugin: it runs one script per hook event and can log, journal, snapshot diffs, run git steps, and show a status line. Everything is off by default behind a master switch, `enabled`.

This walkthrough is based on reading the manifest, README, hook wiring and the `Stop` and git-step scripts. The plugin and its tests were not run.

## What it does

| Feature | Setting | What happens |
| --- | --- | --- |
| Event log | `events`, `log_path` | Appends one JSON row per event, plus what the plugin did, to `.skogai/logs/skogai-core/log.jsonl` at the git root. `events` filters which events are logged (space-separated, globs like `Post*` work). |
| Turn journal | `journal`, `journal_path` | On `Stop`, appends the turn to `.skogai/journal.md` as prompt, reply, and one line per tool use. It then commits only that file as `skogai-core: journal`, leaving the rest of the index alone. |
| State files | `write_state`, `state_dir` | Writes `git-diff`, `git-diff-cached` and `wt-step-diff` to `.skogai/tmp/` on `SessionStart`, `UserPromptSubmit` and `Stop`. Nothing injects them into context yet. |
| Git steps | `{stage,commit,merge}_on_{stop,prompt}` | Six switches that run `git add -A`, `wt step commit` (skipped on a clean tree) and `wt merge --no-remove`, in that order. Failures are logged rather than failing the hook. |
| Status line | `status_line` | Shows `hook: <event>` from the log's last row. This is the only part still implemented as a TypeScript mod (`hooks/register.ts`). |

## Events it acts upon

Thirteen events are wired in `hooks/hooks.json`, each pointing at `scripts/events/<Event>.sh`.

- **Do real work:** `SessionStart`, `UserPromptSubmit` and `Stop`.
- **Log only:** `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `Notification`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PostCompact`, `StopFailure` and `SessionEnd`.

## Where it is heading

The features add up to "diff as handover": `git diff --cached` plus the next message is the full context of a turn, and each `WIP` commit is one round. `DIFF-AS-CONTEXT.md` lists two known problems:

- Rewound or retried prompts are journaled twice.
- Your diff mixes with Claude's turn unless you commit Claude's staged turn first.

## Things to know

- **Dependencies:** the scripts need `bash`, `jq`, `git` and `flock`; the git steps also need `wt`.
- **Journal dependency:** the journal is built from the log, so `events` must include `UserPromptSubmit` and `PostToolUse*`.
- **Outside a git repo:** `Stop` only logs.
- **Settings:** they live under `pluginConfigs` in `~/.claude/settings.json`, so they apply to every project. Run `/reload-plugins` after a change.
- **`CONFIG.md`:** this is the earlier dash `skogai config` design and is not wired in.

## Verification

Run both from the plugin directory.

List every setting with its default:

```sh
jq -r '.userConfig | to_entries[] | "\(.key)=\(.value.default)"' .claude-plugin/plugin.json
```

Test that it ran correctly (expects 14):

```sh
jq '.userConfig | length' .claude-plugin/plugin.json
```

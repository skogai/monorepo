# mise plugin pin evidence: 2026-11-13

Run: Claude (Fable 5.2), Claude Code harness in the Claude desktop app; machine `skogix-workstation`; checkout `/home/skogix/Work`; base `a7f92ff`; branch `mise-16-plugin-pin/claude-skogix-workstation`. Issue: [#16](https://github.com/skogai/monorepo/issues/16).

The pinned commit `7948c1252a32a1a183cce55cbf931934052a869e` is the `mise-plugin` submodule pointer at the base commit and, on 2026-11-13, the head of `main` in `https://github.com/skogai/mise-plugin` (`git ls-remote`).

## Isolation

mise ran as below, with `$S` a per-session scratch directory. The machine's global config, system config and installed plugins were not read or changed. The binary was `/usr/bin/mise` 2026.11.6. Prerequisites outside the checkout: `mise`, Git, and network access to GitHub.

```sh
env -i HOME="$HOME" PATH=/usr/bin:/bin \
  MISE_CONFIG_DIR=$S/iso2/config MISE_SYSTEM_CONFIG_DIR=$S/iso2/system MISE_DATA_DIR=$S/iso2/data \
  MISE_STATE_DIR=$S/iso2/state MISE_CACHE_DIR=$S/iso2/cache MISE_YES=1 MISE_EXPERIMENTAL=1 \
  MISE_AUTO_INSTALL=0 MISE_TRUSTED_CONFIG_PATHS=$PWD mise …
```

## Checks

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise plugins install skogai` in an empty data directory, then `git rev-parse HEAD` in the plugin | The pinned commit | `7948c1252a32a1a183cce55cbf931934052a869e`, detached HEAD | pass |
| `mise env --json` | Plugin variables set | `SKOGAI_MONOREPO_DIR=/home/skogix/Work`, `SKOGAI_CONFIG_DIR=/home/skogix/.config/skogai` | pass |
| `mise doctor` | No plugin warning | None about the plugin | pass |
| Check out `b972489` in the installed plugin by hand, then `mise doctor` | Warning on the mismatch | `plugin skogai is checked out at b972489, but [plugins] pins 7948c12…; run mise plugins install --force skogai` | pass |
| `mise env --json` in that mismatched state | Unknown | Variables still set, no warning. Only `mise doctor` reports the mismatch. | finding |
| `mise plugins update skogai` in that state | Returns to the pin | Stayed at `b972489` | fail |
| `mise plugins install --force skogai` | Returns to the pin | Re-cloned, checked out `7948c125…` | pass |
| Pin changed to the abbreviated `#7948c12`, empty data directory, `mise plugins install skogai` | Refused | `abbreviated commit SHAs are not supported; use the full commit SHA` | pass |
| Host: `mise doctor` in this checkout with the machine's own config | No plugin warning | None; the installed plugin is already at `7948c12` | pass |

The failed row is a wrong expectation, kept as a finding: `mise plugins update` does not move a plugin to the pinned commit. `doc/mise.md` gives `mise plugins install --force skogai` as the update command.

## Not run

- A second machine.
- The plugin's own tests at `7948c12`. "Tested commit" in the issue is not shown here beyond the plugin loading and setting its two variables.
- The `develop` environment, which this change does not touch.

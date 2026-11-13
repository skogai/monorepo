# ADR 0002: The mise binary and the source of jdx tools

Status: accepted by the owner on 2026-11-13, with point 1 changed from "the `mise-bin` package" to "any working `mise`".
Date: 2026-11-13.
Source: issue [#13](https://github.com/skogai/monorepo/issues/13); [evidence](../../.skogai/tests/2026-11-13-mise-tool-provenance.md); owner review on [#22](https://github.com/skogai/monorepo/pull/22).

## Context

On `skogix-workstation`, `mise` exists twice: `/usr/bin/mise` from the pacman package `mise-bin`, and a self-updating copy at `~/.local/bin/mise` that comes first on PATH. `usage` and `fnox` exist both as pacman packages and as mise installs. The root `mise.toml` requested its tools at `latest`.

`mise-bin` is required by the Omarchy packages `omarchy-fish` and `omarchy-zsh`, so it cannot be removed on an Omarchy workstation. Other machines may have no Omarchy, and get `mise` another way. [ADR 0001](0001-starting-tools.md) already treats a tool from an Arch or Omarchy package as a workstation prerequisite.

## Decision

1. A working `mise` on PATH is a required prerequisite. How it was installed (an OS package, the install script, `mise self-update`) is the machine's business, not this repository's. Nothing here depends on a particular install path.
2. Every other jdx tool (`usage`, `fnox`, `hk`, `pitchfork`) comes from mise only. They are not workstation prerequisites.
3. Tools in this repository's `mise.toml` are pinned to exact versions, and `mise.lock` is tracked. A version changes through `mise lock TOOL@VERSION`, in a commit.

## Consequences

- The repository does not pin the `mise` version itself. Behaviour that needs a minimum mise version is recorded where it is needed (for example `min_version` in `mise.toml`) when that comes up.
- A shell without mise activation or shims on PATH has no `usage` or `fnox`. Scripts that need them run through `mise exec` or a mise task.
- `mise install --locked` installs only what `mise.lock` lists and refuses a download whose checksum differs.
- `fnox` is requested by the machine's global config, not by this repository. It is pinned here when issue #18 adds it.

## Machine cleanup on `skogix-workstation`

Not required by this decision, and not run by the agent. Recommended so that one `mise` and only mise copies of the jdx tools are on PATH. `mise-bin` must stay because Omarchy depends on it, so the duplicate to drop is `~/.local/bin/mise`:

```sh
sudo pacman -R usage fnox-bin
rm ~/.local/bin/mise
```

Then `which -a mise usage fnox` should show one `mise` (`/usr/bin/mise`, plus its `/bin` and `/sbin` aliases) and only mise paths for the other two.

## Alternatives

- Require a specific `mise` install (the `mise-bin` package, or `~/.local/bin/mise`). Rejected: it ties the repository to one machine's setup, and not every machine runs Omarchy.
- Keep the pacman `usage` and `fnox-bin` as recorded exceptions. They only take effect where mise is not active, and `usage` there is a major version behind.

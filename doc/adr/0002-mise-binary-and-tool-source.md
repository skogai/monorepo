# ADR 0002: The mise binary and the source of jdx tools

Status: proposed. Not a decision until the owner accepts it.
Date: 2026-11-13.
Source: issue [#13](https://github.com/skogai/monorepo/issues/13); [evidence](../../.skogai/tests/2026-11-13-mise-tool-provenance.md).

## Context

On `skogix-workstation`, `mise` exists twice: `/usr/bin/mise` from the pacman package `mise-bin`, and a self-updating copy at `~/.local/bin/mise` that comes first on PATH. `usage` and `fnox` exist both as pacman packages and as mise installs. The root `mise.toml` requested its tools at `latest`.

`mise-bin` is required by the Omarchy packages `omarchy-fish` and `omarchy-zsh`, so it cannot be removed on an Omarchy workstation. [ADR 0001](0001-starting-tools.md) already treats a tool from an Arch or Omarchy package as a workstation prerequisite.

In the conversation that started this work the owner approved `~/.local/bin/mise` as the default prerequisite. The Omarchy dependency was found afterwards, so this record proposes the opposite and asks the owner to confirm.

## Decision (proposed)

1. The prerequisite `mise` binary is the one from the `mise-bin` package, `/usr/bin/mise`. `~/.local/bin/mise` is a duplicate and is removed.
2. Every other jdx tool (`usage`, `fnox`, `hk`, `pitchfork`) comes from mise only. The pacman packages `usage` and `fnox-bin` are removed.
3. Tools in this repository's `mise.toml` are pinned to exact versions, and `mise.lock` is tracked. A version changes through `mise lock TOOL@VERSION`, in a commit.

## Consequences

- The mise version on a workstation follows Omarchy's package updates, not `mise self-update`.
- A shell without mise activation or shims on PATH has no `usage` or `fnox`. Scripts that need them run through `mise exec` or a mise task.
- `mise install --locked` installs only what `mise.lock` lists and refuses a download whose checksum differs.
- `fnox` is requested by the machine's global config, not by this repository. It is pinned here when issue #18 adds it.

## Commands for the owner

Not run by the agent. Run after accepting this record, on `skogix-workstation`:

```sh
sudo pacman -R usage fnox-bin
rm ~/.local/bin/mise
```

Then `which -a mise usage fnox` should show one `mise` (`/usr/bin/mise`, plus its `/bin` and `/sbin` aliases) and only mise paths for the other two.

## Alternatives

- Keep `~/.local/bin/mise` as the prerequisite. It updates sooner, but `mise-bin` stays installed anyway, so two copies remain and the first on PATH decides.
- Keep the pacman `usage` and `fnox-bin` as recorded exceptions. They only take effect where mise is not active, and `usage` there is a major version behind.

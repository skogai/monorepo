# Shared T3 Code backend

The backend runs as the `t3code.service` systemd user service from
`~/Work/t3`, which is also its T3 base directory. Local clients use
`http://127.0.0.1:3773`. Register each workspace as a project on this backend.

## Install and verify

Install the T3 CLI from [T3 Code](https://t3.codes/). The installer expects `t3` on PATH. From the Work checkout, run:

```sh
./t3/install-service.sh
systemctl --user status t3code.service
mise run t3:health
mise run t3:info
```

The installer seeds missing settings and keybindings from `config/` and
installs the native T3 user service with the checkout base directory. It
disables the legacy custom unit before starting the native service. On this workstation, user lingering is already enabled.

## Pair a client

From Work, run the following and use the one-time pairing link in your
browser or T3 client. Pair each client with this backend.

```sh
t3 pair --base-dir "$PWD/t3"
```

For a client on your tailnet, generate the pairing link with
`t3 pair --base-dir "$PWD/t3" --tailscale`. Open that HTTPS link on the
client you want to pair.

## Configuration and state

The installer, default settings and keybindings are tracked here. T3 generates
the systemd unit for the installed CLI.
The shared [mise fragment](../.config/mise/conf.d/t3.toml) owns the base
directory, port and task commands. Update the tracked defaults when a
configuration change should be reproducible. The installer seeds defaults
only when the corresponding runtime files are absent.

T3 writes live settings, databases, sessions, credentials, caches and
worktrees into this directory. Git ignores runtime files.

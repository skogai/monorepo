#!/usr/bin/env bash
set -euo pipefail

base_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
unit_dir="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"

if [[ "$base_dir" != "$(realpath -m "$HOME/Work/t3")" ]]; then
    printf 'Install this service from %s/Work/t3.\n' "$HOME" >&2
    exit 1
fi

install -d -m 700 "$base_dir/userdata"
for file in settings.json keybindings.json; do
    if [[ ! -e "$base_dir/userdata/$file" ]]; then
        install -m 600 "$base_dir/config/$file" "$base_dir/userdata/$file"
    fi
done

install -d "$unit_dir"
install -m 644 "$base_dir/skogai-t3.service" "$unit_dir/skogai-t3.service"
systemctl --user daemon-reload
systemctl --user enable --now skogai-t3.service

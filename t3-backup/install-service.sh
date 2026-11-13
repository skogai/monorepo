#!/usr/bin/env bash
set -euo pipefail

base_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

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

if systemctl --user cat skogai-t3.service >/dev/null 2>&1; then
    systemctl --user disable --now skogai-t3.service
fi
t3 service install --base-dir "$base_dir"
systemctl --user enable --now t3code.service

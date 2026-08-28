#!/usr/bin/env bash
# Build a theme and install it into ~/.config/omarchy/themes, then apply it.
#   ./install.sh hohmann
#   ./install.sh apoapsis
set -euo pipefail
cd "$(dirname "$0")"

theme="${1:-}"
[[ -d $theme ]] || { echo "usage: $0 <hohmann|apoapsis>" >&2; exit 1; }

./"$theme"/build.sh

dest="$HOME/.config/omarchy/themes/$theme"
mkdir -p "$dest"
rm -rf "$dest/backgrounds"
cp -r "$theme/backgrounds" "$dest/backgrounds"
cp "$theme"/colors.toml "$theme"/icons.theme "$theme"/neovim.lua "$theme"/unlock.png "$dest/"
[[ -d $theme/src ]] && { rm -rf "$dest/src"; cp -r "$theme/src" "$dest/src"; }
cp "$theme/CREDITS.md" "$dest/CREDITS.md"

omarchy theme set "$theme"
echo "installed and applied: $theme"

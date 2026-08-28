#!/usr/bin/env bash
# Render the five drafting sheets and the lock glyph into ./backgrounds and ./unlock.png.
# Requires: python3, rsvg-convert (librsvg), JetBrainsMono Nerd Font.
set -euo pipefail
cd "$(dirname "$0")"

names=(1-hohmann-transfer 2-orbital-elements 3-ground-track 4-libration-points 5-ascent-profile)
mkdir -p backgrounds
cd src

for n in 1 2 3 4 5; do
  python3 "s$n.py"
  rsvg-convert -w 2880 -h 1800 -o "../backgrounds/${names[$((n-1))]}.png" "s$n.svg"
  echo "  sheet $n -> backgrounds/${names[$((n-1))]}.png"
done

python3 unlock.py
rsvg-convert -w 880 -h 660 -o ../unlock.png unlock.svg
echo "  glyph   -> unlock.png"

rm -f ./*.svg

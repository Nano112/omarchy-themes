#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
./fetch-backgrounds.sh "${1:-2880x1800}"
python3 unlock.py
rsvg-convert -w 1000 -h 520 -o unlock.png unlock.svg
rm -f unlock.svg
echo "  glyph -> unlock.png"

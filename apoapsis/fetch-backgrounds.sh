#!/usr/bin/env bash
# Pull the NASA source imagery and crop it to the target wallpaper size.
# All five images are NASA public domain (see ../README.md for per-image credit).
# Requires: curl, magick (ImageMagick 7).
set -euo pipefail
cd "$(dirname "$0")"

SIZE="${1:-2880x1800}"
mkdir -p backgrounds .cache

# nasa_id : extension : output name
IMAGES=(
  "iss044e045215:jpg:1-orbital-night"
  "carina_nebula:png:2-cosmic-cliffs"
  "PIA14934:jpg:3-saturn-eclipse"
  "iss062e081621:jpg:4-earth-limb"
  "as17-152-23272:jpg:5-earthrise"
)

for entry in "${IMAGES[@]}"; do
  IFS=: read -r id ext out <<<"$entry"
  raw=".cache/$id.$ext"
  if [[ ! -s $raw ]]; then
    echo "  fetching $id"
    curl -sL --fail -m 180 -o "$raw" \
      "https://images-assets.nasa.gov/image/$id/$id~orig.$ext"
  fi
  magick "$raw" -resize "${SIZE}^" -gravity center -extent "$SIZE" \
    -quality 92 "backgrounds/$out.jpg"
  echo "  $id -> backgrounds/$out.jpg"
done

#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 5 ]; then
  echo "usage: $0 LEAF OFFSET_Y OFFSET_X HEIGHT WIDTH [SCALE_WIDTH]" >&2
  exit 2
fi

leaf="$1"
offset_y="$2"
offset_x="$3"
height="$4"
width="$5"
scale_width="${6:-2400}"

workdir="${TMPDIR:-/tmp}/wholeearth_epilog_crops"
mkdir -p "$workdir"

leaf_padded="$(printf "%03d" "$leaf")"
src="$workdir/leaf_${leaf_padded}_w2000.jpg"
crop="$workdir/leaf_${leaf_padded}_${offset_y}_${offset_x}_${height}x${width}.jpg"
big="$workdir/leaf_${leaf_padded}_${offset_y}_${offset_x}_${height}x${width}_wide${scale_width}.jpg"
txt="$workdir/leaf_${leaf_padded}_${offset_y}_${offset_x}_${height}x${width}_wide${scale_width}.txt"

url="https://archive.org/download/wholeearthepilog00unse/page/n${leaf}_w2000.jpg"
if [ ! -s "$src" ]; then
  curl -L --fail --silent --show-error "$url" -o "$src"
fi

sips -c "$height" "$width" --cropOffset "$offset_y" "$offset_x" "$src" --out "$crop" >/dev/null
sips --resampleWidth "$scale_width" "$crop" --out "$big" >/dev/null
tesseract "$big" "${txt%.txt}" -l eng --psm 6 >/dev/null 2>&1 || true

echo "$big"
echo "$txt"
cat "$txt"

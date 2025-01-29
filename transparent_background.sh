#!/usr/bin/env bash
# Attempts to remove background from images.
# Usage: transparent_background.sh file1.png file2.png ...

fuzz="5%"

# Create output dir if needed
mkdir -p output

for f in "$@"; do
  width=$(identify -format "%w" "$f")
  height=$(identify -format "%h" "$f")

  convert "$f" \
    -alpha set \
    -fuzz "$fuzz" \
    -fill none \
    -draw "color 0,0 floodfill" \
    -draw "color 0,$((height-1)) floodfill" \
    -draw "color $((width-1)),0 floodfill" \
    -draw "color $((width-1)),$((height-1)) floodfill" \
    "output/$f"
done

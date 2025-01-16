#!/bin/bash

# Given PNG images, scales them to 64x64 and makes 4 mipmaps. Use this for icon graphics.

for f in "$@"; do
  base="${f%.png}"

  w=$(identify -format "%w" "$f")
  h=$(identify -format "%h" "$f")
  if [ "$w" -gt "$h" ]; then
    max=$w
  else
    max=$h
  fi

  # Pad to square
  convert "$f" -background transparent -gravity center \
          -extent "${max}x${max}" "${base}-square.png"

  # Create mipmaps
  convert "${base}-square.png" -resize 64x64 "${base}-mipmap-1.png"
  convert "${base}-square.png" -resize 32x32 "${base}-mipmap-2.png"
  convert "${base}-square.png" -resize 16x16 "${base}-mipmap-3.png"
  convert "${base}-square.png" -resize 8x8  "${base}-mipmap-4.png"

  # Combine them
  convert -background transparent \
          "${base}-mipmap-1.png" \
          "${base}-mipmap-2.png" \
          "${base}-mipmap-3.png" \
          "${base}-mipmap-4.png" +append "${base}-mipmaps.png"

  rm "${base}-square.png" "${base}-mipmap-"?.png
  rm "${base}.png"
  mv "${base}-mipmaps.png" "${base}.png"
done

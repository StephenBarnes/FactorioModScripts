#!/usr/bin/env bash
# Usage: quarter_image.sh fileA.png fileB.png
# Example: quarter_image.sh ./*.png
# Splits images into quarters. For Midjourney-generated images.

for infile in "$@"; do
  base="${infile%.*}"
  ext="${infile##*.}"

  read w h < <(identify -format "%w %h" "$infile")
  hw=$((w/2))
  hh=$((h/2))

  # Top-left
  convert "$infile" -crop "${hw}x${hh}+0+0" +repage "${base}1.${ext}"
  # Top-right
  convert "$infile" -crop "${hw}x${hh}+$((w-hw))+0" +repage "${base}2.${ext}"
  # Bottom-left
  convert "$infile" -crop "${hw}x${hh}+0+$((h-hh))" +repage "${base}3.${ext}"
  # Bottom-right
  convert "$infile" -crop "${hw}x${hh}+$((w-hw))+$((h-hh))" +repage "${base}4.${ext}"
done

#!/bin/bash
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 image scale_factor"
  exit 1
fi

file="$1"
factor="$2"

# Calculate scale percentage (e.g., 2 -> 200, 0.5 -> 50)
percent=$(awk "BEGIN {printf \"%d\", $factor * 100}")

# Create a temporary file for the new image
tmpfile=$(mktemp --suffix="$(basename "$file")")

# Scale the image using ImageMagick's convert
convert "$file" -resize "${percent}%" "$tmpfile" && mv "$tmpfile" "$file"

echo "Optimizing..."
optipng -o7 "$OUTPUT"

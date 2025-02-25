#!/bin/bash

# This script removes every 2nd frame from an animation spritesheet, to reduce file size.

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 input_image num_columns num_rows"
  exit 1
fi

INPUT="$1"
COLS="$2"
ROWS="$3"
BASENAME=$(basename "$INPUT")
NAME="${BASENAME%.*}"
EXT="${BASENAME##*.}"

# Get image dimensions
read WIDTH HEIGHT < <(identify -format "%w %h" "$INPUT")
FRAME_WIDTH=$(( WIDTH / COLS ))
FRAME_HEIGHT=$(( HEIGHT / ROWS ))

echo "Image dimensions: ${WIDTH}x${HEIGHT}"
echo "Frame dimensions: ${FRAME_WIDTH}x${FRAME_HEIGHT}"

# Create temporary directory for frames
mkdir -p frames

# Crop the input into individual frames
convert "$INPUT" -crop "${FRAME_WIDTH}x${FRAME_HEIGHT}" +repage frames/frame_%03d.png

# Process each row: keep every 2nd frame (columns 0,2,4,...)
for (( r=0; r<ROWS; r++ )); do
  row_frames=""
  for (( c=0; c<COLS; c+=2 )); do
    idx=$(( r * COLS + c ))
    row_frames="$row_frames frames/frame_$(printf "%03d" $idx).png"
  done
  # Append the selected frames horizontally for this row
  convert +append $row_frames frames/row_${r}.png
done

# Append all rows vertically into final image
OUTPUT="${NAME}_HALVED.${EXT}"
convert -append frames/row_*.png "$OUTPUT"

# Clean up temporary files
echo "Removing temporary folder"
rm -rf frames

# Optimize PNG filesize
echo "Created output image, now optimizing..."
optipng -o7 "$OUTPUT"

echo "Created $OUTPUT"

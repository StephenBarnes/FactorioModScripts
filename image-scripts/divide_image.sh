#!/usr/bin/env bash
#
# Usage: divide_image.sh [file1.png file2.png ...] [cols rows]
#
# Description:
#   Splits images into a grid of smaller images.
#   The number of columns and rows for the grid can be specified as
#   optional trailing arguments. If not provided, the script defaults
#   to a 2x2 grid (quartering the image), e.g. for images generated
#   by Midjourney.
#
# Examples:
#   # Cut all PNGs in the current directory into quarters (2x2 grid)
#   divide_image.sh ./*.png
#
#   # Cut mypic.png into quarters (2x2 grid)
#   divide_image.sh mypic.png 2 2
#
#   # Cut mypic.png into 6 pieces (3 columns wide by 2 rows tall)
#   divide_image.sh mypic.png 3 2

# --- Argument Parsing ---
# Store all command-line arguments in an array.
all_args=("$@")
num_args=${#all_args[@]}

# Default grid dimensions.
cols=2
rows=2

# Check if there are at least 3 arguments and if the last two are integers.
# This pattern allows for specifying dimensions after a list of files (e.g., *.png 3 2).
if [[ $num_args -ge 3 ]] && [[ "${all_args[-1]}" =~ ^[0-9]+$ ]] && [[ "${all_args[-2]}" =~ ^[0-9]+$ ]]; then
  # The user specified columns and rows.
  cols=${all_args[-2]}
  rows=${all_args[-1]}
  # All arguments except the last two are treated as input files.
  infiles=("${all_args[@]:0:$num_args-2}")
else
  # No dimensions provided; all arguments are treated as input files.
  infiles=("$@")
fi

# --- Image Processing ---
for infile in "${infiles[@]}"; do
  # Skip if the argument is not a regular file (e.g., it's a directory or was a numeric arg).
  if [[ ! -f "$infile" ]]; then
    continue
  fi

  # Separate the filename from its extension.
  base="${infile%.*}"
  ext="${infile##*.}"

  # Get the width and height of the source image using ImageMagick's `identify` command.
  read w h < <(identify -format "%w %h" "$infile")
  if [[ -z "$w" || -z "$h" ]]; then
      echo "Error: Could not get dimensions for $infile. Is ImageMagick installed?"
      continue
  fi

  # Calculate the width and height of each tile using integer division.
  tile_w=$((w / cols))
  tile_h=$((h / rows))

  echo "Processing $infile: Dividing ${w}x${h} image into a ${cols}x${rows} grid of ${tile_w}x${tile_h} tiles."

  # Initialize a counter for the output filenames.
  count=1
  # Loop through each row.
  for ((r = 0; r < rows; r++)); do
    # Loop through each column.
    for ((c = 0; c < cols; c++)); do
      # Calculate the pixel offset for the top-left corner of the crop.
      offset_x=$((c * tile_w))
      offset_y=$((r * tile_h))

      # Define the output filename, matching the original script's style (e.g., base1.png, base2.png).
      outfile="${base}${count}.${ext}"

      # Use ImageMagick's `convert` command to perform the crop.
      # -crop ${tile_w}x${tile_h}+${offset_x}+${offset_y} defines the size and position of the crop.
      # +repage resets the virtual canvas information to prevent issues with the output file's dimensions.
      convert "$infile" -crop "${tile_w}x${tile_h}+${offset_x}+${offset_y}" +repage "$outfile"

      echo "  -> Created ${outfile}"
      
      # Increment the counter for the next filename.
      count=$((count + 1))
    done
  done
done

echo "Done."

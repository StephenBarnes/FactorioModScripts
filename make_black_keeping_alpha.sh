#!/bin/bash

# This file changes all pixels of an image to be black, while preserving alpha value. So it changes half-transparent red/white/gray to half-transparent black.

# Note that you can reduce the filesize of resulting images by like 40% by running optipng on them afterwards, since they don't actually need RGB color data.

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "Error: ImageMagick is not installed. Please install it first."
    exit 1
fi

# Check if arguments were provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 file1.png file2.png ... fileN.png"
    echo "Example: $0 ./*.png"
    exit 1
fi

# Process all PNG files provided as arguments
for file in "$@"; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        echo "Processing: $filename"
        
        # Create a temporary file for the alpha channel
        temp_alpha="/tmp/alpha_${filename}"
        
        # Extract the alpha channel to the temporary file
        convert "$file" -alpha extract "$temp_alpha"
        
        # Convert the image to solid black
        convert "$file" -fill black -colorize 100% "$file"
        
        # Reapply the original alpha channel
        convert "$file" "$temp_alpha" -alpha off -compose CopyOpacity -composite "$file"
        
        # Clean up the temporary file
        rm "$temp_alpha"
    else
        echo "Warning: File not found or not a regular file: $file"
    fi
done

echo "All specified PNG files have been converted to black while preserving their original transparency."

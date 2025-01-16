#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 image_file [image_file2 ...]"
    exit 1
fi

for image in "$@"; do
    if [ ! -f "$image" ]; then
        echo "Error: File '$image' not found, skipping"
        continue
    fi

    echo "Processing: $image"
    
    # Create temporary file
    temp_file=$(mktemp)
    
    # Trim the image and save to temporary file
    if convert "$image" -trim "$temp_file"; then
        # Move temporary file over original
        if mv "$temp_file" "$image"; then
            echo "Successfully cropped: $image"
        else
            echo "Error: Failed to overwrite '$image'"
            rm -f "$temp_file"
        fi
    else
        echo "Error: Failed to process '$image'"
        rm -f "$temp_file"
    fi
done

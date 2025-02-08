#!/bin/bash

# Function to crop images to get rid of mipmapping
demipmap() {
    input_file="$1"
    
    # Check if input file exists
    if [ ! -f "$input_file" ]; then
        echo "Error: Input file '$input_file' not found"
        return 1
    fi
    
    # Check if input file is a valid image
    if ! identify "$input_file" >/dev/null 2>&1; then
        echo "Error: '$input_file' is not a valid image file"
        return 1
    fi
    
    # Get image dimensions using ImageMagick's identify
    dimensions=$(identify -format "%wx%h" "$input_file")
    width=$(echo $dimensions | cut -d'x' -f1)
    height=$(echo $dimensions | cut -d'x' -f2)
    
    # Calculate the target size (smallest dimension)
    if [ $width -le $height ]; then
        target_size=$width
    else
        target_size=$height
    fi
    
    # Create a temporary file
    temp_file=$(mktemp)
    
    # Crop the image to a square using the smallest dimension
    convert "$input_file" -gravity NorthWest -crop "${target_size}x${target_size}+0+0" +repage "$temp_file"
    
    # Move the temporary file over the original
    mv "$temp_file" "$input_file"
    echo "Processed: $input_file (${target_size}x${target_size})"
}

# Check if any arguments were provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <image_file(s)>"
    exit 1
fi

# Process each input file
for file in "$@"; do
    demipmap "$file"
done

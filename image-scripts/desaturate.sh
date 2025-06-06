#!/bin/bash

# Function to print usage information
print_usage() {
    echo "Usage: $(basename "$0") <image_files...>"
    echo "Desaturates the provided image files using ImageMagick."
    echo "Example: $(basename "$0") ./*.png"
    echo ""
    echo "The script will create desaturated versions with '_gray' suffix."
}

# Function to check if ImageMagick is installed
check_imagemagick() {
    if ! command -v convert &> /dev/null; then
        echo "Error: ImageMagick is not installed."
        echo "Please install ImageMagick first:"
        echo "  Ubuntu/Debian: sudo apt-get install imagemagick"
        echo "  macOS: brew install imagemagick"
        echo "  CentOS/RHEL: sudo yum install imagemagick"
        exit 1
    fi
}

# Check if any arguments were provided
if [ $# -eq 0 ]; then
    echo "Error: No input files specified."
    print_usage
    exit 1
fi

# Check for help flag
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    print_usage
    exit 0
fi

# Check for ImageMagick installation
check_imagemagick

# Process each input file
for input_file in "$@"; do
    # Check if input file exists
    if [ ! -f "$input_file" ]; then
        echo "Warning: File not found: $input_file"
        continue
    fi

    # Create temporary output filename
    temp_file=$(mktemp) || exit 1
    temp_file="${temp_file}.${input_file##*.}"

    # Convert the image
    echo "Processing: $input_file"
    if ! convert "$input_file" -colorspace gray "$temp_file"; then
        echo "Error: Failed to process $input_file"
        rm -f "$temp_file"
        continue
    fi

    # Replace original with desaturated version
    if ! mv "$temp_file" "$input_file"; then
        echo "Error: Failed to replace original file $input_file"
        rm -f "$temp_file"
        continue
    fi
done

echo "Done!"

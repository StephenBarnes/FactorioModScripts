#!/bin/bash
# Usage: white_to_alpha.sh ./*.png
# Converts lighter parts of images to transparency. For making sprites from images of semi-transparent objects against white backgrounds.

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "Error: ImageMagick is not installed. Please install it first."
    exit 1
fi

# Function to print usage
print_usage() {
    echo "Usage: $0 <image_files>"
    echo "Example: $0 ./*.png"
    echo "This script creates translucency based on luminance values while preserving existing transparency."
}

# Check if arguments are provided
if [ $# -eq 0 ]; then
    print_usage
    exit 1
fi

# Process each file
for input_file in "$@"; do
    # Check if file exists
    if [ ! -f "$input_file" ]; then
        echo "Error: File '$input_file' not found"
        continue
    fi
    
    # Check if file is an image
    if ! file "$input_file" | grep -qiE 'image|png|jpeg|jpg'; then
        echo "Error: '$input_file' is not an image file"
        continue
    fi
    
    # Create output filename
    filename=$(basename -- "$input_file")
    extension="${filename##*.}"
    filename="${filename%.*}"
    output_file="${filename}_translucent.png"
    
    echo "Processing: $input_file -> $output_file"
    
    # Process the image:
    # 1. Preserve original image
    # 2. Extract existing alpha
    # 3. Create luminance-based alpha (lighter = more transparent)
    # 4. Invert the luminance to make white transparent instead of black
    # 5. Combine alphas
    # 6. Apply to original image
    convert "$input_file" \
        \( -clone 0 -alpha extract \) \
        \( -clone 0 -alpha off -colorspace gray -negate \) \
        -delete 0 \
        -compose multiply -composite \
        "$input_file" +swap \
        -compose copy-opacity -composite \
        "$output_file"
    
    if [ $? -eq 0 ]; then
        echo "Successfully processed: $output_file"
    else
        echo "Error processing: $input_file"
    fi
done

echo "All files processed"

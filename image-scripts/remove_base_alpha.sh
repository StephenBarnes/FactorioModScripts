#!/bin/bash

# This file removes the background alpha value, found by sampling the 4 corners of the image. For example if you have pics of craters for decoratives, and the pictures are mostly transparent around the edges but they still have non-zero alpha, then you get rectangles around the decoratives in-game. This script removes those rectangles.

# Check if ImageMagick is installed
if ! command -v convert &> /dev/null; then
    echo "Error: ImageMagick is not installed. Please install it first."
    exit 1
fi

# Check if at least one filename was provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 <image1.png> [image2.png] [image3.png] ..."
    echo "   or: $0 ./*.png"
    exit 1
fi

# Process each file provided as an argument
for IMAGE_FILE in "$@"; do
    # Check if the file exists
    if [ ! -f "$IMAGE_FILE" ]; then
        echo "Error: File '$IMAGE_FILE' not found. Skipping."
        continue
    fi

    # Check if the file is a PNG
    if [[ ! "$IMAGE_FILE" =~ \.png$ ]]; then
        echo "Error: File '$IMAGE_FILE' must be a PNG image. Skipping."
        continue
    fi

    echo "Processing $IMAGE_FILE..."

    # Create temporary directory and files
    TEMP_DIR=$(mktemp -d)
    TEMP_FILE="${TEMP_DIR}/processed.png"

    # Extract 10x10 pixel samples from the four corners
    convert "$IMAGE_FILE" -crop 10x10+0+0 "${TEMP_DIR}/top_left.png"
    convert "$IMAGE_FILE" -gravity NorthEast -crop 10x10+0+0 "${TEMP_DIR}/top_right.png"
    convert "$IMAGE_FILE" -gravity SouthWest -crop 10x10+0+0 "${TEMP_DIR}/bottom_left.png"
    convert "$IMAGE_FILE" -gravity SouthEast -crop 10x10+0+0 "${TEMP_DIR}/bottom_right.png"

    # Get the average alpha value from each corner
    get_avg_alpha() {
        convert "$1" -alpha extract -format "%[fx:mean]" info:
    }

    ALPHA_TL=$(get_avg_alpha "${TEMP_DIR}/top_left.png")
    ALPHA_TR=$(get_avg_alpha "${TEMP_DIR}/top_right.png")
    ALPHA_BL=$(get_avg_alpha "${TEMP_DIR}/bottom_left.png")
    ALPHA_BR=$(get_avg_alpha "${TEMP_DIR}/bottom_right.png")

    # Find the maximum alpha value
    MAX_ALPHA=$(echo -e "$ALPHA_TL\n$ALPHA_TR\n$ALPHA_BL\n$ALPHA_BR" | sort -g | tail -n 1)

    # Add a small buffer (5%) to the maximum alpha value
    # This ensures we get all the background alpha without affecting the actual crater
    BUFFER=0.05
    BASE_ALPHA=$(echo "$MAX_ALPHA + $BUFFER" | bc)

    # Cap the base alpha at 0.95 to avoid completely removing legitimate alpha
    if (( $(echo "$BASE_ALPHA > 0.95" | bc -l) )); then
        BASE_ALPHA=0.95
        echo "Warning: Very high background alpha detected in $IMAGE_FILE. Capping at 0.95."
    fi

    echo "  - Detected background alpha: $MAX_ALPHA (using $BASE_ALPHA with buffer)"

    # Create an alpha adjustment expression
    # This remaps the alpha channel so that BASE_ALPHA becomes 0, and 1 stays as 1
    ALPHA_EXPR="(a-$BASE_ALPHA)/(1-$BASE_ALPHA)"

    # Process the image to reduce the background alpha
    convert "$IMAGE_FILE" \
        -alpha extract \
        -fx "$ALPHA_EXPR < 0 ? 0 : $ALPHA_EXPR" \
        "${TEMP_DIR}/new_alpha.png"

    # Replace the alpha channel in the original image and save to temp file
    convert "$IMAGE_FILE" "${TEMP_DIR}/new_alpha.png" -alpha off -compose CopyOpacity -composite "$TEMP_FILE"

    # Replace the original file with the processed one
    if [ -f "$TEMP_FILE" ]; then
        mv "$TEMP_FILE" "$IMAGE_FILE"
        echo "  - Successfully processed $IMAGE_FILE"
    else
        echo "  - Error processing $IMAGE_FILE. Original file unchanged."
    fi

    # Clean up temporary files
    rm -rf "$TEMP_DIR"
done

echo "All processing complete!"

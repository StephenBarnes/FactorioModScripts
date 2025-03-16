#!/usr/bin/env python3

# This script produces a PNG to show cross-shpaed exclusion zones for certain entities. For use as data.AssemblingMachinePrototype.radius_visualisation_specification.
# Used in LegendarySpaceAge for the borehole mining drill and air separator, see the code for actually creating the exclusion zones. This PNG is just for the visualization.

# Script written by Claude 3.7 Sonnet.

import sys
from PIL import Image, ImageDraw
import re

def parse_dimensions(dim_str):
    """Parse dimensions in format WxH"""
    match = re.match(r"(\d+)x(\d+)", dim_str)
    if not match:
        raise ValueError(f"Invalid dimension format: {dim_str}. Expected format: WxH")
    return int(match.group(1)), int(match.group(2))

def make_exclusion_pic(building_dims, exclusion_dims):
    """
    Create an image with exclusion zones around a central building.
    
    Args:
        building_dims: Tuple of (width, height) for the central building
        exclusion_dims: Tuple of (width, height) for the exclusion zones
    """
    building_width, building_height = building_dims
    exclusion_width, exclusion_height = exclusion_dims
    
    # Calculate total image dimensions
    total_width = building_width + 2 * exclusion_height
    total_height = building_height + 2 * exclusion_height
    
    # Create a transparent image
    image = Image.new('RGBA', (total_width, total_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Calculate the exact position for the central building area (zero-based)
    building_left = exclusion_height
    building_right = building_left + building_width - 1
    building_top = exclusion_height
    building_bottom = building_top + building_height - 1
    
    # Draw top exclusion zone
    top_left_x = (total_width - exclusion_width) // 2
    draw.rectangle([
        (top_left_x, 0),
        (top_left_x + exclusion_width - 1, building_top - 1)
    ], fill=(255, 255, 255, 255))
    
    # Draw bottom exclusion zone
    bottom_left_x = (total_width - exclusion_width) // 2
    draw.rectangle([
        (bottom_left_x, building_bottom + 1),
        (bottom_left_x + exclusion_width - 1, total_height - 1)
    ], fill=(255, 255, 255, 255))
    
    # Draw left exclusion zone - rotated
    left_top_y = (total_height - exclusion_width) // 2
    draw.rectangle([
        (0, left_top_y),
        (building_left - 1, left_top_y + exclusion_width - 1)
    ], fill=(255, 255, 255, 255))
    
    # Draw right exclusion zone - rotated
    right_top_y = (total_height - exclusion_width) // 2
    draw.rectangle([
        (building_right + 1, right_top_y),
        (total_width - 1, right_top_y + exclusion_width - 1)
    ], fill=(255, 255, 255, 255))
    
    # Generate automatic filename
    output_file = f"exclusion_{building_width}x{building_height}_{exclusion_width}x{exclusion_height}.png"
    
    # Save the image
    image.save(output_file)
    print(f"Image saved to {output_file}")
    return image

def main():
    if len(sys.argv) < 3:
        print("Usage: makeExclusionPic <building_dimensions> <exclusion_dimensions>")
        print("Example: makeExclusionPic 3x3 27x21")
        sys.exit(1)
    
    try:
        building_dims = parse_dimensions(sys.argv[1])
        exclusion_dims = parse_dimensions(sys.argv[2])
        
        make_exclusion_pic(building_dims, exclusion_dims)
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

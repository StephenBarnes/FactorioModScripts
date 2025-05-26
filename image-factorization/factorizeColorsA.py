#!/usr/bin/env python3
"""
Factorize PNG images into component images based on HSV color analysis.
Usage: python factorizeColors.py <num_factors> <image_path>
"""

# Code written by Gemini 2.5 Pro.

import sys
import os
import numpy as np
from PIL import Image
import colorsys
from sklearn.decomposition import PCA, NMF
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


def rgb_to_hsv_vectorized(rgb_array):
    """Convert RGB array to HSV array, handling transparency."""
    # Normalize RGB values to 0-1 range
    rgb_norm = rgb_array[:, :3] / 255.0
    
    # Vectorized RGB to HSV conversion
    r, g, b = rgb_norm[:, 0], rgb_norm[:, 1], rgb_norm[:, 2]
    
    max_val = np.maximum(np.maximum(r, g), b)
    min_val = np.minimum(np.minimum(r, g), b)
    diff = max_val - min_val
    
    # Value
    v = max_val
    
    # Saturation
    s = np.where(max_val != 0, diff / max_val, 0)
    
    # Hue
    h = np.zeros_like(v)
    
    # Where max is R
    mask = (max_val == r) & (diff != 0)
    h[mask] = ((g[mask] - b[mask]) / diff[mask]) % 6
    
    # Where max is G
    mask = (max_val == g) & (diff != 0)
    h[mask] = (b[mask] - r[mask]) / diff[mask] + 2
    
    # Where max is B
    mask = (max_val == b) & (diff != 0)
    h[mask] = (r[mask] - g[mask]) / diff[mask] + 4
    
    h = h / 6.0  # Normalize to 0-1
    
    # Add alpha channel
    alpha = rgb_array[:, 3] / 255.0 if rgb_array.shape[1] == 4 else np.ones(len(rgb_array))
    
    return np.column_stack([h, s, v, alpha])


def prepare_color_features(hsv_array, num_factors):
    """
    Prepare features for factorization, handling circular hue.
    Create richer feature space to support more factors.
    """
    h, s, v, a = hsv_array[:, 0], hsv_array[:, 1], hsv_array[:, 2], hsv_array[:, 3]
    
    # Basic features: hue cartesian coordinates
    hue_x = s * np.cos(2 * np.pi * h)
    hue_y = s * np.sin(2 * np.pi * h)
    
    # Create extended feature set
    features = []
    
    # 1. Basic hue features (shifted to positive)
    features.append(hue_x + 1)
    features.append(hue_y + 1)
    
    # 2. Value (brightness)
    features.append(v)
    
    # 3. Saturation as separate feature
    features.append(s)
    
    # 4. Higher harmonics of hue for more complex color patterns
    # This allows capturing more nuanced color variations
    features.append(s * np.cos(4 * np.pi * h) + 1)
    features.append(s * np.sin(4 * np.pi * h) + 1)
    
    # 5. Interaction features
    features.append(s * v)  # Saturation-value interaction
    features.append(v * v)  # Value squared (for highlights/shadows)
    
    # 6. Color "purity" features
    features.append(s * s)  # Saturation squared (color intensity)
    
    # Convert to numpy array and transpose
    features = np.column_stack(features)
    
    # Limit features to what we need for the requested number of factors
    # NMF requires n_features >= n_components
    max_features = min(features.shape[1], max(num_factors, 3))
    features = features[:, :max_features]
    
    return features, a


def factorize_colors(image_path, num_factors):
    """Factorize an image into color components."""
    # Load image
    img = Image.open(image_path).convert('RGBA')
    width, height = img.size
    
    # Convert to numpy array and reshape
    img_array = np.array(img)
    pixels = img_array.reshape(-1, 4)
    
    # Convert to HSV
    hsv_pixels = rgb_to_hsv_vectorized(pixels)
    
    # Get non-transparent pixels for analysis
    alpha_mask = hsv_pixels[:, 3] > 0.01  # Pixels with some opacity
    non_transparent_pixels = hsv_pixels[alpha_mask]
    
    if len(non_transparent_pixels) == 0:
        print("Error: Image is completely transparent")
        return None
    
    # Prepare features with number of factors considered
    features, alphas = prepare_color_features(non_transparent_pixels, num_factors)
    
    # Weight features by alpha to give less importance to semi-transparent pixels
    weighted_features = features * alphas[:, np.newaxis]
    
    # Use Non-negative Matrix Factorization (NMF) for better interpretability
    # NMF ensures non-negative components which makes more sense for colors
    nmf = NMF(n_components=num_factors, init='nndsvda', random_state=42, max_iter=500)
    
    # Fit on non-transparent pixels
    nmf.fit(weighted_features)
    
    # Transform all pixels (including transparent ones)
    all_features, all_alphas = prepare_color_features(hsv_pixels, num_factors)
    coefficients = nmf.transform(all_features)
    
    # Normalize coefficients to get proportions
    coeff_sums = coefficients.sum(axis=1, keepdims=True)
    coeff_sums[coeff_sums == 0] = 1  # Avoid division by zero
    normalized_coeffs = coefficients / coeff_sums
    
    # Create factor images and analyze colors
    factor_images = []
    factor_colors = []
    
    for factor_idx in range(num_factors):
        # Get the coefficient for this factor for each pixel
        factor_strengths = normalized_coeffs[:, factor_idx]
        
        # Multiply by original alpha to maintain transparency
        factor_alphas = factor_strengths * hsv_pixels[:, 3]
        
        # Create white image with varying alpha
        factor_img = np.ones((height, width, 4))
        factor_img[:, :, 3] = factor_alphas.reshape(height, width)
        
        # Convert to uint8
        factor_img = (factor_img * 255).astype(np.uint8)
        
        factor_images.append(Image.fromarray(factor_img, mode='RGBA'))
        
        # Determine representative color for this factor
        # Find pixels where this factor is dominant
        factor_mask = (factor_strengths > 0.5) & (hsv_pixels[:, 3] > 0.5)
        
        if np.any(factor_mask):
            # Get the average HSV values for pixels where this factor dominates
            dominant_hsv = hsv_pixels[factor_mask].mean(axis=0)
            
            # Convert back to RGB
            h, s, v = dominant_hsv[0], dominant_hsv[1], dominant_hsv[2]
            rgb = colorsys.hsv_to_rgb(h, s, v)
            
            # Convert to hex
            r, g, b = int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            factor_colors.append(hex_color)
        else:
            factor_colors.append("#808080")  # Gray if no dominant pixels
    
    return factor_images, factor_colors


def main():
    if len(sys.argv) != 3:
        print("Usage: python factorizeColors.py <num_factors> <image_path>")
        sys.exit(1)
    
    try:
        num_factors = int(sys.argv[1])
        if num_factors < 1:
            raise ValueError("Number of factors must be at least 1")
    except ValueError as e:
        print(f"Error: Invalid number of factors - {e}")
        sys.exit(1)
    
    image_path = sys.argv[2]
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found")
        sys.exit(1)
    
    print(f"Factorizing {image_path} into {num_factors} components...")
    
    # Factorize the image
    result = factorize_colors(image_path, num_factors)
    
    if result is None:
        sys.exit(1)
    
    factor_images, factor_colors = result
    
    # Save factor images and print color information
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    dir_name = os.path.dirname(image_path)
    
    print("\nFactor analysis:")
    for i, (factor_img, color) in enumerate(zip(factor_images, factor_colors), 1):
        output_path = os.path.join(dir_name, f"{base_name}_{i}.png")
        factor_img.save(output_path)
        print(f"Factor {i} - {color} (saved to {output_path})")
    
    print("Factorization complete!")


if __name__ == "__main__":
    main()

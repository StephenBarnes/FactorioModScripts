#!/usr/bin/env python3

# Code written by Claude Opus 4.

import argparse
import os
import numpy as np
from PIL import Image
import colorsys
from sklearn.decomposition import PCA

def factorize_image_main(input_image_path: str, num_factors_requested_str: str):
    """
    Factorizes a PNG image into component images based on HSV colors using PCA.
    Each output image is white with an alpha channel representing the factor's strength.
    """
    try:
        num_factors_requested = int(num_factors_requested_str)
        if num_factors_requested < 1:
            print("Error: Number of factors must be 1 or greater.")
            return
    except ValueError:
        print(f"Error: Invalid number of factors '{num_factors_requested_str}'. Must be an integer.")
        return

    if not os.path.exists(input_image_path):
        print(f"Error: Input image '{input_image_path}' not found.")
        return

    try:
        img = Image.open(input_image_path)
        img_rgba = img.convert('RGBA') # Ensure image is in RGBA format
        width, height = img_rgba.size
        pixels_rgba_flat = np.array(img_rgba).reshape(-1, 4) # Shape: (num_pixels, 4)
    except Exception as e:
        print(f"Error loading or converting image '{input_image_path}': {e}")
        return

    original_alphas_flat = pixels_rgba_flat[:, 3] / 255.0
    
    # Identify non-fully-transparent pixels (where original alpha > a tiny threshold)
    opaque_mask_flat = original_alphas_flat > 1e-5 
    num_opaque_pixels = np.sum(opaque_mask_flat)

    base_name, ext = os.path.splitext(input_image_path)

    pca_n_components_computed = 0
    normalized_factor_alphas_opaque = np.array([]).reshape(num_opaque_pixels, 0) # Default for no opaque pixels

    if num_opaque_pixels > 0:
        rgb_opaque = pixels_rgba_flat[opaque_mask_flat, :3]

        # Convert opaque RGB values to HSV
        hsv_opaque_list = [colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0) for r, g, b in rgb_opaque]
        hsv_opaque_data = np.array(hsv_opaque_list) # Shape: (num_opaque_pixels, 3)

        H_values = hsv_opaque_data[:, 0]
        S_values = hsv_opaque_data[:, 1]
        
        h_angles = H_values * 2.0 * np.pi
        x_coords = S_values * np.cos(h_angles) 
        y_coords = S_values * np.sin(h_angles)
        
        hs_cartesian_data_opaque = np.stack((x_coords, y_coords), axis=-1) # Shape: (num_opaque_pixels, 2)

        n_features_in_data = hs_cartesian_data_opaque.shape[1] # Should be 2
        
        # Effective number of components PCA will compute.
        pca_n_components_computed = min(num_factors_requested, n_features_in_data, num_opaque_pixels)

        if pca_n_components_computed > 0:
            pca = PCA(n_components=pca_n_components_computed, random_state=42, svd_solver='full')
            try:
                factor_strengths_opaque = pca.fit_transform(hs_cartesian_data_opaque) 
            except Exception as e: 
                print(f"PCA computation failed: {e}. Treating opaque pixels as having zero factor strength.")
                factor_strengths_opaque = np.zeros((num_opaque_pixels, pca_n_components_computed))
            
            normalized_factor_alphas_opaque = np.zeros((num_opaque_pixels, pca_n_components_computed))
            for k_pca_comp in range(pca_n_components_computed):
                component_values = factor_strengths_opaque[:, k_pca_comp]
                min_val = np.min(component_values)
                max_val = np.max(component_values)

                if max_val == min_val: 
                    normalized_factor_alphas_opaque[:, k_pca_comp] = 1.0 
                else:
                    normalized_factor_alphas_opaque[:, k_pca_comp] = (component_values - min_val) / (max_val - min_val)
        else:
            # This case means pca_n_components_computed is 0 (e.g. num_opaque_pixels was 0, or num_factors_requested led to this)
            # normalized_factor_alphas_opaque remains empty or zero-columned.
             print(f"Effective PCA components to compute is {pca_n_components_computed}. Opaque areas in factor images will be transparent.")


    else: # num_opaque_pixels == 0
        print(f"Input image '{input_image_path}' has no opaque pixels. Creating {num_factors_requested} transparent output images.")
    
    # Generate num_factors_requested output images
    for k_output_factor_idx in range(num_factors_requested):
        factor_image_data = np.full((height, width, 4), [255, 255, 255, 0], dtype=np.uint8) # White, fully transparent

        current_factor_strengths_for_opaque_pixels = np.zeros(num_opaque_pixels, dtype=float)

        if k_output_factor_idx < pca_n_components_computed and num_opaque_pixels > 0 :
            current_factor_strengths_for_opaque_pixels = normalized_factor_alphas_opaque[:, k_output_factor_idx]
        
        factor_alphas_flat = np.zeros(width * height, dtype=float)
        if num_opaque_pixels > 0: # Only assign if there were opaque pixels and components
             factor_alphas_flat[opaque_mask_flat] = current_factor_strengths_for_opaque_pixels
        
        final_pixel_alphas_flat = factor_alphas_flat * original_alphas_flat
        
        factor_image_data[:, :, 3] = (final_pixel_alphas_flat.reshape(height, width) * 255).astype(np.uint8)

        output_pil_image = Image.fromarray(factor_image_data, 'RGBA')
        output_filename = f"{base_name}_{k_output_factor_idx + 1}{ext}"
        try:
            output_pil_image.save(output_filename)
            print(f"Saved factor image: {output_filename}")
        except Exception as e:
            print(f"Error saving output image {output_filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Factorize a PNG image into N component images. Each component image is white with an alpha channel representing the strength of that factor, derived from PCA on Hue and Saturation of opaque pixels.",
        formatter_class=argparse.RawTextHelpFormatter # Allows newlines in help string
    )
    parser.add_argument("num_factors", 
                        help="Number of factors to generate (e.g., 1, 2, or 3). \nIf more factors are requested than can be derived from 2D (Hue-Sat) data (max 2),\nextra factor images will be transparent.")
    parser.add_argument("input_image", 
                        help="Path to the input PNG image.")
    
    args = parser.parse_args()
    factorize_image_main(args.input_image, args.num_factors)

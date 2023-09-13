import cv2
import numpy as np
import brightest_patch
import argparse
import os

def main():
    
    parser = argparse.ArgumentParser(description='Brightest partches in the image.')

    # Add an argument for the input image path
    default_image = './img.png'
    parser.add_argument('--image_path', type=str, default=default_image, help=f'Path to the image (default: {default_image})')

    # Add an argument for the output image path with the default set to the root of the project
    default_output_path = os.path.join(os.getcwd(), 'output.png')
    parser.add_argument('--output_path', type=str, default=default_output_path, help=f'Path to the output image (default: {default_output_path})')

    # Parse the command-line arguments
    args = parser.parse_args()
    
    patches = []
    patch_coordinates = [] 
    patch_mean_intensities = []

    brightest_patch.extract_patches(args.image_path, patches, patch_coordinates, patch_mean_intensities)
    brightest_four, brightest_patches_coordinates, mean_brightness = brightest_patch.four_brightest_patches(patches, patch_coordinates, patch_mean_intensities)

    corners = brightest_patch.patch_centers(brightest_patches_coordinates)

    area = brightest_patch.compute_area(corners)
    brightest_patch.draw_area(args.image_path, corners, args.output_path)

    print(f'the area of the quadrilateral which the corners are the centers of the brightest patches of the image is: {area} pixels')

    

if __name__ == "__main__":
    main()
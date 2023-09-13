import cv2
import numpy as np
import brightest_patch
import argparse
import os

def main():
    # Create an ArgumentParser
    parser = argparse.ArgumentParser(description='Brightest partches in the image.')

    # Add an argument for the input image path
    default_image = './img.png'
    parser.add_argument('--image_path', type=str, default=default_image, help=f'Path to the image (default: {default_image})')

    # Add an argument for the output image path with the default set to the root of the project
    default_output_path = os.path.join(os.getcwd(), 'output.png')
    parser.add_argument('--output_path', type=str, default=default_output_path, help=f'Path to the output image (default: {default_output_path})')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Load the image as grayscale
    gray_image = brightest_patch.read_image(args.image_path, grayscale=True)
    

    

if __name__ == "__main__":
    main()
# BrightestPatches

This Python script is designed identify the four brightest patches within an image. It then calculates the area of the quadrilateral formed by connecting the centers of these brightest patches. This README file provides an overview of the script's functionality, usage, and requirements.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Explanation](#explanation)
- [Improvements](#improvements)
- [ToDo](#ToDo)



## Prerequisites

Before using this script, ensure you have the following prerequisites installed:

- Python 3.9
- OpenCV 
- NumPy 

You can install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. clone the directory.

2. Run the script using the following command:

```bash
python main.py --image_path path_to_your_image --output_path path_to_your_output_image
```
The project also includes a test image thus you can simply run:

```bash
python main.py
```
3. Run the tests.

```bash
cd BrightestPatches && pytest
```

## Explanation

### `extract_patches` Function

This function extracts patches from the input image and computes their mean intensities.

### `four_brightest_patches` Function

Compares patches based on their brightness and selects the top four brightest non overlapping patches. 
We begin by sorting the mean intensities of patches and generating an array of sorted indices. We then select the patch with the highest mean intensity as the first brightest element and the patch with the second-highest mean intensity as the second brightest. To determine whether the second brightest patch overlaps with the first one, we perform a check. We continue this process with the third brightest patch, ensuring it doesn't overlap with the previously selected patches (the first and second brightest). If it passes this check, we retain it in our selection.

It returns three lists:
1. `brightest_four`: The top four brightest patches from the given patches.
2. `brightest_patch_coordinates`: The coordinates of the top four brightest patches.
3. `mean_brightness`: The mean brightness intensities of the top four brightest patches.

### `is_overlapping` Function

This function checks if two patches specified by their indices overlap in the image. 
Returns `True` if the two patches overlap and `False` otherwise.

### `patch_centers` Function

This function calculates the center coordinates of the brightest patches and returns a list of corner coordinates.

### `compute_area` Function

This function computes the area of a quadrilateral formed by connecting the corner coordinates.

### `draw_area` Function

This function draws the quadrilateral on the input image and saves the resulting image to the specified output path.

### `main` Function

The main function parses command-line arguments, extracts patches, identifies the brightest patches, calculates the quadrilateral area, and saves the resulting image. It also prints the area of the quadrilateral to the console.

## improvements:
Currently, The `four_brightest_patches` function retains the first patch in the sorted array when two patches overlap and have the same brightness. However, a more logical approach would be to favor the least overlapping patch. For instance, if we choose the first patch, there's a possibility that two other bright patches overlap with it, leading to the exclusion of even brighter patches.

To further optimize the function `extract_patches`'s performance, we can use Python multithreading to reduce the computation time.

## ToDo
Add more tests.
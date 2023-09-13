import cv2
import numpy as np
import pytest
from brightest_patch import four_brightest_patches
from brightest_patch import is_overlapping

# Test case for comparing patches based on brightness
def test_four_brightest_patches() -> None:
    # dummy data
    patches = [np.array([[100, 250], [100, 250]]), 
               np.array([[10, 25], [10, 25]]), 
               np.array([[150, 250], [150, 250]]),
               np.array([[160, 250], [160, 250]]),
               np.array([[90, 250], [90, 250]])]
    patch_coordinates = [(0, 0, 2, 2), (2, 2, 4, 4), (4, 4, 6, 6), (6, 6, 8, 8), (3, 5, 5, 7)]
    patch_mean_intensities = [175, 17.5, 200, 205,170]

    brightest_four, brightest_patch_coordinates, mean_brightness = four_brightest_patches(patches, patch_coordinates, patch_mean_intensities)

    assert len(brightest_four) == 4
    assert len(brightest_patch_coordinates) == 4
    assert len(mean_brightness) == 4

    
    # check that they are sorted
    assert all(mean_brightness[i] >= mean_brightness[i+1] for i in range(len(mean_brightness) - 1))

    # Check that the selected patches are not overlapped
    for i in range(len(brightest_patch_coordinates)):
        for j in range(i + 1, len(brightest_patch_coordinates)):
            assert not is_overlapping(range(len(patch_mean_intensities)), brightest_patch_coordinates, i, j)


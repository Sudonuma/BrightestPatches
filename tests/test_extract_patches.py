import cv2
import numpy as np
import pytest

from brightest_patch import extract_patches

@pytest.fixture
def sample_image_path():

    # if we have an image of 5x5 pixels, the total extracted patches should be 1
    sample_image = np.array([[1, 2, 3, 4, 5],
                            [6, 7, 8, 9, 10],
                            [11, 12, 13, 14, 15],
                            [16, 17, 18, 19, 20],
                            [21, 22, 23, 24, 25]], dtype=np.uint8)

    # Save the sample image: (should be save to a temporary file)
    image_path = './sample_image.png'
    cv2.imwrite(str(image_path), sample_image)
    return str(image_path)


def test_extract_patches_5x5image(sample_image_path) -> None:
    # the test image is 20x20 pixels, if we are extracting all the patches of 5x5 pixels 
    # the total number of patches extracted should be 256
    

    patches = []
    patch_coordinates = []
    patch_mean_intensities = []

    extract_patches(sample_image_path, patches, patch_coordinates, patch_mean_intensities)

    
    expected_num_patches = 1 
    assert len(patches) == expected_num_patches

    # patch coordinates are correctly stored
    assert len(patch_coordinates) == expected_num_patches


def test_extract_patches_20x20image() -> None:
    # the test image is 20x20 pixels, if we are extracting all the patches of 5x5 pixels 
    # the total number of patches extracted should be 256
    
    image_path = './img.png'
    patches = []
    patch_coordinates = []
    patch_mean_intensities = []

    extract_patches(image_path, patches, patch_coordinates, patch_mean_intensities)

    expected_num_patches = 256
    assert len(patches) == expected_num_patches

    # patch coordinates are correctly stored
    assert len(patch_coordinates) == expected_num_patches


    



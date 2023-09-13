import cv2
import numpy as np
import pytest

from brightest_patch import read_image

def test_read_image_color() -> None:
    image_path = './img.jpg'
    img = read_image(image_path)

    assert isinstance(img, np.ndarray)
    assert len(img.shape) == 3
    assert img.shape[0] > 0
    assert img.shape[1]  > 0

def test_read_image_gray() -> None:
    image_path = './img.jpg'
    img = read_image(image_path, grayscale=True)

    assert isinstance(img, np.ndarray)
    assert len(img.shape) == 2
    assert img.shape[0] > 0
    assert img.shape[1]  > 0



import cv2
import numpy as np
import pytest

from brightest_patch import is_overlapping

def test_overlapped_patch() -> None:
    indices = [0, 1, 2]
    patch_coordinates = [(0, 0, 5, 5), (2, 3, 7, 8), (100, 100, 105, 105)]
    i = 0
    saved_i = 1
    assert is_overlapping(indices, patch_coordinates, i, saved_i) is True

def test_non_overlapped_patch() -> None:
    indices = [0, 1, 2]
    patch_coordinates = [(0, 0, 5, 5), (2, 3, 7, 8), (100, 100, 105, 105)]
    i = 0
    saved_i = 2
    assert is_overlapping(indices, patch_coordinates, i, saved_i) is False




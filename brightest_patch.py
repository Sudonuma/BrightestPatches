from typing import Optional, List, Tuple
import numpy as np
import cv2


def read_image(image_path: str, grayscale: Optional[bool] = False) -> np.ndarray:
    """
    Read an image from a file.

    Args:
        image_path (str): The path to the image.
        grayscale (bool, optional): Whether to read the image in grayscale mode (default is False).

    Returns:
        numpy.ndarray: A NumPy array if the image is loaded successfully.

    Raises:
        FileNotFoundError: If the specified image file does not exist.
    """
    if grayscale:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(image_path)

    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    return img



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

def is_overlapping(indices: List[int], patch_coordinates: List[Tuple[int, int, int, int]], i: int, saved_i: int) -> bool:
    """
    Check if two patches specified by their indices overlap in the image.

    Args:
        indices (List[int]): A list of indices representing patches.
        patch_coordinates (List[Tuple[int, int, int, int]]): A list of tuples containing the coordinates of patches
                                  in the format (start_x, start_y, end_x, end_y).
        i (int): Index of the first patch to check for overlap.
        saved_i (int): Index of the second patch to check for overlap with the first patch.

    Returns:
        bool: True if the two patches overlap, False otherwise.
    """
    elemt_a_startx, elemt_a_starty, elemnt_a_endx, elemnt_a_endy = patch_coordinates[indices[saved_i]]
    elemt_b_startx, elemt_b_starty, elemnt_b_endx, elemnt_b_endy = patch_coordinates[indices[i]]
    
    # Check the overlap in x and y axes:
    overlap_x = (elemt_a_startx < elemnt_b_endx) and (elemt_b_startx < elemnt_a_endx)
    overlap_y = (elemt_a_starty < elemnt_b_endy) and (elemt_b_starty < elemnt_a_endy)
        
    return (overlap_x and overlap_y)


def four_brightest_patches(patches: List[np.ndarray], patch_coordinates: List, patch_mean_intensities: List) -> Tuple:
    """
    Compare patches based on their brightness and select the top four brightest patches.

    Args:
        patches (list): A list of patches, represented as numpy arrays.
        patch_coordinates (list): A list of tuples containing the coordinates of patches.
                                  the format (start_x, start_y, end_x, end_y).
        patch_mean_intensities (list): A list of mean brightness intensities corresponding to each patch.

    Returns:
        tuple: A tuple containing three lists -
        1. brightest_four: The top four brightest patches from the given patches (not the full image).
        2. brightest_patch_coordinates: The coordinates of the top four brightest patches.
        3. mean_brightness: The mean brightness intensities of the top four brightest patches.

    Note:
        The function selects the top four patches based on brightness and checks for overlap
        to ensure non-overlapping patches are included in the result.
    """
    # Sort intensities and get corresponding indices (not needed, just for clarity)
    sorted_patch_mean_intensities = sorted(patch_mean_intensities, reverse=True)
    # indices of the sorted intensities
    indices = sorted(range(len(patch_mean_intensities)), key=lambda i: patch_mean_intensities[i], reverse=True)

    brightest_four = [patches[indices[0]]]
    brightest_patch_coordinates = [patch_coordinates[indices[0]]]
    mean_brightness = [patch_mean_intensities[indices[0]]]
    
    count = 0
    saved_indices = [0]

    for i in range(1, len(indices)):
        # Check if the current patch does not overlap with previously selected patches
        overlap = False
        
        for selected_index in saved_indices:
            if is_overlapping(indices, patch_coordinates, i, selected_index) is False:
                overlap = overlap or False
            elif is_overlapping(indices, patch_coordinates, i, selected_index) is True:
                overlap = overlap or True

        if overlap is False:       
            brightest_four.append(patches[indices[i]])
            brightest_patch_coordinates.append(patch_coordinates[indices[i]])
            mean_brightness.append(patch_mean_intensities[indices[i]])
            count += 1
            saved_indices.append(i)
                    
        if count == 3:
            break
    
    return brightest_four, brightest_patch_coordinates, mean_brightness


def extract_patches(image_path: str, patches: List[np.ndarray], patch_coordinates: List, patch_mean_intensities: List[float]):
    """
    Extract patches from an image and calculate their mean intensities.

    Args:
        image_path (str): The path to the image.
        patches (List[np.ndarray]): An empty list to store the extracted patches as NumPy arrays.
        patch_coordinates (List): An empty list to store the coordinates of the patches. format: (start_x, start_y, end_x, end_y).
        patch_mean_intensities (List[float]): An empty list to store the mean brightness intensities of the patches.
    """
    img_gray = read_image(image_path, grayscale=True)
    patch_size = 5
    H, W = img_gray.shape

    for i in range(H - patch_size + 1):
        for j in range(W - patch_size + 1):
            start_x = j
            end_x = j + patch_size
            start_y = i
            end_y = i + patch_size
            patch = img_gray[start_y:end_y, start_x:end_x]
            patches.append(patch)
            patch_coordinates.append((start_x, start_y, end_x, end_y))
            mean_intensity = np.mean(patch)
            patch_mean_intensities.append(mean_intensity)

def patch_centers(brightest_patches_coordinates: List) -> List:
    """
    Calculate the center coordinates of a list of patches.

    Args:
        brightest_patches_coordinates (List): A list of patch coordinates in the format (start_x, start_y, end_x, end_y).

    Returns:
        List: A list of center coordinates as tuples (center_x, center_y).
    """
    centers = []
    for i in brightest_patches_coordinates:
        x_start, y_start, x_end, y_end = i
        center_x = (x_start + x_end) // 2
        center_y = (y_start + y_end) // 2
        centers.append((center_x, center_y))
    return centers

def compute_area(corners: List) -> float:
    """
    Compute the area of a quadrilateral defined by its corner coordinates.

    Args:
        corners (List): A list of corner coordinates as tuples (x, y).

    Returns:
        float: The area of the quadrilateral.
    """
    corners_array = np.array(corners, np.int32)
    corners_array = corners_array.reshape((-1, 1, 2))
    contours = [corners_array]
    area = cv2.contourArea(contours[0])
    return area

def draw_area(image_path: str, corner_coordinates: List, output_path: str) -> None:
    """
    Draw a filled polygon on an image using corner coordinates and save the result.

    Args:
        image_path (str): The path to the input image.
        corner_coordinates (List): the list of corner coordinates.
        output_path (str): The path to save the output image.
    """
    image = read_image(image_path)
    corners = np.array(corner_coordinates, np.int32)
    pts = corners.reshape((-1, 1, 2))
    cv2.fillPoly(image, [pts], (0, 0, 255))
    cv2.imwrite(output_path, image)
